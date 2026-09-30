# Backtest Report — pairs_meanrev on BTCETH-RATIO — 2026-09-23



**Idea source:** 2026-09-23 "Adapting Pairs Trading (OU mean-reversion) — 2609.22639"  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 90, 'entry': 1.0}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | -0.001 | -0.0268 | -0.5809 | 0.048 | 2004 |
| Test (out-of-sample, realistic costs) | -0.555 | -0.073 | -0.3504 | 1.0 | 840 |
| Full sample (winner) | -0.478 | -0.1693 | -0.8977 | 0.001 | 2864 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 90, 'entry': 1.0}` | -0.001 | -0.0268 | -0.5809 | 0.048 |
| 2 | `{'lookback': 90, 'entry': 1.5}` | -0.046 | -0.0267 | -0.5706 | 0.037 |
| 3 | `{'lookback': 20, 'entry': 2.0}` | -0.144 | -0.0207 | -0.2963 | 0.019 |
| 4 | `{'lookback': 60, 'entry': 1.0}` | -0.153 | -0.0604 | -0.6656 | 0.018 |
| 5 | `{'lookback': 40, 'entry': 1.0}` | -0.27 | -0.0858 | -0.6953 | 0.008 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.