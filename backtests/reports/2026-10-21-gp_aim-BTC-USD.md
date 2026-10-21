# Backtest Report — gp_aim on BTC-USD — 2026-10-21



**Idea source:** 2026-10-21 Smerlak "Optimal Trading Filters and the Value of Predictive Signals" (2610.24558)  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'span': 40, 'phi': 0.1, 'longflat': False}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 1.093 | 0.4257 | -0.4282 | 0.898 | 2045 |
| Test (out-of-sample, realistic costs) | 0.404 | 0.0757 | -0.3943 | 1.0 | 857 |
| Full sample (winner) | 0.656 | 0.0559 | -0.1248 | 0.648 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'span': 40, 'phi': 0.1, 'longflat': False}` | 1.093 | 0.4257 | -0.4282 | 0.898 |
| 2 | `{'span': 20, 'phi': 0.1, 'longflat': False}` | 1.025 | 0.3872 | -0.5506 | 0.859 |
| 3 | `{'span': 10, 'phi': 0.1, 'longflat': False}` | 1.014 | 0.3789 | -0.6085 | 0.852 |
| 4 | `{'span': 40, 'phi': 1.0, 'longflat': True}` | 0.942 | 0.3378 | -0.6132 | 0.799 |
| 5 | `{'span': 40, 'phi': 1.0, 'longflat': False}` | 0.942 | 0.3378 | -0.6132 | 0.799 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read (honest verdict) — 2026-10-21

**MIXED — the strongest OOS in 19 runs and the first test to *confirm a paper's mechanism in-sample*, but still not standalone alpha, and it does not beat buy-and-hold.** The 19th straight daily-crypto test, but a different flavour from the 18 reject-leans.

**What this tests.** Smerlak "Optimal Trading Filters and the Value of Predictive Signals" (2610.24558) solves the stationary quadratic trading problem with transient impact by Wiener-Hopf factorization: the optimal policy is a forecast followed by an explicit causal *linear filter*, and under exponential impact-resilience it is the Garleanu-Pedersen aim-portfolio (partial adjustment toward a shrunk Markowitz target, trade rate `phi`). Unlike every prior test, which added a *signal*, this attacks the next overfit knob after `online_window`'s attack on window-selection: the *threshold/filter* that turns a forecast into a position. `phi=1.0` is naive full-chase (the control); `phi<1` is the optimal low-pass filter.

**The one genuinely new result — the paper's mechanism shows up in the data.** The stage-1 top three are **all `phi=0.1`** (train Sharpe 1.093 / 1.025 / 1.014), beating the `phi=1.0` un-filtered controls at ranks 4–5 (0.942). So the optimal low-pass filter **does** add value over naive full-chase — by ~0.15 Sharpe and, more tellingly, by collapsing turnover (~6× less in the ponytail) and drawdown (winner full-sample MaxDD **−12.5%** vs BTC B&H −76.6%). This is the **first time a backtest here has confirmed, rather than merely failed-to-falsify, the anchored paper's central claim.**

**Why it is still not alpha, and does not advance.** Two hard checks say hold:
1. **Fails deflated-SR** (train 0.898, full 0.648 — both < 0.95). The OOS 1.0 is vacuous (single-config validation, no multiple-comparison penalty), per the standing caveat.
2. **It does not beat buy-and-hold.** Reconciled by direct computation on the same cached series: BTC B&H full-sample **Sharpe 0.769, CAGR 32.5%, MaxDD −76.6%**. The gp_aim winner is **Sharpe 0.656 (below B&H), CAGR 5.6% (gives up ~27 pts of return), MaxDD −12.5%**. Risk-adjusted it trails passive; the only thing it wins is drawdown.

**The honest synthesis — and it is Smerlak's own thesis.** The optimal filter governs the *value of a signal under costs*; it does not *manufacture* a signal. On daily BTC there is no persistent return forecast to filter, so the GP/Smerlak filter at `phi=0.1` just holds a small, smooth, vol-normalized long — a de-risked slice of the up-drift with far less drawdown and far less return. The positive OOS 0.404 is real and is the best in recent memory, but it is the Sharpe of *low-exposure smoothing*, not of extracted alpha, and it still underperforms simply holding BTC. **Confirms, does not falsify, Smerlak** (his claim is about optimal implementation, which held); it does **not** falsify "daily BTC single-series is tapped out for alpha" — it sharpens it: even the *mathematically optimal* cost-aware filter finds no daily return signal worth trading, only a better way to dial exposure. 19th straight daily-crypto non-advance; the blocker remains data **resolution** (hourly/multi-coin), now ~8× overdue — the filter would actually bite where a signal with real short-horizon persistence exists.

**Next step:** do **not** advance gp_aim as a return strategy. Shelve the filter until there is a signal worth filtering — i.e. after the hourly/multi-coin loader unblocks the intraday frontier where short-horizon persistence (Kitron-Wengrowicz 15-min reversal, quarter-hour effects) actually lives. The GP/Smerlak filter is the right *implementation* layer to carry forward onto that feed.