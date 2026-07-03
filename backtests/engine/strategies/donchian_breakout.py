"""Short-term Donchian-channel breakout — the canonical trend-following primitive.

Translation of the central claim in Kurth, Eisler, Rej & Bouchaud (CFM),
arXiv:2607.01550, "Is Trend Still Your Friend?: A Microstructural Account of the
Demise of Short-Term Trend-Following". They document that since ~2009 short-term
trend PnL has collapsed on *small-tick* (volatility-normalised) contracts across
all signal horizons, while surviving on large-tick ones. BTC-USD trades at a tiny
tick relative to its volatility, so their thesis predicts short-term trend on BTC
should carry little-to-no reliable edge — this is a confirmatory falsification test.

Donchian "always-in" rule: go long when the close breaks above the highest high
of the prior N bars, short when it breaks below the lowest low of the prior N bars,
and hold the last breakout direction until the opposite channel is broken. Short
lookbacks (N = 5..40 daily bars) target the *short-term* speed the paper indicts.

Look-ahead-free: the channel uses highs/lows through bar t-1 (`.shift(1)`) and the
current close at t; the engine shifts the position by one more bar before applying
returns, so a signal computed at t's close is only entered at t+1.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class DonchianBreakout(Strategy):
    name = "donchian_breakout"

    @staticmethod
    def param_grid() -> list[dict]:
        # short-term trend speeds: ~1 week to ~2 months of daily bars
        return [{"window": w} for w in (5, 10, 20, 30, 40)]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        window = int(self.params.get("window", 20))
        close = df["close"].astype(float)
        upper = df["high"].astype(float).rolling(window).max().shift(1)  # prior-N high
        lower = df["low"].astype(float).rolling(window).min().shift(1)   # prior-N low
        raw = pd.Series(np.nan, index=df.index)
        raw[close > upper] = 1.0
        raw[close < lower] = -1.0
        # hold last breakout direction until the opposite channel breaks; flat pre-warmup
        return raw.ffill().fillna(0.0)
