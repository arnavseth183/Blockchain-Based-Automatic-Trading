"""
web3_layer/gas_manager.py

Handles dynamic gas pricing
"""

class GasManager:

    def __init__(self, w3):
        self.w3 = w3

    def get_gas_price(self):
        return self.w3.eth.gas_price

    def estimate_gas(self, tx):
        return self.w3.eth.estimate_gas(tx)

    def get_priority_fee(self):
        try:
            return self.w3.eth.max_priority_fee
        except:
            return self.w3.to_wei("2", "gwei")