"""Long-only long-horizon trend filter (long / flat, never short).

Capstone falsification for the BTC trend thread. Five prior BTC tests all
REJECTED short/medium directional trend and reversal:
  - tsmom (long/short, 20-120d) — OOS ~0; the report's diagnosis was that the
    SHORT leg bleeds against BTC's structural up-drift.
  - donchian_breakout (fast bands w5-w40) — OOS collapse; faster = weaker,
    matching Kurth/Eisler/Rej/Bouchaud (2607.01550): short-term trend is dead
    on small effective-tick assets (BTC is one).
  - lag1_reversal, cost_aware_momentum (short 5-20d), ma_crossover — all REJECT.

This tests the untested complement of both threads at once:
  (a) drop the bleeding short leg  -> long-or-flat only, and
  (b) use LONG horizons (60-250d)  -> the band Kurth et al. do NOT indict.
Question: once you remove the short leg and go slow, does any trend edge survive
on BTC out-of-sample, or is even long-horizon long-only trend just a worse-timed
proxy for buy-and-hold? The deflated-Sharpe gate and OOS split decide.

Signal is past-only (trailing return through the current close); the engine
shifts one bar, so no look-ahead.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class TrendFilter(Strategy):
    name = "trend_filter"

    @staticmethod
    def param_grid() -> list[dict]:
        # daily bars; ~3 months to ~1 year of trend — the slow band
        return [{"lookback": lb} for lb in (60, 90, 120, 180, 250)]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 120))
        close = df["close"].astype(float)
        trailing = close / close.shift(lookback) - 1.0    # past-only trailing return
        pos = (trailing > 0).astype(float)                # long when up-trend, else flat
        return pos.fillna(0.0)
