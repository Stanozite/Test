# Backtest Report — powerlaw_trend on BTC-USD — 2026-11-14



**Idea source:** 2026-11-13 Baquero-Menezes power-law identifiability (2611.13962)  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'window': 0, 'entry': 0.5, 'longflat': False}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.393 | 0.0747 | -0.6375 | 0.239 | 2045 |
| Test (out-of-sample, realistic costs) | -0.343 | -0.1091 | -0.4619 | 1.0 | 857 |
| Full sample (winner) | -0.255 | -0.1854 | -0.9328 | 0.003 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'window': 0, 'entry': 0.5, 'longflat': False}` | 0.393 | 0.0747 | -0.6375 | 0.239 |
| 2 | `{'window': 0, 'entry': 0.5, 'longflat': True}` | 0.393 | 0.0747 | -0.6375 | 0.239 |
| 3 | `{'window': 0, 'entry': 1.0, 'longflat': False}` | 0.185 | 0.0149 | -0.6217 | 0.092 |
| 4 | `{'window': 0, 'entry': 1.0, 'longflat': True}` | 0.185 | 0.0149 | -0.6217 | 0.092 |
| 5 | `{'window': 0, 'entry': 1.5, 'longflat': False}` | 0.171 | 0.0123 | -0.5369 | 0.086 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read — honest verdict

**REJECT, and a cleaner one than the recent MIXED-leans.** This tests the "Bitcoin power-law corridor" (Santostasi-style log(price)~log(days-since-genesis) support/resistance bands) as a *reversion-timing* rule: long below the fitted corridor ("cheap"), short/flat above ("rich"). Real cached BTC-USD (2922 bars, 2018→2026). The self-test was forced red first (the ponytail confirms the corridor leans net-long-below / net-short-above on a genuine power-law+OU series, and the long-leg goes sparse under persistent random-walk noise — the paper's non-identifiability regime).

**There is barely an in-sample edge to collapse.** The stage-1 winner is `window=0` (expanding / all-history fit), `entry=0.5` at train Sharpe **0.393** (CAGR +7.5%) — weak even in-sample, and the whole grid degrades from there: the two `entry=0.5` arms tie at 0.393, every tighter band (`entry=1.0/1.5`) drops to ≈0.17–0.19, and **no rolling-window fit (365/730d) reaches the top five** — only the expanding all-history corridor fires at all. OOS it inverts: **Sharpe −0.343, CAGR −10.9%**, and on the full sample **Sharpe −0.255, CAGR −18.5%, MaxDD −93.3%, deflated-SR 0.003** (hard fail).

**Two confirming tells, both the familiar crypto-reversion failure signature:**
1. **The short leg is ruinous.** The winner (`longflat=False`) holds **long 34% / short 34% / flat 32%** of the time; `longflat=True` is *identical on train* (0.393) because the short leg rarely fired in the lower-priced train era — but on the full sample shorting every "rich" excursion above the corridor means **shorting the top of BTC's up-drift**, driving MaxDD to −93.3%, exactly as in `weak_meanrev` / `tsmom` / `lag1`.
2. **The corridor is tighter = worse.** Demanding a more extreme deviation (`entry` 0.5→1.5) *lowers* the Sharpe monotonically — there is no band width at which the deviation-from-trend carries a reliable reversion signal. The deviation wanders and stays away rather than reverting, precisely the persistent-noise behavior Baquero & Menezes describe.

**Benchmark:** BTC buy-and-hold on the same cache is full-sample **Sharpe 0.639 / CAGR 21.4% / MaxDD −76.6%** (direct computation, 252-ann). The strategy trails it on every axis and is outright negative — not even the crash-insurance consolation that `vol_regime` / `trend_filter` / `trend_leverage` kept.

**Does NOT falsify Baquero & Menezes (2611.13962) — it confirms them.** Their pre-registered verdict is that BTC's power-law trend is *not statistically identifiable* under persistent noise (a Gompertz ceiling fits as well, the log-age exponent ~5.7 is not rejected but not identified, and "reversion to trend cannot be decided"). A corridor-reversion trade that assumes exactly that reversion therefore *should* have no edge — and it has none. The popular retail power-law-corridor timing model has no daily BTC edge, and its short leg is actively harmful.

**21st straight daily-crypto non-advance.** The regressor was genuinely new (calendar age on a log-log scale, distinct from `weak_meanrev`'s rolling mean and `halving_clock`'s calendar window) and it still fails — further evidence the blocker is data *resolution* (intraday / multi-coin), not the choice of trend object. The intraday/multi-coin loader is now ~10× overdue; three findings in this very digest (Neural Realized Measures at crypto 5-min, wallet-identity ms-grid, Butler multi-asset seasonality/TSMOM) live at resolutions this daily cache cannot reach. Do not advance `powerlaw_trend`.