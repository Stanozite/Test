# Index — Backtest reports

Running log of every backtest produced by `/backtest`. Newest first.

| Date | Report | Strategy · Symbol | Verdict | OOS Sharpe | Deflated-SR |
| --- | --- | --- | --- | --- | --- |
| 2026-06-29 | [2026-06-29-ma_crossover-BTC-USD.md](2026-06-29-ma_crossover-BTC-USD.md) | ma_crossover · BTC-USD | MIXED (leans REJECT) — underperforms buy-and-hold | 0.11 | 0.896 (full, fails) |

---

## How a verdict is decided
- **PROMISING** — survives the out-of-sample split (Sharpe ≥ 0.5) **and** passes the
  deflated-Sharpe gate (prob ≥ 0.95). Advance to deeper validation / paper trading.
- **MIXED** — weak positive edge; needs more data or robustness checks.
- **REJECT** — no edge after costs and out-of-sample testing.
- **INVALID** — ran on synthetic data (no real feed reachable); plumbing only.
