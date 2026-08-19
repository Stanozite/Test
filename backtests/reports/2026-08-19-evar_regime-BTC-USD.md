# Backtest Report — evar_regime on BTC-USD — 2026-08-19



**Idea source:** 2026-08-19 Choi Entropic VaR tempered-stable (arXiv:2608.18022)  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'lookback': 60, 'alpha': 0.1, 'q': 0.6, 'window': 252}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.962 | 0.361 | -0.7021 | 0.848 | 2045 |
| Test (out-of-sample, realistic costs) | 0.032 | -0.0255 | -0.3903 | 1.0 | 857 |
| Full sample (winner) | 0.595 | 0.1624 | -0.7099 | 0.638 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 60, 'alpha': 0.1, 'q': 0.6, 'window': 252}` | 0.962 | 0.361 | -0.7021 | 0.848 |
| 2 | `{'lookback': 60, 'alpha': 0.05, 'q': 0.6, 'window': 252}` | 0.889 | 0.3238 | -0.7021 | 0.798 |
| 3 | `{'lookback': 60, 'alpha': 0.05, 'q': 0.5, 'window': 252}` | 0.835 | 0.2859 | -0.7279 | 0.753 |
| 4 | `{'lookback': 40, 'alpha': 0.05, 'q': 0.6, 'window': 252}` | 0.815 | 0.274 | -0.6874 | 0.745 |
| 5 | `{'lookback': 60, 'alpha': 0.1, 'q': 0.5, 'window': 252}` | 0.814 | 0.2733 | -0.7261 | 0.735 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.