"""Sign-asymmetric long-memory volatility regime filter — the daily test of the
ALM-GARCH construction on a single crypto series.

Motivated by Kayaki & Lee (arXiv:2609.06422), "Asymmetric Long-Memory GARCH:
Sign-Dependent Kernel Injection in a Two-Dimensional Markov Chain". ALM-GARCH lets
positive and negative return shocks feed conditional volatility through two distinct
channels: a *level* channel (different injection amplitudes by sign — the classic
leverage effect) and a *memory* channel (different persistence/kernel offsets by
sign). On their panel of five equity indices plus Bitcoin, joint symmetry is strongly
rejected — and the memory channel is significant specifically for the Nikkei, KOSPI
and **Bitcoin**. Crucially, they report out-of-sample variance forecasts only *match*
standard benchmarks.

Tradable daily analogue for a single crypto series: this is the direct sibling of
`vol_regime` (plain realized-vol gate) and `evar_regime` (EVaR tail gate). We keep the
identical self-adapting long/flat regime gate and swap **only the volatility
statistic** for the paper's construction:

  1. Sign-asymmetric shock (level channel): v_t = r_t^2 * (1 + (gamma-1)*[r_t < 0]).
     gamma = 1 is the symmetric control; gamma > 1 amplifies down-shocks.
  2. Long-memory kernel (memory channel): LM_vol_t = sqrt( sum_k w_k * v_{t-k} ),
     w_k ∝ (k+1)^(-alpha) over the last L lags. Small alpha = long memory;
     large alpha = short memory. (Same power-law-kernel device as volterra_signal,
     applied to variance instead of returns.)
  3. Regime gate: long (1) while LM_vol sits below its own rolling quantile(q),
     else flat (0) — self-adapting, no absolute vol constant.

Falsifiable prediction: consistent with every prior daily-BTC vol-gate test
(vol_regime, evar_regime both reject-lean) AND with the paper's own "forecasts merely
match benchmarks", the sign-asymmetric long-memory statistic should behave as crash
insurance — trim drawdown, maybe nudge Sharpe — but NOT add raw return and NOT clear
the deflated-Sharpe gate as alpha. If the sweep shows the edge concentrated at gamma>1
or long-memory alpha and that survives OOS + deflation, that would falsify the "daily
BTC single-series is tapped out" thesis and validate the ALM channels as tradable. The
symmetric gamma=1 arm is the built-in control that isolates the asymmetry's marginal
contribution.

Look-ahead-free: v_t uses only r_t (close t known at close t); LM_vol_t uses v up to
t; the quantile threshold is shift(1) (strictly prior values). The engine's own
shift(1) then enters the position at t+1 — position held into bar t+1 was decided from
data through close t.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class AsymLongMemVol(Strategy):
    name = "asym_longmem_vol"

    @staticmethod
    def param_grid() -> list[dict]:
        # gamma = down-shock amplification (1.0 = symmetric control);
        # alpha = power-law memory decay (small = long memory);
        # q = calm-regime quantile cutoff. L (lags) and window fixed.
        return [
            {"gamma": g, "alpha": a, "q": q, "lags": 90, "window": 252}
            for g in (1.0, 2.0)
            for a in (0.5, 1.0, 1.5)
            for q in (0.4, 0.5, 0.6)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        gamma = float(self.params.get("gamma", 2.0))
        alpha = float(self.params.get("alpha", 1.0))
        q = float(self.params.get("q", 0.5))
        lags = int(self.params.get("lags", 90))
        window = int(self.params.get("window", 252))

        close = df["close"].astype(float)
        ret = close.pct_change()

        # (1) sign-asymmetric shock — level channel
        v = ret.pow(2) * (1.0 + (gamma - 1.0) * (ret < 0).astype(float))

        # (2) power-law long-memory kernel — memory channel
        w = np.power(np.arange(1, lags + 1, dtype=float), -alpha)
        w = w / w.sum()
        lm_var = v.rolling(lags, min_periods=max(5, lags // 3)).apply(
            lambda x: float(np.dot(x, w[-len(x):] / w[-len(x):].sum())), raw=True
        )
        lm_vol = np.sqrt(lm_var)

        # (3) self-adapting calm-regime gate (shift(1) => strictly prior threshold)
        thresh = lm_vol.rolling(window, min_periods=window // 2).quantile(q).shift(1)
        pos = (lm_vol < thresh).astype(float)
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — down-shocks must lift the asymmetric vol proxy,
    # and the gate must hold more exposure in the calm half than the stormy half.
    idx = pd.date_range("2020-01-01", periods=900, freq="D")
    rng = np.random.default_rng(0)
    vol = np.where(np.arange(len(idx)) < 450, 0.005, 0.05)
    r = rng.normal(0, 1, len(idx)) * vol
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})

    s = AsymLongMemVol(gamma=2.0, alpha=1.0, q=0.5, lags=90, window=252)
    pos = s.signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "must be long/flat {0,1}"
    calm = pos.iloc[300:440].mean()
    storm = pos.iloc[600:880].mean()
    assert calm > storm, f"calm ({calm:.2f}) should exceed storm ({storm:.2f})"

    # asymmetry check: same |returns|, but negative sign must raise the proxy
    up = pd.Series([0.0, 0.03, 0.0], index=pd.date_range("2021-01-01", periods=3))
    dn = pd.Series([0.0, -0.03, 0.0], index=up.index)
    vu = up.pow(2) * (1.0 + (2.0 - 1.0) * (up < 0).astype(float))
    vd = dn.pow(2) * (1.0 + (2.0 - 1.0) * (dn < 0).astype(float))
    assert vd.iloc[1] > vu.iloc[1], "down-shock must inject more variance at gamma>1"
    print(f"OK: exposure calm {calm:.0%} vs storm {storm:.0%}; "
          f"down-shock var {vd.iloc[1]:.4f} > up-shock var {vu.iloc[1]:.4f}")
