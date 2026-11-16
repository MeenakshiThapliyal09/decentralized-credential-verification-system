// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract CredentialRegistry {
    address public owner;

    struct Credential {
        bool exists;
        bool revoked;
    }

    mapping(bytes32 => Credential) private credentials;

    event CredentialIssued(bytes32 indexed fingerprint);
    event CredentialRevoked(bytes32 indexed fingerprint);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function issueCredential(bytes32 fingerprint) external onlyOwner {
        require(!credentials[fingerprint].exists, "Credential already exists");
        credentials[fingerprint] = Credential(true, false);
        emit CredentialIssued(fingerprint);
    }

    function checkCredential(bytes32 fingerprint)
        external
        view
        returns (bool exists, bool revoked)
    {
        Credential memory credential = credentials[fingerprint];
        return (credential.exists, credential.revoked);
    }

    function revokeCredential(bytes32 fingerprint) external onlyOwner {
        require(credentials[fingerprint].exists, "Credential does not exist");
        require(!credentials[fingerprint].revoked, "Credential is already revoked");
        credentials[fingerprint].revoked = true;
        emit CredentialRevoked(fingerprint);
    }
}
