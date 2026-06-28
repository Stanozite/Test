# Backtests — component #2 (idea → backtest pipeline)

Turns findings from the Quant Scout digests (`research/digests/`) into tested,
documented strategies. Each run produces a Markdown report with real metrics and
an overfitting-aware verdict, committed alongside the research it came from.

## How it works — two-stage by design

```
finding/idea  →  strategy spec  →  Stage 1: vectorbt sweep  →  Stage 2: backtrader validate  →  report + verdict
                                   (fast param search,          (winner only, on held-out
                                    on the TRAIN split)          TEST split, realistic costs)
```

- **Stage 1 (vectorbt):** sweep the strategy's parameter grid on the in-sample
  split, rank by Sharpe. Fast and vectorized.
- **Stage 2 (backtrader):** re-run only the winning parameters on a **held-out,
  purged + embargoed** out-of-sample split, with explicit fees and slippage.
- **Verdict** combines the out-of-sample Sharpe with the **Deflated Sharpe Ratio**
  (López de Prado), which penalises a result for how many configurations were
  tested — the guardrail against overfitting.

If a library is missing the pipeline degrades to a dependency-free pandas core, so
it always runs.

## Usage

```bash
pip install -r backtests/requirements.txt

# From the repo root:
python backtests/run.py --symbol BTC-USD --strategy ma_crossover --period 5y
python backtests/run.py --symbol ETH-USD --no-synthetic   # fail loudly if no real data
```

Reports land in `backtests/reports/<date>-<strategy>-<symbol>.md` and are logged in
`backtests/reports/INDEX.md`.

The AI-driven path is the **`/backtest`** skill: give it a digest finding and it
specs the strategy, runs the pipeline, writes the report, and commits.

## ⚠️ Data access — required for real results

The pipeline uses **yfinance** (Yahoo) for crypto/equity data. In a restricted
network environment (including Claude Code cloud sessions on the **Default /
Trusted** policy), Yahoo and other market-data APIs are **blocked**, so live
fetches fail and the pipeline falls back to a clearly-labeled **synthetic** series
(verdict `INVALID`) — useful only for verifying the plumbing.

To get real backtests, allowlist the data domains in your environment:

1. Edit the environment (Routines → pencil → environment settings, or the web
   environment settings) → **Network access → Custom**.
2. Add these domains (keep the default package-manager allowlist checked):
   ```
   query1.finance.yahoo.com
   query2.finance.yahoo.com
   finance.yahoo.com
   ```
3. Save. The next run fetches live data and caches it under `backtests/data/`.

Alternatively, drop your own OHLCV CSVs into `backtests/data/` named
`<SYMBOL>_<interval>.csv` (e.g. `BTC-USD_1d.csv`, columns:
`open,high,low,close,volume`, datetime index) — the cache is checked first, so
this works fully offline.

## Layout

```
backtests/
  run.py                 # CLI entry point
  requirements.txt
  engine/
    data.py              # cache → yfinance → synthetic loader
    metrics.py           # Sharpe, CAGR, MaxDD, Deflated Sharpe
    pipeline.py          # data → split → sweep → validate → verdict
    report.py            # Markdown renderer
    run_vectorbt.py      # stage-1 sweep
    run_backtrader.py    # stage-2 validation
    strategies/          # Strategy interface + seed strategies (registry)
  reports/               # generated reports + INDEX.md
  data/                  # cached/your-own OHLCV CSVs (gitignored)
```

## Notes & limits
- Give the OOS split enough bars for the strategy's longest look-back (e.g. a
  200-day MA needs a multi-year `--period`), or the held-out test stays flat.
- This is research tooling, not trading advice. A `PROMISING` verdict means
  "worth deeper validation," not "deploy capital."
