"""
execution_engine/portfolio_reader.py

Reads on-chain portfolio state
"""

class PortfolioReader:

    def __init__(self, blockchain_interface):
        self.blockchain = blockchain_interface

    def get_user_portfolio(self, user_id):
        """
        Fetch portfolio from blockchain state
        """

        state = self.blockchain.get_state("portfolio", user_id)

        if not state:
            return {
                "cash": 0,
                "holdings": {}
            }

        return state

    def get_position(self, user_id, symbol):
        portfolio = self.get_user_portfolio(user_id)
        return portfolio["holdings"].get(symbol, 0)

    def calculate_portfolio_value(self, user_id, market_prices):
        portfolio = self.get_user_portfolio(user_id)

        total_value = portfolio["cash"]

        for symbol, qty in portfolio["holdings"].items():
            price = market_prices.get(symbol, 0)
            total_value += qty * price

        return total_value