"""Bitcoin power-law corridor — the daily test of "lean against the deviation from
a time-since-genesis log-log power-law trend".

Motivated by Baquero & Menezes (arXiv:2611.13962), "Deceleration without
identification: testing a power-law trend in Bitcoin prices under persistent
noise". They fit log(price) against log(age = days since the genesis block) and
pre-register a single falsifiable protocol. Their verdict is a careful negative:
a constant drift is rejected only *fragile*ly (it survives once persistence beyond
a random walk is allowed), a **Gompertz ceiling fits about as well** as the power
law (so the data do not single out the power law), the log-age exponent ~5.7 is
*not rejected* but also not identified, and crucially **"reversion to trend cannot
be decided from the data."** A good log-log fit / high R^2 is weak evidence,
because random-walk-like deviations manufacture trends and high R^2 where none
exist.

The tradeable question that implies: the "Bitcoin power law corridor" (Santostasi-
style support/resistance bands around a log-log trend) is a popular retail timing
model. If the power law is not statistically identifiable and reversion-to-trend
cannot be decided, then a corridor-reversion *timing* rule should carry **no
reliable out-of-sample edge**. This strategy builds exactly that rule and tests it.

Mechanism (genuinely new regressor vs the book):
  * `weak_meanrev` (2026-10-07) faded the gap to a slow *rolling mean of log-price*
    — reversion to a lagging moving average. REJECT.
  * `halving_clock` (2026-08-05) was a *calendar* window post-halving. MIXED-REJECT.
  * `powerlaw_trend` fades the deviation from a **log(price) ~ a + b*log(age)** fit,
    where age = days since the 2009-01-03 genesis block. The regressor is calendar
    age on a log-log scale, not a moving average and not a halving window — the
    actual Santostasi / Baquero-Menezes object.

Rule (discrete {-1,0,+1}): fit (a_t, b_t) by look-ahead-free rolling/expanding OLS
of logP on log(age) using bars strictly up to t; residual r_t = logP_t - (a_t +
b_t*log(age_t)); z_t = r_t / rolling_std(r); long when z < -entry (price below the
corridor, "cheap"), short when z > +entry ("rich"), flat inside the band.
`longflat=True` drops the short leg (long/flat), since shorting the top of a
strongly up-drifting asset bled in `tsmom`/`lag1`/`weak_meanrev`.

Falsifiable prediction (the repo's standing thesis + the paper's own negative):
BTC's deviation from a power-law trend is itself a persistent (near-random-walk)
process that does NOT revert within any tradeable horizon, so a corridor band is
run over by every multi-year leg. Expect NO out-of-sample return edge (REJECT /
MIXED-leans-REJECT), **confirming (not falsifying)** Baquero & Menezes: the
power-law trend is not identifiable, so neither is a trade that assumes reversion
to it. If the deflated-Sharpe gate passes OOS, that WOULD falsify "daily single-
series crypto is tapped out" and say BTC power-law reversion is real and tradeable.

Look-ahead-free: the OLS coefficients and residual std at bar t use only bars up to
and including t; the engine's own shift(1) then enters the position at t+1.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy

# Bitcoin genesis block: 2009-01-03. Age in days is measured from here.
GENESIS = pd.Timestamp("2009-01-03")


def _rolling_ols_resid(logp: pd.Series, logage: pd.Series,
                       window: int, min_periods: int) -> pd.Series:
    """Residual of a look-ahead-free rolling OLS of logp on logage.

    window<=0 means an expanding fit (all history up to t). Coefficients at bar t
    use bars up to and including t only (the engine shifts the position by 1).
    Slope via rolling cov/var; intercept pins the line through the window means.
    """
    if window and window > 0:
        roll = lambda s: s.rolling(window, min_periods=min_periods)
    else:
        roll = lambda s: s.expanding(min_periods=min_periods)

    mx = roll(logage).mean()
    my = roll(logp).mean()
    mxy = roll(logage * logp).mean()
    mxx = roll(logage * logage).mean()
    cov = mxy - mx * my
    var = mxx - mx * mx
    b = cov / var.replace(0.0, np.nan)
    a = my - b * mx
    fitted = a + b * logage
    return logp - fitted


class PowerLawTrend(Strategy):
    name = "powerlaw_trend"

    @staticmethod
    def param_grid() -> list[dict]:
        # window = OLS fit length in days (0 = expanding/all-history);
        # entry = z-score band; longflat = drop the short leg (long/flat).
        return [
            {"window": w, "entry": e, "longflat": lf}
            for w in (0, 365, 730)
            for e in (0.5, 1.0, 1.5)
            for lf in (False, True)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        window = int(self.params.get("window", 0))
        entry = float(self.params.get("entry", 1.0))
        longflat = bool(self.params.get("longflat", False))

        close = df["close"].astype(float)
        logp = np.log(close)
        age_days = (df.index - GENESIS).days.astype(float)
        # clip to >=1 day so log(age) is defined for any (hypothetical) early bar
        logage = pd.Series(np.log(np.maximum(age_days, 1.0)), index=df.index)

        mp = max(30, (window // 4) if window > 0 else 250)
        resid = _rolling_ols_resid(logp, logage, window, mp)
        sd_win = window if window > 0 else 365
        sd = resid.rolling(sd_win, min_periods=max(30, sd_win // 4)).std()
        z = resid / sd.replace(0.0, np.nan)

        pos = pd.Series(0.0, index=df.index)
        pos[z < -entry] = 1.0                     # below the corridor -> expect reversion up
        if longflat:
            pos[z > entry] = 0.0                  # long/flat: step aside when rich
        else:
            pos[z > entry] = -1.0                 # above the corridor -> expect reversion down
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: force the PREDICTED behaviour red first. The corridor band must,
    # on a genuine power-law-plus-OU series, lean LONG below the fitted trend and
    # SHORT above it; and on a power-law-plus-PERSISTENT-random-walk series (the
    # paper's non-identifiability regime) the long-only band must be structurally
    # starved / run over, not a stable edge.
    idx = pd.date_range("2016-01-01", periods=2000, freq="D")
    age = (idx - GENESIS).days.astype(float)
    logage = np.log(age)

    # (1) exact power law (exponent 5.7) + stationary OU deviation ->
    #     net-long-below / net-short-above must hold.
    rng = np.random.default_rng(0)
    ou = np.zeros(len(idx))
    for t in range(1, len(idx)):
        ou[t] = 0.97 * ou[t - 1] + rng.normal(0, 0.03)       # mean-reverting log-dev
    base = -40.0 + 5.7 * logage                              # intercept keeps price sane
    pl_px = pd.Series(np.exp(base + ou), index=idx)
    df_pl = pd.DataFrame({"close": pl_px})
    pos_pl = PowerLawTrend(window=730, entry=0.5, longflat=False).signals(df_pl)
    assert set(pos_pl.dropna().unique()) <= {-1.0, 0.0, 1.0}, "positions must be {-1,0,1}"
    resid = _rolling_ols_resid(np.log(pl_px), pd.Series(logage, index=idx), 730, 180)
    below = (resid < 0) & pos_pl.ne(0)
    above = (resid > 0) & pos_pl.ne(0)
    assert pos_pl[below].mean() > 0, "should be net LONG when below the fitted corridor"
    assert pos_pl[above].mean() < 0, "should be net SHORT when above the fitted corridor"

    # (2) power law + PERSISTENT random-walk deviation (unit-root; the paper's
    #     'deceleration without identification' regime) -> a long/flat reversion
    #     band rarely fires AND does not reliably catch reversion, because the
    #     deviation does not revert within the window. Assert the long-leg is
    #     structurally sparse (the deviation wanders away and stays away).
    rw = np.cumsum(rng.normal(0, 0.03, len(idx)))            # random walk = persistent noise
    rw_px = pd.Series(np.exp(base + rw), index=idx)
    pos_rw = PowerLawTrend(window=730, entry=1.0, longflat=True).signals(rw_px.to_frame("close"))
    long_frac = (pos_rw > 0).mean()
    assert long_frac < 0.45, f"under persistent (RW) deviation the reversion long-leg should be sparse (got {long_frac:.0%})"

    print(f"OK: corridor net-long-below / net-short-above holds on power-law+OU; "
          f"persistent-noise long-fire only {long_frac:.1%}")
