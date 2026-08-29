"""
integration_test.py

End-to-end system test:
AI → Signal → Risk → Blockchain → Portfolio Update
"""

import pytest
from ai_oracle.prediction.predictor import Predictor
from blockchain_protocol.execution_engine.protocol_controller import ProtocolController


def test_end_to_end_flow():
    # Step 1: Mock prediction
    class DummyModel:
        def predict(self, X):
            return [1]

    predictor = Predictor(DummyModel())
    signal = predictor.predict([[0]*10])[0]

    assert signal in [0, 1]

    # Step 2: Initialize protocol
    protocol = ProtocolController(mock_mode=True)

    # Step 3: Execute trade
    tx_hash = protocol.execute_trade(
        trader="0xUSER",
        asset="RELIANCE",
        quantity=5,
        signal=signal
    )

    assert tx_hash is not None

    # Step 4: Verify portfolio update
    state = protocol.get_protocol_state()
    assert "open_positions" in state