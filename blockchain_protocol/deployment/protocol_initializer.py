"""
deployment/protocol_initializer.py

Initializes deployed contracts and links them together
"""

import json
from web3 import Web3
from deployment.network_config import NetworkConfig
from web3_layer.contract_loader import ContractLoader


class ProtocolInitializer:

    def __init__(self):
        self.config = NetworkConfig()
        self.w3 = Web3(Web3.HTTPProvider(self.config.RPC_URL))
        self.loader = ContractLoader(self.w3)

        with open("deployment/addresses.json") as f:
            self.addresses = json.load(f)

        self.account = self.w3.eth.account.from_key(self.config.DEPLOYER_PRIVATE_KEY)

    def initialize_protocol(self):
        trading_contract = self.loader.load_deployed(
            "TradingProtocol",
            self.addresses["TradingProtocol"]
        )

        tx = trading_contract.functions.setGovernance(
            self.addresses["Governance"]
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 500000
        })

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Protocol initialized:", receipt.status)


if __name__ == "__main__":
    initializer = ProtocolInitializer()
    initializer.initialize_protocol()