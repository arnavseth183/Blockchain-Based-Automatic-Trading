import hashlib
import json
import os
import secrets
from blockchain_protocol.storage.ledger_storage import LedgerStorage
from blockchain_protocol.web3_layer.web3_provider import Web3Provider


class WalletAuth:

    def __init__(self, web3_provider):

        self.web3 = web3_provider
        self.ledger = LedgerStorage()

        self.users_file = "data/users.json"

        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

    # -------------------------------
    # PASSWORD HASH
    # -------------------------------

    def hash_password(self, password):

        return hashlib.sha256(password.encode()).hexdigest()

    # -------------------------------
    # SECRET PHRASE
    # -------------------------------

    def generate_secret_phrase(self):

        words = []

        for _ in range(12):
            words.append(secrets.token_hex(2))

        return " ".join(words)

    # -------------------------------
    # REGISTER USER
    # -------------------------------

    def register_user(self, username, password):

        wallet = self.web3.create_account()

        address = wallet["address"]
        private_key = wallet["private_key"]

        password_hash = self.hash_password(password)

        secret_phrase = self.generate_secret_phrase()

        with open(self.users_file, "r") as f:
            users = json.load(f)

        users[address] = {
            "username": username,
            "password": password_hash,
            "secret": secret_phrase
        }

        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)

        self.ledger.store_user_wallet(address)

        return {
            "address": address,
            "private_key": private_key,
            "secret_phrase": secret_phrase
        }

    # -------------------------------
    # LOGIN
    # -------------------------------

    def login(self, wallet_address, password):

        if not os.path.exists(self.users_file):
            return False

        with open(self.users_file, "r") as f:
            users = json.load(f)

        if wallet_address not in users:
            return False

        password_hash = self.hash_password(password)

        if users[wallet_address]["password"] == password_hash:
            return True

        return False