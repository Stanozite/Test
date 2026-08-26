# Quant Scout Digest — 2026-08-26

_7-day window since 2026-08-19. Swept arXiv q-fin (TR/PM/ST/CP/RM) IDs above the
prior ceiling 2608.18022 → top of batch ~2608.24786. Dedup checked against
`research/INDEX.md`._

## TL;DR
- **A crypto-native directional signal finally surfaces — and it's the sign-reversal thread again.** Kitron & Wengrowicz (2608.21888): at **15-minute** horizons, **90% of 183 Binance pairs** show significant *directional* mean reversion vs **2.7% of 187 US stocks/ETFs**, in every focal coin-year since 2021. The edge **lives in signs, not magnitudes** (lag-1 autocorr ≈ 0 on majors, yet "bet against the previous candle" captures most of it) — but gross edge peaks at **~1.3 bps/trade**, marginal after 5 bps costs. → **backtest target** (daily analogue).
- **KellyBoost** (2608.23393): a single multi-output XGBoost whose softmax output *is* the portfolio, trained on the **exact** negative-log-growth (Kelly) loss with closed-form gradient + Hessian — not a surrogate. Growth-optimal allocation as one gradient-boosted model, dependency-free reference engine shipped.
- **Reconfiguration Premium** (2608.20020): the *rate at which the correlation map turns* — mean-squared sine of principal angles between consecutive 12-mo S&P500 subdominant eigenspaces — is **priced into the variance risk premium (t = 5.40)**; only the *persistent* component is paid, mechanism is "prepayment" (IV up on impact, RV lags 2–3 quarters). Pre-registers **no timing alpha, no crash protection**.
- **Itkin Lean Marketron** (2608.20589): reduces the inelastic-market Marketron **18→9 params** (kills scaling gauges/sign symmetries), log-price obeys a **generalized Langevin equation with state-modulated memory kernel**, makes "market price of flow risk" identifiable, and the well-separated relaxation rates imply a **driven non-equilibrium** market.
- **Backtest: lag1_reversal on ETH-USD → REJECT** — first non-BTC test in the repo. Faithful daily form of 2608.21888's "fade the previous candle": train Sharpe **0.379** → **OOS −0.322, CAGR −13.4%**, full-sample deflated-SR **0.011**. The 15-min crypto reversal **aggregates away by the daily close on ETH too** (as it did on BTC, 07-01). **13th straight daily-crypto reject** — and the daily null now **generalizes across coins**, not just BTC.

## Findings by focus area

### ML / AI for alpha
- **KellyBoost: Growth-Optimal Portfolio Construction with Gradient-Boosted Trees** — Jiayu Li, 2026-08-24 — [link](https://arxiv.org/abs/2608.23393)
  - **What it is:** one multi-output XGBoost model; softmax output = portfolio weights; training loss = `−log(1 + w·y)` (negative log growth rate), so the fit *is* the feature-conditioned Kelly allocation. Exact objective (not a surrogate): closed-form gradient, analytic diagonal + full Hessian, finite-difference-verified, dependency-free engine.
  - **Why it matters for trading:** collapses "predict returns → optimize weights" into a single growth-optimal fit; the exact-Hessian derivation is directly reusable. Caveat: on a *single* asset Kelly degenerates to leverage sizing — the method needs a cross-section to be interesting.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** shelve (no cross-sectional crypto feed yet) — revisit as the template for a multi-coin allocator.
- **Harvesting the Volatility Risk Premium: A Learning-to-Rank Approach** — Maciej Wysocki (UW QFRG), 2026-08-25 — [link](https://arxiv.org/abs/2608.24786)
  - **What it is:** LightGBM LambdaRank over the **SPXW 0DTE** surface ranks 9 strategies (8 short-put + skip) against a Sortino label, with margin-aware sizing, uncertainty-driven abstention, strict out-of-time split (train 2021–24, held-out 2025).
  - **Why it matters for trading:** end-to-end cross-sectional LTR applied to options selection with realistic margin/fees. **Skeptic flag:** headline **OOS Sharpe 5.59 (range 4.31–5.76), MaxDD −2.28%, PSR 0.964** on a *single calm* held-out year is extraordinary for a short-vol book — 0DTE short puts under-sample their own tail; one held-out year cannot see the crash the structure is short. Treat as method, not as a validated 5-Sharpe edge.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (equity-options, no data feed); keep the LTR-for-selection + abstention machinery as reference.

### Microstructure & execution
- **Multi-Level Market Making with Reinforcement Learning** — Patrick Cheridito, Moritz Weiss (ETH Zürich), 2026-08-18 — [link](https://arxiv.org/abs/2608.18195)
  - **What it is:** RL market maker that submits market + limit orders of varying size across **multiple LOB levels** under inventory control; multivariate logistic-normal order-allocation head, deep-set encoder for variable-length book features, potential-based reward shaping.
  - **Why it matters for trading:** the multi-level allocation head + deep-set encoding is a cleaner MM action parameterization than single-quote AS/CJ setups; tested against noise/tactical/strategic synthetic flow.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (needs LOB sim); reference for MM action design.
- **Concentrated Liquidity Provision: a Reinforcement Learning Perspective** — Chionas, Kleitsikas, Leonardos, Sánchez-Betancourt, Ventre, 2026-08-19 — [link](https://arxiv.org/abs/2608.19389)
  - **What it is:** RL for concentrated-liquidity (Uniswap-v3-style) LP range management — where to place and when to reset the active tick band.
  - **Why it matters for trading:** on-chain LP is a live crypto-native yield/impermanent-loss control problem; Ventre/Sánchez-Betancourt group is credible on execution RL.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read — closest to an actionable on-chain crypto strategy this window.
- **Calibrating Inelastic Markets to Options: The Lean Marketron and the Generalized Langevin Equation** — Andrey Itkin, 2026-08-20 — [link](https://arxiv.org/abs/2608.20589)
  - **What it is:** removes structural non-identifiability in the Marketron inelastic-market model — **18→9 params** by killing scaling gauges/sign symmetries + freezing non-financial params — enabling single-parameter-set SPX-surface calibration. Log-price ⇒ **generalized Langevin equation with state-modulated memory kernel**; "market price of flow risk" becomes identifiable; signal vs memory relaxation rates come out well-separated ⇒ **driven, non-equilibrium** regime.
  - **Why it matters for trading:** a calibratable inelastic-flow model of the whole vol surface with an explicit, testable non-equilibrium condition — flow-impact as a priceable, identifiable quantity.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (theory reference; Itkin is on the watchlist).
- **M3: A State-Event Generative Foundation Model for Market Microstructure Dynamics** — Zhang, Ma, Cheng, Li, Duan, 2608.19227 (revision surfacing this window) — [link](https://arxiv.org/abs/2608.19227)
  - **What it is:** foundation model that jointly generates **order events × LOB states** (their interplay, which prior models split), trained on large-scale order-level data; shows scaling behavior + stylized-fact reproduction for counterfactual trajectory simulation.
  - **Why it matters for trading:** a scalable simulator for stress-testing, market-impact, and execution-policy training — the generative counterpart to FlowLOB (2608.13096) captured last window.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (simulation infra).
- **Tradable Itô Signatures: A Model-Free, Interpretable Framework for Dynamic Hedging** — Guo, Wang, Zhang, 2608.18120 (revision surfacing this window) — [link](https://arxiv.org/abs/2608.18120)
  - **What it is:** discretized Itô-signature components are **replicable by simple self-financing strategies**, so nonlinear payoffs become *linear combinations of tradable signature instruments* — model-free hedging with error bounds, no future-conditional-expectation estimation; beats NN benchmarks on SPX options.
  - **Why it matters for trading:** turns the signature transform into an actual basis of hedging instruments — interpretable, sample-efficient, assumption-light.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (hedging reference).

### Risk & portfolio
- **Dynamic Portfolio Optimization under CVaR Constraints** — Anran Hu, Silvana M. Pesenti, Xiaofei Shi, 2026-08-20 — [link](https://arxiv.org/abs/2608.20179)
  - **What it is:** continuous-time dynamic allocation with a **CVaR constraint on terminal loss**; auxiliary-threshold CVaR representation gives existence + strong duality **without market completeness**; nested bisection–golden-search reduces to unconstrained stochastic control.
  - **Why it matters for trading:** binding CVaR produces **asymmetric reallocation** — cut risk after adverse outcomes, hold/add after favorable ones — a formalization of state-dependent de-risking (recovers Merton when slack). Price impact slows adjustment.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** read — the theory behind the "regime gate" family we keep backtesting.
- **The Reconfiguration Premium: Co-movement Structure as an Unspanned Dimension of the Variance Risk Premium** — Lucas Carvalho, 2026-08-20 — [link](https://arxiv.org/abs/2608.20020)
  - **What it is:** measures how fast the cross-section's organizing axes turn — mean-squared sine of principal angles between subdominant eigenspaces of consecutive 12-mo S&P500 correlation matrices (a typical month rewrites ~1/5, carries ~4/5 forward). That **rate is priced into the aggregate VRP (t = 5.40)**; no level measure correlates > 0.32; implied-correlation surface spans ≤ 6.7% of it. Only the *persistent* component is paid; mechanism = prepayment (IV up on impact, RV lags 2–3 quarters, sim-null p < 0.03).
  - **Why it matters for trading:** a genuinely new, unspanned risk-premium dimension — the *pace of correlation-structure revision*, distinct from level/variance. Honestly pre-registers three nulls that hold: **no timing alpha, no crash protection, downside inseparable from intensity.**
  - **Scores:** Novelty 5/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read — sharpest conceptual finding this window.
- **The Market's Conditioning Representation: Equilibrium, Crowding, and Convention Multiplicity** — Alejandro Rodriguez Dominguez, 2026-08-18 — [link](https://arxiv.org/abs/2608.18299)
  - **What it is:** portfolios endogenously select feature *representations* whose induced exposures move prices; a spectral threshold (cross-impact · covariance · deployed capacity) splits three regimes — unique equilibrium below, innovation-free variations at, **a continuum of self-confirming conventions above**. Monotone impact preserves uniqueness; indefinite impact alone can't guarantee multiplicity. Documents a driver-specific signature consistent with **representation crowding** (info-capacity cost *beyond* position crowding), but the threshold stays unestimated.
  - **Why it matters for trading:** extends his crowding/capacity line (2608.08405, 2607.06702) — crowding isn't just too much capital on one signal, it's too much capital on overlapping *representations of the same drivers*.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (theory; threshold not yet measurable).

### Asset class / market
- **Short-horizon mean reversion in cryptocurrency markets: a matched cross-market measurement** — Nadav A. Kitron, Jonathan M. Wengrowicz, 2026-08-22 — [link](https://arxiv.org/abs/2608.21888) — ⭐ **backtest target**
  - **What it is:** under one matched, strictly-OOS protocol at **15-min** horizons, **90% of 183 Binance pairs** carry significant *directional* reversal vs **2.7% of 187 US stocks/ETFs**, in every focal coin-year since 2021. The signal is in **signs, not magnitudes**: lag-1 autocorr ≈ 0 on majors, yet "bet against the previous candle" captures most of it. Gross edge peaks ~**1.3 bps/trade**; class-mean AUC gap +0.011 (95% CI [+0.008,+0.014]) under conservative accounting — **marginal after 5 bps round-trip**.
  - **Why it matters for trading:** the cleanest crypto-vs-equity contrast on short-horizon reversal to date, and it directly extends the Portnaya "bounce has no direction" (2606.29591) thread — reversal is real intraday on crypto but sign-based and thin. Sets up an honest daily boundary test.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** **backtested this run** (daily analogue on ETH-USD → REJECT; see below).
- **Equilibrium in closed constant-function market maker economies** — Muqiao Huang, Ruodu Wang, Yiyun Wang, 2026-08-24 — [link](https://arxiv.org/abs/2608.23915)
  - **What it is:** 2-asset/2-trader fee-free CFMM: an interior unilateral no-trade equilibrium ⟺ CFMM marginal price = both traders' MRS; IR unilateral equilibria are Pareto-optimal vs the fixed invariant; alternating utility-maximizing trades converge to it; derives first-mover advantage/disadvantage conditions.
  - **Why it matters for trading:** foundational micro-theory for on-chain AMM trading order and LP outcomes; Ruodu Wang (watchlist) on the risk-measure side of DeFi.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 1/5
  - **Next step:** shelve (theory reference).

## New resources & tooling
- **Where Does Ethereum Validators' Money Go? A Spectral Analysis** — Irene Aldridge, 2608.23577 — [link](https://arxiv.org/abs/2608.23577) — empirical spectral map of ETH validator revenue flows (staking/MEV economics reference).
- **tse_tick** — Li/Hayashi/Nakatsuma/Romero, 2608.23053 — [link](https://arxiv.org/abs/2608.23053) — Python library for parsing/querying Nikkei NEEDS TSE tick data (data infra for Japanese microstructure).
- **KellyBoost reference engine** — dependency-free growth-optimal XGBoost implementation shipped with 2608.23393 (see above).

## Watchlist updates
- **Patrick Cheridito / Moritz Weiss (ETH Zürich)** — multi-level RL market making (2608.18195).
- **Andrey Itkin** — already tracked (Andersen & Itkin); note his solo inelastic-markets / GLE line (2608.20589) alongside the derivatives-pricing work.
- **Anran Hu / Silvana Pesenti / Xiaofei Shi** — dynamic CVaR-constrained control, duality without completeness (2608.20179).
- **Lucas Carvalho** — reconfiguration premium / eigenspace-rotation asset pricing (2608.20020).
- **Nadav A. Kitron / Jonathan M. Wengrowicz** — matched cross-market crypto microstructure; short-horizon sign-reversal (2608.21888).
- **Jiayu Li** — exact-Kelly gradient-boosted portfolios (2608.23393); also 2608.23416 "The Axiomatic Trader" (canonical form of a quant system).

## Open questions / threads to pull next run
- **Cross-sectional crypto is now quintuple-blocked, and this run confirms *why it matters*.** The daily sign-reversal null now holds on **both** BTC (07-01) and ETH (this run) — single-series daily is definitively exhausted. But 2608.21888's real result is *cross-sectional and intraday*: 90% of 183 pairs reverse at 15-min. The unblocked edge requires (a) a 15-min/hourly bar feed and (b) a multi-coin panel — the same feed the Choi/MINGLE/MFCCA/Halperin/Aste cross-sectional thread has been waiting on. **Next infra priority: an hourly multi-coin OHLCV loader.**
- Does the **Reconfiguration Premium** (2608.20020) have a crypto analogue — is the *rate of rotation* of a crypto correlation matrix priced, given crypto's faster regime turnover? No implied-correlation surface exists, but realized-eigenspace rotation is computable.
- **Concentrated-liquidity RL** (2608.19389) is the most actionable on-chain idea this window — worth a read to see if the LP-range policy is replicable off a DEX pool feed.
- Ceiling for next run: **2608.24786** (top verified ID this sweep).
