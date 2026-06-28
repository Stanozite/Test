"""Strategy interface + a dependency-free vectorized backtest core.

A Strategy turns OHLCV into a target position series in {-1, 0, +1}. Signals are
shifted by one bar inside `run_vectorized` so a position computed from bar t's
close is only entered at bar t+1 — no look-ahead.
"""
from __future__ import annotations

import pandas as pd


class Strategy:
    """Base class. Subclasses set `name`, accept params, and implement `signals`."""
    name: str = "base"

    def __init__(self, **params):
        self.params = params

    @staticmethod
    def param_grid() -> list[dict]:
        """Return the list of param dicts to sweep in stage 1."""
        return [{}]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        """Target position in {-1, 0, +1} aligned to df.index (pre-shift)."""
        raise NotImplementedError

    def label(self) -> str:
        ps = ",".join(f"{k}={v}" for k, v in sorted(self.params.items()))
        return f"{self.name}({ps})"


def run_vectorized(df: pd.DataFrame, position: pd.Series,
                   fee: float = 0.0, slippage: float = 0.0) -> tuple[pd.Series, pd.Series]:
    """Dependency-free vectorized backtest.

    fee/slippage are per-unit-turnover costs (e.g. 0.0010 = 10 bps each).
    Returns (equity_curve, per_period_returns).
    """
    close = df["close"].astype(float)
    ret = close.pct_change().fillna(0.0)
    pos = position.reindex(df.index).shift(1).fillna(0.0)   # enter next bar
    turnover = pos.diff().abs().fillna(pos.abs())
    cost = turnover * (fee + slippage)
    strat_ret = pos * ret - cost
    equity = (1.0 + strat_ret).cumprod()
    return equity, strat_ret
