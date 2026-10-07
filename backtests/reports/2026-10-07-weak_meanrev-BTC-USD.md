# Backtest Report — weak_meanrev on BTC-USD — 2026-10-07



**Idea source:** 2026-10-07 digest / Hoffmann & Rasonyi 'Exponential investors with weakly mean-reverting prices' (2610.08631)  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 120, 'entry': 1.0, 'longflat': False}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.177 | 0.0109 | -0.5 | 0.088 | 2045 |
| Test (out-of-sample, realistic costs) | 0.019 | -0.0204 | -0.3678 | 1.0 | 857 |
| Full sample (winner) | -0.551 | -0.2632 | -0.9758 | 0.0 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 120, 'entry': 1.0, 'longflat': False}` | 0.177 | 0.0109 | -0.5 | 0.088 |
| 2 | `{'lookback': 120, 'entry': 1.0, 'longflat': True}` | 0.177 | 0.0109 | -0.5 | 0.088 |
| 3 | `{'lookback': 120, 'entry': 0.5, 'longflat': False}` | 0.162 | -0.0003 | -0.5194 | 0.081 |
| 4 | `{'lookback': 120, 'entry': 0.5, 'longflat': True}` | 0.162 | -0.0003 | -0.5194 | 0.081 |
| 5 | `{'lookback': 30, 'entry': 1.0, 'longflat': False}` | 0.134 | -0.0102 | -0.4915 | 0.072 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Human read (2026-10-07)
Anchored to **Hoffmann & Rasonyi, "Exponential investors with weakly mean-reverting
prices" (arXiv:2610.08631, 6 Oct 2026)** — for an exponential-utility investor in a
*weakly* (sublinear) mean-reverting price with nonzero drift, an explicit
asymptotically optimal strategy exists, driven by the current gap to the
mean-reverting level. `weak_meanrev` is the honest single-asset daily analogue:
lean against the standardized deviation of log-price from a slow rolling mean (long
when stretched cheap, short/flat when rich), with the 18-combo sweep standing in
for parameter estimation. This is the deliberate **level sibling** of the two
reversion tests already rejected — `lag1_reversal` (horizon-1 fade, 07-01 BTC /
08-26 ETH) and `pairs_meanrev` (BTC/ETH-ratio z-score, 09-23) — filling the last
gap on the mean-reversion axis: a *single asset's own level*.

**REJECT, and a cleaner one than the recent MIXED-leans.** Unlike every prior test
that at least posted a strong grid-selected in-sample Sharpe (~1.0) before
collapsing OOS, here **there is no in-sample edge to collapse**: the best of 18
configs is train Sharpe **0.177** (CAGR +1.1%), the whole grid barely clears zero →
**OOS Sharpe 0.019, CAGR −2.0%**, full-sample Sharpe **−0.551** (deflated-SR 0.0).
Two confirming tells: (1) the stage-1 winner is `lookback=120`, the **longest**
equilibrium window in the grid, and the signal only weakens as the mean gets faster
— there is no window at which BTC's deviation from its own slow mean reverts
profitably; (2) `longflat` True≡False in-sample (ranks 1&2, 3&4 identical) only
because the short leg rarely fires on the lower-priced train era, yet on the full
sample the short leg is **ruinous** (MaxDD **−97.6%**, CAGR −26.3%) — shorting the
top of a strongly up-drifting asset bleeds exactly as it did in `tsmom`/`lag1`.

This **confirms, does not falsify**, Hoffmann & Rasonyi: their edge presupposes a
genuinely (weakly) mean-reverting price; a single trending crypto has strong
positive drift and is non-stationary at the *level*, so the OU-gap premise simply
does not hold for daily BTC. **The mean-reversion axis is now exhausted on daily
crypto from all three angles — horizon-1 (`lag1`), cross-sectional/ratio
(`pairs`), and single-asset level (`weak_meanrev`).** 18th straight daily-crypto
reject-lean (following `online_window` = 17th, 2026-09-30). The standing unblock is
unchanged and now 7× overdue: an **hourly / multi-coin OHLCV loader** — the only
resolution at which any crypto reversion signal (Kitron-Wengrowicz 15-min, the
MintEval / MoE-execution BTCUSDT-15min work this very window) actually lives.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.