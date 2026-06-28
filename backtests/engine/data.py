"""Data layer for the backtest pipeline.

Priority order when loading OHLCV:
  1. Local CSV cache under backtests/data/ (fast, offline, reproducible).
  2. yfinance live download (equities/ETFs/crypto via Yahoo) — requires the
     environment to allowlist Yahoo's domains (see backtests/README.md).
  3. Synthetic generator — ONLY for plumbing/smoke tests when no real data is
     reachable. Clearly flagged; never use synthetic output as a real result.

A successful live download is written back to the cache so later runs are
offline-capable and deterministic.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@dataclass
class PriceData:
    """OHLCV frame plus provenance so reports can state where data came from."""
    df: pd.DataFrame          # columns: open, high, low, close, volume; DatetimeIndex
    symbol: str
    source: str               # "cache" | "yfinance" | "synthetic"
    is_synthetic: bool        # gate: reports must refuse to certify synthetic runs


def _cache_path(symbol: str, interval: str) -> str:
    safe = symbol.replace("/", "-").replace(" ", "")
    return os.path.normpath(os.path.join(DATA_DIR, f"{safe}_{interval}.csv"))


def _from_cache(symbol: str, interval: str) -> pd.DataFrame | None:
    path = _cache_path(symbol, interval)
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df if len(df) else None


def _from_yfinance(symbol: str, period: str, interval: str) -> pd.DataFrame | None:
    try:
        import yfinance as yf
    except ImportError:
        return None
    try:
        raw = yf.download(symbol, period=period, interval=interval,
                          auto_adjust=True, progress=False)
    except Exception:
        return None
    if raw is None or len(raw) == 0:
        return None
    # Normalise to lowercase single-level columns.
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    raw = raw.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
    raw.index = pd.to_datetime(raw.index)
    return raw.dropna()


def _synthetic(symbol: str, periods: int, interval: str, seed: int = 7) -> pd.DataFrame:
    """Deterministic GBM-with-vol-clustering series. NOT a real market.

    Seeded so smoke tests are reproducible. The seed is derived from the symbol
    so different symbols look different, but the same symbol is always identical.
    """
    rng = np.random.default_rng(seed + (abs(hash(symbol)) % 1000))
    mu, sigma = 0.0002, 0.03                       # daily drift / base vol
    vol = sigma * (1 + 0.5 * np.abs(rng.standard_normal(periods).cumsum() / periods**0.5))
    rets = mu + vol * rng.standard_normal(periods)
    close = 100 * np.exp(np.cumsum(rets))
    idx = pd.date_range("2021-01-01", periods=periods, freq="D")
    high = close * (1 + np.abs(rng.standard_normal(periods)) * 0.01)
    low = close * (1 - np.abs(rng.standard_normal(periods)) * 0.01)
    openp = np.concatenate([[close[0]], close[:-1]])
    volume = rng.integers(1_000, 100_000, periods).astype(float)
    return pd.DataFrame(
        {"open": openp, "high": high, "low": low, "close": close, "volume": volume},
        index=idx,
    )


def load_prices(symbol: str, period: str = "5y", interval: str = "1d",
                allow_synthetic: bool = True) -> PriceData:
    """Load OHLCV for `symbol`, trying cache → yfinance → synthetic."""
    cached = _from_cache(symbol, interval)
    if cached is not None:
        return PriceData(cached, symbol, "cache", is_synthetic=False)

    live = _from_yfinance(symbol, period, interval)
    if live is not None:
        os.makedirs(os.path.normpath(DATA_DIR), exist_ok=True)
        live.to_csv(_cache_path(symbol, interval))
        return PriceData(live, symbol, "yfinance", is_synthetic=False)

    if not allow_synthetic:
        raise RuntimeError(
            f"No data for {symbol}: cache miss and yfinance unreachable. "
            "Allowlist Yahoo's domains or drop a CSV into backtests/data/."
        )
    periods = {"5y": 1825, "2y": 730, "1y": 365}.get(period, 1000)
    return PriceData(_synthetic(symbol, periods, interval), symbol,
                     "synthetic", is_synthetic=True)
