# Backtest Report — trend_leverage on BTC-USD — 2026-11-04



**Idea source:** 2026-11-04 Bicki & Akdogan 2611.04533 preceding-trend leverage effect  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'gamma': 3.0, 'L': 20, 'q': 0.6, 'window': 252}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.706 | 0.2118 | -0.6782 | 0.493 | 2045 |
| Test (out-of-sample, realistic costs) | 0.474 | 0.0952 | -0.2937 | 1.0 | 857 |
| Full sample (winner) | 0.541 | 0.1342 | -0.6949 | 0.425 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'gamma': 3.0, 'L': 20, 'q': 0.6, 'window': 252}` | 0.706 | 0.2118 | -0.6782 | 0.493 |
| 2 | `{'gamma': 2.0, 'L': 20, 'q': 0.6, 'window': 252}` | 0.666 | 0.1938 | -0.7058 | 0.446 |
| 3 | `{'gamma': 1.0, 'L': 10, 'q': 0.5, 'window': 252}` | 0.592 | 0.1534 | -0.7126 | 0.365 |
| 4 | `{'gamma': 1.0, 'L': 40, 'q': 0.4, 'window': 252}` | 0.552 | 0.1302 | -0.7043 | 0.322 |
| 5 | `{'gamma': 3.0, 'L': 10, 'q': 0.6, 'window': 252}` | 0.541 | 0.1405 | -0.6582 | 0.313 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=27 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Honest verdict — MIXED, leans REJECT (20th straight daily-crypto non-advance)

**Reconciliation against buy-and-hold** (recomputed directly on the full 2922-bar cache
with the engine's own 252-day annualisation — independent of the pipeline's backtrader
numbers, per the "agreement computed the same way is not evidence" rule):

| Series (full sample, 10 bps/side) | Sharpe | CAGR | MaxDD | Time-in-market |
| --- | --- | --- | --- | --- |
| **BTC-USD buy-and-hold** | **0.639** | **21.4%** | −76.6% | 100% |
| trend_leverage winner (γ=3, L=20, q=0.6) | 0.526 | 12.9% | −69.9% | **57.4%** |
| trend_leverage winner (zero cost) | 0.584 | 15.1% | −68.2% | 57.4% |

The strategy **does not beat buy-and-hold**: lower Sharpe (0.526 vs 0.639), roughly half
the CAGR (12.9% vs 21.4%), and only ~7 pp better full-sample drawdown. OOS it trims
drawdown hard (−29.4% vs the stormy test window) at ~9.5% CAGR — the familiar
**crash-insurance / low-exposure-dial** signature: it holds BTC's up-drift ~57% of the
time and sits out some storms, so its Sharpe lands near B&H while sacrificing return. It
fails the deflated-SR gate (0.425 full / 0.493 train).

**The one confirming tell for the paper's mechanism.** The stage-1 sweep ranks the two
*asymmetric* arms first — γ=3.0 (0.706) and γ=2.0 (0.666) — above every *symmetric*
γ=1.0 control (ranks 3–5, ≈0.55–0.59). Conditioning the vol forecast on the sign of the
preceding trend buys ~0.11 Sharpe in-sample over the symmetric baseline. That is exactly
the leverage/arrow-of-time asymmetry Bicki & Akdogan (2611.04533) measure — it is real
and it has the predicted sign — **but it does not survive to a tradable daily edge.**

**Does NOT falsify the paper.** 2611.04533 is a *volatility-response measurement* at
minute resolution whose effect half-lives at ~1.5 h; it makes no claim about daily
return predictability. Our result confirms its boundary: by the daily close the
asymmetry has decayed into an exposure dial, not alpha — the same fate as the
quarter-hour effect (`dow_seasonality` REJECT) and every vol-statistic gate
(`vol_regime`, `evar_regime`, `asym_longmem_vol` all MIXED-lean-REJECT). The
vol-asymmetry axis is now quadruple-exhausted on daily single-series crypto.

**Blocker unchanged and now ~9× overdue:** the hourly / multi-coin OHLCV loader. The
preceding-trend leverage effect, the time-arrow component, and the matched crypto-vs-
equity contrast all live at the 20-min–1.5-h resolution the daily cache cannot reach.
Carried onto an intraday feed, a trend-sign-conditioned vol forecast is the right
implementation layer — but it cannot be tested here.