# Quant Scout Digest — 2026-07-04

## TL;DR
- **Empty arXiv batch — Sat Jul 4 (US holiday) weekend gap.** No new q-fin submission above the 07-03 ceiling `2607.01765`. Verified across q-fin.TR / PM / ST / CP / RM `/recent`, `/new`, and the July `/2026-07` month view: every category tops out at **2607.01550** (Kurth/Bouchaud, already captured 07-03). q-fin.TR `/2026-07` returns "No updates for this time period." No fresh cross-lists on cs.LG / econ.GN / stat.ML that map to a tradable finding. Ceiling unchanged: **2607.01765**.
- **BTC trend thread — CLOSED after six tests.** Today's backtest ran the capstone: a **long-only, long-horizon trend filter** (long-or-flat, 60–250d) — applying both fixes the prior five failures implied (drop the bleeding short leg; go slower than the horizon Kurth/Bouchaud 2607.01550 indict). Result: train Sharpe 0.918 → **OOS Sharpe 0.093, CAGR −0.4%** — no timing edge, same signature as `tsmom`/`donchian`. The *only* survivor is drawdown mitigation (full-sample MaxDD −60% vs BTC buy-and-hold −77%, Sharpe 0.864 vs 0.769) at the cost of ~5pp CAGR — crash insurance, **not alpha**. Verdict: **MIXED (leans REJECT)**.
- **Net for the day:** no new literature to capture; the actionable output is a **negative result** that retires the "is any trend/reversal alive on daily BTC" question — the answer is no for *return*, marginal-yes only for *risk reduction*.

## Findings by focus area

### ML / AI for alpha
_no notable new findings this run_ — no fresh arXiv batch (weekend/holiday gap); no new alpha-mining or ML-signal paper above the ceiling.

### Microstructure & execution
_no notable new findings this run._ The one microstructure item in the window (Kurth/Eisler/Rej/Bouchaud 2607.01550, "short-term trend is dead on small-tick assets") was captured 07-03; it motivated today's backtest rather than a new capture. One replacement seen — 2604.10005 (Dalen, institutional liquidity in prediction markets) was **withdrawn/superseded**, so dropped.

### Risk & portfolio
- **Backtest capstone (own work, negative result): long-only long-horizon trend filter on BTC-USD** — [report](../../backtests/reports/2026-07-04-trend_filter-BTC-USD.md), 2026-07-04.
  - **What it is:** long-or-flat when the trailing 60–250d return is positive; the complement of the five already-rejected BTC trend/reversal tests, built to falsify "trend fails only because of the short leg and short horizons."
  - **Why it matters for trading:** it comprehensively closes the BTC trend thread. Dropping the short leg and slowing the signal does **not** restore an out-of-sample return edge (OOS Sharpe 0.093, CAGR ~0). The only defensible benefit is defensive: cutting max drawdown ~16pp vs buy-and-hold by sitting out crashes — "trend as crash insurance," consistent with risk-managed momentum (Baltussen et al.), not alpha.
  - **Scores:** Novelty 2/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve as a return strategy; if pursued, re-frame as a **defensive drawdown overlay** and validate on its own terms (vs a vol-target overlay), not as a signal.

### Asset class / market
_no notable new findings this run._

## New resources & tooling
- _none verified this run._ (No new high-signal repos surfaced above the noise bar; nothing added to avoid unverifiable listings.)

## Watchlist updates
- _none._ No new players/sources cleared the bar on an empty batch.

## Open questions / threads to pull next run
- **BTC trend thread is closed** — stop re-testing directional trend/reversal on daily BTC. The next honest backtest target should move **off the trend axis**: either (a) a **defensive vol-target overlay** benchmarked against today's trend-filter drawdown profile, or (b) a **cross-sectional** signal across a small crypto basket (BTC/ETH/SOL), since every test so far has been single-asset time-series.
- **Fresh-paper backlog to check Monday (07-06):** arXiv q-fin weekend submissions will announce Mon; expect a catch-up batch above 2607.01765. Priority scan: any new **microstructure/tick-size** follow-ups to Kurth/Bouchaud, and any **crypto cross-sectional** or **LLM-alpha** work.
- **Intraday crypto predictability** (Wen/Bouri/Xu/Zhao, SSRN — intraday momentum+reversal) noted but **not captured**: it is older than the recency window and needs intraday data the daily pipeline can't test cleanly. Revisit only if an intraday feed is wired in.
