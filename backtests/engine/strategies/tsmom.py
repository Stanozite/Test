"""Time-series momentum (long/short), the canonical "simple rule".

Translation of the benchmark in Pollok & Robik (arXiv:2607.00475), "End-to-End
Parametric Portfolio Policies for Cross-Asset Futures Timing: When Do AI Models
Beat Simple Rules?". They find learned differentiable-Sharpe policies beat
equal-weight / risk-parity / time-series-momentum only non-uniformly, and TSMOM
is one of the hard-to-beat baselines — on the 16 most liquid CME futures.

BTC-USD is *not* in their panel. This tests the standalone question: does the
simple TSMOM rule itself carry OOS edge on crypto? TSMOM (Moskowitz–Ooi–Pedersen):
go long if the trailing L-period return is positive, short if negative. Pure sign,
both directions — distinct from the long-only `cost_aware_momentum` here.

Signals are past-only (trailing return through the current close) and the engine
shifts by one bar, so no look-ahead.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class TSMom(Strategy):
    name = "tsmom"

    @staticmethod
    def param_grid() -> list[dict]:
        # daily bars; lookbacks span ~1 month to ~1 quarter of trend
        return [{"lookback": lb} for lb in (20, 30, 60, 90, 120)]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 60))
        close = df["close"].astype(float)
        trailing = close / close.shift(lookback) - 1.0     # past-only trailing return
        pos = pd.Series(0.0, index=df.index)
        pos[trailing > 0] = 1.0
        pos[trailing < 0] = -1.0
        return pos.fillna(0.0)
