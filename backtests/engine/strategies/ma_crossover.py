"""Seed strategy: moving-average crossover (long/flat).

Long when the fast SMA is above the slow SMA, flat otherwise. Simple, liquid,
and a sane first translation of a trend/momentum finding into testable rules.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class MACrossover(Strategy):
    name = "ma_crossover"

    @staticmethod
    def param_grid() -> list[dict]:
        grid = []
        for fast in (10, 20, 50):
            for slow in (50, 100, 200):
                if fast < slow:
                    grid.append({"fast": fast, "slow": slow})
        return grid

    def signals(self, df: pd.DataFrame) -> pd.Series:
        fast = int(self.params.get("fast", 20))
        slow = int(self.params.get("slow", 100))
        close = df["close"].astype(float)
        fast_ma = close.rolling(fast).mean()
        slow_ma = close.rolling(slow).mean()
        pos = (fast_ma > slow_ma).astype(float)   # 1 long / 0 flat
        return pos.fillna(0.0)
