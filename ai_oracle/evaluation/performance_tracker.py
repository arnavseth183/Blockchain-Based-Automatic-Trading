"""
Performance Tracker
===================
Tracks:
- Strategy growth
- Risk-adjusted metrics
- Trade statistics
- AI performance monitoring
- Benchmark comparison
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PerformanceTracker:

    def __init__(self,
                 backtest_results: pd.DataFrame,
                 benchmark_returns: Optional[pd.Series] = None):

        self.results = backtest_results
        self.benchmark = benchmark_returns

    def total_return(self) -> float:
        return self.results["equity"].iloc[-1] / self.results["equity"].iloc[0] - 1

    def annualized_return(self) -> float:
        total_ret = self.total_return()
        years = len(self.results) / 252
        return (1 + total_ret) ** (1 / years) - 1

    def trade_statistics(self) -> Dict[str, float]:
        returns = self.results["returns"]

        wins = returns[returns > 0]
        losses = returns[returns < 0]

        win_rate = len(wins) / len(returns)
        avg_win = wins.mean() if len(wins) > 0 else 0
        avg_loss = losses.mean() if len(losses) > 0 else 0

        profit_factor = abs(wins.sum() / losses.sum()) if losses.sum() != 0 else np.inf

        return {
            "Win Rate": win_rate,
            "Average Win": avg_win,
            "Average Loss": avg_loss,
            "Profit Factor": profit_factor
        }

    def alpha(self) -> float:
        if self.benchmark is None:
            return 0.0

        strategy_ret = self.results["returns"]
        covariance = np.cov(strategy_ret, self.benchmark)[0][1]
        beta = covariance / np.var(self.benchmark)

        benchmark_annual = np.mean(self.benchmark) * 252
        strategy_annual = np.mean(strategy_ret) * 252

        alpha = strategy_annual - beta * benchmark_annual
        return alpha

    def report(self) -> Dict[str, float]:
        stats = {
            "Total Return": self.total_return(),
            "Annualized Return": self.annualized_return(),
            "Max Drawdown": self._max_drawdown(),
        }

        stats.update(self.trade_statistics())

        if self.benchmark is not None:
            stats["Alpha"] = self.alpha()

        return stats

    def _max_drawdown(self) -> float:
        equity = self.results["equity"]
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        return drawdown.min()