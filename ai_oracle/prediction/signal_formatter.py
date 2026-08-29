"""
Formats prediction output for blockchain Oracle submission
"""

import time


class SignalFormatter:

    def format(self, symbol, prediction_dict, confidence):
        direction = 1 if prediction_dict["direction"] == 1 else -1

        return {
            "symbol": symbol,
            "direction": direction,
            "confidence": confidence,
            "timestamp": int(time.time())
        }

    def validate(self, signal):
        required = {"symbol", "direction", "confidence", "timestamp"}
        if not required.issubset(signal.keys()):
            raise ValueError("Invalid signal format")

        if signal["direction"] not in [1, -1]:
            raise ValueError("Invalid direction")

        if not (0 <= signal["confidence"] <= 100):
            raise ValueError("Invalid confidence")

        return True