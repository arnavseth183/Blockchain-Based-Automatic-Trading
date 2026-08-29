// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
Oracle Interface
================
External AI / price oracle interface
*/

interface OracleInterface {

    function getPrice(address asset) external view returns (uint256);

    function getVolatility(address asset) external view returns (uint256);

    function getConfidenceScore(address asset) external view returns (uint256);

    function getRiskScore(address user) external view returns (uint256);

    function isMarketOpen() external view returns (bool);
}