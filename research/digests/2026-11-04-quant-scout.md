# Quant Scout Digest — 2026-11-04

_14-day window since 2026-10-21. Swept fresh IDs above the 2610.28075 ceiling — the
late-October tail 2610.28xxx→2610.38xxx (q-fin.TR/ST/PM/CP/RM) and the full November
batch 2611.00xxx→2611.05xxx. Theory/honest-evaluation-heavy; the tradable crypto
findings are once again sub-daily (minute / 100 ms) — the daily cache cannot reach
them._

## TL;DR
- **The honest-evaluation thread lands two hard negatives on *live and adaptive* agents, not just offline search.** **OLIVIA** (Dehkordi/Kargarzadeh/Khaledian, 2611.03985): LLM news-reading on S&P 500, daily IC — commercial models align with the overnight move *into* the open (IC ≈0.074–0.077) but not the move *after* it, and **no pre-registered strategy survives costs + deflated-Sharpe → "the market reads the news first."** **PROMOTE** (Benhamou/Ohana, 2611.03384): an anytime-valid, cost-aware e-process that funds each candidate rule at birth and caps lifetime false-promotion probability under adaptive selection — **zero promotions after costs in market replay**; the sequential cousin of deflated-SR and the direct successor to "Propose, Don't Judge."
- **Only crypto-daily-adjacent finding → backtested → MIXED, leans REJECT (20th straight daily-crypto non-advance).** Bicki & Akdogan (2611.04533) measure a *preceding-trend* volatility leverage effect at minute resolution with a crypto-specific arrow-of-time component (BTC/ETH yes, US equities no), half-life ~1.5 h. The daily tradable translation (`trend_leverage`) confirms the asymmetry's sign in-sample but it decays into a low-exposure dial by the daily close — does not beat buy-and-hold, fails deflated-SR.
- **The strongest new crypto signal is sub-daily and on-chain:** Zhai & Ding (2611.05218) rebuild Hyperliquid L4 books with persistent wallet IDs — wallet profitability persists across 10-day windows (ρ=0.52), +11 identity features lift 1-sec OOS R² from 10.88% → ~12% on a 100 ms grid. The arXiv successor to Zhai's 2608.04373.
- **Cleanest replicable cross-sectional overlay this window:** Supriadi's Asym-Sticky-NCO (2611.05310) — downside semi-covariance NCO + sticky-HMM regime persistence for 11-sector rotation, 65 OOS months, CAGR 10.65%→13.41%, MaxDD 14.2% vs SPX 23.9%, turnover halved.
- **Blocker unchanged, now ~9× overdue: the hourly / multi-coin OHLCV loader.** Every tradable crypto finding this month lives at minute (2611.04533) or 100 ms (2611.05218) resolution.

## Findings by focus area

### ML / AI for alpha
- **Thinking Fast, Trading Late: System One Decision Models vs the Market (OLIVIA)** — Dehkordi, A. Kargarzadeh, N. Khaledian, Parvini, Ghatak, A. Khaledian, 2 Nov 2026 — [2611.03985](https://arxiv.org/abs/2611.03985)
  - **What it is:** OLIVIA is a protocol for testing whether LLM news readings predict S&P 500 daily returns while ruling out look-ahead, memorization and selection bias. "Decision models" are non-generative LMs that output calibrated probabilities for typed questions.
  - **Why it matters:** The sharpest honest-negative of the window. A fine-tuned model held IC 0.055/0.065 on two validation quarters but fell to 0.020 (t=1.7) on a blinded Jan–Jul 2026 test; commercial models' readings correlate with the overnight move *into* the open (IC ≈0.074–0.077) but not with the post-open move; name-masking fails (62–74% re-identification vs 28% baseline). **No pre-registered strategy survived costs and the deflated Sharpe.** Code: github.com/AmirDehkordi/NewsAction. Tracked players (Kargarzadeh/Khaledian lineage).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5 (methods + null, not a signal)
  - **Next step:** read (gate methodology; a reusable blinded-IC + deflated-SR harness)
- **Can We Stop the Backtest Yet? Anytime-Valid Promotion Tests for Adaptive Financial Research Agents (PROMOTE)** — Benhamou, Ohana, Guez, Setrouk, Saadi, Jacquot, 2 Nov 2026 — [2611.03384](https://arxiv.org/abs/2611.03384)
  - **What it is:** Each candidate rule is funded a predetermined share of "testing wealth" at birth; evidence accrues in a cost-aware e-process counting only post-birth returns; a weighted Ville argument bounds the probability of *ever* promoting a rule with nonpositive conditional mean, allowing dependent candidates, data-dependent births and indefinite monitoring.
  - **Why it matters:** The anytime-valid, sequential cousin of deflated-Sharpe and the direct successor to Qu/Chen/Wang "Propose, Don't Judge" (frozen referee) and the Giesecke/Gençay honest-eval lineage. Null replay: 94.5% family crossing under unadjusted repeated tests → 0 under PROMOTE; under an agent choosing candidates/births adaptively, 1.77% false-family crossings; **market replay produced zero promotions after costs.** Explicitly "not a certificate that an earlier edge remains profitable at deployment."
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read (candidate for the repo's own promotion gate once a multi-strategy search runs)
- **Are LLM Research Agents Reliable Judges of Predictability? Evidence from Planted-Signal Worlds** — Chang Liu, 4 Nov 2026 — [2611.04070](https://arxiv.org/abs/2611.04070)
  - **What it is:** Tests whether LLM research agents correctly judge predictability in synthetic worlds with *known planted signals* — a controlled probe of the judge side of agentic discovery.
  - **Why it matters:** Complements PROMOTE/OLIVIA from the evaluator angle: if the judge mis-rates ground-truth-known worlds, agentic factor pipelines inherit the error. Continues the "who judges sets false admissions" principle.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (methods read if a judge-agent is adopted)
- **CosmosAlpha: Multi-Relational Graph Search with Pareto-Guided Exploration for LLM-Driven Alpha Mining** — Z-H. Wang, Z-Y. Lang, Y-Y. Li, Q-Y. Lan, Piao, Nov 2026 — [2611.04555](https://arxiv.org/abs/2611.04555)
  - **What it is:** Proposer-side: a multi-relational graph search with Pareto-guided exploration for LLM alpha mining.
  - **Why it matters:** Continues the QuantaAlpha / AlphaPADI / AlphaPROBE proposer lineage; the counterweight to the referee-side papers above. Read alongside FactorBench's "no paradigm dominates."
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

### Microstructure & execution
- **Understanding the Inner Workings of a State-Space Foundation Model for Limit Order Books** — Mohl, Bismuth, Marti-Shahandeh, Nigmatulin, Li, Zohren, Foerster, Cucuringu, Calinescu, Oct 2026 — [2610.28753](https://arxiv.org/abs/2610.28753)
  - **What it is:** Interpretability of a state-space (Mamba-family) foundation model for LOBs — what the latent state actually encodes.
  - **Why it matters:** Tracked player Zohren/Oxford-Man; the interpretability companion to the generative-LOB and impact-benchmark work from the 10-21 run. Mechanism-understanding over black-box scores.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Calibration of Passive Market Impact with a Queue-Sensitive Propagator Model** — Hafsi, Lillo, Szymanski, Oct 2026 — [2610.38442](https://arxiv.org/abs/2610.38442)
  - **What it is:** A propagator model for *passive* (limit-order) market impact that is sensitive to queue position, with a calibration procedure.
  - **Why it matters:** Tracked player Lillo. Passive-impact calibration is the execution-cost layer a limit-order crypto maker would need; complements Barzykin's passive-impact optimal execution.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (execution cost-layer reference)
- **Non-Convex Market Makers: Coherence without Convexity, Friction, and Parallel Composition** — Peter Cotton, Oct/Nov 2026 — [2611.00502](https://arxiv.org/abs/2611.00502)
  - **What it is:** Extends automated-market-maker / scoring-rule theory to non-convex cost functions — coherence conditions without convexity, with friction and parallel composition.
  - **Why it matters:** Tracked player Cotton; broadens his OTC-quoting / covariance-damping lineage into AMM design relevant to on-chain venues.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve
- **TensorLOB: Structure-Preserving Tensor Learning for Limit Order Book Forecasting** — Gu, Mandic, Nov 2026 — [2611.02866](https://arxiv.org/abs/2611.02866)
  - **What it is:** A structure-preserving tensor-learning architecture for LOB forecasting.
  - **Why it matters:** Tracked player Mandic/Imperial GSP (the MINGLE / graph-signal lineage); parameter-efficient LOB prediction in the Hedges/Aste "architecture is the dependence structure" spirit.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve
- **Herding or Racing? Decomposing Cross-Account Order-Flow Persistence in On-Chain Markets** — Bai, Kan, Nov 2026 — [2611.02616](https://arxiv.org/abs/2611.02616)
  - **What it is:** Decomposes on-chain order-flow persistence into herding vs racing (latency-competition) components across accounts.
  - **Why it matters:** The mechanism layer under Zhai's wallet-identity result — whether persistence is correlated views (herding) or speed races changes how a wallet-identity feature should be used.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (pairs with 2611.05218)

### Risk & portfolio
- **Boom-Busty Marketron: How Investor-Market Reflexivity Amplifies Non-Equilibrium** — Igor Halperin, 31 Oct 2026 — [2611.01185](https://arxiv.org/abs/2611.01185)
  - **What it is:** A multi-asset model where one collective investor's demand moves prices and responds to performance (Soros reflexivity), driving a *non-equilibrium steady state* — stationary but never at rest, with a probability current circulating among mispricing, demand and volatility.
  - **Why it matters:** Tracked player Halperin; extends the Itkin/Halperin Marketron lineage. Calibrated to S&P 500 1996–2024, the boom-bust frequency lands inside the index's 1σ ranges, and the author argues the investor-market loop pushes further from equilibrium than leverage-driven stochastic vol alone — a structural account of why regimes cycle rather than settle.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Mitigating Return Drag and Regime Whipsaws in Sector Rotation: An Asymmetric Downside-Aware Nested Clustered Optimization Framework (Asym-Sticky-NCO)** — Supriadi, 3 Nov 2026 — [2611.05310](https://arxiv.org/abs/2611.05310)
  - **What it is:** Replaces symmetric covariance with a *downside semi-covariance* matrix in both the hierarchical clustering and the two-stage NCO allocation, plus a "Sticky Gaussian HMM" with a self-transition persistence prior to damp regime switching. 11 S&P 500 GICS sectors.
  - **Why it matters:** The cleanest replicable cross-sectional overlay this window and a convergence of three tracked threads — NCO/covariance-cleaning (Cotton/Goldberg-Kercheval), drawdown control, and regime persistence. Strictly non-anticipative walk-forward, 65 OOS months (Aug 2020–Dec 2025): vs Plain NCO, CAGR 10.65%→13.41%, total return 72.99%→97.74%; MaxDD suppressed to 14.22% vs SPX 23.93%; monthly turnover ~61%→30%; Calmar 0.94. The downside-semicovariance + sticky-HMM is a direct multi-asset backtest template (blocked on the loader).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest (needs a multi-asset/sector feed — blocked)
- **Penalize the Common Trade: A Collision-Aware Layer for Learned Portfolios** — Benhamou, Ohana, Guez, Setrouk, Saadi, Jacquot, Nov 2026 — [2611.03453](https://arxiv.org/abs/2611.03453)
  - **What it is:** A differentiable "collision-aware" layer that penalizes crowding (overlap with the common trade) inside a learned-portfolio policy.
  - **Why it matters:** The crowding-aware counterpart to Rodriguez Dominguez's capacity-as-causal-inference thread — builds the de-crowding penalty into the policy rather than measuring it after. Same prolific group as PROMOTE this window.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read
- **PanelGP: A Probabilistic Factor Model for Asset-Return Panels** — Ruglioni, Filipovic, Nov 2026 — [2611.04040](https://arxiv.org/abs/2611.04040)
  - **What it is:** A Gaussian-process probabilistic factor model for asset-return panels — calibrated uncertainty over factor structure.
  - **Why it matters:** Damir Filipovic is top-tier; a credible probabilistic alternative to point-estimate factor models, with the uncertainty quantification the risk layer usually lacks.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Robust distortion riskmetrics ×2** — (i) under symmetry, unimodality & Wasserstein constraints (P. Liu, Zhang, Zuo, 2611.01003); (ii) over Bregman–Wasserstein balls & their intersections (P. Liu, Vanduffel, Bernard, 2611.04021) — Nov 2026
  - **What it is:** Worst-case distortion risk measures over shape- and divergence-constrained ambiguity sets.
  - **Why it matters:** Continues the Ruodu-Wang-adjacent robust-risk-measure lineage (Carole Bernard, Steven Vanduffel are credible co-authors); the ambiguity-set machinery behind robust CVaR/EVaR portfolio construction.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Asset class / market (crypto)
- **How Market Volatility Responds to a Preceding Price Trend: a lag-resolved measurement in cryptocurrencies and equities** — Gulsah Bicki, Taylan Akdogan, 3 Nov 2026 — [2611.04533](https://arxiv.org/abs/2611.04533) — **(this run's backtest anchor)**
  - **What it is:** A minute-resolution (2020–2026) measurement of how volatility responds to a *preceding price trend* as a function of lag. For BTC/ETH the asymmetry is positive (leverage sign: down-trends → higher subsequent vol), strongest at ~20 min, half-life ~1.5 h; the asymmetry is split under time reversal and a **time-directed (arrow-of-time) component is detected for BTC and ETH but not for the three US stocks + SPY** at the 20-min lag.
  - **Why it matters:** A crypto-specific, short-lived, *directional* vol-response — the only new finding this window that maps to a cached crypto series. The tradable question: does the preceding-trend leverage asymmetry carry any exploitable edge at the daily close? (Answer below: no — it decays into an exposure dial.)
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** backtest (done — MIXED, leans REJECT; see below)
- **Beyond Anonymous Order Flow: Wallet Identity as a Feature for Short-Horizon Return Prediction** — Jingqiu Ding, Daojing Zhai, 3 Nov 2026 — [2611.05218](https://arxiv.org/abs/2611.05218)
  - **What it is:** Rebuilds full-depth Hyperliquid books from the L4 message feed (persistent pseudonymous wallet addresses). Wallet past-profitability persists across adjacent 10-day windows (Spearman ρ=0.52); 11 wallet-identity features raise 1-second OOS R² from 10.88% to ~12%, with a 3.11 bps covariate-adjusted markout in the top ventile.
  - **Why it matters:** The strongest new crypto predictive result of the window and the arXiv successor to Zhai's 2608.04373 "Public Trader Identity" — reputation is directly return-predictive when the venue is transparent. July 2026 record: 17.1B messages / 147k wallets / $84.3B taker notional across 10 markets, **100 ms grid.** Tracked player Zhai.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** backtest — blocked (needs on-chain L4 / sub-second feed, far below the daily cache)
- **Behavioral Prior Elicitation via LLM for Heterogeneous-Agent Bitcoin Flash-Crash Simulation** — Pham, Ngo, Nguyen, Nguyen, Ngo, Nguyen, Nov 2026 — [2611.03660](https://arxiv.org/abs/2611.03660)
  - **What it is:** Uses an LLM to elicit behavioral priors for heterogeneous agents in an agent-based BTC flash-crash simulator.
  - **Why it matters:** A synthetic-stress generator, not a signal — complements the Halperin reflexivity model and the SS-GEN rare-event line; useful for stress-testing, not timing.
  - **Scores:** Novelty 3/5 · Credibility 2/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

## New resources & tooling
- **AIDA: An AI Outage Registry with Evidence from On-Chain MEV** — Wu, [2611.01656](https://arxiv.org/abs/2611.01656) — a registry mapping AI-service outages to on-chain MEV evidence.
- **RiskReason** — Yousefi et al, [2611.01236](https://arxiv.org/abs/2611.01236) — a benchmark for *verifiable* financial risk reasoning (honest-eval tooling for the risk domain).
- **EventGPT** — Burakov, [2611.03302](https://arxiv.org/abs/2611.03302) — next-event pretraining on banking customer histories (event-sequence foundation model).
- **NewsAction** — github.com/AmirDehkordi/NewsAction — reference implementation of the OLIVIA blinded-IC protocol.

## Watchlist updates
- **Gulsah Bicki & Taylan Akdogan** — lag-resolved preceding-trend volatility leverage effect; crypto-specific arrow-of-time vol response (2611.04533).
- **Eric Benhamou / Jean-Jacques Ohana group (Homa Capital)** — prolific this window on the honest-eval + crowding axes: PROMOTE anytime-valid promotion (2611.03384) and the collision-aware learned-portfolio layer (2611.03453).
- **Amir Dehkordi + Amir/Arman Khaledian (OLIVIA / System-One)** — blinded-IC news-prediction protocol; upgrades the existing Kargarzadeh/Khaledian watchlist line.
- **Supriadi** — downside-semicovariance NCO + sticky-HMM regime-persistent sector rotation.
- **Jingqiu Ding** — Hyperliquid L4 wallet-identity return prediction (co-author with tracked player Daojing Zhai).
- **Yadh Hafsi & Grégoire Szymanski** — queue-sensitive propagator passive-impact calibration (with Lillo).
- **Damir Filipovic & Andrea Ruglioni** — PanelGP probabilistic (GP) factor model for return panels.

## Open questions / threads to pull next run
- **The hourly / multi-coin OHLCV loader is now ~9× overdue and is the single highest-leverage task.** Both tradable crypto findings this window (Bicki-Akdogan minute leverage, Zhai 100 ms wallet identity) and the last three months of crypto-native signals live at sub-daily/cross-sectional resolution the daily cache cannot touch.
- **Supriadi Asym-Sticky-NCO (2611.05310)** and **Benhamou collision-aware layer (2611.03453)** are the two cross-sectional templates worth a multi-asset backtest the moment a sector/multi-coin feed exists — both report honest walk-forward numbers.
- **The proposer↔referee arms race hardens:** CosmosAlpha (proposer) vs PROMOTE / planted-signal judges (referee). Worth a methods read to decide whether the repo should adopt PROMOTE as its promotion gate once more than one strategy is searched at once.
- Next ceiling: **2611.05310**.

---

## Backtest — trend_leverage on BTC-USD → MIXED, leans REJECT
Anchored to **Bicki & Akdogan 2611.04533** (preceding-trend leverage effect). New
strategy `trend_leverage`: a self-adapting calm-regime long/flat vol gate whose vol
forecast is asymmetric in the sign of the **preceding multi-day price trend** (the
paper's exact conditioning variable + its arrow-of-time claim), distinct from
`asym_longmem_vol`, which keyed asymmetry on the per-bar shock sign. γ=1 is the built-in
symmetric control. Real cached BTC (2922 daily bars, offline).

- **Stage-1 winner** γ=3.0, L=20, q=0.6: train Sharpe **0.706**, CAGR 21.2%, deflated-SR
  0.493. **The confirming tell:** the two *asymmetric* arms (γ=3.0, γ=2.0) rank #1–2,
  above every *symmetric* γ=1.0 control (ranks 3–5, ≈0.55–0.59) — the preceding-trend
  leverage asymmetry buys ~0.11 in-sample Sharpe, exactly the sign Bicki-Akdogan measure.
- **OOS** Sharpe 0.474, CAGR 9.5%, MaxDD −29.4% (strong drawdown protection in the stormy
  test window).
- **BUT fails deflated-SR (0.425 full) and does NOT beat buy-and-hold.** Reconciled by
  direct computation on the full cache (engine's 252-day annualisation): trend_leverage
  winner (10 bps/side) full Sharpe **0.526 / CAGR 12.9% / MaxDD −69.9%, 57% time-in-market**
  vs **BTC B&H 0.639 / 21.4% / −76.6%**. The Sharpe lands near B&H only because it holds
  BTC's up-drift ~57% of the time while sitting out some storms — a **low-exposure dial /
  crash insurance**, not alpha.
- **Does NOT falsify the paper** — 2611.04533 is a minute-scale vol-response measurement
  (half-life ~1.5 h) that makes no daily-return claim. By the daily close the asymmetry
  has washed into an exposure dial, exactly as the quarter-hour effect did
  (`dow_seasonality`) and every vol-statistic gate did (`vol_regime`, `evar_regime`,
  `asym_longmem_vol`). **The vol-asymmetry axis is now quadruple-exhausted on daily
  single-series crypto; 20th straight daily-crypto non-advance.** The trend-sign-
  conditioned vol forecast is the right implementation layer to carry onto an intraday
  feed — but cannot be tested here. Report:
  `backtests/reports/2026-11-04-trend_leverage-BTC-USD.md`.
