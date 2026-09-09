# Quant Scout Digest — 2026-09-09

_7-day window since 2026-09-02. Swept arXiv q-fin (TR/PM/ST/CP/RM) above ceiling
2608.31041 into the fresh 2609.0xxxx batch (~1 week into the month, so a thin,
theory-heavy tape). Deduped against the INDEX ledger. All items verified against
their arXiv abstract pages._

## TL;DR
- **Rosenbaum lands a clean theorem with a tradable corollary:** under market impact
  with heterogeneous horizons, the predictable (Volterra / long-memory) signal and the
  aggregate impact term **cancel at equilibrium → observed price is a pure martingale**
  (2609.03115). We backtested the corollary on daily BTC — see below.
- **This is a "no persistent net alpha" week on the AI front, from two directions:**
  Giesecke's group formalizes evaluating the *discovery system* not just its outputs
  and reports negative/limitation findings (AEAP, 2609.00731); a 32-page review finds
  **no AI architecture delivers persistent, cross-regime, capacity-aware net alpha** in
  audited public records (2609.04917).
- **Tracked player Rodriguez Dominguez ships a pair:** costly portfolio-representation
  switching *generates* long-memory order flow, one tail exponent governing spell
  duration + order-flow memory + the scaling breakdown (2609.02525); plus uniform
  (not pointwise) inference for **certified strategy capacity** near reflexive stability
  boundaries with an abstention regime (2609.02535).
- **Risk-measure surprise:** under *unknown* cross-asset dependence, robust optimization
  says **concentrate in one asset**, not diversify (Liu & Liu majorization, 2609.04496)
  — the mirror image of the diversification-backfires superadditivity thread.
- **Backtest: `volterra_signal` on BTC-USD → MIXED, leans REJECT.** Faithful power-law
  long-memory momentum kernel (the paper's Volterra signal): train Sharpe 1.063 →
  **OOS 0.242, CAGR 3.0%**, full deflated-SR **0.308** (hard fail). The tell that
  *confirms* Rosenbaum: edge is **monotone-decreasing in memory length** (30>60>120d) —
  the genuinely long-memory component is exactly the part with no exploitable signal.
  **15th straight daily-crypto reject-lean.**

## Findings by focus area

### ML / AI for alpha

- **Agentic Empirical Asset Pricing: Methodological Foundations** — Yingjian Pan,
  Xiaowei Ding, Kay Giesecke, 2026-09-01 — [link](https://arxiv.org/abs/2609.00731)
  - **What it is:** A paradigm + reference architecture + evaluation standard for
    LLM-agent factor-discovery systems, arguing existing practice backtests only the
    *outputs* (factors/trades), never the autonomous *discovery system* that produced
    them. Their implementation (SEADS) is tested vs five baselines on US equities;
    "no single metric ranks the systems consistently" → multidimensional evaluation,
    with a rolling re-execution analysis of discovery reliability over time.
  - **Why it matters for trading:** This is the evaluation-hygiene layer directly above
    this repo's own gates — it extends the Gençay "honest evaluation" and AgonAlpha
    threads from "was this *strategy* overfit?" to "is this *strategy-generator* reliable
    across regimes?" Giesecke is a credible name (Stanford asset-pricing/ML).
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (methods — adopt the discovery-system evaluation protocol)

- **Artificial Intelligence in Equity and Crypto Markets: Progress, Profitability
  Evidence, and the Limits of Automated Investing** — Linsen Zhu, Mengqing Cai,
  2026-09-04 (review, lit. through 2026-08-31) — [link](https://arxiv.org/abs/2609.04917)
  - **What it is:** A 32-page review organizing the field along an "alpha-translation
    chain" and concluding that **no general AI architecture is shown to deliver
    persistent, cross-regime, capacity-aware net alpha** in examined public records.
    Upstream prediction progress coexists with predictor decay, look-ahead failures,
    survivorship bias, cost/venue/capacity frictions; crypto flagged as needing separate
    spot/perp/DEX treatment. Reports **no concrete profitable strategies or numbers.**
  - **Why it matters for trading:** A citable, honest map of *why* AI edges fail to
    survive to net PnL — the exact failure modes this repo's backtest gate exists to
    catch. Confirms the strategic prior that single-model AI alpha is not the frontier.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** shelve (reference / literature map, not a strategy)

- **The Analyst in the Prompt: Role, Retrieval, and Memory Biases in LLM Financial
  Analysis** — Ahmed Asaad, Amr Mohamed, Yang Zhang, Omneya Abdelsalam, 2026-09-03 —
  [link](https://arxiv.org/abs/2609.03218)
  - **What it is:** Across 3,575 SEC filings × 12 LLMs, isolates whether persona/role
    context biases financial reasoning via *evidence retrieval* vs *interpretation*.
    Finding: most user-context spillover comes from **how models reinterpret the same
    evidence under different roles**, not from retrieving different evidence. Two
    mitigations (investor mindset as user-profile; separating evidence from personalized
    output) reduce but never eliminate spillover; effectiveness varies by model.
  - **Why it matters for trading:** Directly relevant to any LLM-analyst / news-to-signal
    pipeline — role/persona framing silently tilts the read of identical filings, a
    leakage-adjacent bias for LLM-driven alpha or briefs.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (guardrail for LLM-analyst pipelines)

### Microstructure & execution

- **Mean-field equilibrium of heterogeneous agents under market impact** — Joseph
  Leclère, Mathieu Rosenbaum, 2026-09-02 — [link](https://arxiv.org/abs/2609.03115)
  - **What it is:** A linear mean-field model where agents share information but differ
    in horizon and *account for their own impact*. Observed price = martingale +
    common predictable signal (a **Volterra / long-memory process**) + aggregate impact.
    At equilibrium a balance condition makes the **predictable-signal and impact terms
    cancel exactly**, so the observed price collapses to its pure martingale component
    (Hölder-regular, Brownian-like) for a range of signal/horizon distributions.
  - **Why it matters for trading:** A first-principles reason *why* daily single-series
    predictability keeps dying in this repo: if impact cancels the predictable long-memory
    component, a long-memory signal on price carries no exploitable edge. Rosenbaum is a
    top microstructure theorist. **This run's backtest target.**
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest ✅ (done this run — `volterra_signal`, MIXED-leans-REJECT,
    result *consistent* with the theorem)

- **Price manipulation in nonlinear transient impact models: rigidity before memory
  and complete positivity after memory** — Minhyeok Lee, 2026-09-02 —
  [link](https://arxiv.org/abs/2609.02447)
  - **What it is:** Conditions for absence of price manipulation / transaction-triggered
    manipulation in nonlinear transient-impact models, distinguishing a "rigidity"
    regime (before the memory kernel acts) from a "complete positivity" regime (after).
  - **Why it matters for trading:** Execution/cost-model plumbing — tells you which
    nonlinear impact kernels are internally consistent (manipulation-free) before you
    calibrate one into a scheduler. Complements the Udell cross-impact result below.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (execution-theory reference)

- **Switching Frictions, Heterogeneous Trading Horizons, and Long-Memory Order Flow** —
  Alejandro Rodriguez Dominguez, 2026-09-02 — [link](https://arxiv.org/abs/2609.02525)
  - **What it is:** First-passage/renewal analysis showing that costly changes to a
    portfolio's *representation* generate persistent order flow: heterogeneous switching
    thresholds + opportunity volatility → varying residence times whose aggregate is
    long-memory. **One tail exponent** governs representation-spell durations, the
    order-flow memory exponent, *and* the horizon where standard market scaling breaks.
    Ships an empirical protocol to test whether duration-kernel execution-cost models
    are appropriate, via cross-dataset restrictions.
  - **Why it matters for trading:** A microstructural *origin story* for long-memory
    order flow (an alternative to order-splitting) and a testable joint restriction —
    pairs naturally with Rosenbaum's Volterra-signal framing this same week.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (empirical protocol; tracked player)

- **Convex Modeling of Price Cross-Impact over Time** — Vincent Yinjun-Wang, Madeleine
  Udell, 2026-09-04 — [link](https://arxiv.org/abs/2609.04712)
  - **What it is:** A convex-quadratic transaction-cost model capturing *cross-impact*
    (a trade in one contract moves related contracts) + *transient impact* (decay over
    time): a PSD cross-contract coupling from vol/correlation/volume forecasts within
    each period, plus a power-law kernel coupling trades across periods. Manipulation-free
    by construction; improves valuation accuracy for **relative-value / calendar-spread**
    strategies held over multiple days.
  - **Why it matters for trading:** A drop-in, well-behaved cost model for multi-leg,
    multi-day execution — exactly the kind of realistic cost layer this repo's gate
    needs when it moves off single-asset long/flat into spreads/cross-sectional. Udell
    is a credible optimization researcher.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (candidate cost-model upgrade for the engine)

### Risk & portfolio

- **Uniform Inference and Certified Capacity at a Reflexive Stability Boundary** —
  Alejandro Rodriguez Dominguez, 2026-09-02 — [link](https://arxiv.org/abs/2609.02535)
  - **What it is:** Conventional pointwise inference is reliable at a separated spectral
    root but fails near semisimple/defective eigenvalue collisions; the paper projects a
    *joint* confidence region for the inputs instead, giving a **three-regime decision
    framework with abstention** and one-sided **capacity** bounds, verified with
    interval-arithmetic 2D methods so numerics can't flip a sign.
  - **Why it matters for trading:** Continues the capacity/crowding thread (2608.08405,
    2608.18299) — a rigorous, abstention-aware way to *certify* how much capital a
    strategy tolerates before its own crowding degrades it, robust exactly where naive
    error bars break.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (capacity certification method)

- **Portfolio Diversification and Concentration under Dependence Uncertainty: A
  Majorization Approach** — Peng Liu, Yang Liu, 2026-09-03 —
  [link](https://arxiv.org/abs/2609.04496)
  - **What it is:** Formalizes "degree of diversification" via majorization order +
    doubly-stochastic matrices; proves **quasi-convexity is necessary and sufficient**
    for a risk functional to respect that ordering (holds for VaR, ES, std-dev). The
    paradox: under *completely unknown* dependence, robust optimization often recommends
    **concentrating in a single asset** to hedge the worst-case dependence scenario.
    Proposes a weighted-robustness bridge between a reference model and the worst case.
  - **Why it matters for trading:** The constructive mirror of the Ruodu Wang VaR-
    superadditivity results (2606.22884) — "diversification can backfire" now gets a
    when/why and a tunable dial. Directly informs crypto sizing where cross-asset
    dependence is regime-unstable and heavy-tailed.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (portfolio-construction theory)

- **Illiquidity at Risk (IlliQaR)** — Demetrio Lacava, Paolo Santucci de Magistris,
  2026-09-01 — [link](https://arxiv.org/abs/2609.00943)
  - **What it is:** A tail-risk metric on the realized Amihud measure (vol/volume),
    forecast with linear + nonlinear models emphasizing **jump components**. Continuous-
    only models systematically understate liquidity-stress severity; on S&P 500 + 25
    large-caps, individual-stock IlliQaR violations **cluster during index liquidity
    stress**, with the S&P 500 acting as a leading indicator of individual-name dry-ups.
  - **Why it matters for trading:** A concrete, forecastable liquidity-tail measure —
    useful as a de-risking / position-cap gate (systemic dry-ups are somewhat
    predictable and cluster). Jump-inclusion is the actionable methodological point.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (risk-management gate input)

- **An Entropic Factor Model for Robust Portfolio Replication** — Argimiro Arratia,
  Henryk Gzyl, 2026-09-03 — [link](https://arxiv.org/abs/2609.03552)
  - **What it is:** A maximum-entropy construction of a factor model aimed at *robust
    replication* of a target portfolio/index under model uncertainty.
  - **Why it matters for trading:** Index/portfolio replication and factor-exposure
    matching with a principled robustness prior — relevant to low-cost tracking and to
    hedging a target exposure when the factor structure is uncertain.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve (replication reference)

### Asset class / market

- **Pricing the DeFi Tail: Do Protocols or Depositors Price Operational Risk?** — Nils
  Bundi, 2026-09-01 — [link](https://arxiv.org/abs/2609.00911)
  - **What it is:** A per-sector Basel loss-distribution approach on a new dataset of
    **1,075 operational-risk events / $9.45B losses since 2020.** Four core sectors show
    bank-like tails (0.85–1.39); Bridge, Derivatives, "Other" show **~1.6 tails with
    possible infinite mean.** Venues without a safety buffer pay a **125-bps** higher
    premium than those with one, but that premium **falls far short of an adequately
    priced tail** — retail depositors bear uncompensated operational tail risk.
  - **Why it matters for trading:** Quantifies a structural DeFi mispricing (op-risk tail
    under-compensated) and a venue-quality risk gate for any on-chain deployment; second
    Bundi paper in as many weeks (tracked). Empirical, not a directional signal.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (DeFi risk gate / venue selection)

- **Global Multi-Maturity SPX-VIX Calibration Beyond Markovian Stitching** — Atithi
  Acharya, Yue Sun, Brandon Augustino, Shouvanik Chakrabarti, Shree Hari Sureshbabu,
  Charlie Che, 2026-09-03 — [link](https://arxiv.org/abs/2609.04087)
  - **What it is:** Joint SPX + VIX smile calibration across maturities that **relaxes
    the Markovian independence ("stitching") assumption**, via an augmented-Bregman
    mirror-descent scheme preserving quoted prices while monitoring martingale/dispersion
    residuals. Key point: **laws with identical monthly calibrations can price
    multi-period claims differently**; worst fitted-smile error < 0.70 vol points on real
    surfaces.
  - **Why it matters for trading:** Non-Markovian dependence is a first-order pricing
    error for path-dependent / multi-period vol products — matters for anyone trading VIX
    term structure or forward-start vol. Continues Charlie Che's variance-surface thread
    (2608.12493, tracked).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (vol-surface / VIX term-structure pricing)

- **Harvesting the Variance Risk Premium in Nuclear and Energy Equities: A Short-Put
  Portfolio Derisking Strategy** — Jilang Miao, Nonna Sorokina, 2026-09-01 —
  [link](https://arxiv.org/abs/2609.01183)
  - **What it is:** A systematic cash-secured short-put strategy that sells ATM puts when
    **implied vol > GARCH-forecast realized vol**, on a curated nuclear/energy-equity
    universe, 2000–2024 (CRSP + OptionMetrics). Reports positive average premia, high win
    rates, and substantially lower vol than an equal-weight benchmark — but **before
    transaction costs and on a fixed universe** (4-page conference note).
  - **Why it matters for trading:** A clean, sector-focused VRP-harvest template with an
    explicit IV-vs-GARCH mispricing trigger; the pre-cost / fixed-universe caveats and
    short-vol tail risk are the obvious things to stress before believing it.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 2/5 · Actionability 3/5
  - **Next step:** shelve (needs cost + tail stress; no crypto-options data locally)

## Backtest — `volterra_signal` on BTC-USD → MIXED, leans REJECT

Faithful translation of **Leclère & Rosenbaum (2609.03115)**: their theorem says the
common predictable signal is a Volterra / long-memory process that impact *cancels* at
equilibrium, leaving a martingale. Tradable corollary: a long-memory signal from past
returns should have no edge. Built a power-law memory kernel `w_k ∝ k^-alpha` over past
log-returns → sign position; swept `alpha ∈ {0.5,0.7,0.9,1.5}` (0.5–0.9 = long memory /
Volterra regime; 1.5 = near-Markovian control) × span `{30,60,120}` days on 8y cached
BTC-USD (real data).

- Train (best of grid, `length=30, alpha=0.7`): Sharpe **1.063**, CAGR 39.8%, deflated-SR
  0.918 (already < 0.95).
- **OOS (realistic costs): Sharpe 0.242, CAGR 3.0%, MaxDD −34.5%.**
- Full-sample deflated-SR **0.308** — hard fail.
- **The confirming tell:** stage-1 ranking is monotone in memory span — **30 > 60 > 120d**
  at every `alpha`. The *longer* the memory, the *worse* the edge; the residual sits in
  the shortest near-Markovian window (already covered by `tsmom`/`trend_filter`). That is
  exactly impact-cancellation: the genuinely long-memory component carries no exploitable
  signal → **the backtest is consistent with Rosenbaum, not a falsification.**
- No crash-insurance signature this time (full-sample MaxDD −73.7% ≈ B&H −77%).

**15th straight daily-crypto reject-lean.** The long-memory / Volterra-kernel axis joins
direction, trend, vol, calendar, tail-measure, early-warning, and profit-threshold
momentum as exhausted on single-series daily BTC. Full report:
[2026-09-09-volterra_signal-BTC-USD.md](../../backtests/reports/2026-09-09-volterra_signal-BTC-USD.md).

## New resources & tooling
- _No new open-source repo/dataset above the quality bar this week (theory-heavy 2609
  batch). The Bundi DeFi op-risk dataset (1,075 events, 2609.00911) is the closest to a
  reusable dataset but is not released as tooling in the abstract._

## Watchlist updates
- **Joseph Leclère (with M. Rosenbaum)** — mean-field microstructure equilibria under
  market impact; Volterra-signal-cancellation → martingale (2609.03115). Worth tracking
  as the Rosenbaum-lineage co-author on impact equilibria.
- **Madeleine Udell (with V. Y. Wang)** — convex cross-impact + transient-impact cost
  modeling for relative-value/calendar-spread execution (2609.04712); credible
  optimization researcher, directly useful for the engine's cost layer.
- **Kay Giesecke (with Pan, Ding)** — agentic empirical asset pricing; evaluation of the
  *discovery system* not just outputs (2609.00731). High-credibility name for the
  honest-evaluation thread.
- **Peng Liu & Yang Liu** — majorization theory of diversification-vs-concentration under
  dependence uncertainty (2609.04496); companion to the Ruodu Wang superadditivity line.

## Open questions / threads to pull next run
- **Rodriguez Dominguez's long-memory-order-flow origin (2609.02525) vs Rosenbaum's
  Volterra-signal (2609.03115):** two independent 09-02 microstructure papers both center
  long memory — one as the *cause* (switching frictions generate it) and one as the thing
  impact *cancels*. Is there a joint empirical test on order-flow + price data?
- **The blocked frontier is unchanged and now quadruple-overdue: the hourly multi-coin
  OHLCV loader.** Every genuinely tradable crypto signal of the last month
  (Kitron-Wengrowicz 15-min directional reversal, Zhai on-chain identity, Kakinaka-Umeno
  MFCCA, intraday quarter-hour effects) lives at intraday or cross-sectional resolution
  that the current daily BTC/ETH cache cannot reach. Single-series daily is confirmed
  dry (15 rejects). **Building the hourly loader is now the highest-leverage next task.**
- **DisclosureBeta (2609.02900, Wong)** — LLM-as-noisy-measurement-channel regime-
  conditional betas from risk disclosures with formal error budgets; the abstract page
  reports an anomalous 2026-07-05 date under a fresh 2609 ID (likely a revision), so held
  out of the scored findings pending recency confirmation — revisit if it is genuinely new.
- Next ceiling: **2609.04917.**
