"""Critical-slowing-down (CSD) early-warning overlay — the daily test of "can a
scalar pre-state measure grade a coming crypto liquidation cascade?".

Motivated by Ramon Marc Garcia Seuma (arXiv:2608.03616), "Measuring the engine of
a liquidation cascade: subcritical branching inside a first-order transition".
Studying seven crypto-perpetual cascades (2022-2025), he measures the branching
ratio of the Oct-2025 crash in flight and finds it ran deeply *subcritical*
(lambda ~ 0.1-0.2), the Galton-Watson critical-cascade hypothesis is eliminated
at power >= 0.96, and — the load-bearing claim for us — the transition is "abrupt
and scale-robust rather than critical", so "none of the scalar pre-state measures
we can construct grades it". Severity = shock x map-in-path x liquidity-withdrawal,
not a diverging multiplier.

Classic critical-slowing-down (CSD) theory (Scheffer et al.) says a system nearing
a tipping point shows *rising variance* and *rising lag-1 autocorrelation* just
before it flips. If crypto crashes were critical transitions, a CSD overlay —
de-risk when variance+autocorrelation climb — would front-run drawdowns and add
return. Garcia Seuma's result predicts it will NOT: the cascade is first-order, so
the pre-state CSD signal should carry no timing edge.

This is a genuinely different mechanism from the exhausted trend / vol-target
family (nine straight daily-BTC reject-leans): it keys on the *autocorrelation
dynamics* of returns (the CSD tell), not on the trend or the level of realized
vol. vol_regime tested "step aside when vol is high"; this tests "step aside when
the system looks like it is *approaching a tipping point*".

Rule (long/flat, discrete {0,1}): build a composite CSD indicator = z-scored
rolling variance of returns + z-scored rolling lag-1 autocorrelation of returns.
Go flat when that indicator sits ABOVE its own rolling quantile q (elevated
criticality => de-risk), else long. Long-or-flat only — the short leg bled against
BTC up-drift in every prior test (tsmom, trend_filter).

Falsifiable prediction (Garcia Seuma's, restated for a single daily series): the
CSD overlay should NOT clear the deflated-Sharpe gate as an alpha and should NOT
beat buy-and-hold on return. Like every prior daily-BTC overlay it may cut
drawdown (crash insurance) — but if variance+autocorrelation genuinely led the
crash we would see a real OOS return edge. A passing OOS gate would falsify
Garcia Seuma's "no scalar pre-state measure grades it" on daily BTC.

Look-ahead-free: variance and autocorrelation at bar t use returns strictly up to
t; the rolling-quantile threshold uses .shift(1) so today's indicator is never in
its own reference set. The engine's shift(1) then enters at t+1.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


def _zscore(s: pd.Series, window: int) -> pd.Series:
    """Rolling z-score (uses values up to and including bar t)."""
    mu = s.rolling(window, min_periods=max(5, window // 2)).mean()
    sd = s.rolling(window, min_periods=max(5, window // 2)).std()
    return (s - mu) / sd.replace(0.0, pd.NA)


class CascadeWarning(Strategy):
    name = "cascade_warning"

    @staticmethod
    def param_grid() -> list[dict]:
        # lookback = window for variance & lag-1 autocorrelation (days);
        # q = criticality cutoff (flat above this quantile of the CSD indicator);
        # window = rolling reference window for z-scores & the quantile (days).
        return [
            {"lookback": lb, "q": q, "window": w}
            for lb in (20, 30, 60)
            for q in (0.7, 0.8, 0.9)
            for w in (252, 504)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 30))
        q = float(self.params.get("q", 0.8))
        window = int(self.params.get("window", 252))
        close = df["close"].astype(float)
        ret = close.pct_change()

        minp = max(5, lookback // 2)
        # CSD tell #1: rolling variance of returns (rises approaching a tipping point)
        var = ret.rolling(lookback, min_periods=minp).var()
        # CSD tell #2: rolling lag-1 autocorrelation of returns (also rises)
        ac1 = ret.rolling(lookback, min_periods=minp).apply(
            lambda x: pd.Series(x).autocorr(lag=1), raw=False
        )

        # composite criticality indicator (both tells on a comparable scale)
        csd = _zscore(var, window).add(_zscore(ac1, window), fill_value=0.0)

        # elevated-criticality threshold: prior rolling quantile of the indicator
        thresh = csd.rolling(window, min_periods=window // 2).quantile(q).shift(1)

        pos = (csd <= thresh).astype(float)  # 1 long when calm/subcritical, 0 flat when criticality elevated
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — a synthetic run-up that destabilises (rising
    # variance + autocorrelation) before a crash must pull exposure DOWN into the
    # unstable stretch vs the calm early stretch.
    import numpy as np

    idx = pd.date_range("2020-01-01", periods=1000, freq="D")
    rng = np.random.default_rng(0)
    n = len(idx)
    # calm iid early; then AR(1) with rising rho + rising vol (critical slowing down)
    r = np.zeros(n)
    r[:500] = rng.normal(0, 0.005, 500)
    prev = 0.0
    for t in range(500, n):
        rho = 0.2 + 0.6 * (t - 500) / (n - 500)   # autocorrelation climbs
        vol = 0.005 + 0.03 * (t - 500) / (n - 500)  # variance climbs
        prev = rho * prev + rng.normal(0, vol)
        r[t] = prev
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})
    pos = CascadeWarning(lookback=30, q=0.8, window=252).signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "must be long/flat {0,1}"
    calm = pos.iloc[300:480].mean()      # warmed-up, still calm regime
    unstable = pos.iloc[700:980].mean()  # deep in the destabilising stretch
    assert calm > unstable, f"should hold more when calm ({calm:.2f}) than unstable ({unstable:.2f})"
    print(f"OK: exposure calm {calm:.0%} vs pre-crash unstable {unstable:.0%}")
