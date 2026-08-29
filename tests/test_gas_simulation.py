"""
test_gas_simulation.py

Tests gas cost modeling and blockchain fee simulation.
"""

import pytest
from blockchain_protocol.web3_layer.gas_manager import GasManager


@pytest.fixture
def gas_manager():
    return GasManager(mock_mode=True)


def test_gas_estimation(gas_manager):
    gas = gas_manager.estimate_gas("executeTrade")

    assert gas > 0


def test_fee_calculation(gas_manager):
    fee = gas_manager.calculate_fee(gas_used=21000, gas_price=50)

    assert fee > 0


def test_dynamic_gas_adjustment(gas_manager):
    adjusted = gas_manager.adjust_for_network_load(load_factor=1.5)

    assert adjusted >= 1.0


def test_simulation_output(gas_manager):
    simulation = gas_manager.simulate_transaction("executeTrade")

    assert "gas_used" in simulation
    assert "estimated_cost" in simulation