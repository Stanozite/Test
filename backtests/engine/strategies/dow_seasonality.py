"""Day-of-week calendar seasonality — the daily-frequency test of periodic
algorithmic-trading return predictability.

Motivated by Kim & Hansen (arXiv:2607.09426), "The Quarter-Hour Effect: Periodic
Algorithmic Trading and Return Predictability in Cryptocurrency Futures". They
document that periodic (calendar-clock) algorithmic order flow creates return
predictability in crypto — but *intraday* (quarter-hour / 5-min / 1-min marks,
predictive out to 4-12h). Their effect is invisible on daily closes by
construction.

This strategy asks the honest daily-pipeline analogue: does ANY calendar
periodicity survive at daily frequency on BTC? Day-of-week is the daily clock's
equivalent of the intra-hour clock. Rule: hold long into a weekday whose trailing
same-weekday mean return is positive (long/short variant also shorts negative
weekdays). Falsifiable prediction: no reliable edge — the periodicity Kim/Hansen
find lives intraday, not at the daily grid.

Look-ahead-free: the trailing same-weekday mean at bar t uses only same-weekday
returns strictly before t; weekdays themselves are calendar-known in advance. The
`.shift(-1)` pulls tomorrow's (known) weekday profile into today's signal so that
after the engine's one-bar shift, the position held into bar t was decided from
data available before t.
"""
from __future__ import annotations

import pandas as pd

from .base import Strategy


class DowSeasonality(Strategy):
    name = "dow_seasonality"

    @staticmethod
    def param_grid() -> list[dict]:
        # weeks = number of trailing same-weekday occurrences in the profile
        return [
            {"weeks": w, "mode": m}
            for w in (8, 13, 26, 52)
            for m in ("longflat", "longshort")
        ]

    def signals(self, df: pd.DataFrame) -> pd.Series:
        weeks = int(self.params.get("weeks", 26))
        mode = str(self.params.get("mode", "longflat"))
        close = df["close"].astype(float)
        ret = close.pct_change()
        wd = pd.Series(df.index, index=df.index).dt.weekday  # 0=Mon .. 6=Sun

        # trailing same-weekday mean, using occurrences strictly before each bar
        same_wd_mu = pd.Series(0.0, index=df.index)
        for d in range(7):
            mask = wd == d
            sub = ret[mask]
            # mean of prior `weeks` same-weekday returns (shift(1) excludes current)
            mu = sub.rolling(weeks, min_periods=max(4, weeks // 2)).mean().shift(1)
            same_wd_mu.loc[mask] = mu

        raw = pd.Series(0.0, index=df.index)
        raw[same_wd_mu > 0] = 1.0
        if mode == "longshort":
            raw[same_wd_mu < 0] = -1.0

        # pull tomorrow's (calendar-known) weekday profile into today's signal;
        # engine's shift(1) undoes it, leaving a strictly past-informed position.
        return raw.shift(-1).fillna(0.0)


if __name__ == "__main__":
    # ponytail: one runnable check — no look-ahead, correct weekday alignment.
    import numpy as np
    idx = pd.date_range("2020-01-01", periods=400, freq="D")
    # inject a fake Monday premium so the profile must detect it
    rng = np.random.default_rng(0)
    r = rng.normal(0, 0.01, len(idx))
    r[idx.weekday == 0] += 0.02  # Mondays up
    px = pd.Series(100 * (1 + pd.Series(r, index=idx)).cumprod().values, index=idx)
    df = pd.DataFrame({"close": px})
    s = DowSeasonality(weeks=13, mode="longflat")
    pos = s.signals(df)
    assert set(pos.dropna().unique()) <= {0.0, 1.0}, "longflat must be in {0,1}"
    # after warmup, the signal held INTO a Monday (return earned on Monday) should
    # be long: position at bar t earns ret[t]; find Mondays past warmup.
    mondays = df.index[(df.index.weekday == 0)][20:]
    held_long_on_mon = (pos.shift(1).reindex(df.index).loc[mondays] == 1.0).mean()
    assert held_long_on_mon > 0.7, f"should catch Monday premium, got {held_long_on_mon:.2f}"
    print(f"OK: long into Monday {held_long_on_mon:.0%} of the time after warmup")
