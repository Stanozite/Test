"""Volatility-regime filter — the daily test of "manage exposure to elevated /
asymmetric volatility instead of forecasting direction".

Motivated by Lee, Shirvani, Afroz, Rachev & Fabozzi (arXiv:2607.16450),
"Portfolio Optimization under Heavy Tails and Asymmetric Volatility", which model
returns with GJR-GARCH (negative shocks raise conditional vol more than positive
ones) and find tail-sensitive (CVaR) allocations differ systematically from
mean-variance ones. The tradeable daily analogue for a single crypto series is a
volatility-managed overlay (Moreira-Muir style): hold the asset only while its
realized volatility sits in a calm regime, step aside when vol spikes.

This is also the explicit "vol-target overlay" next-axis flagged in the standing
BTC thread after seven straight daily single-series rejects (see 2026-07-04 /
2026-07-15 digests): move OFF direction/trend, onto exposure management.

Rule (long/flat, discrete {0,1}): go long when trailing realized volatility is
below its own rolling quantile over a long window (self-adapting, no magic
absolute vol constant), else flat.

Falsifiable prediction: consistent with every prior daily-BTC test, a vol-regime
filter should behave as *crash insurance* — cut drawdown, maybe nudge Sharpe up —
but NOT add raw return and NOT clear the deflated-Sharpe gate as an alpha. If the
gate passes OOS, that would falsify the "daily BTC single-series is tapped out"
thesis.

Look-ahead-free: realized vol at bar t uses returns strictly up to t; the rolling
quantile at t uses vol values up to t. The engine's own shift(1) then enters the
position at t+1, so the position held into bar t was decided from data before t.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class VolRegime(Strategy):
    name = "vol_regime"

    @staticmethod
    def param_grid() -> list[dict]:
        # lookback = realized-vol window (days); q = calm-regime quantile cutoff;
        # window = lookback for the rolling quantile reference (days).
        return [
            {"lookback": lb, "q": q, "window": w}
            for lb in (10, 20, 30)
            for q in (0.4, 0.5, 0.6)
            for w in (252, 504)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 20))
        q = float(self.params.get("q", 0.5))
        window = int(self.params.get("window", 252))
        close = df["close"].astype(float)
        ret = close.pct_change()

        # trailing realized volatility (uses returns up to and including bar t)
        rv = ret.rolling(lookback, min_periods=max(3, lookback // 2)).std()
        # calm-regime threshold: rolling quantile of past vol (shift(1) => strictly
        # prior vol values, no peeking at today's rv in its own reference set)
        thresh = rv.rolling(window, min_periods=window // 2).quantile(q).shift(1)

        pos = (rv < thresh).astype(float)   # 1 long in calm regime / 0 flat
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — long only in the calm half, flat in the storm.
    import numpy as np
    idx = pd.date_range("2020-01-01", periods=900, freq="D")
    rng = np.random.default_rng(0)
    # first calm (low vol), then stormy (high vol) — filter must prefer calm
    vol = np.where(np.arange(len(idx)) < 450, 0.005, 0.05)
    r = rng.normal(0, 1, len(idx)) * vol
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})
    pos = VolRegime(lookback=20, q=0.5, window=252).signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "must be long/flat {0,1}"
    calm = pos.iloc[300:440].mean()   # warmed-up, still in calm regime
    storm = pos.iloc[600:880].mean()  # deep in high-vol regime
    assert calm > storm, f"should hold more in calm ({calm:.2f}) than storm ({storm:.2f})"
    print(f"OK: exposure calm {calm:.0%} vs storm {storm:.0%}")
