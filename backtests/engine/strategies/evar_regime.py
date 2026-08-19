"""EVaR tail-risk regime gate — the daily test of "govern exposure with a
coherent HEAVY-LEFT-TAIL risk measure rather than symmetric variance".

Motivated by Jaehyung Choi (arXiv:2608.18022), "Entropic Value-at-Risk portfolio
optimization for tempered stable Lévy processes", which argues Entropic VaR (EVaR)
— a coherent risk measure that is an upper bound on CVaR and weights the worst
losses exponentially — is a superior risk control under heavy tails, and reports
several minimum-EVaR / entropic reward-risk sector-ETF portfolios beating their
CVaR-matched and standard benchmarks OOS 2000-2026.

The tradeable single-series analogue: gate exposure on trailing EVaR of the return
distribution instead of realized std. This is a deliberate apples-to-apples sibling
of `vol_regime` (same self-adapting rolling-quantile gate structure) — the ONLY
change is the risk statistic: EVaR (exponential tail weighting, α-tail focus) vs a
plain realized-vol std. BTC-USD is the natural stress test: it is the most heavy-
tailed liquid asset, exactly where an EVaR gate should diverge most from a vol gate.

Rule (long/flat, discrete {0,1}): go long when trailing EVaR sits below its own
rolling quantile over a long reference window (calm tail regime), else flat.

Sample EVaR of losses l = -returns at tail level α:
    EVaR_α(l) = inf_{z>0}  z * ( logmeanexp(l / z) - ln α )
(Ahmadi-Javid 2012). We minimize over a log-spaced z grid scaled to the window's
loss dispersion; logmeanexp is computed with a max-shift for numerical stability.

Falsifiable prediction: consistent with 11 straight daily-BTC single-series rejects
AND with the vol_regime result, an EVaR gate should behave as *crash insurance* —
trim drawdown, maybe nudge Sharpe — but NOT add raw return and NOT clear the
deflated-Sharpe gate as an alpha. If a *tail* measure clears the gate where plain
vol did not, that would be the first crack in the "daily BTC is tapped out" thesis
and would vindicate Choi's "EVaR > variance/CVaR as a control" claim on crypto.

Look-ahead-free: EVaR at bar t uses returns strictly up to t; the rolling-quantile
threshold uses EVaR values up to t-1 (shift(1)). The engine's own shift(1) then
enters the position at t+1.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


def _evar_of_losses(losses: np.ndarray, alpha: float) -> float:
    """Sample EVaR at tail level alpha over an array of losses (= -returns).

    EVaR_alpha = inf_{z>0} z * (logmeanexp(losses/z) - ln alpha).
    """
    l = losses[np.isfinite(losses)]
    if l.size < 3:
        return np.nan
    s = l.std()
    if not np.isfinite(s) or s <= 0:
        return float(l.mean())
    # z grid scaled to loss dispersion; wide enough to bracket the interior inf.
    zgrid = np.geomspace(s * 0.05, s * 20.0, 40)
    la = np.log(alpha)
    best = np.inf
    for z in zgrid:
        m = l / z
        mmax = m.max()
        lme = mmax + np.log(np.mean(np.exp(m - mmax)))  # stable logmeanexp
        val = z * (lme - la)
        if val < best:
            best = val
    return float(best)


class EVaRRegime(Strategy):
    name = "evar_regime"

    @staticmethod
    def param_grid() -> list[dict]:
        # lookback = EVaR estimation window (days); alpha = tail level;
        # q = calm-regime quantile cutoff; window = rolling-quantile reference (days).
        return [
            {"lookback": lb, "alpha": a, "q": q, "window": w}
            for lb in (20, 40, 60)
            for a in (0.05, 0.10)
            for q in (0.5, 0.6)
            for w in (252,)
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 40))
        alpha = float(self.params.get("alpha", 0.05))
        q = float(self.params.get("q", 0.5))
        window = int(self.params.get("window", 252))

        close = df["close"].astype(float)
        ret = close.pct_change()
        losses = (-ret)

        # trailing EVaR of losses (uses returns up to and including bar t)
        evar = losses.rolling(lookback, min_periods=max(3, lookback // 2)).apply(
            lambda a: _evar_of_losses(np.asarray(a, dtype=float), alpha), raw=True
        )
        # calm-tail threshold: rolling quantile of PRIOR EVaR values (shift(1) => no
        # peeking at today's evar inside its own reference set).
        thresh = evar.rolling(window, min_periods=window // 2).quantile(q).shift(1)

        pos = (evar < thresh).astype(float)   # 1 long in calm tail regime / 0 flat
        return pos.fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — long more in the calm half, flat in the fat-tail
    # storm, and EVaR must strictly exceed realized std (it is a tail upper bound).
    idx = pd.date_range("2020-01-01", periods=900, freq="D")
    rng = np.random.default_rng(0)
    vol = np.where(np.arange(len(idx)) < 450, 0.005, 0.05)
    r = rng.normal(0, 1, len(idx)) * vol
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})

    # EVaR is an upper bound on the loss magnitude scale => >= std of losses.
    sample = (-df["close"].pct_change().dropna().iloc[500:560]).to_numpy()
    ev = _evar_of_losses(sample, 0.05)
    assert ev >= sample.std(), f"EVaR {ev:.4f} should exceed std {sample.std():.4f}"

    pos = EVaRRegime(lookback=40, alpha=0.05, q=0.5, window=252).signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "must be long/flat {0,1}"
    calm = pos.iloc[300:440].mean()
    storm = pos.iloc[600:880].mean()
    assert calm > storm, f"should hold more in calm ({calm:.2f}) than storm ({storm:.2f})"
    print(f"OK: EVaR {ev:.4f} >= std {sample.std():.4f}; exposure calm {calm:.0%} vs storm {storm:.0%}")
