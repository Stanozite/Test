# Backtest Report — multiscale_move on BTC-USD — 2026-09-02



**Idea source:** 2026-09-02 Yousefnezhad et al Multi-Scale TCN Profit-Optimized Thresholds (2608.26174)  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'maxh': 10, 'threshold': 0.0}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.731 | 0.2286 | -0.6579 | 0.665 | 2045 |
| Test (out-of-sample, realistic costs) | 0.122 | -0.001 | -0.362 | 1.0 | 857 |
| Full sample (winner) | 0.525 | 0.1307 | -0.6465 | 0.55 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'maxh': 10, 'threshold': 0.0}` | 0.731 | 0.2286 | -0.6579 | 0.665 |
| 2 | `{'maxh': 7, 'threshold': 0.01}` | 0.723 | 0.2161 | -0.5427 | 0.656 |
| 3 | `{'maxh': 10, 'threshold': 0.01}` | 0.705 | 0.2103 | -0.7038 | 0.636 |
| 4 | `{'maxh': 4, 'threshold': 0.0}` | 0.636 | 0.1842 | -0.6658 | 0.559 |
| 5 | `{'maxh': 7, 'threshold': 0.02}` | 0.635 | 0.1678 | -0.4995 | 0.558 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read (honest verdict) — MIXED, leans REJECT

Tests the tradable core of **Yousefnezhad, Mansourfar & Feizi Derakhshi, "Forecasting
Economically Significant Bitcoin Moves: A Multi-Scale TCN with Profit-Optimized
Thresholds"** (arXiv:2608.26174): predict whether BTC rises >5% within 7 days by fusing
dilated 1–4-day features, then apply a **profit-optimized decision threshold** to turn the
score into trades (AUC 0.6316, "profit 1.703" vs 5 baselines). Their headline contribution
is the *threshold*; their inputs are on-chain + market + sentiment through an InceptionTCN.
`multiscale_move` keeps the two pieces we can honestly build from price alone — the
**multi-scale momentum fusion** (mean past-only return over horizons 1..maxh) and the
**profit threshold** (long only when the fused up-signal clears it) — and lets the sweep pick
the threshold, which is exactly what "profit-optimized" means. Real cached BTC-USD (2922
bars, 2018→2026, no synthetic).

**The paper's own headline mechanism optimizes itself away.** The stage-1 winner is
`maxh=10, threshold=0.0` — the profit threshold that is the paper's central contribution is
driven to **zero**; the magnitude gate adds nothing on daily BTC, and every non-zero
threshold ranks *below* it (the whole `threshold` column is monotone-worse than 0.0 at the
long horizons). What's left is just "hold a slow multi-scale trend, flat when it turns
negative." That slow-trend core then does what all 13 prior daily-crypto tests did:
train Sharpe **0.731** → **OOS Sharpe 0.122, CAGR −0.1%** (no return edge — indistinguishable
from zero), and it **fails deflated-SR** (0.665 train / 0.55 full; the OOS 1.0 is vacuous at
Sharpe ≈ 0). The one non-null signature is again **crash insurance, not alpha**: OOS MaxDD
**−36%** vs BTC buy-and-hold ~−77%, because sitting out negative-momentum stretches caps the
tail — the same consolation `trend_filter` / `vol_regime` / `halving_clock` gave, and the
same reason not to advance it as a return strategy.

**Does this falsify the paper? No.** Their edge (AUC 0.63, profit 1.703) rests on *on-chain +
sentiment features* and a *classification-AUC objective with a ranking loss*, none of which a
price-only daily long/flat can reach; a threshold on price momentum alone is not their model.
The honest reading is narrower and still useful: **the price-momentum component of a
"multi-scale + profit-threshold" recipe carries no standalone daily BTC edge, and the
profit-optimized threshold collapses to zero on price-only inputs** — so whatever edge
2608.26174 has must come from the non-price features, not the multi-scale price geometry.
This echoes `cost_aware_momentum` (2026-06-30) and Portnaya's "magnitude is not the edge."

**14th consecutive daily-crypto single-series reject-lean.** Direction · reversal · trend ·
vol-target · calendar · early-warning · tail-measure · and now profit-threshold-gated
multi-scale momentum are all exhausted on a single daily series. The blocked frontier is
unchanged: **multi-coin cross-section + intraday bars**. Note two data-native unlocks that
now sit in the repo — both `BTC-USD_1d.csv` and `ETH-USD_1d.csv` are cached, so a **BTC/ETH
relative-value (pair) test** is buildable without new data; and 2608.26158 (tick- vs
minute-bars) + 2608.29025 (hourly BTC-options hedging) both point at the hourly loader as the
real next infra step.