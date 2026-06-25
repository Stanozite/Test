# Quant Scout Digest — 2026-06-25

## TL;DR
- **LOB prediction obeys a power law** — predictive loss vs. compute is a clean scaling curve; the same study ships **FastBiNLOB**, a hardware-friendly axis-separable mixer that matches SOTA at much lower latency (Hedges). Compute frontier + a deployable fast model in one paper.
- **Calendar-spread alpha via hierarchical graph learning** — Hong & Klabjan (Northwestern) prove spreads beat long-only on information ratio, then learn maturity-dependent contract graphs to position them on CME commodities. Clean stat-arb recipe.
- **Crypto leadership is shifting** — directed Granger-causal HF networks (2020–2025) show **Ethereum now the most influential asset and Bitcoin's relative importance declining**; rankings are unstable, non-stationary (Shukla/Peyyala/Chakraborty).
- **ESG long-short can beat the benchmark** — TODIMSort/MEREC screen + Omega-ratio PSO optimizer on STOXX Europe 600 delivers competitive-to-superior risk-adjusted returns vs. non-ESG and market-cap weights (di Tollo et al.).
- **Pectra compounding pays small ETH stakers ~+5% APR, big providers <1%** — empirical map of who actually benefits from 0x02 auto-reinvest validators (Benseddik/Kraner/Tessone).

## Findings by focus area

### ML / AI for alpha
- **Hierarchical Graph Learning for Calendar Spread Strategies in Commodity Futures Markets** — Yoonsik Hong, Diego Klabjan (Northwestern), 2026-06-24 — [link](https://arxiv.org/abs/2606.25811)
  - **What it is:** (1) analytic proof that calendar spreads achieve higher information ratio and lower risk than long-only; (2) a map from ML predictions to spread positions; (3) a hierarchical graph net that exploits maturity-dependent relationships between contracts. Tested on CME commodities, beats baselines.
  - **Why it matters for trading:** A concrete, implementable stat-arb pipeline for futures — spreads are lower-margin, lower-tail-risk than outright, and the maturity-graph structure is the actionable novelty. Directly buildable for anyone trading commodity term structure.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate — graph construction + spread-mapping is the reusable part.

- **The Inference-Compute Frontier and a Latency-Efficient Architecture for Limit Order Book Prediction** — C. Evans Hedges, 2026-06-24 — [link](https://arxiv.org/abs/2606.25986)
  - **What it is:** On FI-2010, predictive loss vs. structural forward-work is well-summarized by a power law that extrapolates to held-out high-compute architectures. Latency is *not* just noisy compute, motivating **FastBiNLOB** — a dense axis-separable LOB mixer of hardware-friendly temporal/feature ops that matches benchmark accuracy at notably lower latency.
  - **Why it matters for trading:** Scaling-law thinking tells you how much model to throw at LOB signal before diminishing returns; FastBiNLOB is a deployable low-latency predictor for execution/short-horizon alpha where latency is the binding constraint.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read + benchmark FastBiNLOB latency/accuracy vs. your current DeepLOB-class model.

### Microstructure & execution
- **Time-dependent weighted directed networks of cryptocurrency interaction from high-frequency returns** — Shubhangam Shukla, Mahesh Peyyala, Abhijit Chakraborty, 2026-06-24 — [link](https://arxiv.org/abs/2606.25466)
  - **What it is:** Directed, weighted networks built from statistically significant Granger-causal links between crypto returns, 2020–2025 HF data. Normalized returns are heavy-tailed; networks are heterogeneous and non-stationary. **Ethereum is consistently the most influential node; Bitcoin's relative importance declines over time**; rankings vary substantially through time.
  - **Why it matters for trading:** Lead-lag structure is tradable — a directed influence graph is a candidate signal for cross-crypto momentum/mean-reversion and for ordering execution across correlated names. The non-stationarity warning is itself actionable (don't hard-code a static hub).
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** backtest lead-lag signal from the directed graph on a liquid crypto basket.

### Risk & portfolio
- **A Two-Stage Decision Support System for Sustainability-Aware Long Short Portfolio Optimization** — Giacomo di Tollo, Massimiliano Kaucic, Filippo Piccotto, 2026-06-24 — [link](https://arxiv.org/abs/2606.25696)
  - **What it is:** Stage 1 classifies assets with a multi-criteria TODIMSort procedure, weights from the MEREC method; Stage 2 solves a non-convex Omega-ratio-maximizing long-short problem with an adaptive particle-swarm solver + constraint handling. On 421 STOXX Europe 600 names, ESG-enhanced long-short matches or beats non-ESG and the cap-weighted benchmark.
  - **Why it matters for trading:** Shows an ESG tilt need not cost risk-adjusted return when paired with Omega (tail-aware) optimization — useful for mandate-constrained European long-short books. The MEREC→TODIMSort→Omega/PSO stack is a reusable screening-plus-optimization template.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve unless an ESG mandate is live; then lift the Omega-PSO optimizer.

### Asset class / market
- **When Staking Rewards Compound: Measuring the Impact of Ethereum's Pectra Upgrade** — Mohammed Benseddik, Benjamin Kraner, Claudio J. Tessone (UZH Blockchain), 2026-06-22 — [link](https://arxiv.org/abs/2606.23337)
  - **What it is:** Empirical study of Pectra (May 2025), which raised max validator stake 32→2,048 ETH and enabled auto-reinvest 0x02 compounding validators. **Compounding adds ~+5% relative consensus-layer APR for small balances, <1% for large providers.** Solo stakers adopt faster but face ops hurdles; providers cite infrastructure cost. 0x02 migration expected to stay gradual.
  - **Why it matters for trading:** Quantifies the real ETH staking carry by validator size — input to ETH yield/basis and staked-ETH (LST) relative-value trades, and to modeling staking-flow supply dynamics.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve as reference for ETH carry/LST modeling.

## New resources & tooling
- **FastBiNLOB** (architecture, in 2606.25986) — axis-separable LOB mixer, hardware-friendly temporal/feature ops; SOTA accuracy at lower latency. No public repo cited yet — watch for release.

## Watchlist updates
- **Diego Klabjan (Northwestern, Master of Science in Analytics / engineering)** — ML for futures stat-arb; graph learning on term structure. Worth tracking for commodity/futures alpha.
- **C. Evans Hedges** — scaling-laws + latency-efficient architectures for market-microstructure ML.
- **Claudio J. Tessone / UZH Blockchain Center** — empirical crypto/Ethereum economics (staking, validator dynamics). On-chain carry & supply research.

## Open questions / threads to pull next run
- **Multi-Stream Fraud Transformer (MSFT)** — 2606.25007, Dashti Moghaddam/Sciarrilli — 0.996 AUROC on proprietary banking streams. Strong ML but fraud-detection, not trading alpha; revisit only if surveillance/anomaly tooling becomes in-scope.
- **Geometrically convex return risk measures on AM-algebras** — 2606.26031, Laudagé (cross-listed math.FA) — pure risk-measure theory; shelve unless a concrete portfolio application appears.
- **Diagonal Frog FD schemes for anisotropic Fokker-Planck** (2606.23980, Itkin) and **Analytic Bermudan swaption pricing with few exercise dates** (2606.23510, Papa) — derivatives-numerics residue from the 2606.23 batch; pull if options/rates pricing becomes a focus.
- Thin Thursday window (single-day since last digest) — next run should sweep 2606.26–27 announcements plus any GitHub/blog releases not covered here.
