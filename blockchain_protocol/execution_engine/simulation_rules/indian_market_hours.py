"""
execution_engine/simulation_rules/indian_market_hours.py

Simulates NSE trading hours
"""

import datetime


class IndianMarketHours:

    MARKET_OPEN = datetime.time(9, 15)
    MARKET_CLOSE = datetime.time(15, 30)

    def is_market_open(self):
        now = datetime.datetime.now().time()

        if self.MARKET_OPEN <= now <= self.MARKET_CLOSE:
            return True

        return False