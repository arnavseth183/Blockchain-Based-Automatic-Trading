"""
Risk Scoring Engine
===================
Computes:
- VaR (Value at Risk)
- CVaR
- Volatility-based risk
- Drawdown risk
- Tail risk
- AI-based composite risk score
"""

import numpy as np
import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class RiskScore:

    def __init__(self,
                 returns: pd.Series,
                 confidence_level: float = 0.95):

        self.returns = returns
        self.confidence_level = confidence_level

    def historical_var(self) -> float:
        var = np.percentile(self.returns, (1 - self.confidence_level) * 100)
        return var

    def conditional_var(self) -> float:
        var = self.historical_var()
        cvar = self.returns[self.returns <= var].mean()
        return cvar

    def max_drawdown(self) -> float:
        cumulative = (1 + self.returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()

    def volatility_risk(self) -> float:
        return self.returns.std() * np.sqrt(252)

    def tail_risk(self) -> float:
        tail = self.returns[self.returns < 0]
        return np.mean(np.abs(tail))

    def composite_score(self) -> Dict[str, float]:
        var = abs(self.historical_var())
        cvar = abs(self.conditional_var())
        drawdown = abs(self.max_drawdown())
        volatility = self.volatility_risk()
        tail = self.tail_risk()

        # AI-ready weighted scoring
        score = (
            0.25 * var +
            0.25 * cvar +
            0.20 * drawdown +
            0.20 * volatility +
            0.10 * tail
        )

        normalized_score = min(score * 10, 100)

        return {
            "VaR": var,
            "CVaR": cvar,
            "Drawdown": drawdown,
            "Volatility": volatility,
            "Tail Risk": tail,
            "Composite Risk Score": normalized_score
        }