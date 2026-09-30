"""Build a BTC/ETH ratio series from the two cached daily CSVs.

close = BTC_close / ETH_close on the intersection of dates. pct-change of this
ratio ~= the return of a dollar-neutral long-BTC / short-ETH pair, so a standard
single-symbol backtest on this synthetic 'asset' faithfully tests BTC/ETH pairs
mean-reversion. Writes backtests/data/BTCETH-RATIO_1d.csv (cache-first loader
picks it up; no network needed).
"""
import os
import pandas as pd

D = os.path.join(os.path.dirname(__file__), "data")
btc = pd.read_csv(os.path.join(D, "BTC-USD_1d.csv"), index_col=0, parse_dates=True)
eth = pd.read_csv(os.path.join(D, "ETH-USD_1d.csv"), index_col=0, parse_dates=True)
j = pd.DataFrame({"btc": btc["close"], "eth": eth["close"]}).dropna()
ratio = (j["btc"] / j["eth"]).rename("close")
out = pd.DataFrame({"open": ratio, "high": ratio, "low": ratio,
                    "close": ratio, "volume": 0.0})
out.index.name = "Date"
path = os.path.join(D, "BTCETH-RATIO_1d.csv")
out.to_csv(path)
print(f"rows={len(out)}  {out.index.min().date()}..{out.index.max().date()}  "
      f"ratio {ratio.min():.1f}..{ratio.max():.1f}  ->  {path}")
