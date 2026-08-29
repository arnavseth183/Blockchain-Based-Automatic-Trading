"""
test_portfolio_manager.py

Tests blockchain portfolio accounting logic.
"""

import pytest
from blockchain_protocol.execution_engine.portfolio_reader import PortfolioReader


@pytest.fixture
def portfolio():
    return PortfolioReader(mock_mode=True)


def test_initial_balance(portfolio):
    balance = portfolio.get_balance("0xUSER1")
    assert balance >= 0


def test_add_position(portfolio):
    portfolio.add_position("0xUSER1", "INFY", 10)
    positions = portfolio.get_positions("0xUSER1")

    assert "INFY" in positions


def test_remove_position(portfolio):
    portfolio.add_position("0xUSER1", "INFY", 10)
    portfolio.remove_position("0xUSER1", "INFY")

    positions = portfolio.get_positions("0xUSER1")
    assert "INFY" not in positions


def test_portfolio_value_calculation(portfolio):
    portfolio.add_position("0xUSER1", "TCS", 5)
    value = portfolio.calculate_portfolio_value("0xUSER1")

    assert isinstance(value, float)