"""Stage 1 — fast parameter sweep.

Uses vectorbt's vectorized Portfolio when available (honours the "use vectorbt"
choice); otherwise falls back to the dependency-free core in strategies.base so
the pipeline always runs. Same economic model either way: enter next bar, costs
charged on turnover.
"""
from __future__ import annotations

import pandas as pd

from . import metrics
from .strategies import Strategy, run_vectorized


def _sweep_one(df: pd.DataFrame, strat: Strategy, fee: float) -> dict:
    pos = strat.signals(df)
    equity, rets = run_vectorized(df, pos, fee=fee)
    return {"equity": equity, "returns": rets}


def sweep(df: pd.DataFrame, strategy_cls: type[Strategy], fee: float = 0.0010,
          interval: str = "1d") -> dict:
    """Run every param combo; rank by Sharpe. Returns best params + all results.

    `n_trials` (number of combos tested) is threaded into the deflated Sharpe so
    the winner is penalised for the breadth of the search.
    """
    grid = strategy_cls.param_grid()
    n_trials = max(len(grid), 1)

    # Prefer vectorbt if importable — same signals, vectorized across the grid.
    backend = "pandas-core"
    try:
        import vectorbt as vbt  # noqa: F401
        backend = "vectorbt"
    except Exception:
        pass

    rows = []
    for params in grid:
        strat = strategy_cls(**params)
        if backend == "vectorbt":
            import vectorbt as vbt
            pos = strat.signals(df).reindex(df.index).shift(1).fillna(0.0)
            entries = (pos > 0) & (pos.shift(1).fillna(0) <= 0)
            exits = (pos <= 0) & (pos.shift(1).fillna(0) > 0)
            pf = vbt.Portfolio.from_signals(
                df["close"], entries, exits, fees=fee, freq="1D", init_cash=10_000)
            rets = pf.returns()
            equity = (1.0 + rets).cumprod()
        else:
            r = _sweep_one(df, strat, fee)
            equity, rets = r["equity"], r["returns"]

        summ = metrics.summarize(equity, rets, n_trials=n_trials, interval=interval)
        rows.append({"params": params, "label": strat.label(), **summ})

    rows.sort(key=lambda x: x["sharpe"], reverse=True)
    return {"backend": backend, "n_trials": n_trials, "results": rows,
            "best": rows[0] if rows else None}
