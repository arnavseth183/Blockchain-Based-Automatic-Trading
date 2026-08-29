# Decentralized AI Blockchain Trading Protocol

## Overview

This project implements a decentralized trading protocol where:

- AI acts as an oracle for Buy/Sell/Hold prediction.
- Blockchain enforces execution, risk management, and portfolio tracking.
- Streamlit provides a real-time interactive dashboard.
- Trades are stored on-chain.
- Users start with 10,000 simulated Ether.

---

## Architecture

Market Data → AI Oracle → Signal → Smart Contracts → Portfolio Update → UI

AI:
- Historical OHLCV ingestion
- Feature engineering
- Classification model
- Confidence threshold

Blockchain:
- TradingProtocol.sol
- PortfolioManager.sol
- RiskManager.sol
- Governance.sol
- Gas simulation

---

## Features

- Delayed real-time market data
- AI confidence-based execution
- On-chain portfolio accounting
- Gas fee simulation
- Risk scoring
- SEBI simulation constraints
- Auto-refresh UI

---

## How To Run

1. Install dependencies:

   pip install -r requirements.txt

2. Start Ganache:

   docker-compose up

3. Deploy contracts:

   python blockchain_protocol/deployment/deploy_protocol.py

4. Run Streamlit:

   streamlit run app.py

---

## Academic Contribution

This project demonstrates:

- Hybrid AI-Oracle Blockchain architecture
- Decentralized enforcement of trading logic
- Simulation of regulatory compliance in India
- Transparent execution and governance

---

## Disclaimer

This is a simulation-based research project.
No real trading is executed.