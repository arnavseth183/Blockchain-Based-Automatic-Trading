"""
run_backtest.py

Runs full AI + blockchain simulated backtest.
Stores performance metrics.
"""

import json
from datetime import datetime

from ai_oracle.evaluation.backtester import Backtester
from blockchain_protocol.execution_engine.protocol_controller import ProtocolController


OUTPUT_PATH = "data/backtesting/backtest_results.json"


def main():
    print("=======================================")
    print("Running Full System Backtest")
    print("=======================================")

    protocol = ProtocolController(mock_mode=True)
    backtester = Backtester(protocol=protocol)

    results = backtester.run(
        start_date="2022-01-01",
        end_date="2023-01-01",
        initial_capital=100000
    )

    summary = {
        "timestamp": str(datetime.utcnow()),
        "total_return": results["total_return"],
        "sharpe_ratio": results["sharpe_ratio"],
        "max_drawdown": results["max_drawdown"],
        "trades_executed": results["trades"]
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(summary, f, indent=4)

    print("Backtest Completed")
    print("Return:", summary["total_return"])
    print("Sharpe:", summary["sharpe_ratio"])
    print("Drawdown:", summary["max_drawdown"])


if __name__ == "__main__":
    main()