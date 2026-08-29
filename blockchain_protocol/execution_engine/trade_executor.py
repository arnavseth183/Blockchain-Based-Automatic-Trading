"""
execution_engine/trade_executor.py

Responsible for:
- Receiving AI prediction signals
- Validating via state_validator
- Enforcing protocol rules
- Executing trades via smart contracts
- Broadcasting transaction to blockchain node
- Logging transaction details
"""

import time
import uuid
import logging
from web3 import Web3

from .state_validator import StateValidator
from .protocol_controller import ProtocolController
from ..web3_layer.contract_loader import ContractLoader
from ..web3_layer.web3_provider import get_web3_connection
from .simulation_rules.indian_market_hours import IndianMarketHours
from .simulation_rules.circuit_breaker import CircuitBreakerLogic


logging.basicConfig(
    filename="logs/transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TradeExecutor:

    def __init__(self):

        # Connect to blockchain node
        self.web3 = get_web3_connection()

        if not self.web3.is_connected():
            raise Exception("Blockchain node connection failed")

        # Load contracts
        self.contract_loader = ContractLoader(self.web3)

        self.trading_contract = self.contract_loader.load_contract(
            "TradingProtocol"
        )

        self.portfolio_contract = self.contract_loader.load_contract(
            "PortfolioManager"
        )

        # Internal validators
        self.validator = StateValidator()
        self.protocol = ProtocolController()
        self.market_hours = IndianMarketHours()
        self.circuit_breaker = CircuitBreakerLogic()

        logging.info("TradeExecutor initialized successfully")

    def execute_trade(self, user_wallet, symbol, action, quantity, price):
        """
        Main entry for trade execution.
        Executes trade via TradingProtocol smart contract.
        """

        trade_id = str(uuid.uuid4())
        timestamp = int(time.time())

        try:

            # -------------------------------------------------
            # Step 1: Check Market Hours
            # -------------------------------------------------

            if not self.market_hours.is_market_open():
                return {"status": "rejected", "reason": "Market closed"}

            # -------------------------------------------------
            # Step 2: Circuit Breaker Check
            # -------------------------------------------------

            if self.circuit_breaker.is_triggered(symbol, price):
                return {"status": "rejected", "reason": "Circuit breaker active"}

            # -------------------------------------------------
            # Step 3: State Validation
            # -------------------------------------------------

            validation = self.validator.validate_trade(
                user_wallet, symbol, action, quantity, price
            )

            if not validation["valid"]:
                return {"status": "rejected", "reason": validation["reason"]}

            # -------------------------------------------------
            # Step 4: Protocol Governance Rules
            # -------------------------------------------------

            protocol_check = self.protocol.enforce_rules(
                user_wallet, symbol, action, quantity
            )

            if not protocol_check["approved"]:
                return {"status": "rejected", "reason": protocol_check["reason"]}

            # -------------------------------------------------
            # Step 5: Convert Symbol to Bytes
            # Solidity prefers bytes32
            # -------------------------------------------------

            symbol_bytes = Web3.to_bytes(text=symbol)

            # -------------------------------------------------
            # Step 6: Prepare Smart Contract Transaction
            # -------------------------------------------------

            nonce = self.web3.eth.get_transaction_count(user_wallet)

            transaction = self.trading_contract.functions.executeTrade(
                user_wallet,
                symbol_bytes,
                action,
                int(quantity),
                int(price),
                timestamp
            ).build_transaction({
                "from": user_wallet,
                "nonce": nonce,
                "gas": 300000,
                "gasPrice": self.web3.to_wei("20", "gwei")
            })

            # -------------------------------------------------
            # Step 7: Sign Transaction
            # -------------------------------------------------

            private_key = self.contract_loader.get_private_key(user_wallet)

            signed_tx = self.web3.eth.account.sign_transaction(
                transaction,
                private_key
            )

            # -------------------------------------------------
            # Step 8: Broadcast Transaction
            # -------------------------------------------------

            tx_hash = self.web3.eth.send_raw_transaction(
                signed_tx.rawTransaction
            )

            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            # -------------------------------------------------
            # Step 9: Log Transaction
            # -------------------------------------------------

            logging.info(
                f"Trade Executed | TradeID={trade_id} | Wallet={user_wallet} "
                f"| Symbol={symbol} | Action={action} | Qty={quantity} "
                f"| Price={price} | TxHash={tx_hash.hex()}"
            )

            return {
                "status": "executed",
                "trade_id": trade_id,
                "tx_hash": tx_hash.hex(),
                "block": receipt.blockNumber
            }

        except Exception as e:

            logging.error(f"Trade execution failed: {str(e)}")

            return {
                "status": "failed",
                "reason": str(e)
            }

    def cancel_trade(self, trade_id, user_wallet):
        """
        Cancels pending trade via Governance smart contract
        """

        try:

            governance_contract = self.contract_loader.load_contract(
                "Governance"
            )

            nonce = self.web3.eth.get_transaction_count(user_wallet)

            tx = governance_contract.functions.cancelTrade(
                trade_id
            ).build_transaction({
                "from": user_wallet,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": self.web3.to_wei("20", "gwei")
            })

            private_key = self.contract_loader.get_private_key(user_wallet)

            signed_tx = self.web3.eth.account.sign_transaction(
                tx,
                private_key
            )

            tx_hash = self.web3.eth.send_raw_transaction(
                signed_tx.rawTransaction
            )

            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            logging.info(f"Trade cancelled | {trade_id}")

            return {
                "status": "cancelled",
                "tx_hash": tx_hash.hex(),
                "block": receipt.blockNumber
            }

        except Exception as e:

            logging.error(f"Trade cancellation failed: {str(e)}")

            return {
                "status": "failed",
                "reason": str(e)
            }