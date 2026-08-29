// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
import "./ProtocolStorage.sol";

/*
RiskManager
===========
Handles:
- Position validation
- Leverage checks
- Liquidation checks
*/

contract RiskManager is ProtocolStorage {

    event RiskParametersUpdated(uint256 leverage, uint256 size);

    function setRiskParameters(
        uint256 _maxLeverage,
        uint256 _maxPositionSize,
        uint256 _liqThreshold,
        uint256 _maxDrawdown
    ) external onlyOwner {

        riskParams = RiskParameters({
            maxLeverage: _maxLeverage,
            maxPositionSize: _maxPositionSize,
            liquidationThreshold: _liqThreshold,
            maxDrawdown: _maxDrawdown
        });

        emit RiskParametersUpdated(_maxLeverage, _maxPositionSize);
    }

    function validatePosition(
        address trader,
        uint256 size,
        uint256 collateral
    ) external view returns (bool) {

        require(size <= riskParams.maxPositionSize, "Size too large");

        uint256 leverage = (size * 1e18) / collateral;
        require(leverage <= riskParams.maxLeverage, "Excess leverage");

        return true;
    }

    function shouldLiquidate(uint256 positionId) external view returns (bool) {

        Position memory pos = positions[positionId];

        if (!pos.isOpen) return false;

        uint256 price = OracleInterface(oracle).getPrice(pos.asset);

        if (pos.isLong && price < pos.entryPrice * riskParams.liquidationThreshold / 10000) {
            return true;
        }

        if (!pos.isLong && price > pos.entryPrice * riskParams.liquidationThreshold / 10000) {
            return true;
        }

        return false;
    }
}