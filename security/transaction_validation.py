from datetime import datetime


class TransactionValidator:

    """
    Validates transaction parameters before blockchain submission.
    """

    def __init__(self, max_position_limit=1000):
        self.max_position_limit = max_position_limit

    def validate_trade(self, symbol: str, quantity: int, action: str):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > self.max_position_limit:
            raise ValueError("Position limit exceeded")

        if action not in ["BUY", "SELL"]:
            raise ValueError("Invalid trade action")

        return True

    def validate_timestamp(self, timestamp: str):
        tx_time = datetime.fromisoformat(timestamp)
        now = datetime.utcnow()

        delta = (now - tx_time).total_seconds()

        if delta > 120:
            raise ValueError("Transaction expired")

        return True

    def validate_nonce(self, nonce: int, expected_nonce: int):
        if nonce != expected_nonce:
            raise ValueError("Invalid nonce")

        return True

    def validate_signature(self, signature_valid: bool):
        if not signature_valid:
            raise ValueError("Invalid signature")

        return True