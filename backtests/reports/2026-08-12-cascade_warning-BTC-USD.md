# Backtest Report — cascade_warning on BTC-USD — 2026-08-12



**Idea source:** 2026-08-12 Garcia Seuma 2608.03616 liquidation-cascade critical-slowing-down  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 60, 'q': 0.9, 'window': 504}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.658 | 0.2134 | -0.8027 | 0.507 | 2045 |
| Test (out-of-sample, realistic costs) | -0.827 | -0.1548 | -0.4593 | 1.0 | 857 |
| Full sample (winner) | 0.528 | 0.1411 | -0.7852 | 0.478 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 60, 'q': 0.9, 'window': 504}` | 0.658 | 0.2134 | -0.8027 | 0.507 |
| 2 | `{'lookback': 60, 'q': 0.9, 'window': 252}` | 0.594 | 0.1802 | -0.7611 | 0.436 |
| 3 | `{'lookback': 20, 'q': 0.9, 'window': 252}` | 0.586 | 0.1766 | -0.7844 | 0.427 |
| 4 | `{'lookback': 30, 'q': 0.9, 'window': 252}` | 0.58 | 0.1735 | -0.7369 | 0.422 |
| 5 | `{'lookback': 20, 'q': 0.9, 'window': 504}` | 0.529 | 0.1426 | -0.8234 | 0.367 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=18 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read — REJECT (confirmatory falsification of the CSD-crash folk belief)
**What was tested.** A critical-slowing-down (CSD) early-warning overlay on daily BTC-USD:
de-risk to flat when a composite of *rising return-variance* + *rising lag-1
autocorrelation* (the classic Scheffer-et-al. tipping-point tells) sits above its own
rolling quantile; long otherwise. This directly probes the tradable core of Garcia Seuma
(arXiv:2608.03616), who measures the Oct-2025 liquidation cascade *in flight*, finds it ran
deeply **subcritical** (branching ratio λ≈0.1–0.2), eliminates the critical-cascade
(Galton–Watson) hypothesis at power ≥0.96, and concludes the transition is **abrupt /
first-order, not critical — so "none of the scalar pre-state measures we can construct
grades it."**

**Result — the paper's negative prediction holds, hard.** Grid winner
`lookback=60, q=0.9, window=504`: train Sharpe 0.658 → **OOS Sharpe −0.827, CAGR −15.5%**,
fails deflated-SR (0.507 train, 0.478 full). The CSD flag carries **no timing content**:
the days it marks "most critical" are not reliably followed by crashes, so going flat on
them cost upside and did not dodge drawdowns.

**No crash-insurance consolation this time.** Every prior daily-BTC overlay
(`vol_regime`, `trend_filter`, `halving_clock`) at least cut drawdown vs B&H (~−77%) —
crash insurance, not alpha. This one does **not**: train MaxDD **−80%** ≈ buy-and-hold,
because the winner only steps aside on the top-10% CSD days (q=0.9) and those are the
wrong days. So this is a **cleaner REJECT** than the recent MIXED-leans, not a MIXED.

**This does NOT falsify Garcia Seuma — it confirms him.** His load-bearing claim is
precisely that no scalar pre-state statistic grades cascade severity; a daily CSD overlay
with no edge is exactly what "abrupt first-order transition" predicts. Severity = shock ×
map-in-path × liquidity-withdrawal, none of which a price-only pre-state series sees.

**Standing thread.** **10th consecutive daily-BTC reject** (9 leans + this clean one).
Direction, trend, exposure/vol-target, calendar/halving, and now tipping-point
early-warning axes are all tapped out on a single daily series. The genuinely untested
axis remains **cross-sectional crypto** (BTC/ETH/alts long-short; Halperin rank-Markov
2607.27461) — which needs a multi-asset feed the cache does not hold. Until that feed is
allowlisted, further single-series daily BTC tests are low-value.

**Data caveat.** 8y cached daily BTC-USD (2018→2026), real (synthetic=False). Cascades
are a *sub-daily* phenomenon (Garcia Seuma: 88% of forced selling inside 30 min); a daily
close is the wrong resolution to see the mechanism, so this tests only the daily-aggregate
shadow of his signal, not the intraday branching process itself.