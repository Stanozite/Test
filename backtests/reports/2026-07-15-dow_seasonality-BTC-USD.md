# Backtest Report — dow_seasonality on BTC-USD — 2026-07-15



**Idea source:** 2026-07-15 "Quarter-Hour Effect / periodic algorithmic trading (Kim & Hansen 2607.09426)"  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'weeks': 52, 'mode': 'longflat'}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.323 | 0.0439 | -0.762 | 0.297 | 2045 |
| Test (out-of-sample, realistic costs) | -0.929 | -0.2386 | -0.7003 | 1.0 | 857 |
| Full sample (winner) | 0.388 | 0.079 | -0.7831 | 0.445 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'weeks': 52, 'mode': 'longflat'}` | 0.323 | 0.0439 | -0.762 | 0.297 |
| 2 | `{'weeks': 52, 'mode': 'longshort'}` | 0.323 | 0.0439 | -0.762 | 0.297 |
| 3 | `{'weeks': 26, 'mode': 'longflat'}` | 0.271 | 0.0269 | -0.6715 | 0.246 |
| 4 | `{'weeks': 26, 'mode': 'longshort'}` | 0.271 | 0.0269 | -0.6715 | 0.246 |
| 5 | `{'weeks': 13, 'mode': 'longflat'}` | 0.236 | 0.0058 | -0.7718 | 0.217 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=8 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read (2026-07-15)
**REJECT — confirmatory, and it moves the program OFF the trend axis** (the 2026-07-04 capstone said to). Kim & Hansen (2607.09426) show periodic algorithmic order flow creates *return predictability* in crypto — but at the quarter-hour / 5-min / 1-min clock, out to 4–12h. This tests the honest daily-pipeline analogue: does *any* calendar periodicity (day-of-week, the daily clock's equivalent of the intra-hour clock) survive on daily BTC closes? It does not. The best grid pick (52-week look-back, long-flat) earns a weak in-sample Sharpe 0.32 that inverts to **−0.93 OOS** (CAGR −24%), and fails the deflated-SR gate (0.30). This is the 7th consecutive daily BTC signal to die out-of-sample here.

Two honest caveats on *interpretation*, not on the verdict:
- **This is not a faithful replication of Kim/Hansen.** Their claim is intraday and about order-imbalance, both invisible at daily frequency by construction. A REJECT here does **not** falsify their paper — it confirms the boundary they draw: the periodicity is a high-frequency algorithmic artifact that aggregates away by the daily close. A real test needs sub-hour trade-level data (out of this pipeline's scope).
- **Long-short ≡ long-flat at the two longest look-backs** (weeks=52, 26): over 8y of BTC up-drift every weekday's trailing mean stayed positive, so the short leg never fired. The seasonality signal is swamped by the unconditional drift — another way of saying there is no *cross-weekday* structure to trade.

**Next step:** shelve daily calendar seasonality. The whole 2607.xxxxx crypto batch (quarter-hour effect, state-dependent L2 order flow) points the same way — the tradeable edge in crypto this window is **intraday microstructure / order-flow**, which this daily pipeline structurally cannot reach. To keep producing real backtests, either (a) extend the pipeline to hourly/sub-hourly bars + an order-flow proxy, or (b) pivot the daily track to cross-sectional crypto (BTC vs ETH vs alts relative-value) rather than single-series timing.