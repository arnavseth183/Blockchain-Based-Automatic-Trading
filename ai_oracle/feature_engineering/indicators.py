"""
Technical indicators computation
"""

import pandas as pd
import numpy as np


class Indicators:

    def sma(self, series, window=14):
        return series.rolling(window).mean()

    def ema(self, series, window=14):
        return series.ewm(span=window, adjust=False).mean()

    def rsi(self, series, window=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window).mean()

        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def macd(self, series):
        ema12 = self.ema(series, 12)
        ema26 = self.ema(series, 26)
        return ema12 - ema26

    def compute_all(self, df: pd.DataFrame):
        df = df.copy()

        df["sma_14"] = self.sma(df["close"])
        df["ema_14"] = self.ema(df["close"])
        df["rsi"] = self.rsi(df["close"])
        df["macd"] = self.macd(df["close"])

        return df.dropna()