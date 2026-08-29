"""
retrain_model.py

Retrains AI trading model using latest processed data.
Saves trained model, scaler, and evaluation metrics.
"""

import os
import json
import joblib
import numpy as np
from datetime import datetime

from ai_oracle.training.trainer import ModelTrainer
from ai_oracle.data_ingestion.data_cleaner import DataCleaner
from ai_oracle.feature_engineering.pipeline import FeaturePipeline
from ai_oracle.evaluation.performance_tracker import PerformanceTracker


DATA_PATH = "data/processed/latest_market_data.csv"
MODEL_PATH = "models/trained/trading_model.pkl"
SCALER_PATH = "models/scalers/feature_scaler.pkl"
METRICS_PATH = "models/evaluation/metrics.json"


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Processed data not found.")
    return np.loadtxt(DATA_PATH, delimiter=",")


def main():
    print("=======================================")
    print("Retraining AI Trading Model")
    print("=======================================")

    raw_data = load_data()

    cleaner = DataCleaner()
    clean_data = cleaner.clean(raw_data)

    pipeline = FeaturePipeline()
    X, y, scaler = pipeline.transform(clean_data)

    trainer = ModelTrainer()
    model = trainer.train(X, y)

    print("Evaluating model...")
    tracker = PerformanceTracker()
    metrics = tracker.evaluate(model, X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    metadata = {
        "retrained_at": str(datetime.utcnow()),
        "samples": len(X),
        "features": X.shape[1]
    }

    with open("models/trained/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("Model retrained and saved successfully.")


if __name__ == "__main__":
    main()