"""
ai_oracle/training/trainer.py

Core model training logic.
Handles:
- Data preparation
- Model training
- Evaluation
- Saving artifacts
"""

import os
import joblib
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from ai_oracle.feature_engineering.pipeline import FeaturePipeline
from ai_oracle.data_ingestion.market_api_client import MarketAPIClient


class ModelTrainer:

    def __init__(self, symbol, model_dir="models/trained"):
        self.symbol = symbol
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)

        self.pipeline = FeaturePipeline()
        self.client = MarketAPIClient()

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )

    def load_data(self):
        df = self.client.fetch(self.symbol)
        X = self.pipeline.process(df)

        # Rebuild target separately
        df["future_return"] = df["close"].shift(-1) / df["close"] - 1
        df["target"] = (df["future_return"] > 0).astype(int)
        df = df.dropna()

        y = df["target"].values[-len(X):]

        return X, y

    def train(self):
        X, y = self.load_data()

        split = int(len(X) * 0.8)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)

        self.save_model()
        self.save_metrics(accuracy, report)

        return accuracy, report

    def save_model(self):
        path = os.path.join(self.model_dir, "trading_model.pkl")
        joblib.dump(self.model, path)

    def save_metrics(self, accuracy, report):
        metrics = {
            "accuracy": float(accuracy),
            "report": report
        }
        with open(os.path.join(self.model_dir, "metrics.json"), "w") as f:
            json.dump(metrics, f, indent=4)