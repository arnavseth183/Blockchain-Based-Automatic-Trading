"""
seed_users.py

Seeds blockchain with initial test traders.
Creates wallet addresses and assigns roles.
"""

import json
from web3 import Web3
from security.wallet_auth import WalletAuth


PROVIDER = "http://127.0.0.1:8545"
OUTPUT = "blockchain_protocol/deployment/seeded_users.json"


def main():
    print("=======================================")
    print("Seeding Blockchain Users")
    print("=======================================")

    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    wallet_auth = WalletAuth(w3)

    users = []

    for i in range(5):
        account = w3.eth.account.create()
        wallet_auth.register_user(account.address)

        users.append({
            "address": account.address,
            "private_key": account.key.hex()
        })

        print(f"Created user {i+1}: {account.address}")

    with open(OUTPUT, "w") as f:
        json.dump(users, f, indent=4)

    print("Users seeded successfully.")


if __name__ == "__main__":
    main()