"""Long-memory (Volterra) predictable-signal momentum — a falsification test of
Leclere & Rosenbaum, arXiv:2609.03115, "Mean-field equilibrium of heterogeneous
agents under market impact".

Their result: with heterogeneous-horizon agents who *account for their own market
impact*, the observed price decomposes into (martingale) + (common predictable
signal, modelled as a Volterra / long-memory process) + (aggregate market impact),
and at equilibrium the predictable-signal and impact terms **cancel exactly** — the
observed price collapses to its pure martingale component (Holder-regular, Brownian-
like). Tradable corollary: a *long-memory predictable signal* built from past
returns should carry **no exploitable directional edge**; if impact cancels it,
daily BTC behaves as a martingale under that signal.

We build exactly that signal: weight past log-returns with a power-law (long-memory)
kernel w_k proportional to k^-alpha (alpha small => slow decay => genuine long
memory, the Volterra regime), sum, and take the sign as the position. This is
*distinct* from tsmom/trend_filter (flat SMA/EMA windows): the whole point is the
fat-tailed memory kernel that a Volterra process implies. The paper predicts REJECT.

Signals are past-only (log-returns through the current close) and the engine shifts
by one bar, so there is no look-ahead.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


def _kernel(length: int, alpha: float) -> np.ndarray:
    """Power-law long-memory weights over lags 1..length, normalized to sum 1."""
    k = np.arange(1, length + 1, dtype=float)
    w = k ** (-alpha)
    return w / w.sum()


class VolterraSignal(Strategy):
    name = "volterra_signal"

    @staticmethod
    def param_grid() -> list[dict]:
        # alpha: memory decay exponent. 0.5-0.9 = long memory (Volterra regime);
        # 1.5 = near-Markovian short memory (control). length: kernel span (days).
        return [
            {"length": L, "alpha": a}
            for L in (30, 60, 120)
            for a in (0.5, 0.7, 0.9, 1.5)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        length = int(self.params.get("length", 60))
        alpha = float(self.params.get("alpha", 0.7))
        close = df["close"].astype(float)
        logret = np.log(close).diff().fillna(0.0)          # past-only
        w = _kernel(length, alpha)
        # convolve past returns with the long-memory kernel: signal_t uses r_t..r_{t-L+1}
        sig = logret.rolling(length).apply(
            lambda x: float(np.dot(x, w[::-1])), raw=True
        )
        pos = pd.Series(0.0, index=df.index)
        pos[sig > 0] = 1.0
        pos[sig < 0] = -1.0
        return pos.fillna(0.0)


def _demo() -> None:
    # ponytail: one runnable check — kernel is a normalized, monotone-decreasing
    # long-memory weighting, and the signal is past-only (no look-ahead).
    w = _kernel(60, 0.7)
    assert abs(w.sum() - 1.0) < 1e-12, "kernel must sum to 1"
    assert np.all(np.diff(w) < 0), "long-memory kernel must decrease with lag"
    assert w[0] > w[-1], "most recent lag must carry the most weight"

    idx = pd.date_range("2020-01-01", periods=200, freq="D")
    up = pd.DataFrame({"close": np.linspace(100, 200, 200)}, index=idx)
    s = VolterraSignal(length=60, alpha=0.7)
    pos = s.signals(up)
    assert (pos.iloc[70:] == 1.0).all(), "steady uptrend => long"
    # look-ahead guard: dropping the last row must not change earlier signals
    pos_trunc = s.signals(up.iloc[:-1])
    assert pos.iloc[:-1].equals(pos_trunc), "signal must be past-only"
    print("volterra_signal self-check OK")


if __name__ == "__main__":
    _demo()
