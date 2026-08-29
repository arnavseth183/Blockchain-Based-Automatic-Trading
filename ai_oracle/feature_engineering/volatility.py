"""
Volatility feature generation
"""

import numpy as np
import pandas as pd


class VolatilityFeatures:

    def rolling_volatility(self, series, window=14):
        return series.pct_change().rolling(window).std()

    def atr(self, df: pd.DataFrame, window=14):
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)

        return true_range.rolling(window).mean()

    def add_volatility(self, df: pd.DataFrame):
        df = df.copy()
        df["volatility"] = self.rolling_volatility(df["close"])
        df["atr"] = self.atr(df)
        return df.dropna()