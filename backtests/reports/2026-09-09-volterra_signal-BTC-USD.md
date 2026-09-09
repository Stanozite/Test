# Backtest Report — volterra_signal on BTC-USD — 2026-09-09



**Idea source:** 2026-09-09 Leclere & Rosenbaum arXiv:2609.03115 mean-field impact -> martingale  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'length': 30, 'alpha': 0.7}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 1.063 | 0.3976 | -0.4782 | 0.918 | 2045 |
| Test (out-of-sample, realistic costs) | 0.242 | 0.03 | -0.3453 | 1.0 | 857 |
| Full sample (winner) | 0.343 | 0.0471 | -0.7365 | 0.308 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'length': 30, 'alpha': 0.7}` | 1.063 | 0.3976 | -0.4782 | 0.918 |
| 2 | `{'length': 30, 'alpha': 0.5}` | 1.045 | 0.3926 | -0.5139 | 0.909 |
| 3 | `{'length': 60, 'alpha': 0.7}` | 1.044 | 0.3865 | -0.6043 | 0.909 |
| 4 | `{'length': 120, 'alpha': 0.7}` | 0.989 | 0.3581 | -0.5915 | 0.88 |
| 5 | `{'length': 60, 'alpha': 0.5}` | 0.951 | 0.3409 | -0.6409 | 0.854 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=12 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest read (human verdict) — MIXED, leans REJECT

**What was tested.** Leclère & Rosenbaum (arXiv:2609.03115) prove that when heterogeneous-horizon agents account for their own market impact, the common *predictable signal* (a Volterra / long-memory process) and the aggregate impact term **cancel at equilibrium**, so the observed price collapses to a pure martingale. Tradable corollary on daily BTC: a long-memory predictable signal built from past returns should carry **no exploitable directional edge**. I built exactly that — a power-law memory kernel `w_k ∝ k^-alpha` over past log-returns, sign as position — and swept the memory exponent `alpha` (0.5–0.9 = genuine long memory; 1.5 = near-Markovian control) and kernel span (30/60/120d).

**Result.** In-sample the winner looks fine (train Sharpe 1.063, CAGR 39.8%) but already fails the deflation gate (0.918 < 0.95). Out-of-sample it decays to **Sharpe 0.242, CAGR 3.0%** — barely positive, far below BTC buy-and-hold return, and the **full-sample deflated-SR is 0.308**, a hard fail. This is the same shape as the prior 14 daily-crypto tests: a training number that does not survive costs + OOS.

**The tell that *confirms* the paper.** The stage-1 ranking is monotone in kernel span: **length 30 > 60 > 120** at every `alpha`. The *longer* the memory, the *worse* the edge — i.e. the genuinely long-memory (Volterra-regime) component is precisely the part with no exploitable signal, while the residual sits in the shortest, near-Markovian window (which is just short-horizon momentum, already rejected here as `tsmom`/`trend_filter`). That is exactly what impact-cancellation predicts: the predictable long-memory term is arbitraged into the martingale. So this backtest **does not falsify Leclère & Rosenbaum — it is consistent with their equilibrium result** on a single daily crypto series.

**Drawdown.** No robust crash-insurance signature this time: full-sample MaxDD −73.7% ≈ BTC B&H (~−77%); the −34.5% OOS figure is a calmer-window artifact, not a structural hedge.

**Verdict: MIXED, leans REJECT.** No advanceable edge. **15th straight daily-crypto reject-lean** — the long-memory / Volterra-kernel axis joins direction, trend, vol, calendar, tail-measure, early-warning, and profit-threshold-momentum as exhausted on single-series daily BTC. The blocked frontier is unchanged: **cross-sectional / intraday crypto** (needs the hourly multi-coin loader flagged since 08-26), where the tradable signals of the last several weeks (Kitron-Wengrowicz 15-min reversal, on-chain identity, MFCCA) actually live.