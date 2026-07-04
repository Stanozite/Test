# Backtest Report — trend_filter on BTC-USD — 2026-07-04



**Idea source:** 2026-07-04 trend-thread capstone: Kurth/Bouchaud 2607.01550 short-term trend dead — test long-only long-horizon complement  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'lookback': 60}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.918 | 0.3254 | -0.5981 | 0.924 | 2045 |
| Test (out-of-sample, realistic costs) | 0.093 | -0.004 | -0.3422 | 1.0 | 857 |
| Full sample (winner) | 0.864 | 0.278 | -0.6042 | 0.962 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 60}` | 0.918 | 0.3254 | -0.5981 | 0.924 |
| 2 | `{'lookback': 120}` | 0.918 | 0.3267 | -0.5862 | 0.924 |
| 3 | `{'lookback': 250}` | 0.857 | 0.3134 | -0.5306 | 0.896 |
| 4 | `{'lookback': 90}` | 0.659 | 0.2007 | -0.6199 | 0.747 |
| 5 | `{'lookback': 180}` | 0.596 | 0.1704 | -0.65 | 0.694 |

## Notes & caveats
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=5 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human verdict — MIXED (leans REJECT on alpha; the only survivor is drawdown mitigation)

This was the **capstone** of the BTC trend thread. Five prior tests
(`tsmom`, `donchian_breakout`, `cost_aware_momentum`, `lag1_reversal`, `ma_crossover`)
all REJECTED directional trend/reversal on BTC. The two recurring diagnoses were
(a) the long/short **short leg bleeds** against BTC's structural up-drift, and
(b) Kurth/Eisler/Rej/Bouchaud (2607.01550) show **short-term** trend is dead on
small effective-tick assets. So this test applied both implied fixes at once:
**drop the short leg** (long-or-flat) and **go slow** (60–250d lookbacks) — the
horizon band the paper does *not* indict.

**It still does not produce an out-of-sample timing edge.** Train Sharpe 0.918
(lookback 60) collapses to **OOS Sharpe 0.093 with CAGR −0.4%** — flat, same
signature as every prior trend test. The in-sample edge is BTC's up-drift showing
through a long-biased position, not timing skill.

The one honest nuance vs the pure-REJECTs: benchmarked against **BTC buy-and-hold**
over the full 2018→2026 span (CAGR 0.325 · Sharpe 0.769 · MaxDD −76.6%), the
long-only long-horizon filter full-sample delivers **CAGR 0.278 · Sharpe 0.864 ·
MaxDD −60.4%** — i.e. it **cuts max drawdown by ~16pp and lifts Sharpe modestly by
sitting out crashes, while giving up ~5pp of CAGR**. That is the classic
"trend-following as crash insurance" property (cf. risk-managed momentum,
Baltussen et al.), *not* alpha. And even that risk benefit is a full-sample
statement — the OOS split shows no dependable edge of any kind.

**Do not advance as a return strategy.** The BTC trend thread is now closed across
six tests: there is no reliable OOS *return* edge from trend or reversal on daily
BTC; the only defensible use of a slow long-only trend filter is **defensive
drawdown reduction**, and that should be validated on its own terms (e.g. vs a
vol-target overlay) rather than sold as alpha. Turnover is low (slow signal), so
costs are not the binding constraint here — the absence of an OOS signal is.