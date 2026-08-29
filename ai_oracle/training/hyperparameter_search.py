"""
Hyperparameter tuning using GridSearch
"""

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


class HyperparameterSearch:

    def __init__(self):
        self.param_grid = {
            "n_estimators": [100, 200, 300],
            "max_depth": [5, 10, 15],
            "min_samples_split": [2, 5]
        }

    def search(self, X, y):
        model = RandomForestClassifier(random_state=42)

        grid = GridSearchCV(
            model,
            self.param_grid,
            cv=3,
            scoring="accuracy",
            verbose=1,
            n_jobs=-1
        )

        grid.fit(X, y)

        return {
            "best_params": grid.best_params_,
            "best_score": float(grid.best_score_)
        }