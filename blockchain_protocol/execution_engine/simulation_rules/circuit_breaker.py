"""
execution_engine/simulation_rules/circuit_breaker_logic.py

Implements price movement circuit breaker
"""


class CircuitBreakerLogic:

    PRICE_LIMIT_PERCENT = 10

    def __init__(self):
        self.reference_prices = {}

    def set_reference_price(self, symbol, price):
        self.reference_prices[symbol] = price

    def is_triggered(self, symbol, current_price):
        reference = self.reference_prices.get(symbol)

        if not reference:
            return False

        change_percent = abs((current_price - reference) / reference) * 100

        if change_percent > self.PRICE_LIMIT_PERCENT:
            return True

        return False