"""
test_risk_manager.py

Tests blockchain risk management logic.
"""

import pytest
from blockchain_protocol.execution_engine.state_validator import RiskValidator


@pytest.fixture
def risk_validator():
    return RiskValidator(max_position_limit=100)


def test_valid_position(risk_validator):
    assert risk_validator.validate_position("TCS", 50) is True


def test_exceed_position_limit(risk_validator):
    with pytest.raises(ValueError):
        risk_validator.validate_position("TCS", 150)


def test_risk_score_calculation(risk_validator):
    score = risk_validator.calculate_risk_score(volatility=0.3, exposure=0.5)

    assert 0 <= score <= 1


def test_circuit_breaker_trigger(risk_validator):
    triggered = risk_validator.circuit_breaker(market_drop=0.2)

    assert isinstance(triggered, bool)