# Backtest Report — cost_aware_momentum on BTC-USD — 2026-06-30



**Idea source:** 2026-06-30 "Cost-aware execution filter (Bysik/Slepaczuk 2606.00060)"  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 20, 'threshold': 0.05}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.808 | 0.2459 | -0.5652 | 0.786 | 2045 |
| Test (out-of-sample, realistic costs) | -0.533 | -0.1206 | -0.4202 | 1.0 | 857 |
| Full sample (winner) | 0.628 | 0.1587 | -0.5135 | 0.735 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 20, 'threshold': 0.05}` | 0.808 | 0.2459 | -0.5652 | 0.786 |
| 2 | `{'lookback': 20, 'threshold': 0.0}` | 0.775 | 0.2519 | -0.6669 | 0.757 |
| 3 | `{'lookback': 20, 'threshold': 0.02}` | 0.766 | 0.2405 | -0.6446 | 0.749 |
| 4 | `{'lookback': 10, 'threshold': 0.0}` | 0.667 | 0.2027 | -0.6605 | 0.65 |
| 5 | `{'lookback': 5, 'threshold': 0.05}` | 0.598 | 0.1462 | -0.2928 | 0.574 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=9 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human verdict (2026-06-30) — REJECT, but the *mechanism* tested clean

**What was tested.** Bysik & Słepaczuk ([2606.00060](https://arxiv.org/abs/2606.00060))
claim the crypto bottleneck is execution, not prediction: a filter that only trades
when the forecast magnitude clears a transaction-cost threshold rescues an
otherwise cost-killed signal. I replicated the *mechanism* with the simplest honest
proxy — a daily lookback-return standing in for their ML forecast, long-only when
momentum clears a threshold band — on 5y real BTC-USD (cached, not synthetic).

**Result.** No edge. Train winner (lookback=20, threshold=0.05) posts Sharpe 0.808
in-sample but **−0.533 out-of-sample** with a −42% drawdown, and the full grid fails
the deflated-Sharpe gate (0.74–0.79 < 0.95). This is a textbook overfit-to-grid
pattern — not a tradable strategy.

**What the threshold filter actually did.** Comparing the three threshold levels at
lookback=20 isolates the paper's mechanism cleanly:

| threshold | Train Sharpe | Train MaxDD |
| --- | --- | --- |
| 0.00 (no filter) | 0.775 | −66.7% |
| 0.02 | 0.766 | −64.5% |
| 0.05 | 0.808 | −56.5% |

The cost-band filter did roughly what the paper says — it **cut tail drawdown by ~10pp
and nudged risk-adjusted return up** by suppressing low-edge entries. So the *idea* is
not refuted. What's refuted is the *underlying signal*: a naive daily momentum proxy
has no out-of-sample predictive power, and no execution filter can rescue a signal
that isn't there. The paper's >65%/Sharpe-1.0 result came from an **ML forecast on
hourly bars** — the filter was the polish, not the alpha.

**Honest next step:** shelve this daily proxy. To fairly test the paper, the filter
needs (a) a signal with genuine OOS edge underneath it, and (b) hourly bars where
turnover/cost trade-offs actually bite. Until we wire in a real predicted-return
series, this is a clean negative: mechanism plausible, proxy signal empty. Do not
advance.