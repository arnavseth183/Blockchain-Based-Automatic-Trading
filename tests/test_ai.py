"""
test_ai.py

Unit tests for AI model training, prediction,
evaluation and signal formatting pipeline.
"""

import os
import pytest
import numpy as np
import joblib

from ai_oracle.training.trainer import ModelTrainer
from ai_oracle.prediction.predictor import Predictor
from ai_oracle.prediction.confidence_calculator import ConfidenceCalculator
from ai_oracle.evaluation.sharpe_ratio import SharpeRatioCalculator


@pytest.fixture
def sample_training_data():
    X = np.random.rand(200, 10)
    y = np.random.randint(0, 2, 200)
    return X, y


def test_model_training(sample_training_data):
    X, y = sample_training_data
    trainer = ModelTrainer()

    model = trainer.train(X, y)
    assert model is not None
    assert hasattr(model, "predict")


def test_model_prediction(sample_training_data):
    X, y = sample_training_data
    trainer = ModelTrainer()
    model = trainer.train(X, y)

    predictor = Predictor(model)
    predictions = predictor.predict(X[:10])

    assert len(predictions) == 10
    assert set(np.unique(predictions)).issubset({0, 1})


def test_confidence_calculation():
    probabilities = np.array([0.8, 0.6, 0.9])
    confidence = ConfidenceCalculator.calculate(probabilities)

    assert 0 <= confidence <= 1


def test_sharpe_ratio_calculation():
    returns = np.random.normal(0.01, 0.05, 100)
    sharpe = SharpeRatioCalculator.calculate(returns)

    assert isinstance(sharpe, float)


def test_model_persistence(tmp_path, sample_training_data):
    X, y = sample_training_data
    trainer = ModelTrainer()
    model = trainer.train(X, y)

    file_path = tmp_path / "model.pkl"
    joblib.dump(model, file_path)

    assert os.path.exists(file_path)

    loaded_model = joblib.load(file_path)
    assert hasattr(loaded_model, "predict")