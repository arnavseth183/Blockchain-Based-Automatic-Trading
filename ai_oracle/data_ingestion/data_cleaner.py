"""
Data cleaning and validation logic
"""

import pandas as pd
import numpy as np


class DataCleaner:

    def remove_outliers(self, df: pd.DataFrame):
        df = df.copy()

        for col in ["open", "high", "low", "close"]:
            z_score = (df[col] - df[col].mean()) / df[col].std()
            df = df[(z_score < 3) & (z_score > -3)]

        return df

    def fill_missing(self, df: pd.DataFrame):
        return df.fillna(method="ffill").fillna(method="bfill")

    def validate_structure(self, df: pd.DataFrame):
        required = {"open", "high", "low", "close", "volume"}
        if not required.issubset(df.columns):
            raise ValueError("Invalid data structure")
        return True

    def clean(self, df: pd.DataFrame):
        self.validate_structure(df)
        df = self.fill_missing(df)
        df = self.remove_outliers(df)
        return df