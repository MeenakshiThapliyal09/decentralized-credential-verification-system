# Decentralized Credential Verification System

**Status: In Development**

## Project overview

This college mini project is planned to help check that a digital credential is genuine and has not been changed. Today, someone may need to contact the issuer directly to check a document. This project aims to make checking easier by storing a credential's cryptographic fingerprint on a local blockchain. The credential itself is not planned to be stored on the blockchain.

## Planned workflow

1. An authorized issuer creates a credential.
2. The application generates a credential file.
3. The credential's cryptographic fingerprint is registered on the blockchain.
4. A user uploads a credential for verification. The application will calculate its fingerprint and compare it with the blockchain record.
5. An authorized issuer can revoke a credential so it is no longer considered valid.

## Planned technology stack

- **Python 3.12** - application logic and credential file handling.
- **Streamlit** - the web-based user interface for issuers and users.
- **Solidity** - the smart contract planned to register fingerprints and support revocation.
- **Web3.py** - communication between the Python application and the blockchain.
- **Ethereum Tester** - the local blockchain testing environment for development.
- **Git and GitHub** - version control and hosting the project source code.

## Planned features

- Issuer flow for creating a credential file.
- Fingerprint registration through a Solidity smart contract.
- Credential upload and fingerprint-based verification.
- Revocation by an authorized issuer.
- A simple Streamlit interface for the planned actions.

These features are planned and may change during development.

## Basic setup (planned)

The following steps describe the planned development setup. Application code and dependency files have not been created yet.

1. Install Python 3.12 and Git. Ethereum Tester will provide the local blockchain testing environment.
2. Open this project folder in VS Code.
3. Create and activate a virtual environment in the project folder:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. When a dependency list is added, install the project packages into the active environment.
5. Configure the application to use Ethereum Tester when the blockchain connection is added.

No project features are claimed as implemented or tested at this stage.
