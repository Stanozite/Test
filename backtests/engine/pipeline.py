"""End-to-end backtest pipeline: data -> split -> sweep -> validate -> verdict.

Two-stage by design:
  Stage 1 (vectorbt): sweep the param grid on the TRAIN split, rank by Sharpe.
  Stage 2 (backtrader): re-run only the winner on the held-out TEST split with
  realistic fees + slippage.

The train/test split is purged with an embargo gap so indicator look-back near
the boundary can't leak train data into test (cf. López de Prado).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from . import metrics, run_backtrader, run_vectorbt
from .data import load_prices
from .strategies import get, run_vectorized


@dataclass
class BacktestResult:
    symbol: str
    strategy: str
    source: str
    is_synthetic: bool
    train: dict
    test: dict
    best_params: dict
    full: dict
    verdict: str
    notes: list[str] = field(default_factory=list)


def _split(df: pd.DataFrame, train_frac: float = 0.7, embargo: int = 20):
    n = len(df)
    cut = int(n * train_frac)
    train = df.iloc[:cut]
    test = df.iloc[cut + embargo:]          # embargo gap drops leak-prone bars
    return train, test


def _verdict(full: dict, test: dict, is_synthetic: bool) -> tuple[str, list[str]]:
    notes = []
    if is_synthetic:
        notes.append("DATA IS SYNTHETIC — plumbing smoke-test only; not a real result.")
        return "INVALID (synthetic data)", notes

    oos = test.get("sharpe", 0.0)
    if not full.get("passes_dsr", False):
        notes.append("Fails deflated-Sharpe (<0.95): likely overfit to the search grid.")
    if oos <= 0:
        notes.append("Out-of-sample Sharpe <= 0: does not survive the held-out split.")

    if full.get("passes_dsr", False) and oos >= 0.5:
        return "PROMISING — advance to deeper validation", notes
    if oos > 0 and full.get("sharpe", 0) > 0:
        return "MIXED — weak edge, needs more data/robustness", notes
    return "REJECT — no edge after costs and OOS", notes


def run(symbol: str, strategy: str = "ma_crossover", period: str = "5y",
        interval: str = "1d", fee: float = 0.0010, slippage: float = 0.0005,
        allow_synthetic: bool = True) -> BacktestResult:
    pdata = load_prices(symbol, period=period, interval=interval,
                        allow_synthetic=allow_synthetic)
    df = pdata.df
    strat_cls = get(strategy)
    train_df, test_df = _split(df)

    # Stage 1 — sweep on train.
    sweep = run_vectorbt.sweep(train_df, strat_cls, fee=fee, interval=interval)
    best = sweep["best"] or {"params": {}, "label": strategy}
    best_params = best["params"]

    # Stage 2 — validate winner on test.
    winner = strat_cls(**best_params)
    test = run_backtrader.validate(test_df, winner, fee=fee, slippage=slippage,
                                   interval=interval)

    # Full-sample metrics for the winner (context for the report).
    eq, rets = run_vectorized(df, winner.signals(df), fee=fee, slippage=slippage)
    full = metrics.summarize(eq, rets, n_trials=sweep["n_trials"], interval=interval)

    verdict, notes = _verdict(full, test, pdata.is_synthetic)
    notes.append(f"stage1 backend={sweep['backend']}, stage2 engine={test.get('engine')}, "
                 f"grid={sweep['n_trials']} combos, data source={pdata.source}.")

    result = BacktestResult(
        symbol=symbol, strategy=strategy, source=pdata.source,
        is_synthetic=pdata.is_synthetic, train=best, test=test,
        best_params=best_params, full=full, verdict=verdict, notes=notes)
    result.leaderboard = sweep["results"]   # attached for the report leaderboard
    return result
