"""
Advanced confidence scoring logic
"""

import numpy as np


class ConfidenceCalculator:

    def calculate(self, probabilities):
        max_prob = max(probabilities)

        entropy = -sum(
            p * np.log(p + 1e-9) for p in probabilities
        )

        confidence = max_prob * (1 - entropy)

        confidence_score = min(max(confidence * 100, 0), 100)

        return round(float(confidence_score), 2)

    def calibrate(self, confidence, volatility_factor):
        adjusted = confidence * (1 - volatility_factor)
        return round(max(min(adjusted, 100), 0), 2)