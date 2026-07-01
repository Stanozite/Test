# Backtest Report — lag1_reversal on BTC-USD — 2026-07-01



**Idea source:** 2026-07-01 "The Bounce Has No Direction (Portnaya)"  
**Verdict:** REJECT — no edge after costs and OOS  
**Best params (stage-1 winner):** `{'lookback': 5, 'threshold': 0.0}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.172 | -0.0125 | -0.572 | 0.122 | 2045 |
| Test (out-of-sample, realistic costs) | -0.087 | -0.0666 | -0.5043 | 1.0 | 857 |
| Full sample (winner) | -0.469 | -0.312 | -0.9881 | 0.0 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'lookback': 5, 'threshold': 0.0}` | 0.172 | -0.0125 | -0.572 | 0.122 |
| 2 | `{'lookback': 2, 'threshold': 0.0}` | 0.113 | -0.0384 | -0.6959 | 0.091 |
| 3 | `{'lookback': 2, 'threshold': 0.05}` | 0.015 | -0.0218 | -0.5388 | 0.052 |
| 4 | `{'lookback': 5, 'threshold': 0.02}` | 0.009 | -0.0644 | -0.6918 | 0.051 |
| 5 | `{'lookback': 3, 'threshold': 0.02}` | -0.019 | -0.0705 | -0.5595 | 0.042 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- Out-of-sample Sharpe <= 0: does not survive the held-out split.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read (honest verdict) — 2026-07-01

**REJECT, and that is the *expected, confirmatory* result — not a disappointment.**

This was a deliberate **falsification test** of Portnaya (arXiv:2606.29591): she
finds lag-1 return autocorrelation is *magnitude shrinkage* (bid-ask bounce /
staleness), **not** directional reversal — the sign is not predictable — and that
crypto in her 21-asset panel is indistinguishable from a random walk. A naive
"fade the recent move" rule should therefore have **no directional edge net of
costs**. On 8y of real (non-synthetic) BTC-USD daily data, that is exactly what
happened:

- The literal **lag-1** fade did not even make the stage-1 top-5; the best fade
  config (lookback=5, threshold=0) managed only **train Sharpe 0.172** with a
  **negative CAGR (−1.25%)** — i.e. it lost money even in-sample.
- Out-of-sample it flips to **Sharpe −0.087, CAGR −6.7%**, and fails the
  **deflated-SR gate (in-sample prob 0.122 ≪ 0.95)**.
- Full-sample the winner is **Sharpe −0.47, MaxDD −98.8%** — the fade rule is a
  capital-destroyer once you actually trade it through costs.

**Takeaway for the system:** ✅ Portnaya replicates on BTC — do **not** build a
short-horizon mean-reversion / "fade the bounce" strategy on crypto; the lag-1
autocorrelation is a microstructure artifact with no exploitable *direction*.
This is a useful negative result: it prunes a whole family of tempting reversal
ideas. The one loose thread worth a future run is Portnaya's **lag-3** directional
reversal channel (p=0.02) — a multi-lag structure, not tested here.

**Caveat:** daily bars can't see the intra-day bid-ask bounce that drives her
lag-1 effect, so this tests the *tradeable* (daily) horizon, which is the one that
matters for us — not her microstructure mechanism itself.