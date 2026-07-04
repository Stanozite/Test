# Index — Backtest reports

Running log of every backtest produced by `/backtest`. Newest first.

| Date | Report | Strategy · Symbol | Verdict | OOS Sharpe | Deflated-SR |
| --- | --- | --- | --- | --- | --- |
| 2026-07-04 | [2026-07-04-trend_filter-BTC-USD.md](2026-07-04-trend_filter-BTC-USD.md) | trend_filter · BTC-USD | MIXED (leans REJECT) — **capstone** closing the BTC trend thread (6th test). Long-only long-horizon filter (60–250d, long-or-flat) applies both fixes the prior 5 rejects implied — drop the short leg (which bled in `tsmom`) + go slower than the horizon Kurth/Bouchaud 2607.01550 indict. Train Sharpe 0.918→**OOS 0.093, CAGR −0.4%**: no timing edge, same signature as `tsmom`/`donchian`. Only survivor is drawdown mitigation — full-sample MaxDD −60% vs BTC buy-and-hold −77%, Sharpe 0.864 vs 0.769, at −5pp CAGR = crash insurance, **not alpha**. Do not advance as a return strategy; next backtest should move OFF the trend axis | 0.093 | 1.0 (OOS, but Sharpe ~0 — passes gate vacuously; full-sample 0.962) |
| 2026-07-03 | [2026-07-03-donchian_breakout-BTC-USD.md](2026-07-03-donchian_breakout-BTC-USD.md) | donchian_breakout · BTC-USD | MIXED (leans REJECT) — confirmatory falsification of Kurth/Eisler/Rej/Bouchaud 2607.01550 "short-term trend is dead on small-tick assets"; short-term Donchian on BTC (tiny effective tick) shows train Sharpe 0.98 but OOS collapses to ~0 with negative CAGR, fails full-sample deflated-SR 0.581; in-sample edge decays monotonically toward faster signals (w40>w20>…>w5) — the fast band the paper indicts is weakest here too. Do not advance | 0.051 | 0.581 (full sample, fails) |
| 2026-07-02 | [2026-07-02-tsmom-BTC-USD.md](2026-07-02-tsmom-BTC-USD.md) | tsmom · BTC-USD | MIXED (leans REJECT) — tests the TSMOM "simple rule" benchmark from Pollok/Robik 2607.00475 on a crypto series outside their futures panel; in-sample plateau Sharpe ~0.92 but OOS collapses to ~0 with negative CAGR — long/short short-leg bleeds against BTC up-drift, no dependable standalone edge | 0.093 | 0.924 (in-sample train, fails) |
| 2026-07-01 | [2026-07-01-lag1_reversal-BTC-USD.md](2026-07-01-lag1_reversal-BTC-USD.md) | lag1_reversal · BTC-USD | REJECT (expected/confirmatory) — falsification test of Portnaya 2606.29591; "fade the recent move" has no directional edge on real 8y BTC, confirming lag-1 autocorrelation is bounce not reversal | -0.087 | 0.122 (in-sample, fails) |
| 2026-06-30 | [2026-06-30-cost_aware_momentum-BTC-USD.md](2026-06-30-cost_aware_momentum-BTC-USD.md) | cost_aware_momentum · BTC-USD | REJECT — cost-band cut drawdown ~10pp but proxy momentum signal has no OOS edge (Bysik/Słepaczuk 2606.00060) | -0.53 | 0.74–0.79 (grid, fails) |
| 2026-06-29 | [2026-06-29-ma_crossover-BTC-USD.md](2026-06-29-ma_crossover-BTC-USD.md) | ma_crossover · BTC-USD | MIXED (leans REJECT) — underperforms buy-and-hold | 0.11 | 0.896 (full, fails) |

---

## How a verdict is decided
- **PROMISING** — survives the out-of-sample split (Sharpe ≥ 0.5) **and** passes the
  deflated-Sharpe gate (prob ≥ 0.95). Advance to deeper validation / paper trading.
- **MIXED** — weak positive edge; needs more data or robustness checks.
- **REJECT** — no edge after costs and out-of-sample testing.
- **INVALID** — ran on synthetic data (no real feed reachable); plumbing only.
