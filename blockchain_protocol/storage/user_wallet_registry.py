"""
user_wallet_registry.py
"""

import json
import os
import hashlib
import logging
import secrets
from web3 import Web3

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/blockchain.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class UserWalletRegistry:

    def __init__(self):

        self.file = "data/user_wallets.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f)

        self.w3 = Web3()

    # -------------------------------------------------------
    # FILE OPERATIONS
    # -------------------------------------------------------

    def load(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    # -------------------------------------------------------
    # HASH
    # -------------------------------------------------------

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # -------------------------------------------------------
    # CREATE USER (FIXED STEP 2 CORE)
    # -------------------------------------------------------

    def create_user(self, username, password):

        data = self.load()

        if username in data:
            raise Exception("User already exists")

        account = self.w3.eth.account.create()

        wallet_address = account.address
        private_key = account.key.hex()

        password_hash = self.hash_password(password)

        recovery_secret = secrets.token_hex(16)

        data[username] = {

            "username": username,
            "wallet_address": wallet_address,
            "private_key": private_key,
            "password_hash": password_hash,
            "recovery_secret": recovery_secret,

            # 💰 FIXED: SINGLE SOURCE OF TRUTH
            "balance": float(10000),

            # 💼 FIXED PORTFOLIO STRUCTURE
            "portfolio": {
                "cash": float(10000),
                "holdings": {}
            },

            "transactions": []
        }

        self.save(data)

        logging.info(f"User created: {username}")

        return {
            "username": username,
            "wallet_address": wallet_address,
            "private_key": private_key,
            "recovery_secret": recovery_secret
        }

    # -------------------------------------------------------
    # AUTH (UNCHANGED)
    # -------------------------------------------------------

    def authenticate_user(self, username, password):

        data = self.load()

        if username not in data:
            return None

        if data[username]["password_hash"] == self.hash_password(password):

            return {
                "username": username,
                "wallet_address": data[username]["wallet_address"],
                "private_key": data[username]["private_key"]
            }

        return None

    # -------------------------------------------------------
    # RESET (UNCHANGED)
    # -------------------------------------------------------

    def reset_password(self, username, private_key, new_password):

        data = self.load()

        if username not in data:
            return False

        if data[username]["private_key"] != private_key:
            return False

        data[username]["password_hash"] = self.hash_password(new_password)

        self.save(data)

        return True

    # -------------------------------------------------------
    # WALLET ACCESS
    # -------------------------------------------------------

    def get_wallet(self, username):
        data = self.load()
        return data.get(username, {}).get("wallet_address")

    def get_private_key(self, username):
        data = self.load()
        return data.get(username, {}).get("private_key")

    # -------------------------------------------------------
    # BALANCE (SAFE FIX)
    # -------------------------------------------------------

    def get_balance(self, username):
        data = self.load()
        return float(data.get(username, {}).get("balance", 0))

    def update_balance(self, username, amount):

        data = self.load()

        if username not in data:
            return False

        data[username]["balance"] = float(data[username]["balance"]) + float(amount)

        self.save(data)
        return True

    # -------------------------------------------------------
    # PORTFOLIO STATE (MAIN FIX FOR TRADE PANEL)
    # -------------------------------------------------------

    def get_portfolio_state(self, username):

        data = self.load()

        if username not in data:
            return {"cash": 0.0, "holdings": {}}

        portfolio = data[username].get("portfolio", {})

        return {
            "cash": float(portfolio.get("cash", 0)),
            "holdings": portfolio.get("holdings", {})
        }

    def set_portfolio_state(self, username, portfolio):

        data = self.load()

        if username not in data:
            return False

        data[username]["portfolio"] = {
            "cash": float(portfolio.get("cash", 0)),
            "holdings": portfolio.get("holdings", {})
        }

        data[username]["balance"] = float(portfolio.get("cash", 0))

        self.save(data)
        return True

    # -------------------------------------------------------
    # OLD PORTFOLIO METHODS (KEPT - NOT REMOVED)
    # -------------------------------------------------------

    def update_portfolio(self, username, stock, quantity):

        data = self.load()

        if username not in data:
            return False

        portfolio = data[username]["portfolio"]

        if stock not in portfolio:
            portfolio[stock] = 0

        portfolio[stock] += quantity

        if portfolio[stock] <= 0:
            del portfolio[stock]

        self.save(data)
        return True

    def get_portfolio(self, username):

        data = self.load()

        if username not in data:
            return {}

        return data[username]["portfolio"]

    # -------------------------------------------------------
    # CASH UPDATE SAFE
    # -------------------------------------------------------

    def update_cash(self, username, amount):

        data = self.load()

        if username not in data:
            return False

        if "portfolio" not in data[username]:
            data[username]["portfolio"] = {"cash": 10000, "holdings": {}}

        data[username]["portfolio"]["cash"] = float(
            data[username]["portfolio"].get("cash", 0)
        ) + float(amount)

        self.save(data)
        return True

    # -------------------------------------------------------
    # TRANSACTIONS
    # -------------------------------------------------------

    def store_transaction(self, username, tx_hash):

        data = self.load()

        if username not in data:
            return

        data[username]["transactions"].append(tx_hash)

        self.save(data)

    def get_transactions(self, username):

        data = self.load()

        if username not in data:
            return []

        return data[username]["transactions"]

    # -------------------------------------------------------
    # RECOVERY
    # -------------------------------------------------------

    def recover_account(self, username, recovery_secret):

        data = self.load()

        if username not in data:
            return None

        if data[username]["recovery_secret"] == recovery_secret:
            return {
                "wallet_address": data[username]["wallet_address"],
                "private_key": data[username]["private_key"]
            }

        return None

    # -------------------------------------------------------
    # UTILITIES
    # -------------------------------------------------------

    def list_users(self):
        return list(self.load().keys())

    def user_exists(self, username):
        return username in self.load()