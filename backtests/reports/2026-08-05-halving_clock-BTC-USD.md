# Backtest Report — halving_clock on BTC-USD — 2026-08-05



**Idea source:** 2026-08-05 "Bitcoin Runs on a Clock (Molnar 2607.26188)"  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'entry': 0, 'exit': 546, 'mode': 'longflat'}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.97 | 0.2874 | -0.5306 | 0.821 | 2045 |
| Test (out-of-sample, realistic costs) | 0.641 | 0.161 | -0.28 | 1.0 | 857 |
| Full sample (winner) | 0.869 | 0.2466 | -0.5306 | 0.869 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'entry': 0, 'exit': 546, 'mode': 'longflat'}` | 0.97 | 0.2874 | -0.5306 | 0.821 |
| 2 | `{'entry': 0, 'exit': 546, 'mode': 'longshort'}` | 0.97 | 0.2874 | -0.5306 | 0.821 |
| 3 | `{'entry': 60, 'exit': 546, 'mode': 'longflat'}` | 0.956 | 0.2755 | -0.5306 | 0.81 |
| 4 | `{'entry': 60, 'exit': 546, 'mode': 'longshort'}` | 0.956 | 0.2755 | -0.5306 | 0.81 |
| 5 | `{'entry': 120, 'exit': 546, 'mode': 'longflat'}` | 0.94 | 0.2617 | -0.5306 | 0.798 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read — honest verdict (MIXED, leans REJECT)

**Idea tested.** Molnar's "Bitcoin Runs on a Clock" (arXiv:2607.26188) argues every *price* oscillator (Pi Cycle, MVRV, Mayer, Puell) decayed to silence while Bitcoin's *time* structure held: tops 525/546/534 days after each halving, bottoms 406/364/366 days after those tops. We tested the tradable core — be long through the post-halving accumulation-and-run-up window (day `entry`..`exit`), flat/short through the post-top bear — on daily BTC-USD.

**The fatal sample-size problem.** The cached BTC-USD series spans **2018-06-29 → 2026-06-29** — only **two** complete halving cycles (2020-05-11 and 2024-04-20), plus the tail of the 2016-cycle bear at the start. A calendar rule with n≈2 cycles has almost no out-of-sample power: the purged split trains on ~one-and-a-half cycles and "tests" on essentially the single 2024 cycle. The OOS test's Deflated-SR = 1.0 is an artifact of only one config passing through to the test — it applies **no** multiple-comparisons penalty. The honest number is the **train** Deflated-SR that penalises all 18 grid configs: **0.821 < 0.95 → fails the gate.**

**It does not beat buy-and-hold on return.** Against B&H on the identical data (CAGR 32.5%, Sharpe 0.77, MaxDD −76.6%), the winner (`entry=0, exit=546, longflat`) delivers **lower** CAGR (24.7% vs 32.5%, −8pp), a **modestly higher** Sharpe (0.87 vs 0.77), and a **much shallower** MaxDD (−53% vs −77%). This is the same profile as the `trend_filter` capstone (2026-07-04): the edge is **drawdown mitigation from sitting out the bear phase, not alpha** — mechanically, holding ~1.5 years post-halving and going flat cuts the crash but sacrifices return.

**Verdict: MIXED, leans REJECT.** Consistent with the whole BTC single-series thread (now 8+ price/calendar rejects). The clock's only survivor is crash insurance, echoing `trend_filter` and `vol_regime`. Critically, Molnar's own claim is *not* falsified here — he explicitly rests nothing on per-epoch significance, calls the current-cycle edge "one holdout, suggestive not decisive," and pre-registers windows (2026 bottom Oct 5–Nov 16; next top 525–546d after the following halving). Our result simply confirms the **boundary**: with n=2 daily cycles, the halving clock is **unvalidatable by backtest**, exactly as the paper's honesty implies. To actually test it you need the pre-registered forward windows to resolve, not more in-sample slicing.

**Next axis.** The daily BTC single-series well is dry (trend, momentum, breakout, seasonality, vol-regime, halving-clock all reject or reduce to crash insurance). Move to (a) **cross-sectional crypto** (BTC/ETH/majors long-short — Halperin's rank-Markov approach 2607.27461, CryptoGAT) or (b) **honest forward paper-trading** of pre-registered calendar windows, which is the only design that can validate a low-n calendar claim.