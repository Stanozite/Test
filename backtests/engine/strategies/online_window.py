"""Online window-size aggregation — attack the overfitting mechanism itself.

Tradable analogue of Liu & Hsieh, "Cost-Sensitive Online Window Size Selection
for Portfolio Management" (arXiv:2609.29887, Sep 2026). Their thesis: don't pick
one estimation window; treat several candidate windows as *experts* and aggregate
their portfolios online (Hedge / Fixed-Share) on *turnover-inclusive* (cost-aware)
losses, so the mix adapts as regimes change and no single static window has to be
right.

Why this is the sharpest test to run now: every one of the repo's 16 straight
daily-crypto reject-leans died the SAME way — a fixed lookback that looked great
in-sample was grid-selected, then collapsed out-of-sample. This paper proposes a
principled fix to exactly that failure. So instead of sweeping the window (the
thing that overfits), we FREEZE a spread of candidate momentum windows and sweep
only the aggregator's hyper-parameters. That makes it a genuinely different kind
of test from all priors, and it engages the standing thesis head-on rather than
swapping in yet another signal.

Mechanism (long/flat, look-ahead-free):
  - Experts: for each candidate window W, expert position p_W,t = 1 if the trailing
    W-bar log-return is > 0 else 0 (a long/flat momentum vote from data up to t).
  - Aggregate target P_t = sum_W ( weight_W,t * p_W,t ), a number in [0,1].
  - Update weights AFTER the bar with Hedge on realized, turnover-inclusive expert
    reward g_W = p_W,{t-1}*ret_t - cost*|p_W,t - p_W,{t-1}| :
        weight_W *= exp(eta * g_W); renormalize; then Fixed-Share mix toward uniform
    so the mix can re-weight quickly when a different horizon starts working.
  - P_t is formed from weights carrying information only through bar t-1, and each
    expert's p_W,t uses returns only up to t; the engine's own shift(1) then enters
    P_t at t+1. No look-ahead.

Swept params are the AGGREGATOR's, not the window:
  eta  = Hedge learning rate; cost = per-turnover penalty in the expert loss;
the candidate window set is fixed at (10, 20, 40, 80, 160) days.

Falsifiable prediction: if online aggregation genuinely cures the fixed-window
overfitting, OOS Sharpe should hold up (degrade far less train->OOS than the
fixed-window strategies did) and clear the deflated-SR gate. Consistent with the
16 priors, the honest base rate says it still won't manufacture standalone daily
alpha — but the decisive diagnostic here is the train->OOS *decay*, not the level:
a smaller decay than vol_regime/tsmom would be the paper's robustness claim
showing up even without alpha. A clean OOS pass would falsify "daily BTC is
tapped out".
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy

# Fixed candidate momentum horizons (days). The point of the method is that the
# aggregator, not a grid search, decides which of these to trust over time.
WINDOWS = (10, 20, 40, 80, 160)
FIXED_SHARE = 0.02   # small mix toward uniform each step -> stays adaptive


class OnlineWindow(Strategy):
    name = "online_window"

    @staticmethod
    def param_grid() -> list[dict]:
        # Sweep only the aggregator hyper-params (9 combos). NOT the window.
        return [
            {"eta": eta, "cost": cost}
            for eta in (0.5, 1.0, 2.0)
            for cost in (0.0, 0.001, 0.002)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        eta = float(self.params.get("eta", 1.0))
        cost = float(self.params.get("cost", 0.001))
        close = df["close"].astype(float)
        ret = close.pct_change().fillna(0.0).to_numpy()
        logc = np.log(close.to_numpy())

        n = len(close)
        nw = len(WINDOWS)
        # Expert long/flat votes: p[i, t] = 1 if trailing W_i log-return > 0.
        p = np.zeros((nw, n))
        for i, w in enumerate(WINDOWS):
            mom = logc - np.concatenate([np.full(w, np.nan), logc[:-w]])
            p[i] = (mom > 0).astype(float)
            p[i, :w] = 0.0   # not enough history -> flat

        weight = np.full(nw, 1.0 / nw)
        target = np.zeros(n)
        for t in range(n):
            # form target from weights that carry info only through t-1
            target[t] = float(weight @ p[:, t])
            # update AFTER emitting: realized turnover-inclusive expert reward at t
            if t > 0:
                g = p[:, t - 1] * ret[t] - cost * np.abs(p[:, t] - p[:, t - 1])
                weight = weight * np.exp(eta * g)
                s = weight.sum()
                weight = weight / s if s > 0 and np.isfinite(s) else np.full(nw, 1.0 / nw)
                # Fixed-Share: keep the mix responsive to regime change
                weight = (1.0 - FIXED_SHARE) * weight + FIXED_SHARE / nw

        return pd.Series(target, index=close.index).fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — the aggregator must lean long in a clean
    # uptrend (every momentum expert votes long) and near-flat in a downtrend.
    idx = pd.date_range("2020-01-01", periods=800, freq="D")
    up = pd.Series(100 * (1.0 + 0.002) ** np.arange(400), index=idx[:400])
    down = pd.Series(up.iloc[-1] * (1.0 - 0.002) ** np.arange(400), index=idx[400:])
    px = pd.concat([up, down])
    df = pd.DataFrame({"close": px})
    pos = OnlineWindow(eta=1.0, cost=0.001).signals(df)
    assert (pos >= -1e-9).all() and (pos <= 1.0 + 1e-9).all(), "target must be in [0,1]"
    trend_up = pos.iloc[250:390].mean()    # deep in the uptrend, warmed up
    trend_down = pos.iloc[650:790].mean()  # deep in the downtrend
    assert trend_up > trend_down, f"should hold more in uptrend ({trend_up:.2f}) than downtrend ({trend_down:.2f})"
    print(f"OK: exposure uptrend {trend_up:.0%} vs downtrend {trend_down:.0%}")
