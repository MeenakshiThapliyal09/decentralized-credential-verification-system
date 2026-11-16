# Decentralized Credential Verification System

An educational college mini project that demonstrates how a blockchain can help verify digital credentials. It is a local demonstration, not a production deployment.

## Problem and purpose

Checking whether a certificate is authentic can require contacting the issuing institution. This application lets an authorized issuer register a SHA-256 fingerprint of a credential on a local blockchain. Anyone with the JSON credential can check whether it is unchanged, registered, and not revoked.

No student name, course, institution, certificate ID, or other personal information is stored on the blockchain. The blockchain stores only a `bytes32` fingerprint and its status.

## Technologies

- Python 3.12
- Streamlit 1.66.1
- Solidity 0.8.20
- Web3.py 8.0.0
- Ethereum Tester with Py-EVM
- Py-Solc-X

## How it works

### Issue a credential

The issuer enters the student name, course, institution, certificate ID, and issue date. The app adds a random salt, creates a SHA-256 fingerprint from a consistently serialized JSON structure, and registers that fingerprint through the smart contract. Download the generated JSON file and keep it safe.

### Verify a credential

Upload the JSON credential. The app recalculates the SHA-256 fingerprint and first checks it against the fingerprint saved in the file. It then asks the smart contract whether that fingerprint exists and whether it was revoked. A credential is valid only when all three checks succeed.

### Revoke a credential

The authorized issuer uploads a valid, registered credential in the Manage Credentials tab and selects **Revoke Credential**. The smart contract prevents anyone other than its owner from issuing or revoking credentials, and prevents repeat revocation.

## Install and run

From the project folder in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit. The Solidity compiler version 0.8.20 must be installed for Py-Solc-X before starting the app.

## Local blockchain limitations

The app uses Ethereum Tester and Py-EVM, which run entirely in memory. The first Streamlit session creates and deploys a fresh contract, and cached resources preserve it during reruns in that application process. Restarting Streamlit resets the blockchain, contract, and all issued or revoked records. This project has no persistent database, network blockchain, wallets, private keys, login system, or production security controls.
