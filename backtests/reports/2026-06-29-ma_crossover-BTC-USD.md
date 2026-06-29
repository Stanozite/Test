# Backtest Report — ma_crossover on BTC-USD — 2026-06-29



**Idea source:** 2026-06-29 / CryptoGAT (arXiv:2606.27670) — temporal trend baseline on crypto  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'fast': 10, 'slow': 100}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.97 | 0.365 | -0.5745 | 0.894 | 2045 |
| Test (out-of-sample, realistic costs) | 0.11 | -0.0001 | -0.3705 | 1.0 | 857 |
| Full sample (winner) | 0.809 | 0.2601 | -0.6054 | 0.896 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'fast': 10, 'slow': 100}` | 0.97 | 0.365 | -0.5745 | 0.894 |
| 2 | `{'fast': 20, 'slow': 100}` | 0.917 | 0.3345 | -0.5619 | 0.866 |
| 3 | `{'fast': 20, 'slow': 50}` | 0.89 | 0.3068 | -0.5545 | 0.862 |
| 4 | `{'fast': 10, 'slow': 50}` | 0.884 | 0.3026 | -0.5791 | 0.857 |
| 5 | `{'fast': 10, 'slow': 200}` | 0.836 | 0.283 | -0.55 | 0.823 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=8 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest verdict (human read) — 2026-06-29

**Why this idea:** CryptoGAT (arXiv:2606.27670) argues that *temporal* models (LSTM/GRU/Transformer) fail on crypto and that cross-asset structure is the real signal. We can't reproduce a GAT in this engine, but we *can* falsify the weaker corollary: does a plain temporal trend rule (MA crossover) carry a real edge on BTC after costs and out-of-sample? If it collapses, that is evidence consistent with the paper's thesis.

**What happened:** Train Sharpe ≈ **0.97** collapses to OOS Sharpe ≈ **0.11**, with OOS CAGR ≈ **0%** and a **−37%** max drawdown. The full-sample winner fails the deflated-Sharpe gate (0.896 < 0.95), so the in-sample number is not convincingly better than grid-search luck.

**Benchmark (the honest comparison):** over the same OOS window (2024-02-23 → 2026-06-29), **buy-and-hold BTC returned +16.6%** (CAGR 4.6%, Sharpe **0.31**, MaxDD −52.6%). The MA crossover delivered ~0% return at Sharpe 0.11 — it **underperformed simply holding BTC on both return and risk-adjusted return**, beating it only on max drawdown (−37% vs −53%) by sitting in cash through part of the chop.

**Conclusion:** REJECT/MIXED-leaning-REJECT. The naive temporal trend rule has no durable, cost-surviving edge on BTC out-of-sample — directly consistent with CryptoGAT's claim that the time-axis is the wrong frame for crypto. The drawdown reduction is the only redeeming property and is not worth the foregone upside.

**Next step:** The interesting, untested variant is Angelini's (arXiv:2606.27932) Grünwald–Letnikov Hurst regime switch — gate the MA crossover to trade *only* when H>0.5 (persistent/trending regime). That is the natural follow-up backtest; it needs a Hurst-estimator strategy module, out of scope for this run.

### Harness fix applied this run
The first run produced a **flat OOS curve (Sharpe/CAGR/MaxDD all 0.0, zero fills)** — a bug, not a result. Cause: backtrader truncates order size to whole units, so a $10k account cannot afford even one ~$50k BTC unit → every order rounded to size 0 and never filled. Fixed in `engine/run_backtrader.py` by scaling starting cash to `max(10k, max_price × 10k)` so ≥10k whole units are always affordable (truncation error <0.01%; metrics are ratio-based, so the cash level does not bias them). Re-ran after the fix; numbers above are post-fix.