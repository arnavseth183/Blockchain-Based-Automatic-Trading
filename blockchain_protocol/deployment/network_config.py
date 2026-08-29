"""
deployment/network_config.py

Manages blockchain network configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class NetworkConfig:

    def __init__(self):
        self.NETWORK = os.getenv("NETWORK", "local")

        if self.NETWORK == "local":
            self.RPC_URL = "http://127.0.0.1:8545"
        elif self.NETWORK == "testnet":
            self.RPC_URL = os.getenv("TESTNET_RPC")
        else:
            raise Exception("Unsupported network")

        self.DEPLOYER_PRIVATE_KEY = os.getenv("PRIVATE_KEY")

        if not self.DEPLOYER_PRIVATE_KEY:
            raise Exception("Missing private key")

        self.CHAIN_ID = 1337 if self.NETWORK == "local" else 5

    def summary(self):
        return {
            "network": self.NETWORK,
            "rpc_url": self.RPC_URL,
            "chain_id": self.CHAIN_ID
        }