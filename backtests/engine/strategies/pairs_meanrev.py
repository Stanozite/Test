"""Pairs mean-reversion on a relative-price (ratio) series — cross-sectional axis.

Tradable analogue of Liu/Thomas/Baer/Donovan "Adapting Pairs Trading to Gambling
Markets" (2609.22639): model a mean-reverting spread (they use a latent OU process
with a time-varying reversion level) and trade divergences back to the mean.

Here the "asset" is a BTC/ETH price *ratio* series (close = BTC_close / ETH_close),
whose per-bar pct-change ~= the return of a dollar-neutral long-BTC / short-ETH pair.
The signal is a rolling z-score of log(ratio): when the ratio is rich (z high) short
it (-1 = short BTC / long ETH); when cheap (z low) long it (+1); flat inside the band.
Stateless and look-ahead-free (the engine shifts positions by one bar).

ponytail: standard z-score band, not a fitted OU — the OU MLE adds params to sweep
without changing the mechanism; upgrade to an OU half-life estimate only if the band
version shows a real edge worth refining.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


class PairsMeanRev(Strategy):
    name = "pairs_meanrev"

    @staticmethod
    def param_grid() -> list[dict]:
        grid = []
        for lookback in (20, 40, 60, 90):
            for entry in (1.0, 1.5, 2.0):
                grid.append({"lookback": lookback, "entry": entry})
        return grid

    def signals(self, df: pd.DataFrame) -> pd.Series:
        lookback = int(self.params.get("lookback", 40))
        entry = float(self.params.get("entry", 1.5))
        logc = np.log(df["close"].astype(float))
        mean = logc.rolling(lookback).mean()
        std = logc.rolling(lookback).std()
        z = (logc - mean) / std.replace(0.0, np.nan)
        pos = pd.Series(0.0, index=df.index)
        pos[z > entry] = -1.0    # ratio rich -> short BTC / long ETH
        pos[z < -entry] = 1.0    # ratio cheap -> long BTC / short ETH
        return pos.fillna(0.0)
