import os
import joblib
import numpy as np
import pandas as pd


class Predictor:

    def __init__(self, config):

        self.config = config
        model_path = config.MODEL_PATH
        scaler_path = config.SCALER_PATH

        self.model = None
        self.scaler = None

        # Load model safely
        if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
            try:
                self.model = joblib.load(model_path)
            except Exception as e:
                print("Model load failed:", e)
        else:
            print("Model file missing or empty. Running in mock mode.")

        # Load scaler safely
        if os.path.exists(scaler_path) and os.path.getsize(scaler_path) > 0:
            try:
                self.scaler = joblib.load(scaler_path)
            except Exception as e:
                print("Scaler load failed:", e)
        else:
            print("Scaler file missing or empty.")

    # ------------------------------------------------
    # MOCK DATA FETCH
    # ------------------------------------------------

    def fetch_latest_data(self, stock):

        # Simple dummy data so app runs
        data = pd.DataFrame({
            "Close": np.random.uniform(1000, 2000, 100)
        })

        return data

    # ------------------------------------------------
    # MOCK PREDICTION
    # ------------------------------------------------

    def generate_signal(self, market_data):

        if self.model is None:
            # Mock signal if model not loaded
            return {
                "signal": np.random.choice(["BUY", "SELL", "HOLD"]),
                "confidence": np.random.uniform(0.5, 0.9)
            }

        # Real model logic would go here
        return {
            "signal": "HOLD",
            "confidence": 0.5
        }