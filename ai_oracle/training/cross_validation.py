"""
Performs time-series cross validation.
"""

import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score


class TimeSeriesCrossValidator:

    def __init__(self, model, splits=5):
        self.model = model
        self.splits = splits

    def validate(self, X, y):
        tscv = TimeSeriesSplit(n_splits=self.splits)
        scores = []

        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            self.model.fit(X_train, y_train)
            preds = self.model.predict(X_test)

            score = accuracy_score(y_test, preds)
            scores.append(score)

        return {
            "mean_accuracy": float(np.mean(scores)),
            "std_accuracy": float(np.std(scores)),
            "fold_scores": scores
        }