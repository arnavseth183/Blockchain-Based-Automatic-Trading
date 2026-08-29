// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
/*
ProtocolStorage
===============
Central storage layer for upgradeable architecture.
All core contracts inherit this to maintain layout consistency.
*/

contract ProtocolStorage {

    /* ========== STRUCTS ========== */

    struct Position {
        address trader;
        address asset;
        uint256 size;
        uint256 entryPrice;
        uint256 timestamp;
        bool isLong;
        bool isOpen;
    }

    struct Portfolio {
        uint256 totalValue;
        uint256 totalPnL;
        uint256 openPositions;
        uint256 riskScore;
    }

    struct RiskParameters {
        uint256 maxLeverage;
        uint256 maxPositionSize;
        uint256 liquidationThreshold;
        uint256 maxDrawdown;
    }

    /* ========== STATE VARIABLES ========== */

    address public owner;
    address public governance;
    address public oracle;
    address public riskManager;
    address public portfolioManager;

    uint256 public protocolFee; // basis points
    uint256 public totalOpenInterest;

    mapping(uint256 => Position) internal positions;
    mapping(address => Portfolio) internal portfolios;
    mapping(address => uint256[]) internal userPositions;

    RiskParameters public riskParams;

    uint256 internal nextPositionId;

    /* ========== EVENTS ========== */

    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);
    event GovernanceUpdated(address indexed newGov);
    event OracleUpdated(address indexed newOracle);
    event RiskManagerUpdated(address indexed newRiskManager);

    /* ========== MODIFIERS ========== */

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyGovernance() {
        require(msg.sender == governance, "Not governance");
        _;
    }

    /* ========== CONSTRUCTOR ========== */

    constructor() {
        owner = msg.sender;
        nextPositionId = 1;
        protocolFee = 20; // 0.20%
    }

    /* ========== ADMIN FUNCTIONS ========== */

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function setGovernance(address _gov) external onlyOwner {
        governance = _gov;
        emit GovernanceUpdated(_gov);
    }

    function setOracle(address _oracle) external onlyOwner {
        oracle = _oracle;
        emit OracleUpdated(_oracle);
    }

    function setRiskManager(address _risk) external onlyOwner {
        riskManager = _risk;
        emit RiskManagerUpdated(_risk);
    }

    function setPortfolioManager(address _pm) external onlyOwner {
        portfolioManager = _pm;
    }
}