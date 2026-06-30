"""Cost-aware momentum (long/flat).

Translation of Bysik & Slepaczuk (arXiv:2606.00060): the bottleneck in crypto
trading is not the forecast but turning it into trades after costs. Their fix is
a filter that only acts when the predicted move exceeds a transaction-cost-based
threshold, cutting turnover.

Here the "forecast" is a simple lookback return (momentum) standing in for the ML
signal. Go long only when momentum clears a threshold band; otherwise stay flat.
threshold=0 degenerates to plain "long if up", giving a baseline to measure whether
the magnitude filter actually helps net of costs.

ponytail: momentum proxies the ML forecast; the threshold band IS the paper's
mechanism. Swap in a real predicted-return series later if we want to replicate
the XGBoost config exactly.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class CostAwareMomentum(Strategy):
    name = "cost_aware_momentum"

    @staticmethod
    def param_grid() -> list[dict]:
        grid = []
        for lookback in (5, 10, 20):
            for threshold in (0.0, 0.02, 0.05):
                grid.append({"lookback": lookback, "threshold": threshold})
        return grid

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 10))
        threshold = float(self.params.get("threshold", 0.02))
        close = df["close"].astype(float)
        mom = close / close.shift(lookback) - 1.0        # past-only lookback return
        pos = (mom > threshold).astype(float)            # long only when edge clears band
        return pos.fillna(0.0)
