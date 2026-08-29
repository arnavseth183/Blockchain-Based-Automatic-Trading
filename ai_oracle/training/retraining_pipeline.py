"""
Automated retraining pipeline
"""

import datetime
import json
from ai_oracle.training.trainer import ModelTrainer


class RetrainingPipeline:

    def __init__(self, symbol):
        self.symbol = symbol

    def retrain(self):
        trainer = ModelTrainer(self.symbol)
        accuracy, report = trainer.train()

        metadata = {
            "symbol": self.symbol,
            "retrained_at": str(datetime.datetime.utcnow()),
            "accuracy": float(accuracy)
        }

        with open("models/trained/metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        return metadata