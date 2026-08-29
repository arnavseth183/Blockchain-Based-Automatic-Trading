// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
/*
CircuitBreaker
==============
Emergency pause & drawdown protection
*/

contract CircuitBreaker {

    bool public paused;
    uint256 public maxSystemDrawdown;
    uint256 public lastTriggerTime;

    event Paused(address indexed by);
    event Unpaused(address indexed by);
    event BreakerTriggered(uint256 timestamp);

    modifier whenNotPaused() {
        require(!paused, "Paused");
        _;
    }

    function _triggerBreaker() internal {
        paused = true;
        lastTriggerTime = block.timestamp;
        emit BreakerTriggered(block.timestamp);
    }

    function pause() external {
        paused = true;
        emit Paused(msg.sender);
    }

    function unpause() external {
        paused = false;
        emit Unpaused(msg.sender);
    }
}