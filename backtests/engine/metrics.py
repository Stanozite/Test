"""Performance & robustness metrics for backtests.

Includes the Deflated Sharpe Ratio (López de Prado) so reports can flag results
that are likely products of multiple-testing / overfitting rather than skill.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm  # scipy ships with most scientific stacks; see requirements


def _ann_factor(interval: str) -> float:
    return {"1d": 252.0, "1h": 24 * 365.0, "1wk": 52.0}.get(interval, 252.0)


def sharpe(returns: pd.Series, interval: str = "1d", rf: float = 0.0) -> float:
    r = returns.dropna()
    if r.std(ddof=1) == 0 or len(r) < 2:
        return 0.0
    excess = r - rf / _ann_factor(interval)
    return float(np.sqrt(_ann_factor(interval)) * excess.mean() / excess.std(ddof=1))


def cagr(equity: pd.Series, interval: str = "1d") -> float:
    eq = equity.dropna()
    if len(eq) < 2 or eq.iloc[0] <= 0:
        return 0.0
    years = len(eq) / _ann_factor(interval)
    if years <= 0:
        return 0.0
    return float((eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1)


def max_drawdown(equity: pd.Series) -> float:
    eq = equity.dropna()
    if len(eq) == 0:
        return 0.0
    peak = eq.cummax()
    return float((eq / peak - 1).min())


def deflated_sharpe(returns: pd.Series, n_trials: int, interval: str = "1d") -> float:
    """Probability the strategy's true Sharpe is > 0, deflated for `n_trials`
    configurations tested (López de Prado, 2014). Returns a value in [0, 1];
    treat < 0.95 as "not convincingly better than luck".
    """
    r = returns.dropna()
    n = len(r)
    if n < 3 or r.std(ddof=1) == 0:
        return 0.0
    sr = sharpe(r, interval) / np.sqrt(_ann_factor(interval))   # per-period SR
    skew = float(pd.Series(r).skew())
    kurt = float(pd.Series(r).kurtosis()) + 3.0                 # pandas gives excess

    n_trials = max(int(n_trials), 1)
    emc = 0.5772156649
    e = (1 - emc) * norm.ppf(1 - 1.0 / n_trials) + emc * norm.ppf(1 - 1.0 / (n_trials * np.e))
    sr0 = np.sqrt(1.0 / (n - 1)) * e                            # expected max SR under null

    denom = np.sqrt(1 - skew * sr + (kurt - 1) / 4.0 * sr**2)
    if denom <= 0:
        return 0.0
    return float(norm.cdf(((sr - sr0) * np.sqrt(n - 1)) / denom))


def summarize(equity: pd.Series, returns: pd.Series, n_trials: int = 1,
              interval: str = "1d") -> dict:
    dsr = deflated_sharpe(returns, n_trials, interval)
    return {
        "sharpe": round(sharpe(returns, interval), 3),
        "cagr": round(cagr(equity, interval), 4),
        "max_drawdown": round(max_drawdown(equity), 4),
        "deflated_sharpe_prob": round(dsr, 3),
        "n_trials": int(n_trials),
        "n_periods": int(returns.dropna().shape[0]),
        "passes_dsr": bool(dsr >= 0.95),
    }
