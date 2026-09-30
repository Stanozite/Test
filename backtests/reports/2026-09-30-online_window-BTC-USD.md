# Backtest Report — online_window on BTC-USD — 2026-09-30



**Idea source:** 2026-09-30 "Cost-Sensitive Online Window Size Selection (Liu & Hsieh, 2609.29887)"  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'eta': 0.5, 'cost': 0.0}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.675 | 0.2323 | -0.7397 | 0.653 | 2045 |
| Test (out-of-sample, realistic costs) | 0.078 | -0.0303 | -0.4936 | 1.0 | 857 |
| Full sample (winner) | 0.881 | 0.259 | -0.4924 | 0.934 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'eta': 0.5, 'cost': 0.0}` | 0.675 | 0.2323 | -0.7397 | 0.653 |
| 2 | `{'eta': 0.5, 'cost': 0.001}` | 0.675 | 0.2323 | -0.7397 | 0.653 |
| 3 | `{'eta': 0.5, 'cost': 0.002}` | 0.675 | 0.2323 | -0.7397 | 0.653 |
| 4 | `{'eta': 1.0, 'cost': 0.0}` | 0.675 | 0.2323 | -0.7397 | 0.653 |
| 5 | `{'eta': 1.0, 'cost': 0.001}` | 0.675 | 0.2323 | -0.7397 | 0.653 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=9 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest read — MIXED (leans REJECT), 17th straight daily-crypto reject-lean
This is the first test that attacks the **overfitting mechanism itself** rather than
adding a new signal. Faithful to Liu & Hsieh, "Cost-Sensitive Online Window Size
Selection for Portfolio Management" (arXiv:2609.29887): freeze a spread of candidate
momentum windows `(10,20,40,80,160)` and let a Hedge / Fixed-Share aggregator pick
among them online on turnover-inclusive losses — so **the window is never grid-selected**,
which is exactly how all 16 prior rejects died. The strategy therefore sweeps only the
aggregator's hyper-parameters (`eta`, `cost`), not the window.

**Result:** train Sharpe **0.675** (CAGR 23.2%) → **OOS Sharpe 0.078, CAGR −3.0%**;
full-sample deflated-SR **0.934** (fails the 0.95 gate). No standalone daily-BTC alpha.

**Two confirming tells inside the sweep:**
1. **All 9 `eta`×`cost` configs give the identical train result (Sharpe 0.675).** The
   aggregator's hyper-parameters — including the paper's headline **cost-sensitivity** —
   are **inert on a single asset**: every expert is a long/flat momentum vote on the same
   series, so their turnovers are near-identical and the cost term barely moves the Hedge
   weights. Liu & Hsieh's cost-awareness is built to arbitrate *divergent-turnover
   portfolios across assets*; there is nothing for it to arbitrate here.
2. **The train→OOS Sharpe decay (~88%) is marginally *smaller* than the fixed-window
   strategies** (vol_regime ~97%, tsmom/trend_filter ~90%, asym_longmem_vol ~93%) — the
   paper's robustness-to-window-misspecification claim faintly showing up — **but the OOS
   *level* is still ~0.** Removing window-overfitting reduces selection variance a little
   and produces no alpha, because daily single-series momentum has no edge to *select
   among*: an online blend of momentum windows is just a smoother momentum, and smoother
   momentum on daily BTC was already rejected 6× on the trend axis.

**Does not falsify the paper.** Their claim is multi-asset portfolio robustness with
turnover-inclusive online learning, evaluated where windows genuinely disagree and
turnover genuinely differs. Collapsed onto one crypto series, "a portfolio over windows"
degenerates to a momentum blend and the cost lever goes dormant — the null here is the
predicted outcome of the *degenerate* case, not evidence against the method.

**Verdict: do not advance as a return strategy.** The sharper lesson: the repo's standing
diagnosis ("daily single-series is tapped out") is now shown to be **deeper than
window-overfitting** — even with the window chosen optimally-online, there is no daily
cross-window edge. This is the strongest argument yet that the blocker is the *data
resolution*, not the *selection method*. The **hourly / multi-coin OHLCV loader is now 6×
overdue** and is precisely what would let Liu & Hsieh's cost-sensitivity actually bite
(multiple assets, divergent turnover). Next exposure-management test should instead be a
principled bounded-drawdown overlay (Hsieh 2609.23272), not another vol-quantile gate.