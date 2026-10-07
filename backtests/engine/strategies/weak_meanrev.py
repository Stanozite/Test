"""Weak (single-asset, level) mean-reversion band — the daily test of "trade the
gap to a slow equilibrium when the price is weakly mean-reverting".

Motivated by Hoffmann & Rasonyi (arXiv:2610.08631), "Exponential investors with
weakly mean-reverting prices": for an exponential-utility investor in a market
whose (log) price is *weakly* (sublinear) mean-reverting with nonzero drift, the
certainty equivalent grows as O(T^{2β+1}) and an explicit asymptotically optimal
strategy exists, with position essentially driven by the current gap to the
mean-reverting level. The tradeable daily analogue for a single crypto series is
an Ornstein-Uhlenbeck-style band: estimate a slow equilibrium (rolling mean of
log-price), measure the standardized deviation z, and lean *against* it — long
when price is stretched below equilibrium (expect reversion up), short/flat when
stretched above.

This is the deliberate single-asset *level* sibling of the two reversion tests
already on the books, filling the last gap on that axis:
  * `lag1_reversal` (2026-07-01 BTC / 2026-08-26 ETH) faded the *previous bar*
    (horizon = 1 day) — rejected on both coins.
  * `pairs_meanrev` (2026-09-23) faded a z-score of the *BTC/ETH ratio*
    (cross-sectional / cointegration axis) — rejected; the ratio trends.
`weak_meanrev` fades the z-score of a *single asset's* log-price deviation from
its own slow mean — the direct OU-gap trade Hoffmann & Rasonyi's premise implies.

Rule (discrete {-1,0,+1}): z_t = (logP_t - MA_lookback(logP)_t) / rolling_std;
  long when z < -entry (cheap vs equilibrium), short when z > +entry (rich),
  flat inside the band. `longflat=True` drops the short leg (long-or-flat), since
  shorting the top of a strongly up-drifting asset bled in `tsmom`/`lag1`.

Falsifiable prediction (the repo's standing thesis): BTC is NOT weakly
mean-reverting at the *level* — it has strong positive drift and keeps printing
new highs, so the deviation from any slow mean is non-stationary and a level-
reversion band gets run over by every trend leg. Expect NO out-of-sample return
edge (REJECT / MIXED-leans-REJECT), confirming (not falsifying) the paper: its
edge lives where a genuine mean-reverting anchor exists, which a single trending
crypto lacks. If the deflated-Sharpe gate passes OOS, that WOULD falsify "daily
single-series crypto is tapped out" and say BTC level-reversion is real.

Look-ahead-free: z_t uses log-price and its rolling mean/std strictly up to bar t;
the engine's own shift(1) then enters the position at t+1.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class WeakMeanRev(Strategy):
    name = "weak_meanrev"

    @staticmethod
    def param_grid() -> list[dict]:
        # lookback = slow-equilibrium window (days); entry = z-score band;
        # longflat = drop the short leg (long/flat) vs full long/short.
        return [
            {"lookback": lb, "entry": e, "longflat": lf}
            for lb in (30, 60, 120)
            for e in (0.5, 1.0, 1.5)
            for lf in (False, True)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 60))
        entry = float(self.params.get("entry", 1.0))
        longflat = bool(self.params.get("longflat", False))

        logp = np.log(df["close"].astype(float))
        mp = max(3, lookback // 2)
        mean = logp.rolling(lookback, min_periods=mp).mean()
        dev = logp - mean                                   # gap to slow equilibrium
        sd = dev.rolling(lookback, min_periods=mp).std()
        z = dev / sd.replace(0.0, np.nan)

        pos = pd.Series(0.0, index=df.index)
        pos[z < -entry] = 1.0                               # cheap -> expect reversion up
        if longflat:
            pos[z > entry] = 0.0                            # long/flat: step aside when rich
        else:
            pos[z > entry] = -1.0                           # rich -> expect reversion down
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: force the predicted behaviour red first. On a genuine OU series the
    # band must lean LONG when below equilibrium and SHORT when above; on a pure
    # up-trend the long-leg should rarely fire (price is never stretched *below* a
    # lagging mean) — i.e. the strategy is structurally run over by drift.
    idx = pd.date_range("2020-01-01", periods=1200, freq="D")

    # (1) stationary OU around a constant level -> net exposure should track -sign(dev)
    rng = np.random.default_rng(0)
    x = np.zeros(len(idx))
    for t in range(1, len(idx)):
        x[t] = 0.95 * x[t - 1] + rng.normal(0, 0.05)        # mean-reverting log-dev
    ou_px = pd.Series(100 * np.exp(x), index=idx)
    df_ou = pd.DataFrame({"close": ou_px})
    pos_ou = WeakMeanRev(lookback=60, entry=0.5, longflat=False).signals(df_ou)
    assert set(pos_ou.dropna().unique()) <= {-1.0, 0.0, 1.0}, "must be {-1,0,1}"
    logp = np.log(ou_px); mean = logp.rolling(60, min_periods=30).mean()
    below = (logp < mean) & pos_ou.ne(0)
    above = (logp > mean) & pos_ou.ne(0)
    # when acting below equilibrium it should be long; above, short
    assert pos_ou[below].mean() > 0, "should be net LONG when below equilibrium"
    assert pos_ou[above].mean() < 0, "should be net SHORT when above equilibrium"

    # (2) pure deterministic up-trend -> long-leg structurally starved (run over by drift)
    up_px = pd.Series(100 * np.exp(np.linspace(0, 2, len(idx))), index=idx)
    pos_up = WeakMeanRev(lookback=60, entry=1.0, longflat=True).signals(up_px.to_frame("close"))
    long_frac = (pos_up > 0).mean()
    assert long_frac < 0.15, f"long-only reversion should rarely fire in an uptrend (got {long_frac:.0%})"

    print(f"OK: OU net-long-below / net-short-above holds; uptrend long-fire only {long_frac:.1%}")
