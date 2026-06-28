"""Stage 2 — realistic validation of the winning params.

Re-runs the single best configuration through backtrader's event-driven engine
with explicit commission and slippage, on the held-out test split. This catches
costs and path-dependence that the vectorized sweep glosses over. If backtrader
isn't installed, falls back to the vectorized core with the same cost inputs.
"""
from __future__ import annotations

import pandas as pd

from . import metrics
from .strategies import Strategy, run_vectorized


def validate(df: pd.DataFrame, strat: Strategy, fee: float = 0.0010,
             slippage: float = 0.0005, interval: str = "1d") -> dict:
    try:
        import backtrader as bt
    except Exception:
        equity, rets = run_vectorized(df, strat.signals(df), fee=fee, slippage=slippage)
        s = metrics.summarize(equity, rets, n_trials=1, interval=interval)
        return {"engine": "pandas-core(fallback)", **s}

    pos = strat.signals(df).reindex(df.index).shift(1).fillna(0.0)

    class _Feed(bt.feeds.PandasData):
        params = (("datetime", None), ("open", "open"), ("high", "high"),
                  ("low", "low"), ("close", "close"), ("volume", "volume"),
                  ("openinterest", None))

    class _Strat(bt.Strategy):
        def __init__(self):
            self.target = pos
            self.curve = []

        def next(self):
            self.curve.append(self.broker.getvalue())
            ts = self.data.datetime.datetime(0)
            want = float(self.target.get(pd.Timestamp(ts), 0.0))
            held = self.position.size != 0
            if want > 0 and not held:
                self.order_target_percent(target=0.99)
            elif want <= 0 and held:
                self.order_target_percent(target=0.0)

    cerebro = bt.Cerebro()
    cerebro.adddata(_Feed(dataname=df))
    cerebro.addstrategy(_Strat)
    cerebro.broker.setcash(10_000)
    cerebro.broker.setcommission(commission=fee)
    cerebro.broker.set_slippage_perc(perc=slippage)
    strat_run = cerebro.run()[0]

    curve = pd.Series(strat_run.curve, index=df.index[: len(strat_run.curve)])
    if len(curve) < 2:
        return {"engine": "backtrader", "sharpe": 0.0, "cagr": 0.0,
                "max_drawdown": 0.0, "deflated_sharpe_prob": 0.0,
                "n_trials": 1, "n_periods": int(len(curve)), "passes_dsr": False}
    rets = curve.pct_change().fillna(0.0)
    s = metrics.summarize(curve / curve.iloc[0], rets, n_trials=1, interval=interval)
    return {"engine": "backtrader", **s}
