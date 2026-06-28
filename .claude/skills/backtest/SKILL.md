---
name: backtest
description: Translate a Quant Scout finding (or a free-text strategy idea) into a concrete, testable strategy, run it through the two-stage backtest pipeline (vectorbt sweep + backtrader out-of-sample validation with deflated-Sharpe overfitting checks), write a dated report into backtests/reports/, and commit it. Use when the user wants to backtest, validate, or stress-test a trading idea or research finding.
argument-hint: "[digest-date \"finding title\"  |  free-text idea]"
allowed-tools: Read, Write, Edit, Bash(python3 backtests/run.py *), Bash(pip install *), Bash(git *), Bash(ls *), Bash(cat *)
model: claude-opus-4-8
---

# Backtest

You turn a research finding into a tested strategy. Be rigorous and honest:
the goal is to find out whether an edge is **real after costs and out-of-sample**,
not to manufacture a good-looking number.

`$ARGUMENTS` = either a reference to a digest finding (a date + title, e.g.
`2026-06-16 "QuantaAlpha"`) or a free-text idea (e.g. "BTC 20/100 MA crossover").
If empty, ask which finding or idea to test, or offer the most recent digest's
"replicate/backtest" items.

## Step 1 — Get the idea
- If given a digest reference, read `research/digests/<date>-quant-scout.md` and pull
  the finding (its rules, asset class, and the "Next step" tag).
- If free-text, use it directly.
- Restate the idea as a concrete spec: **asset/symbol, timeframe, entry rule, exit
  rule, parameters to sweep.** If the idea is vague, choose a sensible, simple first
  translation and say so in the report (you can iterate later).

## Step 2 — Map to a strategy
- Check `backtests/engine/strategies/` for an existing strategy that fits
  (currently `ma_crossover`). Reuse it if the idea maps cleanly.
- If not, **write a new strategy module** in `backtests/engine/strategies/<name>.py`
  subclassing `Strategy` (implement `signals(df) -> position in {-1,0,1}` and a
  `param_grid()`), and register it in `strategies/__init__.py`. Keep signals
  look-ahead-free (the engine shifts by one bar; don't peek at the current close
  for the current position beyond what indicators legitimately use).

## Step 3 — Pick the symbol (crypto-first)
- Default to crypto via yfinance tickers: `BTC-USD`, `ETH-USD`, etc.
- Choose `--period` long enough for the strategy's longest look-back (e.g. a
  200-period MA needs several years of daily bars).

## Step 4 — Ensure deps, then run
```bash
pip install -r backtests/requirements.txt        # first run only
python backtests/run.py --symbol <SYM> --strategy <name> --period 5y \
    --idea-source "<digest-date / title or 'manual'>"
```
- The pipeline does: load data → purged/embargoed train/test split → **vectorbt**
  parameter sweep on train → **backtrader** validation of the winner on test →
  deflated-Sharpe gate → verdict. It writes the report itself.
- **Data note:** if Yahoo is unreachable (restricted network), the run falls back to
  **synthetic data** and the verdict is `INVALID`. Do **not** present synthetic
  numbers as a result. Instead, tell the user to allowlist Yahoo's domains
  (`query1/query2/finance.yahoo.com`) per `backtests/README.md`, or to drop a CSV
  into `backtests/data/`. Then re-run.

## Step 5 — Read the report critically
Open the generated `backtests/reports/<date>-<strategy>-<symbol>.md` and sanity-check:
- Did it survive **out-of-sample** (test Sharpe > 0)?
- Does it pass the **deflated-Sharpe** gate (prob ≥ 0.95)? If not, say plainly it's
  likely overfit to the grid.
- Is the max drawdown tolerable? Is turnover/cost realistic?
Add a short human read on whether this is worth advancing.

## Step 6 — Log & commit
- Prepend a row to `backtests/reports/INDEX.md` (date, report link, strategy·symbol,
  verdict, OOS Sharpe, deflated-SR prob).
- Commit and push to `claude/trading-ai-research-prompt-e3v01m`:
```bash
git add backtests/ && git commit -m "backtest: <strategy> on <symbol> <date> — <verdict>" \
  && git push -u origin claude/trading-ai-research-prompt-e3v01m
```
Retry push with backoff on network errors. Do not open a PR. Then summarise to the
user: the idea, the verdict, the key metrics, and the honest next step.

## Honesty rules
- Never fabricate metrics, fills, or data. If data is synthetic or missing, say so.
- A passing in-sample Sharpe means nothing on its own — only out-of-sample +
  deflated-Sharpe survival counts.
- Prefer simple, transparent strategies first; add complexity only when justified.
