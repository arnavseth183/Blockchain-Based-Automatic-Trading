# ui/utils/data_source_manager.py

import random
import pandas as pd
import yfinance as yf
from datetime import datetime

class DataSourceManager:

    def __init__(self, mode="SIMULATED"):
        self.mode = mode

    def set_mode(self, mode):
        self.mode = mode

    def is_market_open(self):
        now = datetime.now()
        return now.hour >= 9 and now.hour <= 15

    def get_data(self, symbol):
        if self.mode == "LIVE" and self.is_market_open():
            return self.get_live_data(symbol)
        else:
            return self.get_simulated_data(symbol)

    def get_live_data(self, symbol):
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            hist = ticker.history(period="1d", interval="1m")

            if hist.empty:
                return self.get_simulated_data(symbol)

            price = float(hist["Close"].iloc[-1])

            return {
                "symbol": symbol,
                "price": price,
                "historical": hist["Close"]
            }

        except Exception:
            return self.get_simulated_data(symbol)

    def get_simulated_data(self, symbol):
        price = random.uniform(1000, 3000)
        historical = pd.Series(
            [price + random.uniform(-10, 10) for _ in range(50)]
        )

        return {
            "symbol": symbol,
            "price": price,
            "historical": historical
        }