# Quant Scout Digest — 2026-08-05

_Window: since the 2026-07-29 run (ceiling 2607.25xxx). Swept q-fin.TR/PM/ST/CP/RM `/recent`, IDs 2607.26xxx → 2608.03xxx. 10 findings + 2 resources. Dedupe: none of the below appear in the INDEX ledger (which tops at 2607.24410)._

## TL;DR
- **The honest-OOS reckoning continues.** Two pre-registered papers this window post great development-window numbers that die out-of-sample: **Conformal Kelly** (Ryan, 2608.01494) — 28.5%/yr, Sharpe 1.34 in-sample → **7–8%/yr OOS, below passive**; **Bitcoin's halving clock** (Molnar, 2607.26188) — every *price* oscillator (Pi Cycle/MVRV/Mayer/Puell) decayed to silence, only the *time* clock (tops 525–546d post-halving) survives, but on "one holdout, suggestive not decisive." Both authors seal data and pre-register — the methods are the takeaway.
- **Halperin ships a real cross-sectional edge with almost no machinery** (2607.27461): three fixed matrices from price/volume/cap (correlation-distance + two rank-Markov transition matrices) replace Markowitz's μ and Σ, no matrix inversion — **volatility rank is one-step forecastable, return rank isn't**, OOS Sharpes 1.06/1.32 on two non-overlapping windows net of 5bps, beats min-var and max-diversification. Our next crypto axis.
- **Barzykin doubles down on passive execution** (2607.28323): a mesoscopic optimal-liquidation model from two observables — exponential fill-probability decay with quote distance + linear order-flow-imbalance price response — calibrated on NASDAQ + public FX. Tactical passive-quoting alpha, not just theory.
- **Amaral closes microstructure mean-reversion in closed form** (2608.00885): all the profit is the *option value of waiting* — trade the instant the gap covers the spread and you earn zero; the optimal band half-width solves θ*(θ*−φ)=s_G².
- **Backtest: `halving_clock` on BTC-USD → MIXED, leans REJECT.** Tested Molnar's tradable core. OOS Sharpe 0.64 (positive!) but fails deflated-SR on the full grid (0.821), doesn't beat B&H on return (−8pp CAGR), only edge is drawdown (−53% vs −77%) = crash insurance not alpha. **Fatal: cached BTC is only ~2 halving cycles — unvalidatable at n=2.** 9th straight daily-BTC reject-lean; daily single-series is tapped out.

## Findings by focus area

### ML / AI for alpha

- **Are Three Matrices All You Need To Beat the Market? Observable Matrix Dynamics for Portfolio Optimization** — Igor Halperin, 2026-07-29 — [arXiv:2607.27461](https://arxiv.org/abs/2607.27461)
  - **What it is:** A dynamic portfolio method whose entire state is three fixed-size matrices built from daily price/volume/cap history: the return-correlation distance matrix + two Markov-chain transition matrices that rank S&P 500 names monthly by trailing return and by trailing volatility. These replace Markowitz's expected-return vector and covariance matrix — no matrix inversion, outlier-robust cross-sectional ranks, dynamic not single-period. Empirically the **volatility rank is forecastable one step ahead while the return rank stays ~unforecastable**; a market-neutral momentum long-short blended with an opportunistic long-only sleeve beats the market OOS on two non-overlapping sets (Jan-2022→Dec-2024 and Jan-2025→Jul-2026) at Sharpe 1.06 and 1.32 vs market 0.78 and 1.14, net of 5bps, marked daily. Beats classical min-variance and max-diversification; a residual-distance diversification of the long sleeve lifts Sharpe to 1.08/1.44.
  - **Why it matters for trading:** A transparent, invertible-free, rank-based cross-sectional engine that actually clears its OOS bar — and the "vol-rank forecastable, return-rank not" split is a clean design principle. Directly portable to a crypto cross-section (BTC/ETH/majors), which is exactly the axis our BTC single-series thread has been pointing to.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate/backtest (crypto cross-section adaptation — top priority next axis)

- **Train Often, Deploy Selectively: Forward-Gated Model Replacement in Crypto Markets** — Aditya Dutta, 2026-07-30 — [arXiv:2607.28577](https://arxiv.org/abs/2607.28577)
  - **What it is:** "Shadow Before Swap" (SBS) — a deployment methodology that gates promoting a retrained challenger over a continuously-maintained incumbent by requiring a fixed paired negative-log-likelihood advantage on identical delayed-label data. On 48 weeks of Binance crypto-futures data: 0.147% relative NLL reduction vs calendar replacement, 0.076% vs schedule-matched auto-promotion, and a **78.4% cut in deployed model changes** (only 114 of 528 challengers promoted), stable across seeds/assets/contract types.
  - **Why it matters for trading:** The retraining-cadence question is under-discussed and directly operational — "retrain often, deploy rarely, gate on held-out likelihood" is a concrete MLOps discipline for any live crypto forecaster, cutting churn/turnover risk without losing accuracy.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read (adopt the gating discipline; not a standalone alpha to backtest)

### Microstructure & execution

- **Optimal Execution with Passive Market Impact** — Alexander Barzykin, Robert Boyce, Eyal Neuman, Sturmius Tuschmann, 2026-07-30 — [arXiv:2607.28323](https://arxiv.org/abs/2607.28323)
  - **What it is:** A mesoscopic optimal-liquidation model for limit orders built from two empirical observables: (1) approximately exponential decay of limit-order fill probability with distance from mid, and (2) short-term linear price response to order-flow imbalance. Combined, they give a reduced-form passive-impact rate decaying exponentially in quote distance; the trader controls passive-sell-quote aggressiveness, trading off fill intensity + accumulated impact vs non-execution risk. Calibrated on NASDAQ equities + public FX; extensions for heterogeneous decay, transient impact, target schedules.
  - **Why it matters for trading:** Most execution theory is about *aggressive* impact; this is a tractable, calibrated framework for *passive* quoting — where market-making and cost-sensitive execution actually live. Barzykin (HSBC, tracked) continues to translate microstructure into deployable quoting rules.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (execution/MM reference; needs L2 data to implement)

- **Optimal Trading of Microstructure Mean Reversion** — Lucas Rabechini Amaral, 2026-08-01 — [arXiv:2608.00885](https://arxiv.org/abs/2608.00885)
  - **What it is:** At the seconds scale the observed mid carries a stationary mean-reverting error (gap G) around a latent efficient price. Under a balanced-response condition the gap's conditional mean/covariance are exactly Ornstein-Uhlenbeck (rate α, stationary sd s_G), though paths jump. The optimal rule is a symmetric band: buy at G=−θ, sell at +θ, hold inside. Closed form: **θ*(θ*−φ)=s_G²** (φ = tight-book half-spread), profit rate R*=α·s_G·√(2/π)·e^(−θ*²/2s_G²). Punchline: **trading as soon as the gap merely covers the spread earns zero — all profit is the option value of waiting.**
  - **Why it matters for trading:** A clean, parameter-light theory of the classic "fade the microstructure noise" trade with an explicit entry-band formula and an unambiguous warning that threshold=spread is the break-even. Directly relevant to any large-tick mean-reversion market-making book.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (needs tick/L2 data; not testable on daily bars — logged for the HF track)

### Risk & portfolio

- **Drawdown Risk Beyond Brownian Motion: A Monte-Carlo Framework, Non-Gaussian Extensions, and Long Memory** — Francesco Landolfi, 2026-07-31 — [arXiv:2608.00127](https://arxiv.org/abs/2608.00127)
  - **What it is:** Extends the Rej-Seager-Bouchaud (2017) drawdown framework: reframes their closed-form results as a transparent Monte-Carlo experiment, then maps Sharpe + return structure onto four decision-relevant measures — max drawdown, max loss, final negative time, longest recovery time. Relaxing Gaussianity (skew, fat tails, vol clustering, Sharpe-estimation uncertainty) **moves the four measures differently, so a single Gaussian table mis-warns.** Under fractional Brownian motion, the apparent amplification of drawdown risk from persistence is — for max-DD depth — **almost entirely self-similar dispersion scaling (T^(H−1/2)), not path geometry**: a square-root-of-time calibration failure, not intrinsic danger. Ships reproducible lookup tables + a calibration recipe.
  - **Why it matters for trading:** This is the rigorous version of the exact question our whole BTC thread keeps hitting — "is this strategy's drawdown normal for its Sharpe?" It gives honest, distribution-aware drawdown expectations and debunks a common over-fear of long-memory. A direct methods upgrade for our verdict framework.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read (adopt the four-measure drawdown lookup as a backtest-report enhancement)

- **Conformal Kelly: Conformal Prediction Intervals as the Scale in Fractional Kelly Position Sizing** — Robert Jacob Ryan, 2026-08-02 — [arXiv:2608.01494](https://arxiv.org/abs/2608.01494)
  - **What it is:** Uses a 75% conformal prediction interval as the *scale* in fractional-Kelly sizing — wider interval → smaller position, narrower → larger. On a 2016–2021 development window (costs + leverage caps): 28.5%/yr net log growth, Sharpe 1.34, MaxDD 27.7%, vs 15.9% S&P and 21–22% passive. Counter-intuitively, **every adaptive-interval tweak cost 0.7–5.3 pts/yr; the winner was the simplest — slow, unweighted, per-asset rolling quantiles** ("width stability beats local sharpness when an interval sizes a position"). Beats textbook σ-sizing by 2.1 pts. The honesty: an autonomous LLM agent searched 200 configs, so **all data from 2022 on was sealed and pre-registered** — and OOS growth collapsed to **7.0–8.5%/yr, below passive benchmarks**, though calibration held (0.745 vs 0.750). Reported as pre-registered win *and* loss.
  - **Why it matters for trading:** Two lessons: (1) a genuinely novel, simple position-sizing idea (interval-width as Kelly scale) worth stealing; (2) a model example of pre-registration exposing dev-window overfit — exactly the discipline our deflated-Sharpe gate enforces. The OOS failure is the *feature*, not the bug.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (sizing-overlay idea; the pre-registration protocol is the real transferable asset)

### Asset class / market

- **Bitcoin Runs on a Clock: Why Every Price Indicator Dies and the Halving Clock Doesn't** — Josh Molnar, 2026-07-28 — [arXiv:2607.26188](https://arxiv.org/abs/2607.26188)
  - **What it is:** Across four halving epochs (2011–2026), every widely-followed *price* cycle oscillator (Pi Cycle, MVRV, Mayer, Puell) called turns precisely then degraded in one sequence — precise → early → silent — as per-cycle maxima decline monotonically and minima end higher, so any threshold calibrated on past cycles must stop firing. Yet Bitcoin's *time* structure stays fixed: mature-cycle tops 525/546/534 days after halvings, bottoms 406/364/366 days after tops. Block-bootstrapped nulls under the identical rule never reproduce the top cluster (0 of 10,000); the bottom cluster is largely intrinsic to the drawdown process. The **only** signal with sign stable across mature epochs is a causal power law in time-since-genesis (exponent ~5.6), which replicates on a second source and on Ethereum. The author rests nothing on per-epoch significance (rotation null shows HAC over-rejects, p=0.21) and **pre-registers falsifiable windows: a 2026 bottom Oct 5–Nov 16, and a next top 525–546 days after the following halving.**
  - **Why it matters for trading:** The sharpest possible framing of why our 8 prior daily-BTC price-indicator tests kept failing — it's structural, and the paper argues the *time* clock is the only survivor. Perfect backtest target (below), and a model of pre-registered forecasting honesty.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate/backtest → **done this run** (see backtest below)

- **Where does the criticality live? Early-warning signals are event-heterogeneous across seven crypto-perpetual liquidation cascades** — Ramon Marc Garcia Seuma, 2026-07-29 — [arXiv:2607.27070](https://arxiv.org/abs/2607.27070)
  - **What it is:** Studies seven major BTC perpetual-futures liquidation cascades (2022–2025, incl. the record $19B 10-Oct-2025 event) on minute-level price + 5-minute leverage/order-flow data, testing rolling variance and lag-1 autocorrelation as critical-slowing-down early warnings. Finding: **the warning fingerprint is event-heterogeneous** — price shows critical slowing down in 5 of 7 events but *no* signal in two sudden tariff-shock cases (endogenous buildup vs exogenous shock); the Oct-2025 event warned in *leverage*, not price. The only cross-event consistency is a compression of taker order-flow variance — but that's a population-level indicator, not a per-event alarm. Conclusion: single-event critical-slowing-down claims in crypto derivatives are unreliable.
  - **Why it matters for trading:** An honest reality check on crash early-warning for leveraged crypto — you cannot rely on one universal precursor; endogenous vs exogenous cascades need different watch variables (leverage/order-flow vs price). Directly relevant to any crypto risk/liquidation-avoidance overlay.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (risk overlay reference; taker order-flow-variance compression worth monitoring)

## New resources & tooling
- **OpenMarket** — [arXiv:2607.26245](https://arxiv.org/abs/2607.26245) (Gregory Young). First public **millisecond-level paired Polymarket-BTC / Binance BTC-USDT corpus** with explicit pairing metadata: 727M deduplicated rows, 202 snapshots, 54 Polymarket / 57 Binance days (2026-02-12→05-15), 2.9M explicit lead-lag pairs, + a reproducible Rust pipeline. Central result is an **honest null**: a walk-forward logit over 43 microstructure features does *not* beat Polymarket's own order-book-implied probability (−0.116 normalized payoff/trade after fees). Cross-venue: Polymarket quotes respond to large Binance moves after ~347ms median. A gift for prediction-market ↔ spot microstructure research.
- **FinanceHarness** — [arXiv:2607.27853](https://arxiv.org/abs/2607.27853) (Xiao, Han, Chen et al., incl. Google). An autonomous financial deep-research framework (agentic multi-step research over financial sources). Relevant as tooling for the intelligence-gathering component itself; depth unverified this run — logged for evaluation.

## Watchlist updates
New authors added to `watchlist.md` this run:
- **Josh Molnar** — pre-registered structural BTC cycle timing (halving clock, time-since-genesis power law).
- **Francesco Landolfi** — distribution-aware drawdown risk (extends Rej-Seager-Bouchaud; four-measure MC framework).
- **Robert Jacob Ryan** — conformal-interval position sizing; exemplary pre-registration protocol.
- **Lucas Rabechini Amaral** — closed-form optimal microstructure mean-reversion bands.
- **Ramon Marc Garcia Seuma** — crypto-perpetual liquidation-cascade early-warning empirics.
(Halperin, Barzykin already tracked.)

## Open questions / threads to pull next run
- **Cross-sectional crypto is now the clear next backtest axis.** Halperin's rank-Markov three-matrix engine (2607.27461) is the most concrete, OOS-validated template — adapt the "vol-rank forecastable / return-rank not" split to a BTC/ETH/majors long-short. This is the exit from the exhausted daily-BTC single-series well (now 9 reject-leans incl. today's halving_clock).
- **Not verified in depth this run** (title/abstract only, chase next time): Kanazawa et al "exactly solvable diffusive price-dynamics paradox under long-range correlated order flow" (2608.00988); Ibikunle/Muravyev "Data-Driven Measures of HFT" (2608.00858); Izadyar "AI and Exchange Rate Predictability" (2608.00761, cross-listed widely); Halperin's second August paper on the same theme.
- **Forward paper-trading as a validation design.** Both Molnar and Ryan show the same lesson: low-n calendar/regime claims can only be validated *forward* under pre-registration, never by more in-sample slicing. Worth standing up a pre-registered forward tracker for the Molnar 2026 bottom window (Oct 5–Nov 16) as an honest out-of-sample test the backtest pipeline structurally cannot do.
