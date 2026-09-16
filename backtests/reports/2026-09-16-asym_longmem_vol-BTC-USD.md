# Backtest Report — asym_longmem_vol on BTC-USD — 2026-09-16



**Idea source:** 2026-09-16 Kayaki & Lee ALM-GARCH (arXiv:2609.06422)  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'gamma': 2.0, 'alpha': 1.5, 'q': 0.6, 'lags': 90, 'window': 252}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 1.026 | 0.4056 | -0.6275 | 0.85 | 2045 |
| Test (out-of-sample, realistic costs) | 0.069 | -0.0088 | -0.3395 | 1.0 | 857 |
| Full sample (winner) | 0.496 | 0.1224 | -0.7496 | 0.435 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'gamma': 2.0, 'alpha': 1.5, 'q': 0.6, 'lags': 90, 'window': 252}` | 1.026 | 0.4056 | -0.6275 | 0.85 |
| 2 | `{'gamma': 1.0, 'alpha': 1.5, 'q': 0.5, 'lags': 90, 'window': 252}` | 0.977 | 0.348 | -0.5567 | 0.814 |
| 3 | `{'gamma': 1.0, 'alpha': 1.5, 'q': 0.6, 'lags': 90, 'window': 252}` | 0.92 | 0.3386 | -0.682 | 0.772 |
| 4 | `{'gamma': 2.0, 'alpha': 1.0, 'q': 0.6, 'lags': 90, 'window': 252}` | 0.885 | 0.3175 | -0.6712 | 0.741 |
| 5 | `{'gamma': 1.0, 'alpha': 1.0, 'q': 0.5, 'lags': 90, 'window': 252}` | 0.848 | 0.2804 | -0.7238 | 0.706 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest read — MIXED, leans REJECT (16th straight daily-crypto reject-lean)

**What this tested.** The tradable daily analogue of Kayaki & Lee's ALM-GARCH
(arXiv:2609.06422): the same self-adapting long/flat regime gate as `vol_regime` and
`evar_regime`, with **only the volatility statistic swapped** for the paper's two
channels — a sign-asymmetric shock (level channel, `gamma`) fed through a power-law
long-memory kernel (memory channel, `alpha`). `gamma=1.0` is the built-in symmetric
control; small `alpha` is long memory.

**Verdict: no tradable edge on single-series daily BTC.** Train Sharpe 1.026 →
**OOS Sharpe 0.069, OOS CAGR −0.88%**; full-sample deflated-SR **0.435** (hard fail of
the 0.95 gate). The in-sample number is grid-selection, not signal.

**Two confirming tells, both inside the sweep:**
1. **The asymmetry buys ~nothing.** Rank-1 is `gamma=2.0` (Sharpe 1.026); ranks 2–3
   are `gamma=1.0` (symmetric) at 0.977 / 0.92 — a ~0.05 Sharpe gap in-sample that
   vanishes OOS. The "level channel" leverage asymmetry adds no *timing* value here.
2. **The long-memory component is the part with no edge.** The winner is `alpha=1.5`,
   the **shortest** memory in the grid; no long-memory (`alpha=0.5`) config reaches the
   top 5. Exactly last week's `volterra_signal` result mirrored onto variance: the
   genuinely long-memory piece is precisely the piece with no exploitable signal, and
   the best config collapses toward a plain short-window vol gate.

**Only surviving signature = crash insurance.** OOS MaxDD −34.0% vs BTC buy-&-hold
≈ −77% — the gate roughly halves drawdown, but at the cost of a flat return. Same
profile as `vol_regime` / `evar_regime`.

**Does NOT falsify the paper.** Kayaki & Lee's claim is about *variance-forecast fit*
(joint symmetry rejected; memory channel significant for BTC), and they themselves
report OOS forecasts only *match* benchmarks — they never claim a directional/timing
edge. A significant-but-non-tradable long-memory vol channel is fully consistent with
this null: persistence in *volatility* ≠ exploitable single-asset *timing* alpha.

**Where this leaves the thread.** The vol-statistic axis is now triple-exhausted on
daily single-series BTC — plain RV (`vol_regime`), coherent tail measure
(`evar_regime`), and now sign-asymmetric long-memory (`asym_longmem_vol`) all land in
the same crash-insurance-but-no-alpha basin. Combined with the 15 prior rejects across
direction/trend/calendar/tail/early-warning/profit-threshold/Volterra, the daily
single-series well is dry on every statistic tried. **The unblocking task is unchanged
and now five-times overdue: an hourly / multi-coin OHLCV loader** — every fresh
tradable crypto signal (Kitron-Wengrowicz 15-min reversal, Zhai on-chain identity,
Quarter-Hour effects, this window's order-flow-regime work) lives at intraday or
cross-sectional resolution the daily cache cannot reach.