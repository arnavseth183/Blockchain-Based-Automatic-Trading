import json
import os
import time
import hashlib


class LedgerStorage:

    def __init__(self):

        self.ledger_file = "data/blockchain_ledger.json"

        if not os.path.exists(self.ledger_file):

            with open(self.ledger_file, "w") as f:
                json.dump([], f)

    # -------------------------------
    # HASH BLOCK
    # -------------------------------

    def hash_block(self, block):

        encoded = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded).hexdigest()

    # -------------------------------
    # GET LAST BLOCK
    # -------------------------------

    def get_last_block(self):

        with open(self.ledger_file, "r") as f:
            chain = json.load(f)

        if len(chain) == 0:
            return None

        return chain[-1]

    # -------------------------------
    # ADD BLOCK
    # -------------------------------

    def add_block(self, data):

        with open(self.ledger_file, "r") as f:
            chain = json.load(f)

        last_block = self.get_last_block()

        block = {
            "index": len(chain) + 1,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": last_block["hash"] if last_block else "0"
        }

        block["hash"] = self.hash_block(block)

        chain.append(block)

        with open(self.ledger_file, "w") as f:
            json.dump(chain, f, indent=4)

    # -------------------------------
    # STORE USER
    # -------------------------------

    def store_user_wallet(self, address):

        data = {
            "type": "USER_REGISTER",
            "wallet": address
        }

        self.add_block(data)

    # -------------------------------
    # STORE TRADE
    # -------------------------------

    def store_trade(self, trade):

        data = {
            "type": "TRADE",
            "trade": trade
        }

        self.add_block(data)