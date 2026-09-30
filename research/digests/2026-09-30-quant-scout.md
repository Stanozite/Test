# Quant Scout Digest — 2026-09-30

_14-day window since 2026-09-16. Swept arXiv q-fin TR/PM/ST/RM/CP for IDs above the
09-16 ceiling `2609.12793` → top of window now `2609.35744`. Full-month batch (well
into the month), so richer than the last two thin weekly sweeps. All items below are
above the ceiling and absent from the INDEX dedupe ledger._

## TL;DR
- **Backtest — `online_window` on BTC-USD → MIXED (leans REJECT), 17th straight daily-crypto reject-lean.** First test that attacks the *overfitting mechanism itself* rather than adding a signal: faithful to Liu & Hsieh's cost-sensitive online window aggregation (2609.29887), it freezes a spread of momentum windows and lets Hedge/Fixed-Share pick among them online, sweeping only the aggregator's hyper-params. Train Sharpe **0.675 → OOS 0.078**, CAGR −3.0%, full deflated-SR **0.934** (fails). **Two confirming tells:** (1) **all 9 eta×cost configs give the identical train result** — the "cost-sensitive" lever is inert on a single asset (all experts are long/flat momentum on the same series → near-identical turnover → cost never moves the weights); (2) the train→OOS Sharpe decay (~88%) is marginally *smaller* than the fixed-window strategies (vol_regime ~97%, tsmom ~90%) — the paper's robustness claim faintly present — **but the OOS level is still ~0**. Removing window-overfitting entirely still yields no alpha, because daily single-series momentum has no edge to select among. Does **not** falsify the paper (their claim is multi-asset, turnover-divergent portfolio robustness, not single-asset timing).
- **Honest-evaluation thread hardens into a design principle (Qu/Chen/Wang, 2609.27051):** "Propose, Don't Judge" — let an LLM agent propose factors but force a **frozen, anytime-valid statistical referee** it cannot touch to judge, scoring only post-submission outcomes by betting (false-discovery guarantee at every stopping time). Frozen referee admits **5–11× fewer** sub-threshold factors than leaky ones; **who judges sets false admissions, who proposes sets yield**; the certificate's price is ~500 trading days of lag, so the gated Sharpe trails an ungated one. Direct successor to Giesecke SEADS (09-09) + Gençay (09-02).
- **A conservation law for our own OOS splits (Jiayu Li, 2609.29530):** "The Impossible Trinity of Time-Series Validation" — training sufficiency, test coverage, and temporal causality cannot all be maximised at once; tightening one loosens another. This is the theory behind why every reject in this repo shows a lossy train→OOS collapse; it is a structural tax on validation, not a defect of any one strategy.
- **Itkin explains our two long-memory nulls (2609.20293):** "Beyond Rough Volatility" imports a **generalized Langevin equation** that *decouples* how volatility scales from how it remembers (fBm forces one parameter to do both). Physical-measure tests **decisively reject** memoryless-leverage and time-reversal-symmetry corners; the central rough-scaling constraint is left **identification-limited, not refuted**. Reconciles `volterra_signal` + `asym_longmem_vol`: a real-but-non-tradable memory channel is exactly what a separable-memory model predicts.
- **Cotton reframes covariance-cleaning (2609.21271):** Nested Clustered Optimization and Schur complements are the **two endpoints of one bridge**, and the **interior is sometimes provably better** than either — a tunable continuum, not a choice between two recipes.

## Findings by focus area

### ML / AI for alpha
- **Propose, Don't Judge: An Anytime-Valid Referee for LLM Agents That Mine Investment Factors** — Bo Qu, Mingguang Chen, Licheng Wang, 2026-09-22 — [link](https://arxiv.org/abs/2609.27051)
  - **What it is:** governed self-evolution — agent proposes factors; a frozen, betting-based referee judges only on post-submission market outcomes, with an anytime-valid FDR guarantee. Cross-tests 3 proposers × leaky/frozen referees on synthetic planted-truth + 10y CSI 500 walk-forward.
  - **Why it matters for trading:** the cleanest statement yet of *separation of duties* in agentic quant — it is the referee, not the agent, that controls false discovery; matches this repo's own deflated-SR-as-necessary-not-sufficient stance and adds a positive construction.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read (adopt the frozen-referee framing for the gate; the ~500-day certification lag is the key cost to internalise)
- **The Impossible Trinity of Time-Series Validation: A Conservation Law among Training Sufficiency, Test Coverage, and Temporal Causality** — Jiayu Li (tracked), 2026-09-27 — [link](https://arxiv.org/abs/2609.29530)
  - **What it is:** a formal trilemma — you cannot simultaneously maximise how much a model trains on, how much held-out ground it is tested over, and strict temporal causality; improving one degrades another.
  - **Why it matters for trading:** the theory under every OOS collapse we log; makes the train→OOS decay a measurable tax to report, not a surprise. Reframes how to *read* a reject.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read (use to standardise how the backtest reports frame train→OOS decay)
- **Separated Signal Libraries: Packing, Saturation, and Joint Spectral Limits** — Marc da Costa Nunes (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.17609)
  - **What it is:** direct successor to his 09-16 signal-library-geometry piece — how many *separated* (non-redundant) signals a library can pack before spectral saturation, and the joint limits on their PnL spectra.
  - **Why it matters for trading:** quantifies the crowding/artifact boundary for large alpha libraries — when adding signals stops adding independent information.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (theory; revisit if we build a multi-signal library)
- **EverMine: Dissecting the Self-Evolution of Research Capabilities in Long-Horizon Alpha Research** — Siyuan Li et al., 2026-09 — [link](https://arxiv.org/abs/2609.33524)
  - **What it is:** decomposes how an agentic alpha-research system's *research capability* (not just its factors) improves over an extended horizon.
  - **Why it matters for trading:** capability-level (not output-level) evaluation — the same axis Giesecke/Qu are pushing; system-quality is becoming the unit of measurement.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve
- **Self-Evolving Multi-Agent Symbolic Discovery for Financial Fundamental Analysis** — Kelvin J.L. Koa, Filip Orestav, Shengqiong Wu, Michael Wooldridge, Ke-Wei Huang, 2026-09 — [link](https://arxiv.org/abs/2609.32746)
  - **What it is:** cooperative multi-agent system that discovers *symbolic* (interpretable) relationships for fundamental analysis, evolving its own search.
  - **Why it matters for trading:** symbolic (vs black-box) discovery keeps the artifact auditable — the property that lets a frozen referee (2609.27051) actually check it.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve
- **Can You Delete a Year of Market Data? Machine Unlearning Against Exact Retraining Oracles** — Junyi Ye (tracked), 2026-09-26 — [link](https://arxiv.org/abs/2609.26242)
  - **What it is:** tests whether financial ML models can *forget* a defined slice of history to match an exact-retraining oracle — regime removal / leakage remediation without full retrain.
  - **Why it matters for trading:** practical hygiene for models that must drop a contaminated or non-repeating regime (e.g. a one-off crash) without discarding everything.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Microstructure & execution
- **Event-Time Order-Flow Memory, Operational-Time Impact, and Subordinated Market Observables** — Christopher Angstmann & Tim Gebbie (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.13715)
  - **What it is:** disentangles the three clocks of microstructure — event time (order-flow memory), operational time (impact), calendar time (observables) — via subordination.
  - **Why it matters for trading:** the right time-change is what makes impact and long-memory look stationary; foundational for any impact/execution model calibrated on crypto's uneven flow.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Herding and Liquidity in Order-Book Markets. III. Leverage and the Onset of Endogenous Liquidity Crises under Weak Anchoring** — Jan Novotny (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.20192)
  - **What it is:** third in the Novotny herding/liquidity series — how leverage plus weak fundamental anchoring tips an order-book market into an endogenous liquidity crisis.
  - **Why it matters for trading:** a mechanism for crypto's leverage-driven cascades (echoes Garcia Seuma) — endogenous, not exogenous, dry-ups.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Model-Free Passive Execution via Order-Level Shadowing** — Vincent Maciejewski, 2026-09 — [link](https://arxiv.org/abs/2609.18019)
  - **What it is:** passive execution that shadows existing resting orders rather than fitting an impact model — model-free child-order placement.
  - **Why it matters for trading:** a cheap, calibration-light execution primitive; relevant when a fitted impact model is unavailable or unstable (i.e. most crypto venues).
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read
- **Agentic Limit Order Books: Phase Transitions and Market Impact** — Jan Rosenzweig, 2026-09 — [link](https://arxiv.org/abs/2609.31260)
  - **What it is:** agent-based LOB where collective behaviour undergoes phase transitions that reshape the impact function.
  - **Why it matters for trading:** impact is regime-dependent (a phase, not a constant) — a caution against a single fitted impact curve.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve
- **Feasible Multi-Asset Optimal Execution under Cash Constraints** — Ryuji Hashimoto & Namid R. Stillman, 2026-09 — [link](https://arxiv.org/abs/2609.27786)
  - **What it is:** optimal execution across several assets subject to a hard cash/funding constraint — feasibility, not just optimality.
  - **Why it matters for trading:** the realistic version of multi-asset liquidation (you cannot go cash-negative); relevant to any dollar-neutral crypto basket execution.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Risk & portfolio
- **Cost-Sensitive Online Window Size Selection for Portfolio Management** — Yi-Chen Liu & Chung-Han Hsieh, 2026-09-24 — [link](https://arxiv.org/abs/2609.29887)
  - **What it is:** a two-level framework — build candidate portfolios from several lookback windows, then aggregate them online (Hedge / Fixed-Share) on **turnover-inclusive** losses; regret bounds, no static window.
  - **Why it matters for trading:** a principled attack on the exact failure mode of all 16 prior rejects — the grid-selected fixed window that collapses OOS. **Backtested this run (see below).**
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate/backtest → **done this run (MIXED, leans REJECT)**
- **Beyond Rough Volatility: Decoupling Memory and Scaling via a Generalized Langevin Equation** — Andrey Itkin (tracked), 2026-09 (cross-listed; v1 2026-07-31) — [link](https://arxiv.org/abs/2609.20293)
  - **What it is:** GLE stochastic-vol framework (memory kernel K, potential U, noise covariance C) that separates volatility's scaling from its memory — the two properties fBm forces together. Physical tests reject memoryless-leverage + time-reversal-symmetry; rough scaling left identification-limited.
  - **Why it matters for trading:** directly explains this repo's `volterra_signal` and `asym_longmem_vol` nulls — a significant-but-non-tradable long-memory channel is what a separable-memory model predicts; the asymmetric potential is a new lever on variance skew.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** read (companion paper promises risk-neutral construction + SPX–VIX calibration — track for a derivatives test)
- **Nested Clustered Optimization Is One End of a Schur Bridge, and the Interior Is Sometimes Provably Better** — Peter Cotton (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.21271)
  - **What it is:** shows NCO (López de Prado) and Schur-complement damping are the two endpoints of a single parametric bridge; the interior can provably dominate both.
  - **Why it matters for trading:** turns two competing covariance-cleaning recipes into one tunable knob — a cleaner default for portfolio construction than picking a camp.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read
- **Principal Component Error in High-Dimensional Factor Models** — Alex Bernstein, Lisa R. Goldberg, Nicholas Gunther, Alec N. Kercheval, Tian Lan, Yian Lin, Dayi Yao, 2026-09 — [link](https://arxiv.org/abs/2609.20550)
  - **What it is:** characterises the estimation error introduced by PCA-based factor extraction as dimension grows — where PC estimates degrade and by how much.
  - **Why it matters for trading:** a bound on how much to trust PCA factors in a wide universe; complements Cotton's covariance-cleaning bridge.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **On Control of Drawdown: Robust Invariance and Optimality** — Chung-Han Hsieh, 2026-09 — [link](https://arxiv.org/abs/2609.23272)
  - **What it is:** treats a drawdown cap as a robust-invariance constraint and derives control policies that keep the equity curve inside it under uncertainty.
  - **Why it matters for trading:** the crash-insurance signature that survives every reject here has been *ad hoc*; this is the principled version of "keep drawdown bounded" and worth a future overlay test.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (candidate for the next exposure-management backtest)
- **Weighted Universal Value-at-Risk Superadditivity for Discrete Distributions** — Alfred Müller, 2026-09 — [link](https://arxiv.org/abs/2609.26398)
  - **What it is:** extends the universal VaR-superadditivity result (Chen/Lin/Wang; Ruodu Wang lineage) to weighted, discrete distributions — when diversification provably backfires.
  - **Why it matters for trading:** sharpens the "concentrate, don't diversify, under heavy tails / unknown dependence" caution for discrete/quantised return data.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve
- **Risk Diversification for Infinitely Divisible Distributions** — Peng Liu (tracked) & Tiantian Mao, 2026-09 — [link](https://arxiv.org/abs/2609.25452)
  - **What it is:** diversification principles for the infinitely-divisible class (Lévy-type), where tail behaviour governs whether pooling helps.
  - **Why it matters for trading:** the crypto-relevant tail class; tells you when a basket genuinely reduces risk vs merely spreading it.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Asset class / market (crypto & derivatives)
- **Loss Choice or Model Choice? The Role of Forecast Level in Cryptocurrency Volatility Forecasting** — Andrzej Tokajuk & Jarosław A. Chudziak, 2026-09-22 — [link](https://arxiv.org/abs/2609.27024)
  - **What it is:** 7 losses × 5 models across major cryptos; after **validation-based level alignment**, *model* choice (not loss) becomes the larger source of variation and cross-loss VaR-breach differences narrow — raw comparisons conflate forecast-level with day-to-day movement.
  - **Why it matters for trading:** methods caution for crypto vol pipelines — a "better loss" is often just a level shift; echoes RG-ResMoE "route, don't feed" and our own vol-statistic-swap exhaustion.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (vol-forecasting, not a directional signal — consistent with the triple-exhausted vol axis)
- **CAST: A Cross-Asset State-Space Trading System for Drawdown Control in Stock Markets** — Yu Peng, Matloob Khushi, Josiah Poon (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.14205)
  - **What it is:** cross-asset state-space (Mamba-style) trading system explicitly optimised for drawdown control on equity markets.
  - **Why it matters for trading:** same team as CryptoGAT; drawdown-first design converges with Hsieh (2609.23272) — the field is moving toward loss-control as the objective, matching what actually survives here.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (equities; watch for a crypto variant)
- **Taming the Greeks: Option Portfolios with Inductive Biases** — Wee Ling Tan, Stephen Roberts, Stefan Zohren (tracked), 2026-09 — [link](https://arxiv.org/abs/2609.33767)
  - **What it is:** neural option-hedging that bakes in financial inductive biases (Greeks structure) instead of learning them from scratch.
  - **Why it matters for trading:** the deep-hedging thread with structure priors — the fix for Kumar's "deep nets never learn inactivity" (09-02) negative result.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** read
- **Taming the Option Factor Zoo: A High-Dimensional Analysis** — Alexander Walter, Lukas Zimmer, Maxim Ulrich, 2026-09 — [link](https://arxiv.org/abs/2609.31263)
  - **What it is:** high-dimensional shrinkage/selection across the proliferating set of option-return factors.
  - **Why it matters for trading:** the options analogue of the equity factor-zoo cleanup; which option factors survive joint testing.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve
- **Diffusion Models for Dynamic Volatility Surface Generation and Data-Driven Hedging** — Yinbin Han, Jack Yuxiang Zhang, Manuel Torres, Fernando Acero, Renyuan Xu, 2026-09 — [link](https://arxiv.org/abs/2609.13402)
  - **What it is:** diffusion generative model for evolving IV surfaces, used to drive data-driven hedges.
  - **Why it matters for trading:** synthetic-surface generation for hedge stress-testing where real option data is thin (crypto).
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

## New resources & tooling
- **SAiFE-gym** — model-based RL environments for automated market making with concentrated liquidity — Chionas, Kleitsikas, Leonardos, Sánchez-Betancourt, Ventre — [link](https://arxiv.org/abs/2609.17788) — a simulator for AMM/concentrated-liquidity strategies (extends the Ventre-group on-chain RL line).
- **StableEval Arena** — cost-aware agentic benchmark for stablecoin price-stability prediction — Wan, Liu, Zhang — [link](https://arxiv.org/abs/2609.18949) — a graded task for evaluating trading agents on de-peg risk.
- **FinAutoRubric** — expert-guided automatic rubric generation for evaluating financial research agents — Lee, Yun, … Halperin, Lopez-Lira, Choi, Lee (large author list) — [link](https://arxiv.org/abs/2609.35744) — auto-built evaluation rubrics; the tooling layer under the honest-evaluation thread.

## Watchlist updates
New players/sources worth adding to `watchlist.md`:
- **Chung-Han Hsieh** — cost-aware online window aggregation + robust drawdown control (2609.29887, 2609.23272); this run's backtest anchor and a natural next-overlay source.
- **Bo Qu / Licheng Wang** — anytime-valid frozen-referee for agentic factor mining (2609.27051); extends the Giesecke/Gençay honest-evaluation lineage.
- **Kelvin J.L. Koa** — self-evolving symbolic discovery + retrieval-augmented diffusion SDF portfolios (2609.32746, 2609.35086); prolific this window.
- **Lisa R. Goldberg / Alec N. Kercheval** — PC error bounds in high-dimensional factor models (2609.20550).

## Open questions / threads to pull next run
- **Drawdown control is converging from three directions** (Hsieh robust-invariance 2609.23272, CAST cross-asset 2609.14205, and the crash-insurance signature that survives every reject here). The next exposure-management backtest should test a *principled* bounded-drawdown overlay (Hsieh) rather than another self-adapting-quantile gate — the vol-statistic axis is triple-exhausted and a new quantile gate would just be a fourth swap.
- **The infra unblock is now 6× overdue** and the `online_window` result sharpens *why*: single-series daily has no cross-window edge to select, so the paper's own mechanism can't help until there are multiple assets with divergent turnover for the cost-sensitivity to bite. **The hourly / multi-coin OHLCV loader is the single highest-leverage next task** — it is what every tradable finding of the last two months (Kitron-Wengrowicz 15-min reversal, quarter-hour effects, on-chain identity, MFCCA/MINGLE cross-section) actually requires, and now also what would make Liu & Hsieh's cost-sensitive aggregation testable as intended.
- **Adopt the frozen-referee + impossible-trinity framing** (2609.27051, 2609.29530) as the standard way the backtest reports state their gate and their train→OOS decay — the field has now formalised both.
- Next ceiling: `2609.35744`.
