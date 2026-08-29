"""
web3_layer/transaction_builder.py

Builds, signs and sends transactions safely
"""

from deployment.network_config import NetworkConfig
from web3_layer.gas_manager import GasManager
from web3 import Web3


class TransactionBuilder:

    def __init__(self, w3):
        self.w3 = w3
        self.config = NetworkConfig()
        self.gas_manager = GasManager(w3)
        self.account = self.w3.eth.account.from_key(self.config.DEPLOYER_PRIVATE_KEY)

    def build_and_send(self, contract_function):
        nonce = self.w3.eth.get_transaction_count(self.account.address)

        tx = contract_function.build_transaction({
            "from": self.account.address,
            "nonce": nonce,
            "gasPrice": self.gas_manager.get_gas_price(),
            "chainId": self.config.CHAIN_ID
        })

        tx["gas"] = self.w3.eth.estimate_gas(tx)

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt