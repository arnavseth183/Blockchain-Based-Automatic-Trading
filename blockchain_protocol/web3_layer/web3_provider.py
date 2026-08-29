"""
web3_layer/web3_provider.py

Creates and manages Web3 connection for the blockchain protocol.

Responsibilities:
- Establish blockchain connection
- Provide Web3 instance globally
- Wallet generation & import
- Transaction signing & broadcasting
- Gas estimation
- Nonce management
- Transaction confirmation
- Smart contract interaction helpers
- Blockchain diagnostics
"""

import logging
import time
from web3 import Web3
from web3.exceptions import ProviderConnectionError
from ..deployment.network_config import NetworkConfig


# ---------------------------------------------------
# Logging Setup
# ---------------------------------------------------

logging.basicConfig(
    filename="logs/blockchain.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------
# Web3 Provider Class
# ---------------------------------------------------

class Web3Provider:

    def __init__(self):

        self.config = NetworkConfig()
        self.rpc_url = self.config.RPC_URL

        logging.info(f"Connecting to blockchain node: {self.rpc_url}")

        self.w3 = self._connect()

    # ---------------------------------------------------
    # Connection Logic
    # ---------------------------------------------------

    def _connect(self, retries: int = 3, delay: int = 2):

        for attempt in range(retries):

            try:

                w3 = Web3(Web3.HTTPProvider(self.rpc_url))

                if w3.is_connected():

                    logging.info("Web3 connection established successfully")

                    return w3

                else:

                    logging.warning(
                        f"Connection attempt {attempt+1} failed"
                    )

            except ProviderConnectionError as e:

                logging.error(f"Provider error: {str(e)}")

            time.sleep(delay)

        raise ConnectionError(
            f"Failed to connect to blockchain node after {retries} attempts."
        )

    # ---------------------------------------------------
    # Basic Getters
    # ---------------------------------------------------

    def get_web3(self):

        """Returns Web3 instance"""

        return self.w3

    def get_chain_id(self):

        """Returns network chain ID"""

        return self.w3.eth.chain_id

    def get_block_number(self):

        """Returns latest block"""

        return self.w3.eth.block_number

    def get_gas_price(self):

        """Returns gas price in GWEI"""

        gas_price = self.w3.eth.gas_price

        return float(self.w3.from_wei(gas_price, "gwei"))

    # ---------------------------------------------------
    # Wallet Utilities
    # ---------------------------------------------------

    def create_account(self):

        """
        Generate new wallet
        """

        account = self.w3.eth.account.create()

        wallet = {
            "address": account.address,
            "private_key": account.key.hex()
        }

        logging.info(f"New wallet created: {wallet['address']}")

        return wallet

    def import_wallet(self, private_key):

        """
        Import wallet from private key
        """

        account = self.w3.eth.account.from_key(private_key)

        wallet = {
            "address": account.address,
            "private_key": private_key
        }

        logging.info(f"Wallet imported: {wallet['address']}")

        return wallet

    def is_valid_address(self, address):

        return self.w3.is_address(address)

    def checksum_address(self, address):

        if not self.is_valid_address(address):
            raise ValueError("Invalid Ethereum address")

        return self.w3.to_checksum_address(address)

    def get_balance(self, address):

        address = self.checksum_address(address)

        balance = self.w3.eth.get_balance(address)

        return float(self.w3.from_wei(balance, "ether"))

    # ---------------------------------------------------
    # Nonce Handling
    # ---------------------------------------------------

    def get_nonce(self, address):

        """
        Returns wallet nonce
        """

        address = self.checksum_address(address)

        return self.w3.eth.get_transaction_count(address)

    # ---------------------------------------------------
    # Transaction Utilities
    # ---------------------------------------------------

    def estimate_gas(self, transaction):

        """
        Estimate gas usage
        """

        return self.w3.eth.estimate_gas(transaction)

    def sign_transaction(self, transaction, private_key):

        """
        Sign transaction with private key
        """

        signed_tx = self.w3.eth.account.sign_transaction(
            transaction,
            private_key
        )

        return signed_tx

    def send_signed_transaction(self, signed_tx):

        """
        Broadcast signed transaction
        """

        tx_hash = self.w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        logging.info(f"Transaction broadcasted: {tx_hash.hex()}")

        return tx_hash.hex()

    def wait_for_confirmation(self, tx_hash, timeout=120):

        """
        Wait for blockchain confirmation
        """

        start_time = time.time()

        while True:

            try:

                receipt = self.w3.eth.get_transaction_receipt(tx_hash)

                if receipt:

                    logging.info(f"Transaction confirmed: {tx_hash}")

                    return receipt

            except Exception:

                pass

            if time.time() - start_time > timeout:

                raise TimeoutError("Transaction confirmation timeout")

            time.sleep(2)

    # ---------------------------------------------------
    # Transaction Readers
    # ---------------------------------------------------

    def get_transaction(self, tx_hash):

        return self.w3.eth.get_transaction(tx_hash)

    def get_transaction_receipt(self, tx_hash):

        return self.w3.eth.get_transaction_receipt(tx_hash)

    # ---------------------------------------------------
    # Event Listener Support
    # ---------------------------------------------------

    def create_event_filter(self, contract, event_name, from_block="latest"):

        """
        Create filter for smart contract events
        """

        event = getattr(contract.events, event_name)

        return event.create_filter(fromBlock=from_block)

    # ---------------------------------------------------
    # Block Utilities
    # ---------------------------------------------------

    def get_block_timestamp(self, block_number):

        block = self.w3.eth.get_block(block_number)

        return block["timestamp"]

    # ---------------------------------------------------
    # Network Diagnostics
    # ---------------------------------------------------

    def network_status(self):

        """
        Returns network health metrics
        """

        try:

            status = {

                "connected": self.w3.is_connected(),

                "chain_id": self.get_chain_id(),

                "latest_block": self.get_block_number(),

                "gas_price_gwei": self.get_gas_price()

            }

            return status

        except Exception as e:

            logging.error(f"Network status error: {str(e)}")

            return {

                "connected": False,

                "error": str(e)

            }


# ---------------------------------------------------
# Global Helper
# ---------------------------------------------------

def get_web3_connection():

    """
    Global helper used across the project
    """

    provider = Web3Provider()

    return provider.get_web3()