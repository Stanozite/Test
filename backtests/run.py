#!/usr/bin/env python3
"""CLI entry point for the backtest pipeline.

Usage:
    python backtests/run.py --symbol BTC-USD --strategy ma_crossover --period 5y
    python backtests/run.py --symbol ETH-USD --no-synthetic   # fail loud if no real data

Writes a Markdown report to backtests/reports/<date>-<strategy>-<symbol>.md and
prints the report path + verdict. Run from the repo root.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import pipeline, report  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTC-USD")
    ap.add_argument("--strategy", default="ma_crossover")
    ap.add_argument("--period", default="5y")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--fee", type=float, default=0.0010)
    ap.add_argument("--slippage", type=float, default=0.0005)
    ap.add_argument("--idea-source", default="")
    ap.add_argument("--date", default=None, help="report date YYYY-MM-DD (default: today)")
    ap.add_argument("--no-synthetic", action="store_true",
                    help="fail instead of falling back to synthetic data")
    args = ap.parse_args()

    res = pipeline.run(args.symbol, strategy=args.strategy, period=args.period,
                       interval=args.interval, fee=args.fee, slippage=args.slippage,
                       allow_synthetic=not args.no_synthetic)

    date = args.date or _dt.date.today().isoformat()
    md = report.render(res, date=date, idea_source=args.idea_source)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(out_dir, exist_ok=True)
    slug = f"{date}-{args.strategy}-{args.symbol}".replace("/", "-")
    out_path = os.path.join(out_dir, f"{slug}.md")
    with open(out_path, "w") as fh:
        fh.write(md)

    print(f"VERDICT: {res.verdict}")
    print(f"SOURCE:  {res.source} (synthetic={res.is_synthetic})")
    print(f"REPORT:  {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
