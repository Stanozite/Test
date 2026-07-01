"""Lag-1 (short-lookback) reversal — the falsification test from Portnaya
(arXiv:2606.29591, "The Bounce Has No Direction").

Her result: SPY lag-1 return autocorrelation is real but comes from *magnitude
shrinkage* (bid-ask bounce/staleness), not *directional reversal* — the sign test
is insignificant (p=0.11). Across a 21-asset panel, crypto is indistinguishable
from a random walk. So a naive "fade the recent move" rule should have NO
directional edge net of costs.

This strategy IS that naive rule, so the backtest is a falsification test: go the
opposite way to the last `lookback`-bar move, but only when the move clears a
magnitude band (the paper's "large move yesterday" condition). If Portnaya is
right, out-of-sample edge on BTC-USD should be ~0 / negative after costs.

ponytail: past-only lookback return; the engine shifts positions +1 bar so no
look-ahead. lookback=1 is the literal lag-1 test; larger values probe whether any
short-horizon fade survives.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class Lag1Reversal(Strategy):
    name = "lag1_reversal"

    @staticmethod
    def param_grid() -> list[dict]:
        grid = []
        for lookback in (1, 2, 3, 5):
            for threshold in (0.0, 0.02, 0.05):
                grid.append({"lookback": lookback, "threshold": threshold})
        return grid

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 1))
        threshold = float(self.params.get("threshold", 0.0))
        close = df["close"].astype(float)
        mom = close / close.shift(lookback) - 1.0        # past-only move
        pos = -np.sign(mom)                              # fade it
        pos = pos.where(mom.abs() > threshold, 0.0)      # only when move clears band
        return pos.fillna(0.0)
