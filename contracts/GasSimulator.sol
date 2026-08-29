// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
/*
GasSimulator
============
Estimates gas costs for complex transactions
*/

contract GasSimulator {

    uint256 public constant BASE_GAS = 21000;
    uint256 public constant POSITION_OPEN_GAS = 120000;
    uint256 public constant POSITION_CLOSE_GAS = 90000;

    function estimateOpenPosition(uint256 complexity)
        external
        pure
        returns (uint256)
    {
        return BASE_GAS + POSITION_OPEN_GAS + (complexity * 1000);
    }

    function estimateClosePosition(uint256 complexity)
        external
        pure
        returns (uint256)
    {
        return BASE_GAS + POSITION_CLOSE_GAS + (complexity * 800);
    }

    function simulateBatch(uint256 count)
        external
        pure
        returns (uint256 totalGas)
    {
        totalGas = BASE_GAS;

        for (uint256 i = 0; i < count; i++) {
            totalGas += POSITION_OPEN_GAS;
        }
    }
}