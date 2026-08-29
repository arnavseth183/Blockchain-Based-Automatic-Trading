"""
test_trading_protocol.py

Tests smart contract interaction and protocol logic.
"""

import pytest
from blockchain_protocol.execution_engine.protocol_controller import ProtocolController


@pytest.fixture
def protocol():
    return ProtocolController(mock_mode=True)


def test_protocol_initialization(protocol):
    assert protocol is not None
    assert protocol.initialized is True


def test_trade_execution(protocol):
    tx_hash = protocol.execute_trade(
        trader="0xABC123",
        asset="RELIANCE",
        quantity=10,
        signal=1
    )

    assert tx_hash is not None
    assert isinstance(tx_hash, str)


def test_invalid_trade_rejection(protocol):
    with pytest.raises(ValueError):
        protocol.execute_trade(
            trader="0xABC123",
            asset="RELIANCE",
            quantity=-5,
            signal=1
        )


def test_protocol_state_update(protocol):
    protocol.execute_trade("0xABC", "TCS", 5, 1)
    state = protocol.get_protocol_state()

    assert "open_positions" in state
    assert isinstance(state["open_positions"], dict)


def test_event_emission(protocol):
    event = protocol.get_last_event()
    assert event is not None