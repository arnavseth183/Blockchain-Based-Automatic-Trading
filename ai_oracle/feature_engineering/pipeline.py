"""
Full feature engineering pipeline
"""

from ai_oracle.feature_engineering.indicators import Indicators
from ai_oracle.feature_engineering.volatility import VolatilityFeatures
from ai_oracle.feature_engineering.feature_builder import FeatureBuilder
from ai_oracle.data_ingestion.data_cleaner import DataCleaner


class FeaturePipeline:

    def __init__(self):
        self.indicators = Indicators()
        self.volatility = VolatilityFeatures()
        self.builder = FeatureBuilder()
        self.cleaner = DataCleaner()

    def process(self, df):
        df = self.cleaner.clean(df)
        df = self.indicators.compute_all(df)
        df = self.volatility.add_volatility(df)

        X, _ = self.builder.prepare(df)
        return X