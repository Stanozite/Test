#!/usr/bin/env python3
"""Quick check: can the pipeline reach real market data in this environment?

Run after allowlisting Yahoo's domains to confirm live data works:
    python backtests/check_data.py

Exits 0 and prints REACHABLE if a real download succeeds; exits 1 and prints the
exact allowlist instructions if the data host is blocked.
"""
from __future__ import annotations

import sys

DOMAINS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com", "finance.yahoo.com"]


def main() -> int:
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance not installed. Run: pip install -r backtests/requirements.txt")
        return 1

    try:
        df = yf.download("BTC-USD", period="5d", interval="1d",
                         auto_adjust=True, progress=False)
    except Exception as exc:  # network/policy errors surface here
        df = None
        err = repr(exc)
    else:
        err = ""

    if df is not None and len(df) > 0:
        last = float(df["Close"].iloc[-1]) if "Close" in df else float(df.iloc[-1, 0])
        print("REACHABLE ✅  Yahoo data is accessible.")
        print(f"  BTC-USD last close (5d sample): {last:,.2f} over {len(df)} bars.")
        print("  Real backtests will now work: python backtests/run.py --symbol BTC-USD")
        return 0

    print("BLOCKED ❌  No real data reached this environment.")
    if err:
        print(f"  error: {err}")
    print("  Fix: allowlist these domains in the environment's Network settings")
    print("       (Routines → edit → environment → Network access → Custom):")
    for d in DOMAINS:
        print(f"         {d}")
    print("  Or drop a CSV into backtests/data/ named <SYMBOL>_<interval>.csv.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
