"""
Adapter for NSE-specific formatting
"""

import pandas as pd


class NSEAdapter:

    def __init__(self):
        self.exchange_suffix = ".NS"

    def format_symbol(self, symbol: str):
        if not symbol.endswith(self.exchange_suffix):
            return symbol + self.exchange_suffix
        return symbol

    def normalize_data(self, df: pd.DataFrame):
        df = df.copy()

        df["returns"] = df["close"].pct_change()
        df["log_returns"] = (df["close"] / df["close"].shift(1)).apply(
            lambda x: 0 if pd.isna(x) else pd.np.log(x)
        )

        df = df.dropna()

        return df