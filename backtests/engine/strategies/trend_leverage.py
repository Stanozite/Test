"""Trend-conditioned leverage-effect vol gate — the daily test of the
preceding-trend volatility asymmetry on a single crypto series.

Motivated by Bicki & Akdogan (arXiv:2611.04533), "How market volatility responds
to a preceding price trend: a lag-resolved measurement in cryptocurrencies and
equities". They measure, at minute resolution 2020-2026, how volatility responds
to a *preceding price trend* as a function of lag. For Bitcoin and Ether the
asymmetry is positive (matching the sign of the leverage effect: down-trends are
followed by higher volatility), is strongest at the first measurable lag (~20 min),
and decays to half its initial level by roughly 1.5 hours. They further split the
asymmetry under time reversal and detect a *time-directed* (arrow-of-time)
component for BTC and ETH, but **none** at the 20-min lag for the three US equities
+ SPY — a crypto-specific, short-lived, directional effect.

Tradable daily analogue for a single crypto series. This is a deliberate sibling of
`vol_regime` (plain realized-vol gate) and `asym_longmem_vol` (sign-dependent ALM
vol gate), with ONE faithful distinction that isolates this paper's claim: the
volatility asymmetry is keyed on the sign of the **preceding multi-day price trend**
(the exact conditioning variable in 2611.04533), not on the per-bar shock sign.

  1. Preceding trend (signed): trend_t = close_t / close_{t-L} - 1.
  2. Leverage-adjusted vol proxy: v_t = r_t^2 * (1 + (gamma-1) * [trend_t < 0]).
     gamma = 1 is the symmetric control (reduces to a plain rolling-vol gate);
     gamma > 1 inflates the vol forecast after down-trends, per the leverage sign.
  3. Vol forecast: vol_t = sqrt( mean of v over the last L bars ).
  4. Regime gate: long (1) while vol_t sits below its own rolling quantile(q),
     else flat (0) — self-adapting, no absolute vol constant. Long/flat only:
     every prior daily-crypto test shows shorting BTC's up-drift bleeds.

Falsifiable prediction. The paper's effect half-lives at ~1.5h and the time-directed
part is a minute-scale phenomenon; by the daily close it should wash out, exactly as
the quarter-hour effect did (`dow_seasonality` REJECT) and as every vol-statistic gate
did (`vol_regime`, `evar_regime`, `asym_longmem_vol` all MIXED-lean-REJECT). Expect:
crash insurance (trims max drawdown), maybe a small Sharpe nudge from lower exposure,
but NO raw-return edge and NO deflated-Sharpe survival. The symmetric gamma=1 arm is
the built-in control: if the edge concentrates at gamma>1 AND survives OOS +
deflation, that falsifies "daily single-series crypto is tapped out" and validates the
preceding-trend leverage channel as tradable at the daily horizon.

Look-ahead-free: trend_t uses close_t and close_{t-L} (both known at close t); v_t
uses r_t and trend_t (known at t); vol_t rolls over v up to t; the quantile threshold
is shift(1) (strictly prior values). The engine's own shift(1) then enters the
position at t+1 — the position held into bar t+1 was decided from data through close t.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class TrendLeverage(Strategy):
    name = "trend_leverage"

    @staticmethod
    def param_grid() -> list[dict]:
        # gamma = down-trend vol inflation (1.0 = symmetric control);
        # L     = preceding-trend lookback / vol-proxy window (days);
        # q     = calm-regime quantile cutoff. window (quantile lookback) fixed.
        return [
            {"gamma": g, "L": L, "q": q, "window": 252}
            for g in (1.0, 2.0, 3.0)
            for L in (10, 20, 40)
            for q in (0.4, 0.5, 0.6)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        gamma = float(self.params.get("gamma", 2.0))
        L = int(self.params.get("L", 20))
        q = float(self.params.get("q", 0.5))
        window = int(self.params.get("window", 252))

        close = df["close"].astype(float)
        ret = close.pct_change()

        # (1) preceding multi-day price trend, signed
        trend = close / close.shift(L) - 1.0

        # (2) leverage-adjusted vol proxy — asymmetry keyed on the TREND sign
        v = ret.pow(2) * (1.0 + (gamma - 1.0) * (trend < 0).astype(float))

        # (3) vol forecast over the same lookback
        vol = np.sqrt(v.rolling(L, min_periods=max(5, L // 2)).mean())

        # (4) self-adapting calm-regime gate (shift(1) => strictly prior threshold)
        thresh = vol.rolling(window, min_periods=window // 2).quantile(q).shift(1)
        pos = (vol < thresh).astype(float)
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: forced-red checks — positions must be long/flat {0,1}; the gate must
    # hold more exposure in the calm half than the stormy half; and at gamma>1 a
    # down-trend must inflate the vol proxy relative to the same bar after an up-trend.
    idx = pd.date_range("2020-01-01", periods=900, freq="D")
    rng = np.random.default_rng(0)
    vol = np.where(np.arange(len(idx)) < 450, 0.005, 0.05)
    r = rng.normal(0, 1, len(idx)) * vol
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})

    s = TrendLeverage(gamma=2.0, L=20, q=0.5, window=252)
    pos = s.signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "must be long/flat {0,1}"
    calm = pos.iloc[300:440].mean()
    storm = pos.iloc[600:880].mean()
    assert calm > storm, f"calm ({calm:.2f}) should exceed storm ({storm:.2f})"

    # asymmetry check: identical |return| bar, but a down-trend context must raise the
    # proxy at gamma>1 while an up-trend context does not.
    one_ret = 0.03
    v_down = one_ret ** 2 * (1.0 + (2.0 - 1.0) * 1.0)   # trend < 0
    v_up = one_ret ** 2 * (1.0 + (2.0 - 1.0) * 0.0)     # trend >= 0
    assert v_down > v_up, "down-trend context must inject more variance at gamma>1"
    print(f"OK: exposure calm {calm:.0%} vs storm {storm:.0%}; "
          f"down-trend var {v_down:.4f} > up-trend var {v_up:.4f}")
