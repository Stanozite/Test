# Backtest Report — vol_regime on BTC-USD — 2026-07-29



**Idea source:** 2026-07-29 Lee/Rachev/Fabozzi 2607.16450 — heavy tails & asymmetric vol → vol-regime overlay  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'lookback': 10, 'q': 0.5, 'window': 252}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.773 | 0.2269 | -0.7085 | 0.637 | 2045 |
| Test (out-of-sample, realistic costs) | 0.025 | -0.0226 | -0.3135 | 1.0 | 857 |
| Full sample (winner) | 0.653 | 0.1681 | -0.6277 | 0.645 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 10, 'q': 0.5, 'window': 252}` | 0.773 | 0.2269 | -0.7085 | 0.637 |
| 2 | `{'lookback': 10, 'q': 0.6, 'window': 504}` | 0.74 | 0.2275 | -0.7302 | 0.6 |
| 3 | `{'lookback': 10, 'q': 0.6, 'window': 252}` | 0.641 | 0.1843 | -0.6682 | 0.488 |
| 4 | `{'lookback': 10, 'q': 0.5, 'window': 504}` | 0.629 | 0.1685 | -0.7347 | 0.475 |
| 5 | `{'lookback': 30, 'q': 0.6, 'window': 504}` | 0.535 | 0.1385 | -0.7435 | 0.374 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest read (human)
**Verdict: MIXED — leans REJECT.** The strategy's own falsifiable prediction was: a
vol-regime filter should behave as *crash insurance* (cut drawdown, maybe nudge Sharpe)
but **not** add raw return and **not** clear the deflated-SR gate OOS. That is exactly
what happened — the prediction was **not** falsified.

- **No return edge OOS.** Train Sharpe 0.773 → **OOS 0.025** (CAGR **−2.3%**). The
  in-sample "edge" is grid-selection luck: the winner is the fastest vol window
  (`lookback=10`) at the median cutoff (`q=0.5`), and it doesn't carry OOS. Same
  signature as `trend_filter`, `tsmom`, `donchian` — an in-sample plateau that
  collapses to ~0 out-of-sample.
- **Drawdown *is* cut.** OOS MaxDD **−31.4%** vs the winner's full-sample −62.8% and
  BTC buy-and-hold's ~−77%. So the overlay does what a vol filter is supposed to do —
  it sidesteps the storms — but that is risk reduction, not alpha, and you pay for it
  in CAGR (negative OOS).
- **Fails the gate.** Deflated-SR **0.637 train / 0.645 full**, both well below 0.95.
  The "1.0" on the Test row is *vacuous* — with a single winning config re-run on the
  test split there is no multiple-testing penalty to deflate, and Sharpe is ~0 anyway
  (same footnote as the 07-04 / 07-15 reports). The honest gate reads off train/full: **fails**.

**Thread status.** This is the **first test of the vol-target-overlay axis** the thread
has pointed at since 07-04 ("move OFF direction/trend, onto exposure management"). Result:
that axis reads **crash-insurance-not-alpha**, identical to the trend axis it replaced.
Counting it as the **8th consecutive daily single-series BTC reject-lean**. The
"daily BTC single-series is tapped out" thesis stands — a passing OOS gate here would have
falsified it, and it didn't.

**Do not advance** as a return strategy. If drawdown control is the goal, this is a
usable overlay, but it is not the alpha we're hunting. **Next axis: cross-sectional
crypto** (BTC/ETH — and alts — long/short, market-neutral), per this run's AlphaZeroBeta
(2607.18001) and the market-neutral framing. Single-series daily is exhausted across
both direction *and* exposure management.