# Backtest Report — donchian_breakout on BTC-USD — 2026-07-03



**Idea source:** 2026-07-03 Kurth/Eisler/Rej/Bouchaud 2607.01550 short-term trend demise  
**Verdict:** MIXED — weak edge, needs more data/robustness  
**Best params (stage-1 winner):** `{'window': 40}`  
**Data source:** cache

## Metrics
| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |
| --- | --- | --- | --- | --- | --- |
| Train (in-sample, best of grid) | 0.976 | 0.3557 | -0.5398 | 0.945 | 2045 |
| Test (out-of-sample, realistic costs) | 0.051 | -0.013 | -0.3481 | 1.0 | 857 |
| Full sample (winner) | 0.41 | 0.0838 | -0.8806 | 0.581 | 2922 |

## Stage-1 sweep (top configurations on train)
| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |
| --- | --- | --- | --- | --- | --- |
| 1 | `{'window': 40}` | 0.976 | 0.3557 | -0.5398 | 0.945 |
| 2 | `{'window': 20}` | 0.926 | 0.333 | -0.5225 | 0.928 |
| 3 | `{'window': 30}` | 0.85 | 0.2975 | -0.5488 | 0.892 |
| 4 | `{'window': 10}` | 0.768 | 0.2572 | -0.6855 | 0.841 |
| 5 | `{'window': 5}` | 0.424 | 0.094 | -0.8132 | 0.506 |

## Notes & caveats
- Fails deflated-Sharpe (<0.95): likely overfit to the search grid.
- stage1 backend=vectorbt, stage2 engine=backtrader, grid=5 combos, data source=cache.

## Interpretation
- **Deflated-SR prob** is the probability the true Sharpe > 0 after penalising for the number of configurations tested. Treat < 0.95 as "not convincingly better than luck."
- A result is only worth advancing if it **survives the out-of-sample split** with positive Sharpe *and* passes the deflated-SR gate.

## Human read — honest verdict (MIXED, leans REJECT; confirmatory)

**This is a falsification test of Kurth/Eisler/Rej/Bouchaud (CFM, arXiv:2607.01550),
not a hunt for a live signal.** Their thesis: since ~2009 short-term trend PnL has
collapsed on *small-tick* (volatility-normalised) contracts across all signal
horizons. BTC-USD trades at a tiny tick relative to its vol → the prediction is
that short-term Donchian trend on BTC should carry no dependable edge. It doesn't:

- **OOS collapse.** The stage-1 winner (`window=40`) shows train Sharpe **0.976 / CAGR
  +35.6%**, but out-of-sample Sharpe falls to **0.051** with **negative CAGR (-1.3%)**.
  The in-sample number is the classic trend-follower plateau; none of it survives the
  purged/embargoed test split. This mirrors the last two crypto momentum/trend tests
  in this repo (tsmom 2607.00475 → OOS ~0; cost_aware_momentum → REJECT).
- **Fails the overfitting gate.** Full-sample deflated-SR **0.581** (< 0.95). The edge
  is not convincingly better than grid luck.
- **The speed gradient is the tell — and it agrees with the paper.** Across the sweep,
  in-sample edge decays *monotonically toward faster signals*: window 40 (0.98) > 20
  (0.93) > 30 (0.85) > 10 (0.77) > **5 (0.42, MaxDD -81%)**. The very short-term speeds
  the paper indicts are the weakest here too — exactly the "worst at the fast end"
  pattern of a dead short-term-trend regime. Only the slowest edge of the short band
  (40d, drifting into medium-term) shows any in-sample life, and even that dies OOS.
- **Drawdowns are brutal** (winner full-sample MaxDD **-88%**), typical of an always-in
  long/short breakout fighting BTC's fat down-legs.

**Verdict: MIXED (leans REJECT), confirmatory.** No reliable standalone short-term
trend edge on BTC after costs and out-of-sample — consistent with the Bouchaud
small-tick prediction. The engine tags MIXED only because the slowest in-sample config
skims the deflated-SR gate (0.945 on train); on the honest OOS + full-sample basis this
is a rejection of *short-term* trend on this small-tick series. **Do not advance.**

**Caveats / what would change the read.** (1) Single asset, single (long) structural
drift — BTC's secular up-trend flatters long-biased trend in-sample and punishes the
short leg OOS. (2) The paper's real claim is *cross-sectional* (small-tick vs large-tick);
a proper replication needs a tick-normalised trend screen across many futures/cryptos,
which this one-series test can only gesture at. (3) A large-tick counterpart (e.g. a
high-tick-size futures proxy) is the missing other half — the thesis predicts trend
would *survive* there. That cross-sectional screen is the natural next-run experiment.