# Quant Scout Digest — 2026-07-29

_14-day catch-up since the 2026-07-15 run. Swept the whole 2607.13xxx→2607.25xxx
window (q-fin.TR / PM / ST / RM / CP) above the prior ceiling **2607.12990**. New
ceiling: **2607.25599**._

## TL;DR
- **Two independent, rigorous audits gut popular retail/candle timing signals** — Darmanin (2607.20093): 5 signal families, correct for multiple comparisons + costs + leverage-survival, "**none is SUPPORTED**", trend/momentum merely *unresolved* (too little data); Jadouli (2607.19453): candle-based Binance-spot ML timing, ROC-AUC 0.87–0.90 but **executable policy value = NO_TRADE**, a 10-pair selector **lost 6.72%** over 19 cycles after costs, underperforms buy-and-hold. Both *independently confirm* our 7-straight daily-BTC-reject thread with better statistics than we run.
- **The vol-target overlay axis has a fresh anchor:** Lee/Shirvani/Afroz/**Rachev**/**Fabozzi** (2607.16450) — GJR-GARCH asymmetric vol + heavy tails → CVaR allocations are *systematically more concentrated* than mean-variance. → **today's backtest target** (`vol_regime` on BTC-USD).
- **Sepp & Lucic (2607.19497), "The Science and Practice of Trend-Following Systems"** — practitioner-grade closed-form theory: trend PnL = "excess spectral mass at low frequencies," profitable iff long-horizon autocorrelation > 0 even amid short-term mean-reversion; structural positive skew; closed-form Sharpe + cost-adjusted span selection. Direct post-mortem lens on our closed BTC-trend thread.
- **RL cross-sectional axis heats up:** Halperin & Itkin SciPhy (2607.15195, HJB-via-PINN, one-shot offline) and Belyakov AlphaZeroBeta (2607.18001, CNN-GRU Recurrent-PPO **market-neutral**, 7 indices) — both report Sharpe gains; the market-neutral framing is the cross-sectional-crypto direction the thread flagged.
- **Risk-model plumbing:** Alouadi & **Lehalle** CD-DFM (2607.24410) builds covariance from *fundamentals* w/ zero-shot onboarding of new assets; Bongiorno/**Mantegna** (2607.23068) compact NN min-variance for vol-drag control under leverage.

## Findings by focus area

### ML / AI for alpha
- **SciPhy Reinforcement Learning for Portfolio Optimization** — Igor Halperin & Andrey Itkin, 2026-07-16 — [link](https://arxiv.org/abs/2607.15195)
  - **What it is:** Physics-informed RL that reformulates portfolio choice as a Hamilton-Jacobi-Bellman equation solved *pathwise* by a PINN in one offline pass over historical trajectories (no policy/value iteration). Tested on a 14-asset ETF book.
  - **Why it matters for trading:** A continuous-time, cost-and-vol-aware allocator trained without a simulator or reward-shaping loop; the "solve HJB on observed paths" trick is a cleaner alternative to model-free RL for a small liquid universe like BTC/ETH + majors.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (method reference; hard to replicate cheaply)
- **AlphaZeroBeta: Deep Reinforcement Learning for Market-Neutral Portfolios** — Boris Belyakov, 2026-07-20 — [link](https://arxiv.org/abs/2607.18001)
  - **What it is:** CNN-GRU policy trained by Recurrent PPO with a composite reward (risk-adjusted alpha + low benchmark correlation + costs); walk-forward across 7 equity indices 2014–2024, reports higher Sharpe than factor/convex baselines at near-zero beta.
  - **Why it matters for trading:** The **market-neutral / cross-sectional** framing is exactly the axis our thread flagged after daily single-series BTC kept failing — the tradeable crypto analogue is a BTC-vs-ETH-vs-alt long/short, not a single-series timer.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (equities-only; port the market-neutral idea, not the code)
- **FinBench: Time-Gated Calibration and Uncertainty Benchmarking for Agentic Financial Forecasting** — Rishab Ghosh & Vinay Devarakonda, 2026-06-24 (surfaced this window) — [link](https://arxiv.org/abs/2607.16229)
  - **What it is:** A strictly time-gated benchmark that scores LLM forecasts on *calibration* (Brier + Winkler interval scores on P(up) and 80% log-return intervals) vs hard baselines, separating "confident-but-fragile" from genuinely uncertainty-aware models.
  - **Why it matters for trading:** Reinforces our own gate discipline — accuracy without calibration and without a time-gate is the exact trap the audits below expose. Proper-scoring + look-ahead lockout is the standard our backtests should keep meeting.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (methods reference for gates)

### Microstructure & execution
- **Herding and Liquidity in Order-Book Markets. II. Fundamental Anchoring and the Resilience of Liquidity** — Jan Novotny, 2026-07-18 — [link](https://arxiv.org/abs/2607.16970)
  - **What it is:** Part II of the tracked thread (Part I = 2607.08907, captured 07-15). Anchoring price to a fundamental value is the *intrinsic* stabiliser — it lets order books refill and mean-revert after shocks; remove the anchor and self-sustaining fire sales emerge. Stressed markets fail to transmit liquidity crises to neighbours across multiple channels.
  - **Why it matters for trading:** Reframes liquidity crises as failures of fundamental anchoring, not market-maker dysfunction — relevant to crypto, where a weak/absent fundamental anchor predicts the fire-sale reflexivity we already model as crash risk (the case *for* a vol-regime overlay).
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (theory; continues tracked thread)

### Risk & portfolio
- **Portfolio Optimization under Heavy Tails and Asymmetric Volatility: Evidence from Taiwan-Exposed ETFs** — Ting-Jung Lee, Abootaleb Shirvani, Farzana Afroz, Svetlozar T. Rachev, Frank J. Fabozzi, 2026-07-17 — [link](https://arxiv.org/abs/2607.16450)
  - **What it is:** 30 Taiwan-exposure ETFs, 2015–2025. Hill tail-index → heavy tails across the universe (semis worse); GJR-GARCH → persistent *asymmetric* vol (negative shocks raise conditional vol more); CVaR optimization yields **substantially more concentrated** allocations than mean-variance, and rankings flip depending on variance- vs tail-based measures.
  - **Why it matters for trading:** The tradeable daily analogue for a single crypto series is a **volatility-managed overlay** — hold the asset only while realized vol sits in a calm regime, step aside on spikes (Moreira-Muir flavor). This is the exact "vol-target overlay" next-axis the thread has been pointing at since 07-04.
  - **Scores:** Novelty 3/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** **backtest** → `vol_regime` on BTC-USD (this run)
- **The Science and Practice of Trend-Following Systems** — Artur Sepp & Vladimir Lucic, 2026-07-21 — [link](https://arxiv.org/abs/2607.19497)
  - **What it is:** Unified closed-form framework for European / American / TSMOM trend systems. Trend PnL comes from "excess spectral mass at low frequencies"; systems are profitable iff long-horizon autocorrelation is positive (works even under short-term mean-reversion), with structurally positive skew; gives closed-form Sharpe and cost-adjusted span selection.
  - **Why it matters for trading:** A rigorous post-mortem lens on our **closed BTC-trend thread** — it predicts exactly when trend has no edge (no low-freq spectral mass / non-positive long-horizon autocorr), which is what our six trend tests found on BTC. Best single reference for *why* those rejects were structural, not tuning.
  - **Scores:** Novelty 3/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (theory reference; frames the trend rejects)
- **The Fundamental Structure of Risk: From Characteristics to Covariance** — Alexandre Alouadi & Charles-Albert Lehalle, 2026-07-27 — [link](https://arxiv.org/abs/2607.24410)
  - **What it is:** CD-DFM — a latent-factor ML model that builds asset covariance from *company fundamentals* rather than noisy return history, learning interpretable factor exposures and enabling **zero-shot onboarding of unseen assets** (no retrain).
  - **Why it matters for trading:** Competitive covariance forecasts without a long return sample is directly useful for evolving universes / new listings — the crypto pain point is exactly short/unstable histories. Lehalle co-authorship raises the credibility bar.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (equities-fundamentals; watch for a crypto-characteristics analogue)
- **Neural Network-Driven Volatility Drag Mitigation under Aggressive Leverage** — Christian Bongiorno, Efstratios Manolakis, Rosario N. Mantegna, 2026-07-25 (ICAIF '25) — [link](https://arxiv.org/abs/2607.23068)
  - **What it is:** Compact min-variance NN (39.6k→2.2k params) — a 5-parameter hyperbolic weighted MA + saturating exponential for features, plus a bidirectional-GRU covariance-cleaning module; lower realized variance than SOTA and "enhanced over-leverage resilience" with preserved drawdown control in margin-realistic sims.
  - **Why it matters for trading:** Vol-drag under leverage is the crypto perpetuals problem in one line; a small, transparent covariance-cleaner that survives realistic margin dynamics is a plausible sizing layer over a leveraged BTC/ETH book.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (sizing/leverage reference)

### Asset class / market
- **Predictive Extrema, Unprofitable Policies: An AI-Assisted Audit of Candle-Based Binance Spot Timing Models** — Ayoub Jadouli, 2026-07-21 — [link](https://arxiv.org/abs/2607.19453)
  - **What it is:** Forensic, fixed-seed, deterministic-simulator audit of candle-based ML timing on Binance-spot OHLCV (code on GitHub). Result is decisively negative: **no positive executable policy value** across protocols (all decisions NO_TRADE); ROC-AUC 0.87–0.90 did *not* translate to profit; a 10-pair selector **lost 6.72%** over 19 cycles at assumed costs, below buy-and-hold.
  - **Why it matters for trading:** A clean, reproducible demonstration that **high classification metrics ≠ tradeable edge** on crypto candles after costs — the same wall our daily-BTC tests keep hitting. Strong external confirmation of the "single-series daily crypto is tapped out" thesis, and a template for AUC-vs-policy separation.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read (confirmatory; methods template for our gates)
- **Retail Trader's Ruin: An Anatomy of Popular Signal Failure** — Adam Darmanin, 2026-07-22 — [link](https://arxiv.org/abs/2607.20093)
  - **What it is:** Evaluates 5 popular signal families (trend, oscillator, candlestick, volume, calendar) for a *genuine* edge after costs, with multiple-comparisons correction, economic-viability tests, and leverage survival analysis. Verdict: 4 of 6 candidates statistically refuted; trend & momentum *unresolved* (insufficient sample) — "**none is SUPPORTED.**"
  - **Why it matters for trading:** This is the honest-gate paper of the window — it operationalizes exactly the discipline (MC correction + cost + survival) that separates a real edge from grid luck, and its verdict mirrors our own daily-crypto reject streak. Calendar-rule refutation independently backs our `dow_seasonality` REJECT.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read (methods must-read; adopt MC-correction + survival framing)
- **Are cryptocurrencies real financial bubbles? Evidence from quantitative analyses** — Marco Bianchetti, Camilla Ricci, Marco Scaringi, 2026-07-23 (v2; first version 2017) — [link](https://arxiv.org/abs/2607.21826)
  - **What it is:** LPPL (OLS/GLS/MLE) + Phillips-Shi-Yu explosive-root tests on BTC/ETH; detects bubble signatures before major crashes and reads crypto excursions as exuberance-driven departures from fundamentals.
  - **Why it matters for trading:** LPPL/PSY explosive-root monitors are a cheap, well-understood *crash-warning* overlay that pairs naturally with a vol-regime filter. Caveat: this is a v2 refresh of a 2017 study on 2016–2018 data — treat as method reference, not new evidence.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (dated sample; keep LPPL/PSY on the crash-overlay shortlist)

## New resources & tooling
- **Jadouli — candle-timing audit code** (GitHub, linked from 2607.19453) — a reproducible, fixed-seed harness for AUC-vs-executable-policy separation on Binance OHLCV; useful as an external sanity check on our own gate logic.

## Watchlist updates
- **Artur Sepp & Vladimir Lucic** — practitioners; closed-form trend-following theory (spectral mass / low-freq autocorrelation, cost-adjusted span selection). _Add to Global players._
- **Charles-Albert Lehalle** (w/ Alouadi) — execution/microstructure heavyweight; here on fundamentals-driven covariance (CD-DFM, zero-shot asset onboarding). _Add to Global players._
- **Igor Halperin & Andrey Itkin** — physics-informed RL for portfolio choice (HJB-via-PINN, SciPhy). _Add to Global players._
- **Rosario N. Mantegna / Christian Bongiorno** — econophysics; compact NN covariance cleaning, vol-drag under leverage. _Add to Global players._

## Open questions / threads to pull next run
- **Backtest axis has officially moved off direction/trend → onto exposure management.** `vol_regime` (this run) is the first vol-target test; if it behaves as crash-insurance-not-alpha (predicted), the *next* backtest axis is **cross-sectional crypto** (BTC/ETH long-short), which both AlphaZeroBeta and the market-neutral framing point at.
- **Adopt Darmanin's gate stack** (multiple-comparisons correction + leverage-survival analysis) into our own deflated-Sharpe report — our gate currently does DSR but not explicit survival-under-leverage.
- **LPPL / PSY explosive-root crash monitor** (Bianchetti) as a companion overlay to vol_regime — worth a small standalone test if vol_regime shows drawdown value.
- Ceiling for next run: **2607.25599** (top CP ID this window). Watch for the 2608.xxxxx August batch.
