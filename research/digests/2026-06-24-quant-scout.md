# Quant Scout Digest — 2026-06-24

## TL;DR
- **Lillo strikes again on AMM design:** dynamic fees on Uniswap-v3 pools don't *reduce* loss-versus-rebalancing — they pay LPs *more in toxic states*, i.e. fee timing > fee level (Di Nosse/Lillo, ABM).
- **Leakage-aware LLM factor ranking:** a 7B LLM fed only decision-time data (lagged macro + real-time inflation nowcasts) hits median monthly rank-IC +0.154, but its edge over a kNN baseline lives in the *extreme* deciles — the only part that matters for long/short construction (Guan/Chen).
- **Square-root impact law confirmed for a single US large-cap** from anonymous ITCH alone — 178 days of AAPL, metaorders reconstructed, prefactor c≈0.69, linear/log rejected (Vasaikar). A clean, replicable impact-calibration recipe.
- **Diversification can be provably wrong:** Chen/Lin/Wang give conditions ("universal VaR superadditivity") under which every distortion risk measure is superadditive → the optimal allocation *concentrates on one asset* (Ruodu Wang).
- **Engineering, not theory, as edge:** "Asymmetry PRISM" rebalances 500 institutional accounts in 25 min where a baseline solver did 4 — 3.4×–126.7× GPU speedup on deadline-bounded constrained optimization (Ghosh).

## Findings by focus area

### ML / AI for alpha
- **Leakage-Aware Benchmarking of LLM Forecasting: Real-Time Nowcasts as the Decision-Time Input for Macro Factor Ranking** — Mao Guan, Qian Chen, Jun 2026 — [arXiv:2606.22719](https://arxiv.org/abs/2606.22719)
  - **What it is:** Benchmarks a 7B LLM on equity factor ranking using *only* decision-time-observable inputs (lagged macro variables + real-time inflation nowcasts), explicitly to stop confounding model skill with look-ahead leakage. Median monthly Spearman rank-IC +0.154.
  - **Why it matters for trading:** The leakage-aware protocol is the actionable bit — most LLM-alpha claims are contaminated by hindsight. The honest result (LLM ≈ kNN except in the extreme rankings) tells you where the marginal edge actually is: the long/short tails, not the middle.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate the leakage-aware harness as a template for evaluating our own signal models
- **Anatomy of the Market: A Body-Tail Test of Factor Models** — Useong Shin, Jun 2026 — [arXiv:2606.23596](https://arxiv.org/abs/2606.23596)
  - **What it is:** Splits an investible market portfolio into size-ranked slices that recombine into the whole, then tests whether models that price the aggregate also price the parts. The q5 factor model shows systematic *offsetting* alphas — negative in the body, positive in the tail — that cancel at the aggregate and create a false appearance of efficiency.
  - **Why it matters for trading:** A diagnostic warning: passing an aggregate GRS/alpha test does not mean a factor model is clean. Body-tail decomposition is a cheap robustness check before trusting any factor model for cross-sectional bets. Pairs with Shin's earlier construction-dependence result ([2606.19550], 06-20).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve as a model-validation checklist item

### Microstructure & execution
- **Mitigating Adverse Selection in Concentrated Liquidity AMMs with Dynamic Fees: An Agent-Based Model Approach** — Daniele Maria Di Nosse, Fabrizio Lillo, Jun 2026 — [arXiv:2606.23070](https://arxiv.org/abs/2606.23070)
  - **What it is:** ABM of Uniswap-v3 LPs measuring loss-versus-rebalancing (LVR). Tests volatility- and toxicity-conditioned dynamic fees. Key result: dynamic fees raise LP profitability mainly by *increasing fee income in stale-price / high-toxicity states*, not by reducing the underlying LVR exposure.
  - **Why it matters for trading:** Reframes AMM fee design as state-conditional compensation rather than risk reduction — directly relevant to LP/MM strategy on concentrated-liquidity DEXs, and a counterpoint to the closed-form optimal-fee result from 06-23 ([2606.21769], Ghasemlu). Lillo (tracked) again.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read alongside the Ghasemlu LVR paper; contrast ABM vs stochastic-control conclusions
- **Empirical Confirmation of the Square-Root Law of Market Impact in a U.S. Large-Cap Equity** — Aniket Vasaikar, Jun 2026 — [arXiv:2606.24019](https://arxiv.org/abs/2606.24019)
  - **What it is:** Reconstructs metaorders from anonymous Nasdaq TotalView-ITCH (AAPL, 178 days, ~0.5B events) and tests impact ∝ Q^α. Finds α≈1/2 with prefactor c_raw≈0.69; decisively rejects linear and logarithmic alternatives; structural tests rule out spuriousness.
  - **Why it matters for trading:** A reproducible recipe to calibrate the square-root impact constant from public anonymized data — directly feeds execution-cost models and optimal-scheduling. Single-name scope is the limitation.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate the metaorder-reconstruction method on our traded names

### Risk & portfolio
- **Universal Value-at-Risk Superadditivity** — Yuyu Chen, Liyuan Lin, Ruodu Wang, Jun 2026 — [arXiv:2606.22884](https://arxiv.org/abs/2606.22884)
  - **What it is:** Studies VaR superadditivity at *all* probability levels as a property of random *vectors* (not marginals), with preservation rules under transformations. Shows that under weighted universal VaR superadditivity, every distortion risk measure is superadditive, so the optimal allocation concentrates on a single asset.
  - **Why it matters for trading:** A precise statement of when diversification *backfires* under heavy tails — a guardrail for risk-parity / min-var construction and for stress regimes where naive diversification adds tail risk. Ruodu Wang is a top risk-measure theorist.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; map conditions to our portfolio's tail-dependence assumptions
- **Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk** — Abdulrahman Alswaidan, Cade Jin, Jeffrey D. Varner, Jun 2026 — [arXiv:2606.23492](https://arxiv.org/abs/2606.23492)
  - **What it is:** Continuous HMM separating temporal dynamics from the return distribution, fit by a unified EM with heavy-tailed emissions. Finds that heavy-tailed *marginals* — not extra temporal-decay modes — explain volatility clustering, yielding a simpler, interpretable regime + regime-conditional VaR model.
  - **Why it matters for trading:** A parsimonious regime-detection + tail-risk engine that's interpretable enough to trust in a risk overlay; the "marginals, not memory" finding simplifies model selection for vol-clustering.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest as a regime filter for position sizing
- **Asymmetry PRISM: A CPU/GPU Portfolio Optimization Engine for Deadline-Bounded Institutional Rebalancing** — Debdoot Ghosh, Jun 2026 — [arXiv:2606.23367](https://arxiv.org/abs/2606.23367)
  - **What it is:** A parallel (CPU+GPU) constrained-portfolio-optimization engine for rebalancing hundreds of accounts under a hard wall-clock deadline. CPU build 4.5×–24.1× faster than reference solvers; GPU build does 500 accounts in 25 min where the baseline finished 4 (3.4×–126.7× speedup).
  - **Why it matters for trading:** Throughput, not alpha, is the constraint at scale — this is the kind of execution-infrastructure edge that lets a desk rebalance everything inside the close window. Relevant if/when the strategy library moves to multi-account.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 4/5
  - **Next step:** shelve; revisit when multi-account rebalancing is on the roadmap
- **Randomized Neural Networks for Estimation of Exposure Profiles and CVA for American Equity Options** — Isidro Moroso Varona, Jakub Michańków, Paweł Sakowski, Jun 2026 — [arXiv:2606.24309](https://arxiv.org/abs/2606.24309)
  - **What it is:** Uses randomized feedforward NNs inside Monte Carlo to estimate exposure profiles and CVA for American options under Black–Scholes and Heston. Matches Least-Squares Monte Carlo accuracy at lower compute, scaling better in high-dimensional multi-asset baskets.
  - **Why it matters for trading:** Counterparty-risk (CVA/XVA) pricing at lower cost and better scaling — useful for any book carrying American-style or basket options. The randomized-NN-as-fast-regressor trick generalizes beyond CVA.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve as a fast-pricing technique reference

### Asset class / market
- _Crypto/DEX coverage this run folds into the Lillo AMM item above; no standalone new asset-class finding above the bar._

## New resources & tooling
- _No new repos/datasets this run — all findings are method papers. KineticSim ([2606.21784], 06-23) remains the most recent open-tooling lead._

## Watchlist updates
- **Mao Guan / Qian Chen** — leakage-aware LLM forecasting & macro-factor ranking; rigorous evaluation protocol worth following. *(add)*
- **Useong Shin** — factor-model diagnostics (construction-dependence + body-tail tests); two papers in two weeks. *(add)*
- **Ruodu Wang (Waterloo)** — risk-measure theory; VaR (super)additivity and diversification limits. *(add)*
- **Jakub Michańków / Paweł Sakowski (Univ. of Warsaw QFRG)** — ML for derivatives pricing / XVA (randomized NNs). *(add)*

## Open questions / threads to pull next run
- Contrast the two AMM dynamic-fee results — Di Nosse/Lillo (ABM, fee *timing*) vs Ghasemlu (stochastic control, optimal fee *level*, 06-23). Is there a unified state-conditional fee rule?
- Did not chase: 2606.22162 (Mori, temporal coarse-graining → posterior-implied default copulas) and 2606.22615 (SV-in-mean heavy-tail fast Bayesian HMM) — credit/vol modeling residue.
- Endogenous-randomness-from-adversarial-learning ([2606.22743], Jian Sun) — theory; revisit if it produces a tradable prediction.
- arXiv announce gap: 2606.24xxx is the leading edge (24 Jun) — next run should sweep 2606.24xxx+ for the rest of this batch.
