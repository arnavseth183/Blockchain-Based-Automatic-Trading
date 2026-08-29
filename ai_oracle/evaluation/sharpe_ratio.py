"""
Sharpe Ratio Calculator
=======================
Supports:
- Rolling Sharpe
- Annualized Sharpe
- Sortino Ratio
- Risk-adjusted metrics
"""

import numpy as np
import pandas as pd
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class SharpeRatio:
    def __init__(self,
                 returns: pd.Series,
                 risk_free_rate: float = 0.05,
                 trading_days: int = 252):

        self.returns = returns
        self.risk_free_rate = risk_free_rate
        self.trading_days = trading_days

    def annualized_return(self) -> float:
        compounded = (1 + self.returns).prod()
        years = len(self.returns) / self.trading_days
        return compounded ** (1 / years) - 1

    def annualized_volatility(self) -> float:
        return self.returns.std() * np.sqrt(self.trading_days)

    def calculate(self) -> float:
        excess_return = self.annualized_return() - self.risk_free_rate
        volatility = self.annualized_volatility()

        if volatility == 0:
            return 0.0

        sharpe = excess_return / volatility
        logger.info(f"Sharpe Ratio: {sharpe}")
        return sharpe

    def rolling_sharpe(self, window: int = 60) -> pd.Series:
        rolling_mean = self.returns.rolling(window).mean()
        rolling_std = self.returns.rolling(window).std()

        rolling_sharpe = (rolling_mean * np.sqrt(self.trading_days)) / rolling_std
        return rolling_sharpe

    def sortino_ratio(self) -> float:
        downside_returns = self.returns[self.returns < 0]
        downside_std = downside_returns.std() * np.sqrt(self.trading_days)

        if downside_std == 0:
            return 0.0

        excess_return = self.annualized_return() - self.risk_free_rate
        return excess_return / downside_std

    def information_ratio(self, benchmark_returns: pd.Series) -> float:
        active_returns = self.returns - benchmark_returns
        tracking_error = active_returns.std() * np.sqrt(self.trading_days)

        if tracking_error == 0:
            return 0.0

        return active_returns.mean() / tracking_error