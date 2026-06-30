# Quant Scout Digest — 2026-06-30

## TL;DR
- **Cost-aware execution beats better prediction** (Bysik/Ślepaczuk, UW QFRG): hourly
  BTC-USDT forecasts (XGBoost/LSTM/iTransformer, 27-fold walk-forward, 2018–2026) all
  earn gross alpha, but naive sign-flipping dies at 10 bps cost. A filter that trades
  only when forecast magnitude exceeds a cost threshold restores a long-only XGBoost
  config to >65% ann. return, Sharpe >1.0. **Backtest target this run.**
- Methods reference: ML-bias-in-economic-history guide (Johansen/Koschnick/Vedel) —
  systematic prediction error from training on biased historical labels; a checklist
  relevant to any backtest that trains on its own price history.
- **Thin Tuesday window.** The June-30 arXiv batch was not yet announced at run time;
  the q-fin /new and /recent listings still topped out at the 06-29 batch (2606.27932,
  already captured). Fresh IDs above the ceiling (2606.28063/28312/27924/27525, plus
  2606.27845) are overwhelmingly econ.GN / non-trading; only the items below cleared the bar.

## Findings by focus area

### ML / AI for alpha
- **Machine Learning-Based Bitcoin Trading Under Transaction Costs: Evidence From
  Walk-Forward Forecasting** — Andrei Bysik & Robert Ślepaczuk (Univ. of Warsaw QFRG),
  19 May 2026 — [arXiv:2606.00060](https://arxiv.org/abs/2606.00060)
  - **What it is:** XGBoost, LSTM, and iTransformer predict hourly BTC-USDT returns over
    ~70k observations (2018–2026) under a 27-fold walk-forward protocol. All three beat
    buy-and-hold gross, but naive sign-based trading is wiped out by a 10 bps round-trip
    cost. Their fix — a *cost-aware execution filter* that suppresses a trade unless the
    predicted move exceeds a transaction-cost-based threshold — slashes turnover and
    restores profitability; the best long-only XGBoost config clears >65% annualized with
    Sharpe >1.0.
  - **Why it matters for trading:** The thesis is operational, not predictive — "the
    bottleneck isn't weak forecasts, it's how forecasts become trades." A magnitude
    threshold is a one-line overlay on any signal we already trade, and it is directly
    testable on BTC-USD daily without ML: only act when the signal's expected edge clears
    costs. This is the rare finding that is both crypto-native and trivially replicable.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 5/5
  - **Next step:** backtest (cost-aware threshold overlay on a BTC-USD momentum signal — this run)

### Microstructure & execution
_no notable new findings this run_

### Risk & portfolio
_no notable new findings this run_

### Asset class / market
_(covered above — the BTC finding is the only crypto item clearing the bar)_

## New resources & tooling
- **How to deal with machine learning bias in economic history** — Johansen, Koschnick,
  Vedel, 30 Jun 2026 — [arXiv:2606.28063](https://arxiv.org/abs/2606.28063). Methods
  reference (econ.GN), not a strategy: a practical guide to systematic prediction error
  when ML is trained on biased historical data. Read as a checklist for label/leakage bias
  in any model trained on its own price history. Scores low on trading relevance (2/5) but
  earns a slot as a backtest-hygiene reference.

## Watchlist updates
- **Andrei Bysik & Robert Ślepaczuk (Univ. of Warsaw QFRG)** — add as players.
  Ślepaczuk's group (already noted via Michańków/Sakowski for derivatives/CVA) also does
  rigorous cost-aware crypto ML with proper walk-forward; worth following for execution-
  realistic strategy papers.

## Open questions / threads to pull next run
- **Revisiting Factor Momentum: A One-Month Lag Perspective** (Rönkkö & Holmi, SSRN
  5333744) surfaced in search: replacing the 12-month formation window with a 1-month
  window reportedly doubles the share of factors with significant momentum (~20%→40%)
  after controlling for positive-mean tilt. SSRN returned 403 at run time — **[DATA NEEDED:
  confirm posting date and abstract]** before capturing; could be older than the window.
- Re-scan the **June-30 / July-01 arXiv batches** next run once announced — this run hit
  them before they went live.
