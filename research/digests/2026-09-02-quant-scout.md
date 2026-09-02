# Quant Scout Digest — 2026-09-02

_7-day window since 2026-08-26. Swept arXiv q-fin TR/PM/ST/CP/RM `/recent` above last
ceiling 2608.24786, through top ID 2608.31041 (early 2609 not yet announced at run time).
Deduped against `research/INDEX.md`. 13 findings captured._

## TL;DR
- **Two independent honest-evaluation reckonings land in the same week, and both point the same way we do.** Gençay "What survives honest evaluation?" (2608.27734): across 453 stocks + 39 ETFs with realistic costs, an LLM strategy-search **rejects *every* discovered strategy** across two frontier models and search budgets to 100 candidates — while a **deliberately leaky oracle posting Sharpe 35 sails through Deflated-Sharpe and PBO untouched**. The lesson for our own pipeline: the deflation gate is *necessary but not sufficient* — leakage must be excluded *structurally* (feature-space guardrails), not caught statistically after the fact.
- **The sharpest microstructure result is a tracked player's negative result:** Goliath & **Gebbie** "Metaorder modelling and identification from public data" (2608.30999) — you can reconstruct metaorders from *anonymous* public trade/quote data (239 JSE stocks), but reproducing aggregate impact stylised facts **does not identify** Lillo-Mike-Farmer order-splitting; the LMF relation is only recoverable *by construction*. Consistency ≠ validation without trader-ID data.
- **Deep hedging loses to a 1990s no-trade band on real BTC options.** Kumar (2608.29025): on 5y of Bitcoin options, **none of three deep-hedging models beat any classical benchmark on any metric**; Whalley-Wilmott's no-trade band saves ~$1.79/episode vs BS-delta by trading ~8× less. The NN "kept trading almost every hour regardless of penalty weight" — no built-in inactivity. Same moral as our cost-band rejects: the edge is *not trading*, not smarter forecasting.
- **Best portfolio finding is a tracked-lineage covariance upgrade:** Bongiorno & Villassero (2608.30446) — end-to-end **neural shrinkage of *indefinite* pairwise-complete correlation matrices** for small-cap-inclusive universes: ~**+40% Sharpe, −20% vol**, 99.9% Model Confidence Set retains only the neural estimator, 26y / 1500 US equities net of frictions. Cross-sectional equity, not single-series crypto.
- **Backtest: `multiscale_move` on BTC-USD → MIXED (leans REJECT).** Faithful price-only core of the multi-scale-TCN BTC paper (2608.26174): the **profit-optimized threshold optimizes itself to 0.0** on train (the paper's headline mechanism adds nothing on price-only inputs), train Sharpe 0.731 → **OOS Sharpe 0.122, CAGR −0.1%**, fails deflated-SR. Only signature is crash-insurance (OOS MaxDD −36% vs B&H −77%). **14th straight daily-crypto reject-lean.**

## Findings by focus area

### ML / AI for alpha

- **What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery** — Eray Gençay, 2026-08-27 — [link](https://arxiv.org/abs/2608.27734)
  - **What it is:** A strategy-discovery system that makes two corrections *structural* not procedural: (1) the agent acts only through registry-validated tools whose feature space excludes look-ahead by construction; (2) it records every evaluation and deflates reported performance by that trial count. A deliberately leaky oracle at Sharpe 35 survives Deflated-Sharpe + PBO completely; honest evaluation then certifies passive benchmarks and **rejects every LLM-discovered strategy** (2 frontier models, budgets to 100 candidates, 5 repeated runs) on a 453-stock point-in-time universe + 39-ETF multi-asset universe with realistic transaction/impact/borrow costs.
  - **Why it matters for trading:** This is the methodological spine of our own repo, stated cleanly by someone else: our deflated-Sharpe gate catches *selection* luck but a leaky feature can still post an unbeatable Sharpe. Adopt the "feature registry excludes look-ahead by construction" idea as a structural guardrail alongside the statistical gate.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read + adopt (harden our pipeline's leakage guardrails)

- **Forecasting Economically Significant Bitcoin Moves: A Multi-Scale TCN with Profit-Optimized Thresholds** — Yousefnezhad, Mansourfar, Feizi Derakhshi, 2026 — [link](https://arxiv.org/abs/2608.26174)
  - **What it is:** Binary forecast "will BTC rise >5% within 7 days?" from on-chain + market + sentiment data (Feb 2018–Dec 2025) via an InceptionTCN fusing dilated 1–4-day features + CNN channel attention + pairwise-ranking loss, then a **profit-optimized decision threshold**. AUC 0.6316, "profit 1.703", beating ImprovedTCN-GRU / LSTM / TCN / XGBoost / RF.
  - **Why it matters for trading:** Crypto-native, explicitly tradable, and the "profit-optimized threshold" is exactly the kind of decision rule we translate. **Backtested this run** (see below) — the price-only core rejects; their edge must live in the non-price features.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest ✅ (MIXED, leans REJECT — `multiscale_move`)

- **Tabular Deep Learning for Algorithmic Trading: Cross-Regime Bayesian Optimisation for Equity Signal Generation** — Joshua Le Grice, 2026-08 — [link](https://arxiv.org/abs/2608.27076)
  - **What it is:** Tabular deep-learning equity signal generator tuned by cross-regime Bayesian optimisation, so hyperparameters are selected for robustness across market conditions rather than a single backtest window.
  - **Why it matters for trading:** The cross-regime BO objective is the transferable idea — it directly attacks the regime-overfit failure mode our OOS split is built to expose.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (method reference)

### Microstructure & execution

- **Metaorder modelling and identification from public data** — Ezra Goliath & Tim Gebbie, 2026-08-31 — [link](https://arxiv.org/abs/2608.30999)
  - **What it is:** Tests whether Lillo-Mike-Farmer order-splitting theory can be recovered from *anonymous* public data (no trader IDs) via synthetic metaorder reconstruction, grid-searching reconstruction parameters over 239 JSE stocks (2023–2025). Configs tuned to metaorder impact stylised facts reproduce those facts but **yield a poor LMF relation**; configs tuned to LMF recover it *by construction*. Recovering aggregate impact facts alone is insufficient to identify LMF-consistent splitting.
  - **Why it matters for trading:** A tracked-player (Gebbie) reproducibility check that draws a hard line: impact "stylised-fact matching" is not evidence of the underlying mechanism. Cautions any impact/metaorder model calibrated on public data alone.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read

- **The Convergence Rate of Stochastic Tracking with Application to Optimal Execution** — Marcel Nutz & Moritz Voss, 2026-08 — [link](https://arxiv.org/abs/2608.29468)
  - **What it is:** Analyses the convergence rate of a stochastic-tracking problem and applies it to optimal execution — how fast a trading schedule that tracks a moving target converges, with explicit rates.
  - **Why it matters for trading:** Execution-theory reference; rates quantify the cost of tracking a drifting optimal-execution target, relevant to schedule design under signal decay.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

- **Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices** — Nils Bundi, 2026-08 — [link](https://arxiv.org/abs/2608.30321)
  - **What it is:** Derives the block time that optimises AMM liquidity-provider outcomes when the reference price follows a jump-diffusion — a DeFi-microstructure design lever (how block cadence trades off LVR/adverse selection against fee capture) under discontinuous prices.
  - **Why it matters for trading:** On-chain LP economics; extends the LVR/dynamic-fee thread (Ghasemlu 2606.21769, Di Nosse/Lillo 2606.23070) to the *timing* dimension of block production.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read/shelve

### Risk & portfolio

- **End-to-End Neural Shrinkage of Indefinite Pairwise Correlation Matrices for Small-Cap-Inclusive Portfolios** — Christian Bongiorno & Lorenzo Villassero, 2026-08-31 — [link](https://arxiv.org/abs/2608.30446)
  - **What it is:** Adapts a rotation-invariant neural covariance estimator to *indefinite* correlation matrices arising from pairwise-complete estimation (intermittently-traded small caps): mask-aware moments + signed spectrum via a bidirectional GRU maps all eigenvalues (including negative) to a positive inverse spectrum, guaranteeing a positive-definite reconstruction. ~**+40% Sharpe, −20% 5-day vol** vs next-best, 99.9% MCS retains only the neural estimator, 2000–2025 on up to 1500 US equities net of frictions.
  - **Why it matters for trading:** Continues the Bongiorno/Mantegna covariance-cleaning lineage and solves the concrete small-cap problem (missing pairwise data → indefinite Σ) that breaks naive shrinkage. Directly usable for portfolio construction on wide, patchy universes.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read / replicate (cross-sectional equity)

- **Portfolio Risk Bounds without Cross-Asset Return Covariances: Distributional Fields from Language-Model Representations** _(+ companion: Wasserstein-Barycentric Interaction Fields for Spatial Factor Models, 2608.29669)_ — Marcus Gawronsky & Chun-Sung Huang, 2026-08 — [link](https://arxiv.org/abs/2608.29692)
  - **What it is:** Derives one-sided portfolio-risk certificates from **Wasserstein-2 dispersion of firm-level, distribution-valued characteristics built from LLM news embeddings (Qwen3-Embedding)** — no cross-asset return covariance required — under a weighted pairwise relaxation that is convex in checkable conditions.
  - **Why it matters for trading:** A genuinely novel angle (risk geometry from language representations, not returns), but **in-sample only, 52 firms, 2018–2022**, leaning on maintained characteristic→exposure→return assumptions. A direction to watch, not to trust yet.
  - **Scores:** Novelty 4/5 · Credibility 2/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve / watch (needs OOS)

- **Option-Implied Signals and Crash Risk: Predictability and Machine-Learning Evidence from U.S. Equity Options** — Baichuan Li & Mengxiao Wang, 2026-08 — [link](https://arxiv.org/abs/2608.26115)
  - **What it is:** Extracts crash-risk predictors from U.S. equity-option-implied signals and tests their predictability with machine learning — implied-vol / skew structure as forward crash indicators.
  - **Why it matters for trading:** Option-implied crash signals are a recurring risk-overlay lead; ML framing lets it be layered onto an equity book. Needs options data we don't yet ingest.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read

### Asset class / market

- **Deep Hedging Under Realistic Market Frictions: A Regime-Conditional Empirical Study of Dynamic Option Hedging on Bitcoin Options** — Sheryan Kumar, 2026-08 — [link](https://arxiv.org/abs/2608.29025)
  - **What it is:** Real-data (5y BTC options) horse-race of three deep-hedging models vs classical benchmarks under realistic frictions, regime-conditioned. **None of the deep models beat any classical benchmark on any metric;** the Whalley-Wilmott no-trade band beats BS-delta by ~$1.79/episode (95% CI [−2.21,−1.39], p<0.0001) via ~8× less trading. Deep nets "kept trading almost every hour regardless of penalty weight." The no-trade-band edge shrinks/vanishes in calm regimes.
  - **Why it matters for trading:** The cleanest crypto finding this window and squarely in our wheelhouse: it's the same lesson our cost-band rejects keep teaching — the durable edge is *fewer trades*, and complex models fail to learn inactivity. Regime-conditional read: reduced-rebalancing pays in volatile regimes, less so in calm ones.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read / port the "no-trade band beats delta" insight

- **A Frequency-Controlled Comparison of Tick- and Minute-Based Information Bars for Cryptocurrency Markets** — Fayyaz, Jabbar, Qureshi, Jalil, 2026-08 — [link](https://arxiv.org/abs/2608.26158)
  - **What it is:** Frequency-controlled comparison of tick-based vs minute-based information-bar construction for crypto — how the sampling/aggregation choice changes downstream statistical properties, holding effective frequency fixed.
  - **Why it matters for trading:** Directly informs the **hourly/intraday loader** this repo keeps flagging as the unblock for cross-sectional crypto — bar construction is the first design choice once we leave daily close.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (infra input for the intraday feed)

- **Pricing and Calibration of Bitcoin Inverse Options via the Rough Bergomi Model** — Riccardo Caruso, 2026-08 — [link](https://arxiv.org/abs/2608.27575)
  - **What it is:** Applies rough-volatility (rough Bergomi) pricing + calibration to **Bitcoin inverse options** (coin-margined, non-standard payoff), handling the roughness of crypto vol and the inverse contract's convexity.
  - **Why it matters for trading:** Reference for anyone marking/hedging coin-margined crypto option books; pairs with Kumar (2608.29025) on the empirical-hedging side.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

## New resources & tooling
- **Agentic Quantitative Trading: A Survey of Workflows, Systems, and Evaluation** — Hua, Yang, Hao, Zhang, Cao, Qi, Li, **Jian Guo**, 2026-08 — [link](https://arxiv.org/abs/2608.31041) — a field map of agent-based trading systems (workflows / systems / evaluation); a fast orientation to the LLM-agent-trading space and its (weak) evaluation norms — read alongside Gençay 2608.27734 as the "how it's evaluated badly / how to evaluate it honestly" pair.
- **CIFQA: A Deterministic Tool-Grounded Multi-Agent LLM Framework for Financial Query Answering** — Parekh, Tiwari, Saxena, 2026-08 — [link](https://arxiv.org/abs/2608.26114) — deterministic, tool-grounded multi-agent scaffold for financial QA; useful pattern for reproducible LLM-in-the-loop research tooling.

## Watchlist updates
_New authors discovered this run worth tracking:_
- **Eray Gençay** — leakage-safe, search-aware honest evaluation of LLM strategy discovery; structural (not statistical) look-ahead guardrails. *Directly load-bearing for our pipeline.*
- **Ezra Goliath** (with tracked **Tim Gebbie**) — metaorder reconstruction / LMF identification from anonymous public data.
- **Sheryan Kumar** — real-data deep-hedging vs classical no-trade-band on crypto options; honest negative results.
- **Christian Bongiorno & Lorenzo Villassero** — neural shrinkage of indefinite correlation matrices (extends the Bongiorno/Mantegna covariance-cleaning lineage already tracked).
- **Marcus Gawronsky & Chun-Sung Huang** — portfolio risk geometry from language-model representations (Wasserstein fields; early/in-sample).
- **Parsa Yousefnezhad** — multi-scale-TCN + profit-threshold BTC move forecasting (this run's backtest source).

## Open questions / threads to pull next run
- **The BTC/ETH pair test is now buildable with zero new data.** Both `BTC-USD_1d.csv` and `ETH-USD_1d.csv` are cached — a dollar-neutral BTC/ETH relative-value strategy would be the first genuine step off the single-series axis the last 14 rejects have exhausted (n=2 is a pair, not a cross-section, but it directly tests whether *relative* crypto momentum/reversion carries what *absolute* does not). Small engine change (two-symbol loader + spread signal).
- **Where does 2608.26174's edge actually live?** This run showed the price-only multi-scale-momentum core is null and the profit threshold collapses to 0. If we ever ingest on-chain + sentiment features, the honest question is whether *those* features — not the multi-scale price geometry — are the AUC source. A feature-ablation, not another price-only test.
- **Hourly loader is now double-motivated:** 2608.26158 (tick vs minute bars) tells us how to construct intraday bars; 2608.29025 (hourly BTC-options hedging) shows the frequency where the no-trade-band edge lives. Both point at the same infra unblock.
- **Adopt Gençay's structural leakage guardrail (2608.27734):** our deflated-SR gate is necessary-not-sufficient; a feature-registry that excludes look-ahead by construction would close the "leaky-oracle survives DSR" hole in our own harness.
