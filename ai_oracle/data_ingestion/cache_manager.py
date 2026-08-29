"""
Caches market data locally to reduce API calls
"""

import os
import pandas as pd


class CacheManager:

    def __init__(self, cache_dir="ai_oracle/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def cache_path(self, symbol):
        return os.path.join(self.cache_dir, f"{symbol}.csv")

    def save(self, symbol, df):
        df.to_csv(self.cache_path(symbol), index=False)

    def load(self, symbol):
        path = self.cache_path(symbol)
        if os.path.exists(path):
            return pd.read_csv(path, parse_dates=["timestamp"])
        return None

    def get_or_fetch(self, symbol, fetch_function):
        cached = self.load(symbol)
        if cached is not None:
            return cached

        df = fetch_function(symbol)
        self.save(symbol, df)
        return df