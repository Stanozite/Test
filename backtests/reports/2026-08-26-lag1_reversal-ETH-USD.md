# Backtest Report — lag1_reversal on ETH-USD — 2026-08-26



**Idea source:** 2026-08-26 Kitron/Wengrowicz short-horizon crypto mean reversion (2608.21888)  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 1, 'threshold': 0.02}`  
**Data source:** yfinance

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.379 | 0.074 | -0.5425 | 0.28 | 2045 |
| Test (out-of-sample, realistic costs) | -0.322 | -0.1343 | -0.4881 | 1.0 | 857 |
| Full sample (winner) | -0.178 | -0.2034 | -0.9521 | 0.011 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 1, 'threshold': 0.02}` | 0.379 | 0.074 | -0.5425 | 0.28 |
| 2 | `{'lookback': 2, 'threshold': 0.0}` | 0.348 | 0.0447 | -0.7866 | 0.25 |
| 3 | `{'lookback': 2, 'threshold': 0.02}` | 0.272 | 0.0194 | -0.7777 | 0.186 |
| 4 | `{'lookback': 3, 'threshold': 0.0}` | 0.241 | -0.0175 | -0.7858 | 0.165 |
| 5 | `{'lookback': 2, 'threshold': 0.05}` | 0.192 | 0.0072 | -0.5731 | 0.131 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=yfinance.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read — honest verdict

**Idea tested.** The tradable core of Kitron & Wengrowicz "Short-horizon mean reversion
in cryptocurrency markets" (2608.21888): *bet against the previous candle's direction*
— the paper's headline crypto result (90% of 183 Binance pairs show significant
directional reversal at **15-minute** horizons vs 2.7% of US equities; the edge is in
**signs, not magnitudes**). The `lag1_reversal` strategy is exactly this rule
(`pos = −sign(past move)`, with an optional magnitude band). Winner: `lookback=1,
threshold=0.02` — "fade yesterday's daily candle when it moved > 2%."

**Why ETH-USD, and why this is not a re-run.** All 11 prior backtests in this repo are
BTC-USD; `lag1_reversal` was already REJECTED on BTC (2026-07-01, Portnaya thread).
2608.21888's distinctive claim is **cross-market pervasiveness** (the effect holds "in
every focal coin-year," across 183 pairs). The faithful new test is therefore a
**second, fresh coin** — the first non-BTC series this repo has run. Real Yahoo data
(2922 daily bars, 2018-08-26 → 2026-08-26), no synthetic.

**Result — REJECT.** Train Sharpe **0.379** (weak even in-sample; weaker than BTC's
grid), CAGR 7.4% → **OOS Sharpe −0.322, CAGR −13.4%**, full-sample deflated-SR **0.011**
(fails hard). The pure lag-1 sign-fade (`threshold=0`) is not even the grid winner — a
magnitude band helps slightly, echoing Portnaya's "the bounce is magnitude, not sign."

**What it means.** The strong 15-min crypto reversal **aggregates away by the daily
close on ETH, exactly as it did on BTC.** This does **not falsify** Kitron & Wengrowicz —
they explicitly locate the signal at 15-min and call it marginal (~1.3 bps/trade) even
there after 5 bps costs; a daily bar is the wrong frequency and the null is the
*predicted* outcome. What is newly established: the daily-crypto reversal null now
**generalizes across coins**, not just BTC. Single-series *daily* crypto is definitively
tapped out on the direction/reversal axis — **13th straight daily-crypto reject.**

**Next step.** The unblocked version of this exact idea is (a) a **15-min/hourly** bar
feed and (b) a **multi-coin cross-section** (fade the coins that rose most, buy those
that fell most, dollar-neutral) — the same intraday multi-asset feed the Choi / MINGLE /
MFCCA / Halperin / Aste cross-sectional thread has been blocked on. Do **not** advance
the daily single-series form. Infra priority: an hourly multi-coin OHLCV loader.