# Backtest Report — tsmom on BTC-USD — 2026-07-02



**Idea source:** 2026-07-02 Pollok/Robik TSMOM benchmark (2607.00475)  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'lookback': 60}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.918 | 0.3254 | -0.5981 | 0.924 | 2045 |
| Test (out-of-sample, realistic costs) | 0.093 | -0.004 | -0.3422 | 1.0 | 857 |
| Full sample (winner) | 0.603 | 0.1947 | -0.6282 | 0.807 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 60}` | 0.918 | 0.3254 | -0.5981 | 0.924 |
| 2 | `{'lookback': 120}` | 0.918 | 0.3267 | -0.5862 | 0.924 |
| 3 | `{'lookback': 30}` | 0.909 | 0.3178 | -0.5785 | 0.92 |
| 4 | `{'lookback': 20}` | 0.775 | 0.2519 | -0.6669 | 0.848 |
| 5 | `{'lookback': 90}` | 0.659 | 0.2007 | -0.6199 | 0.747 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=5 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read (2026-07-02)
**Verdict: MIXED, leans REJECT — no reliable standalone edge on BTC.**

The idea under test: Pollok & Robik (arXiv:2607.00475) find learned differentiable-Sharpe
policies beat simple rules — equal-weight, risk-parity, **time-series momentum (TSMOM)** —
only *non-uniformly* on the 16 most liquid CME futures, and TSMOM is a hard-to-beat baseline
*there*. BTC-USD is outside their panel, so this asks: does the simple TSMOM rule carry
standalone OOS edge on crypto?

What the data says (real 8y BTC-USD, 2922 daily bars, purged/embargoed split):
- **In-sample it looks like a real trend asset.** Best lookback (60d) trains to Sharpe 0.92,
  CAGR 33%, and lookbacks 30/60/120 all cluster ~0.91 — the parameter *plateau* (not a single
  spiky winner) is the one genuinely encouraging sign: the in-sample trend signal isn't a knife-edge fit.
- **But it does not survive out-of-sample.** OOS Sharpe collapses to **0.093** with CAGR
  **−0.4%** — flat-to-slightly-negative after realistic costs. And it fails the deflated-SR gate
  even *in-sample* (0.924 < 0.95), so the ~0.9 train Sharpe is not convincingly better than luck
  once you penalise for testing 5 configs.
- **Why the long/short rule bleeds:** unlike the long-only momentum tested on 06-30, this is the
  canonical **long/short** TSMOM (sign of trailing return, both directions). In an asset with a
  strong secular up-drift, the *short* leg is the problem — being short BTC during recoveries
  gives back what the trend-following long leg earns. The in-sample window looked good largely
  because it spanned the 2022 bear (where shorts paid); the OOS window did not reward shorting.
- **Ignore the OOS "Deflated-SR 1.0":** on the test split only the single winning config is
  evaluated, so there is no multiple-testing penalty to deflate — with OOS Sharpe ≈ 0 that 1.0 is
  vacuous, not a pass.

**Conclusion.** Consistent with the paper's thesis, and with this repo's earlier momentum results
(cost_aware_momentum REJECT 06-30, ma_crossover MIXED-lean-REJECT 06-29): plain trend rules on
BTC are grid-overfit and regime-dependent, with the short leg a structural drag. TSMOM is a
"hard-to-beat baseline" in Pollok/Robik's futures panel but has **no dependable standalone edge on
BTC net of costs and out-of-sample**. Not worth advancing as-is. If revisited, the only defensible
variants are (a) **long/flat** TSMOM (drop the short leg, since it's the drag) benchmarked honestly
against buy-and-hold, or (b) a vol-scaled / risk-parity position size rather than ±1 — but neither
is promised an edge by this test.