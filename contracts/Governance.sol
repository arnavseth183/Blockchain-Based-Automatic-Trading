// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./RiskManager.sol";
import "./PortfolioManager.sol";
import "./OracleInterface.sol";
import "./CircuitBreaker.sol";
import "./ProtocolStorage.sol";

/*
Governance
==========
DAO-based proposal system
*/

contract Governance is ProtocolStorage {

    struct Proposal {
        uint256 id;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
    }

    uint256 public nextProposalId;
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public voted;

    event ProposalCreated(uint256 id);
    event Voted(uint256 id, address voter, bool support);
    event ProposalExecuted(uint256 id);

    function createProposal(string calldata description, uint256 duration)
        external
        onlyGovernance
    {
        proposals[nextProposalId] = Proposal({
            id: nextProposalId,
            description: description,
            votesFor: 0,
            votesAgainst: 0,
            deadline: block.timestamp + duration,
            executed: false
        });

        emit ProposalCreated(nextProposalId);
        nextProposalId++;
    }

    function vote(uint256 proposalId, bool support) external {

        Proposal storage p = proposals[proposalId];
        require(block.timestamp < p.deadline, "Ended");
        require(!voted[proposalId][msg.sender], "Already voted");

        voted[proposalId][msg.sender] = true;

        if (support) {
            p.votesFor++;
        } else {
            p.votesAgainst++;
        }

        emit Voted(proposalId, msg.sender, support);
    }

    function executeProposal(uint256 proposalId) external {

        Proposal storage p = proposals[proposalId];
        require(block.timestamp >= p.deadline, "Not ended");
        require(!p.executed, "Executed");

        require(p.votesFor > p.votesAgainst, "Not approved");

        p.executed = true;

        emit ProposalExecuted(proposalId);
    }
}