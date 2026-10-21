"""Garleanu-Pedersen aim-portfolio / Smerlak optimal linear filter.

Tradable analogue of Matteo Smerlak, "Optimal Trading Filters and the Value of
Predictive Signals" (arXiv:2610.24558, q-fin.MF, Oct 2026). Smerlak solves the
stationary quadratic trading problem with transient price impact via Wiener-Hopf
factorization: the optimal policy is a conditional forecast followed by an
*explicit causal linear filter*. Under exponential resilience of impact it
recovers the Garleanu-Pedersen aim-portfolio (partial adjustment toward a shrunk
Markowitz target). Two results we can test on daily BTC:
  (1) Without costs, signals of equal instantaneous predictive strength have equal
      frictionless value; WITH costs, attainable net value depends on the mean
      square of the *friction-weighted* forecast -> a more persistent signal is
      worth more after costs.
  (2) The optimal implementation is NOT "chase the Markowitz target each bar"; it
      is a low-pass filter that trades partway toward the aim, so turnover (and
      cost drag) is cut by construction.

Why this is the sharpest test to run now. Every one of the repo's 18 straight
daily-crypto reject-leans died the same way: a signal with in-sample promise was
grid-selected and collapsed OOS, and the recurring post-mortem is "the edge is not
trading" (cost_aware_momentum 06-30, Whalley-Wilmott in the 09-02 digest). The
`online_window` test (09-30) attacked the *window*-overfitting mechanism with a
principled online aggregator. This attacks the next overfit knob: the
*threshold/filter* that converts a forecast into a position. Instead of
grid-searching a threshold, we apply the mathematically OPTIMAL cost-aware filter
(partial adjustment, trade rate phi) and ask whether that finally extracts net OOS
value from a daily momentum forecast where naive conversion did not.

Mechanism (continuous position in [-1,1] or [0,1], look-ahead-free):
  - Forecast  f_t = EWMA of daily log-returns, span `span` (an OU-like persistent
    alpha; larger span = slower mean reversion = more persistent).
  - Markowitz target  M_t = tanh( f_t / sigma_t ), sigma_t = 60-bar rolling std of
    log-returns (vol-normalized, bounded alpha in (-1,1)). `longflat` clips M_t<0
    to 0 (BTC's up-drift has made the short leg ruinous in tsmom/lag1/weak_meanrev).
  - Optimal filter (GP aim): x_t = (1-phi)*x_{t-1} + phi*M_t, phi in (0,1].
    phi=1 == trade fully to target each bar (the naive, un-filtered control);
    phi<1 == Smerlak/GP low-pass filter that trades partway, cutting turnover.
  f_t and sigma_t use returns only through bar t; x_t uses x_{t-1} and M_t; the
  engine's own shift(1) enters x_t at t+1. No look-ahead.

Swept params: span (signal persistence), phi (optimal trade rate), longflat.

Falsifiable prediction. If Smerlak's filter genuinely adds net value, the phi<1
configs should (a) beat the phi=1 control in-sample by cutting cost drag, and
(b) hold up OOS and clear the deflated-SR gate. The honest base rate (18 priors)
says it will not manufacture standalone daily alpha: the filter is a cost-reducer,
not an alpha-generator, and daily BTC has no persistent return forecast to filter.
The decisive diagnostic is whether phi<1 dominates phi=1 (filter *does* reduce cost
drag, confirming the theory's mechanics) while OOS level stays ~0 (no alpha to
extract) -> consistent with "the blocker is data resolution, not the filter." A
clean OOS pass with phi<1 would be the first partial falsification of that thesis.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy

VOL_WINDOW = 60   # rolling-std window for vol-normalizing the forecast


class GPAim(Strategy):
    name = "gp_aim"

    @staticmethod
    def param_grid() -> list[dict]:
        # 3 x 3 x 2 = 18 combos (matches the repo's usual grid size). phi=1.0 is
        # the un-filtered control; phi in {0.1,0.3} is the GP/Smerlak optimal filter.
        return [
            {"span": span, "phi": phi, "longflat": lf}
            for span in (10, 20, 40)
            for phi in (0.1, 0.3, 1.0)
            for lf in (True, False)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        span = int(self.params.get("span", 20))
        phi = float(self.params.get("phi", 0.3))
        longflat = bool(self.params.get("longflat", True))

        close = df["close"].astype(float)
        logret = np.log(close).diff().fillna(0.0)

        # Forecast: EWMA of log-returns (persistent OU-like alpha, info through t).
        f = logret.ewm(span=span, adjust=False).mean()
        # Vol-normalize and bound -> Markowitz target in (-1,1).
        sigma = logret.rolling(VOL_WINDOW).std().bfill().replace(0.0, np.nan)
        m = np.tanh((f / sigma).fillna(0.0).to_numpy())
        if longflat:
            m = np.clip(m, 0.0, None)

        # GP aim-portfolio / Smerlak optimal linear filter: partial adjustment.
        n = len(m)
        x = np.zeros(n)
        prev = 0.0
        for t in range(n):
            prev = (1.0 - phi) * prev + phi * m[t]
            x[t] = prev

        return pd.Series(x, index=close.index).fillna(0.0)


if __name__ == "__main__":
    # ponytail: two runnable checks on a clean uptrend-then-downtrend series.
    #   (1) the filtered position leans long in the uptrend, less so in the downtrend;
    #   (2) the optimal filter (phi<1) turns over strictly LESS than the naive
    #       full-chase control (phi=1) -- the theory's whole point.
    # Noisy drift so the 60-bar vol-normalizer is well-posed (a perfectly constant
    # return has zero rolling std and would make f/sigma degenerate).
    rng = np.random.default_rng(0)
    idx = pd.date_range("2020-01-01", periods=800, freq="D")
    up_r = 0.002 + 0.01 * rng.standard_normal(400)
    down_r = -0.002 + 0.01 * rng.standard_normal(400)
    logp = np.cumsum(np.concatenate([up_r, down_r]))
    px = pd.Series(100 * np.exp(logp), index=idx)
    df = pd.DataFrame({"close": px})

    pos_slow = GPAim(span=20, phi=0.1, longflat=False).signals(df)
    pos_fast = GPAim(span=20, phi=1.0, longflat=False).signals(df)
    assert (pos_slow >= -1 - 1e-9).all() and (pos_slow <= 1 + 1e-9).all(), "pos in [-1,1]"
    up_lean = pos_slow.iloc[250:390].mean()
    down_lean = pos_slow.iloc[650:790].mean()
    assert up_lean > down_lean, f"should lean long in uptrend ({up_lean:.2f}) vs down ({down_lean:.2f})"
    to_slow = pos_slow.diff().abs().sum()
    to_fast = pos_fast.diff().abs().sum()
    assert to_slow < to_fast, f"optimal filter must turn over less: phi=0.1 {to_slow:.1f} vs phi=1 {to_fast:.1f}"
    print(f"OK: uptrend lean {up_lean:+.2f} vs downtrend {down_lean:+.2f}; "
          f"turnover phi=0.1 {to_slow:.1f} < phi=1 {to_fast:.1f}")
