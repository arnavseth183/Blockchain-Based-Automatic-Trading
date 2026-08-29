// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
import "./ProtocolStorage.sol";

/*
TradingProtocol
===============
Core engine:
- Open/Close positions
- Risk validation
- Fee collection
- Oracle pricing
*/

contract TradingProtocol is ProtocolStorage {

    event PositionOpened(uint256 id, address trader);
    event PositionClosed(uint256 id, int256 pnl);

    modifier onlyMarketOpen() {
        require(OracleInterface(oracle).isMarketOpen(), "Market closed");
        _;
    }

    function openPosition(
        address asset,
        uint256 size,
        uint256 collateral,
        bool isLong
    ) external onlyMarketOpen {

        require(
            RiskManager(riskManager).validatePosition(msg.sender, size, collateral),
            "Risk invalid"
        );

        uint256 price = OracleInterface(oracle).getPrice(asset);

        positions[nextPositionId] = Position({
            trader: msg.sender,
            asset: asset,
            size: size,
            entryPrice: price,
            timestamp: block.timestamp,
            isLong: isLong,
            isOpen: true
        });

        userPositions[msg.sender].push(nextPositionId);
        totalOpenInterest += size;

        emit PositionOpened(nextPositionId, msg.sender);
        nextPositionId++;
    }

    function closePosition(uint256 id) external {

        Position storage pos = positions[id];
        require(pos.trader == msg.sender, "Not owner");
        require(pos.isOpen, "Closed");

        uint256 price = OracleInterface(oracle).getPrice(pos.asset);

        int256 pnl;

        if (pos.isLong) {
            pnl = int256(price - pos.entryPrice) * int256(pos.size);
        } else {
            pnl = int256(pos.entryPrice - price) * int256(pos.size);
        }

        pos.isOpen = false;
        totalOpenInterest -= pos.size;

        emit PositionClosed(id, pnl);
    }
}