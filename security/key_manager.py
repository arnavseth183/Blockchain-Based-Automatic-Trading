"""
Key Manager
Handles wallet key generation and transaction signing
"""

import os
import json
import secrets
from eth_account import Account
from eth_account.messages import encode_defunct

class KeyManager:

    def __init__(self, storage_path="data/keys"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def generate_wallet(self, username):
        """
        Generate Ethereum wallet for a new user
        """
        account = Account.create(secrets.token_hex(32))

        wallet_data = {
            "username": username,
            "address": account.address,
            "private_key": account.key.hex()
        }

        file_path = os.path.join(self.storage_path, f"{username}.json")

        with open(file_path, "w") as f:
            json.dump(wallet_data, f, indent=4)

        return wallet_data

    def load_wallet(self, username):
        """
        Load wallet from storage
        """
        file_path = os.path.join(self.storage_path, f"{username}.json")

        if not os.path.exists(file_path):
            raise Exception("Wallet does not exist")

        with open(file_path) as f:
            wallet = json.load(f)

        return wallet

    def sign_message(self, private_key, message):
        """
        Sign arbitrary message
        """
        encoded = encode_defunct(text=message)

        signed = Account.sign_message(encoded, private_key)

        return signed.signature.hex()

    def verify_signature(self, address, message, signature):
        """
        Verify signature
        """
        encoded = encode_defunct(text=message)

        recovered = Account.recover_message(encoded, signature=signature)

        return recovered.lower() == address.lower()

    def get_address(self, username):
        """
        Return public address of wallet
        """
        wallet = self.load_wallet(username)

        return wallet["address"]

    def get_private_key(self, username):
        """
        Return private key
        """
        wallet = self.load_wallet(username)

        return wallet["private_key"]

    def wallet_exists(self, username):
        """
        Check if wallet already exists
        """
        file_path = os.path.join(self.storage_path, f"{username}.json")

        return os.path.exists(file_path)

    def list_wallets(self):
        """
        List all wallets in storage
        """
        wallets = []

        for file in os.listdir(self.storage_path):
            if file.endswith(".json"):
                wallets.append(file.replace(".json", ""))

        return wallets