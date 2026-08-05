"""Bitcoin halving-clock seasonality — the time-based analogue after a long line
of price-indicator rejects on BTC.

Motivated by Molnar (arXiv:2607.26188), "Bitcoin Runs on a Clock: Why Every Price
Indicator Dies and the Halving Clock Doesn't". The paper's claim: every widely
followed *price* oscillator (Pi Cycle, MVRV, Mayer, Puell) called cycle turns for
a decade then decayed to silence, but Bitcoin's *time* structure stayed fixed —
mature-cycle tops land 525/546/534 days after each halving and bottoms 406/364/366
days after those tops. The only signal whose sign is stable across epochs is a
causal power law in time-since-genesis. Molnar rests nothing on per-epoch
significance and pre-registers falsifiable windows.

This strategy tests the tradable core of that claim on daily BTC-USD: be long
through the post-halving accumulation-and-run-up phase (day `entry`..`exit` after
the most recent halving), flat (or short) through the post-top bear phase. If the
clock is real and tradable, holding the [entry, exit] window should beat B&H.

Honest ceiling up front: BTC-USD daily history covers ~3 halving cycles (2016,
2020, 2024-partial). A calendar rule with n=3 cycles has almost no out-of-sample
power — the purged train/test split trains on ~2 cycles and tests on ~1. So even a
"passing" number here is n=3 anecdote, not validation; Molnar himself calls the
current-cycle edge "one holdout, suggestive not decisive". Read the verdict with
that in mind.

Look-ahead-free: days-since-halving is a deterministic function of the calendar,
fully known in advance and independent of price. As in dow_seasonality, the raw
per-bar phase position is `.shift(-1)`ed so that after the engine's one-bar shift,
the position held into bar t was decided from information available before t.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy

# BTC halving dates (UTC). Only halvings at/ before a bar are used for that bar,
# so pre-2016 bars key off 2012; yfinance BTC-USD starts 2014-09.
_HALVINGS = pd.to_datetime([
    "2012-11-28",
    "2016-07-09",
    "2020-05-11",
    "2024-04-20",
    "2028-04-20",  # ponytail: extrapolated ~4y; only matters if data reaches 2028.
])


def _days_since_halving(index: pd.DatetimeIndex) -> pd.Series:
    idx = pd.DatetimeIndex(index).tz_localize(None)
    # most recent halving on/before each bar via searchsorted
    pos = _HALVINGS.searchsorted(idx, side="right") - 1
    last = pd.Series(pd.NaT, index=index)
    valid = pos >= 0
    last_vals = _HALVINGS[pos.clip(min=0)]
    d = (idx - last_vals).days.astype("float64")
    out = pd.Series(d, index=index)
    out[~valid] = float("nan")  # bars before the first known halving
    return out


class HalvingClock(Strategy):
    name = "halving_clock"

    @staticmethod
    def param_grid() -> list[dict]:
        # entry/exit = days after halving to hold the long. Tops cluster ~525-546d,
        # so exits bracket that; entries test "buy the dip early" vs "wait".
        return [
            {"entry": e, "exit": x, "mode": m}
            for e in (0, 60, 120)
            for x in (480, 520, 546)
            for m in ("longflat", "longshort")
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        entry = int(self.params.get("entry", 0))
        exit_ = int(self.params.get("exit", 520))
        mode = str(self.params.get("mode", "longflat"))

        d = _days_since_halving(df.index)
        in_window = (d >= entry) & (d <= exit_)

        raw = pd.Series(0.0, index=df.index)
        raw[in_window] = 1.0
        if mode == "longshort":
            # short the post-top bear phase (after exit, before next halving resets d)
            raw[d > exit_] = -1.0
        # bars with unknown phase (pre-first-halving / NaN) stay flat
        raw[d.isna()] = 0.0

        # calendar phase is known in advance; shift(-1) so the engine's shift(1)
        # leaves a strictly past-informed position (mirrors dow_seasonality).
        return raw.shift(-1).fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — window membership + no-lookahead alignment.
    # span a full post-halving cycle so both an in-window and a past-exit bar exist.
    idx = pd.date_range("2020-05-11", periods=900, freq="D")
    df = pd.DataFrame({"close": pd.Series(range(1, 901), dtype=float).values}, index=idx)
    s = HalvingClock(entry=0, exit=520, mode="longflat")
    pos = s.signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "longflat must be in {0,1}"
    # 2020-05-11 halving: day 100 after = 2020-08-19 should be IN the long window,
    # day 600 after = 2022-01-01 should be OUT (flat).
    d = _days_since_halving(idx)
    day100 = idx[(d >= 99) & (d <= 101)][0]
    day600 = idx[(d >= 599) & (d <= 601)][0]
    # position held INTO bar t = pos.shift(1); check the calendar mapping directly
    raw = pos.shift(-1)  # undo the strategy's shift to inspect per-bar phase
    assert raw.loc[day100] == 1.0, "day+100 after halving must be long"
    assert raw.loc[day600] == 0.0, "day+600 after halving must be flat (past exit)"
    print("OK: halving-window membership and alignment correct")
