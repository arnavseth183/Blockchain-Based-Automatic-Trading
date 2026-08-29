"""
Builds final ML-ready features
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler


class FeatureBuilder:

    def __init__(self):
        self.scaler = StandardScaler()

    def build_target(self, df: pd.DataFrame):
        df["future_return"] = df["close"].shift(-1) / df["close"] - 1
        df["target"] = (df["future_return"] > 0).astype(int)
        return df

    def select_features(self, df: pd.DataFrame):
        features = [
            "sma_14",
            "ema_14",
            "rsi",
            "macd",
            "volatility",
            "atr"
        ]
        return df[features]

    def scale(self, X):
        return self.scaler.fit_transform(X)

    def prepare(self, df: pd.DataFrame):
        df = self.build_target(df)
        df = df.dropna()

        X = self.select_features(df)
        y = df["target"]

        X_scaled = self.scale(X)

        return X_scaled, y