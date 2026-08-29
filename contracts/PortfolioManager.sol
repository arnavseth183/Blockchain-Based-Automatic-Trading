// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
import "./ProtocolStorage.sol";

/*
PortfolioManager
================
Tracks portfolio metrics & PnL
*/

contract PortfolioManager is ProtocolStorage {

    event PortfolioUpdated(address indexed user, uint256 value);

    function updatePortfolio(address user) public {

        uint256[] memory ids = userPositions[user];
        uint256 totalValue;

        for (uint256 i = 0; i < ids.length; i++) {
            Position memory pos = positions[ids[i]];
            if (!pos.isOpen) continue;

            uint256 price = OracleInterface(oracle).getPrice(pos.asset);

            if (pos.isLong) {
                totalValue += (price - pos.entryPrice) * pos.size;
            } else {
                totalValue += (pos.entryPrice - price) * pos.size;
            }
        }

        portfolios[user].totalValue = totalValue;

        emit PortfolioUpdated(user, totalValue);
    }

    function getPortfolio(address user) external view returns (Portfolio memory) {
        return portfolios[user];
    }
}