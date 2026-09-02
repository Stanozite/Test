"""Multi-scale move-threshold (long/flat).

Translation of Yousefnezhad, Mansourfar & Feizi Derakhshi (arXiv:2608.26174),
"Forecasting Economically Significant Bitcoin Moves: A Multi-Scale TCN with
Profit-Optimized Thresholds". Their model asks "will BTC rise >5% within 7 days?"
using an InceptionTCN that fuses dilated features over 1-4 day horizons, then
applies a *profit-optimized decision threshold* to turn the score into trades.

The tradable core, stripped of the TCN and the on-chain/sentiment inputs we don't
have: (a) a **multi-scale momentum fusion** — average past-only lookback returns
over horizons 1..maxh, standing in for the 1-4d dilated features — and (b) a
**profit threshold**: go long only when the fused up-signal is large enough to be
"economically significant", flat otherwise (their task is long-only up-moves).
The paper's "profit-optimized threshold" is exactly what the vectorbt sweep does:
it picks the threshold that maximises train performance, then we check OOS.

Distinct from `cost_aware_momentum` (single lookback, cost-band framing) by the
multi-horizon fusion that is the paper's signature.

ponytail: momentum fusion proxies the InceptionTCN score; the profit threshold IS
the paper's decision rule. Swap in a real predicted-probability series later to
replicate the deep model exactly.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class MultiscaleMove(Strategy):
    name = "multiscale_move"

    @staticmethod
    def param_grid() -> list[dict]:
        grid = []
        for maxh in (4, 7, 10):              # fuse momentum over 1..maxh days (paper: 1-4d features, 7d target)
            for threshold in (0.0, 0.01, 0.02, 0.03):
                grid.append({"maxh": maxh, "threshold": threshold})
        return grid

    def signals(self, df: pd.DataFrame) -> pd.Series:
        maxh = int(self.params.get("maxh", 4))
        threshold = float(self.params.get("threshold", 0.02))
        close = df["close"].astype(float)
        # multi-scale fusion: mean of past-only lookback returns over horizons 1..maxh
        moms = [close / close.shift(h) - 1.0 for h in range(1, maxh + 1)]
        fused = sum(moms) / len(moms)
        pos = (fused > threshold).astype(float)   # long only when fused up-signal clears profit threshold
        return pos.fillna(0.0)
