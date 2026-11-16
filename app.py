import hashlib
import json
import secrets
from pathlib import Path

import streamlit as st
from eth_tester import EthereumTester, PyEVMBackend
from solcx import compile_files, set_solc_version
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider


st.set_page_config(
    page_title="Decentralized Credential Verification System",
    page_icon="🔐",
    layout="centered",
)

CONTRACT_FILE = Path(__file__).parent / "contracts" / "CredentialRegistry.sol"
REQUIRED_FIELDS = ["student_name", "course", "institution", "certificate_id", "issue_date"]


def credential_text(credential_data):
    """Create one consistent JSON representation before hashing."""
    return json.dumps(credential_data, sort_keys=True, separators=(",", ":"))


def create_fingerprint(credential_data):
    return hashlib.sha256(credential_text(credential_data).encode("utf-8")).hexdigest()


def fingerprint_bytes(fingerprint):
    return bytes.fromhex(fingerprint)


def read_credential(uploaded_file):
    """Read a credential file and confirm that its fingerprint is genuine."""
    try:
        file_data = json.loads(uploaded_file.getvalue().decode("utf-8"))
        credential_data = file_data["credential"]
        salt = file_data["salt"]
        saved_fingerprint = file_data["sha256_fingerprint"]

        if not isinstance(credential_data, dict) or not isinstance(salt, str):
            raise ValueError("Credential data is incomplete.")
        if set(credential_data) != set(REQUIRED_FIELDS):
            raise ValueError("Credential fields are invalid.")
        if not all(
            isinstance(credential_data[field], str) and credential_data[field].strip()
            for field in REQUIRED_FIELDS
        ):
            raise ValueError("Credential fields must contain text.")
        if not isinstance(saved_fingerprint, str) or len(saved_fingerprint) != 64:
            raise ValueError("The fingerprint is invalid.")

        calculated_fingerprint = create_fingerprint(
            {"credential": credential_data, "salt": salt}
        )
        if calculated_fingerprint != saved_fingerprint.lower():
            raise ValueError("The credential file has been modified.")

        # This also confirms that the fingerprint contains hexadecimal characters.
        fingerprint_bytes(calculated_fingerprint)
        return credential_data, calculated_fingerprint, None
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        return None, None, str(error)


@st.cache_resource
def connect_blockchain():
    """Create one in-memory blockchain and deploy the registry once per app process."""
    tester = EthereumTester(PyEVMBackend())
    web3 = Web3(EthereumTesterProvider(tester))

    set_solc_version("0.8.20")
    compiled_contracts = compile_files([str(CONTRACT_FILE)], output_values=["abi", "bin"])
    contract_data = next(
        data
        for name, data in compiled_contracts.items()
        if name.endswith(":CredentialRegistry")
    )

    issuer_account = web3.eth.accounts[0]
    registry_factory = web3.eth.contract(
        abi=contract_data["abi"], bytecode=contract_data["bin"]
    )
    deployment_transaction = registry_factory.constructor().transact({"from": issuer_account})
    deployment_receipt = web3.eth.wait_for_transaction_receipt(deployment_transaction)
    registry = web3.eth.contract(
        address=deployment_receipt.contractAddress, abi=contract_data["abi"]
    )
    return web3, registry, issuer_account


def chain_status(registry, fingerprint):
    return registry.functions.checkCredential(fingerprint_bytes(fingerprint)).call()


st.title("Decentralized Credential Verification System")
st.write(
    "Issue, verify, and revoke digital credential fingerprints on a local "
    "blockchain. Personal information stays inside the downloaded credential file."
)
st.info(
    "Local demonstration: restarting Streamlit creates a fresh in-memory blockchain "
    "and removes all registered records."
)

try:
    web3, registry, issuer_account = connect_blockchain()
    st.success(f"Blockchain connected. Authorized issuer: {issuer_account}")
except Exception as error:
    st.error(f"Blockchain setup failed: {error}")
    st.stop()

issue_tab, verify_tab, manage_tab = st.tabs(
    ["Issue Credential", "Verify Credential", "Manage Credentials"]
)

with issue_tab:
    st.subheader("Issue a credential")
    st.write("The authorized issuer creates a credential and registers its fingerprint.")

    with st.form("issue_credential_form"):
        student_name = st.text_input("Student Name")
        course = st.text_input("Course")
        institution = st.text_input("Institution")
        certificate_id = st.text_input("Certificate ID")
        issue_date = st.date_input("Issue Date")
        submitted = st.form_submit_button("Issue Credential", type="primary")

    if submitted:
        credential_data = {
            "student_name": student_name.strip(),
            "course": course.strip(),
            "institution": institution.strip(),
            "certificate_id": certificate_id.strip(),
            "issue_date": issue_date.isoformat(),
        }
        if not all(credential_data.values()):
            st.error("Please complete every field.")
        else:
            credential_for_hashing = {
                "credential": credential_data,
                "salt": secrets.token_hex(16),
            }
            fingerprint = create_fingerprint(credential_for_hashing)
            try:
                transaction_hash = registry.functions.issueCredential(
                    fingerprint_bytes(fingerprint)
                ).transact({"from": issuer_account})
                receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
                credential_file = {
                    **credential_for_hashing,
                    "sha256_fingerprint": fingerprint,
                }
                st.session_state["issued_credential"] = json.dumps(
                    credential_file, indent=2, sort_keys=True
                )
                st.success("Credential fingerprint registered on the blockchain.")
                st.code(fingerprint, language=None)
                st.caption(f"Transaction hash: {receipt.transactionHash.hex()}")
            except Exception as error:
                st.error(f"Credential could not be registered: {error}")

    if "issued_credential" in st.session_state:
        st.download_button(
            "Download JSON Credential",
            data=st.session_state["issued_credential"],
            file_name="credential.json",
            mime="application/json",
        )

with verify_tab:
    st.subheader("Verify a credential")
    uploaded_credential = st.file_uploader(
        "Upload a credential JSON file", type="json", key="verify_upload"
    )

    if uploaded_credential is not None:
        credential_data, fingerprint, error = read_credential(uploaded_credential)
        if error:
            st.error(f"INVALID: {error}")
        else:
            exists, revoked = chain_status(registry, fingerprint)
            st.caption(f"Credential fingerprint: {fingerprint}")
            if not exists:
                st.warning("NOT FOUND: The fingerprint is not registered on the blockchain.")
            elif revoked:
                st.error("REVOKED: This registered credential has been revoked.")
            else:
                st.success("VALID: The credential matches the blockchain record.")

with manage_tab:
    st.subheader("Manage credentials")
    st.write("Upload a valid credential to view its status or revoke it as the issuer.")
    credential_to_manage = st.file_uploader(
        "Upload a credential JSON file", type="json", key="manage_upload"
    )

    if credential_to_manage is not None:
        credential_data, fingerprint, error = read_credential(credential_to_manage)
        if error:
            st.error(f"Cannot manage this credential: {error}")
        else:
            exists, revoked = chain_status(registry, fingerprint)
            if not exists:
                st.warning("NOT FOUND: This credential is not registered and cannot be revoked.")
            else:
                st.write("Credential details")
                st.json(credential_data)
                st.caption(f"Credential fingerprint: {fingerprint}")
                if revoked:
                    st.error("REVOKED: This credential has already been revoked.")
                elif st.button("Revoke Credential", type="primary"):
                    try:
                        transaction_hash = registry.functions.revokeCredential(
                            fingerprint_bytes(fingerprint)
                        ).transact({"from": issuer_account})
                        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
                        st.success("Credential revoked successfully.")
                        st.caption(f"Transaction hash: {receipt.transactionHash.hex()}")
                    except Exception as error:
                        st.error(f"Credential could not be revoked: {error}")
