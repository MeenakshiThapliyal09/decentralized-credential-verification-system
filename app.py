import streamlit as st

st.set_page_config(
    page_title="Decentralized Credential Verification System",
    page_icon="🔐",
    layout="centered",
)

st.title("🔐 Decentralized Credential Verification System")
st.write(
    "This project aims to verify digital credentials using blockchain, "
    "helping users check that a credential is authentic and unchanged."
)

st.info("Project Status: In Development")

issue_tab, verify_tab, manage_tab = st.tabs(
    ["Issue Credential", "Verify Credential", "Manage Credentials"]
)

with issue_tab:
    st.subheader("Issue a credential")
    st.write(
        "This section will allow an authorized issuer to create credentials. "
        "The credential's cryptographic fingerprint will eventually be "
        "registered on the blockchain."
    )
    st.warning("Not implemented yet — credential issuing is a placeholder.")

with verify_tab:
    st.subheader("Verify a credential")
    st.write(
        "Users will eventually upload a credential file. The application "
        "will compare its fingerprint with the blockchain record."
    )
    st.warning("Not implemented yet — file upload and verification are placeholders.")

with manage_tab:
    st.subheader("Manage credentials")
    st.write(
        "An authorized issuer will eventually be able to view and revoke "
        "registered credentials."
    )
    st.warning("Not implemented yet — credential management is a placeholder.")
