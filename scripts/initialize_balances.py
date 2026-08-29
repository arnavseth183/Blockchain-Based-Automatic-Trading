"""
initialize_balances.py

Assigns initial token balances to seeded users.
Interacts with PortfolioManager smart contract.
"""

import json
from web3 import Web3
from blockchain_protocol.web3_layer.contract_loader import ContractLoader


PROVIDER = "http://127.0.0.1:8545"
SEED_FILE = "blockchain_protocol/deployment/seeded_users.json"


def main():
    print("=======================================")
    print("Initializing User Balances")
    print("=======================================")

    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    loader = ContractLoader(w3)

    portfolio_contract = loader.load_contract("PortfolioManager")

    with open(SEED_FILE, "r") as f:
        users = json.load(f)

    for user in users:
        tx = portfolio_contract.functions.initializeBalance(
            user["address"],
            Web3.to_wei(100, "ether")
        ).transact({"from": w3.eth.accounts[0]})

        receipt = w3.eth.wait_for_transaction_receipt(tx)

        print(f"Initialized balance for {user['address']}")
        print("Transaction Hash:", receipt.transactionHash.hex())

    print("All balances initialized successfully.")


if __name__ == "__main__":
    main()