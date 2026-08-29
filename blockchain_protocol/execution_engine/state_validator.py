"""
execution_engine/state_validator.py

Ensures trade consistency before blockchain commit
"""
from .portfolio_reader import PortfolioReader


class StateValidator:

    def __init__(self):
        self.reader = PortfolioReader(blockchain_interface=None)

    def validate_trade(self, user_id, symbol, action, quantity, price):
        """
        Validate:
        - Sufficient balance
        - Sufficient holdings
        """

        portfolio = self.reader.get_user_portfolio(user_id)

        if action == "BUY":
            required_cash = quantity * price
            if portfolio["cash"] < required_cash:
                return {
                    "valid": False,
                    "reason": "Insufficient cash balance"
                }

        elif action == "SELL":
            holdings = portfolio["holdings"].get(symbol, 0)
            if holdings < quantity:
                return {
                    "valid": False,
                    "reason": "Insufficient holdings"
                }

        return {"valid": True}