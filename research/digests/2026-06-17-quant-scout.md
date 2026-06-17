# Quant Scout Digest — 2026-06-17

_Window: items newer than the 2026-06-16 run (mostly 11–17 Jun 2026 submissions). All
items below verified against live arXiv abstracts; deduped against `INDEX.md`. Note:
"Trading in the Sunshine on Hyperliquid" (Barone & Lillo, 2606.15715) surfaced again but
was already captured on 2026-06-16 — skipped._

## TL;DR
- **Per-action causal impact detection** (Zovko): stop guessing from slippage — test for *timing synchronicity* between your fill and the next adverse event to tell self-impact from a competitor stealing the same liquidity. Opposite optimal response in each case.
- **Schur-damping identity** (Cotton): hierarchical-risk-parity ↔ min-variance and spatial-statistics shrinkage are *the same closed-form operation*; the weather modelers' fitted damping intensity is a ready recipe for portfolio covariance shrinkage.
- **PIVOT** (Horvath/Buehler et al.): a differentiable Jäckel "Let's Be Rational" IV layer with an open Triton kernel — Pareto-dominates baselines, up to 43% lower held-out price MAE on SPX. Plug-in for option-learning pipelines.
- **CFOs as LLM digital twins** (Campbell Harvey et al.): LLM role-playing a specific CFO forecasts that CFO's actual survey optimism, surviving firm + year-quarter fixed effects → scalable high-frequency expectations data.
- **Crypto diversification is a downside illusion** (tail-dependence graphs): standard models underestimate market-wide crash probability ~8×; lower-tail graph near-complete and stable.

## Findings by focus area

### ML / AI for alpha
- **CFOs Meet LLMs** — John R. Graham, Campbell R. Harvey, Manish Jha (arXiv q-fin.CP), 11 Jun 2026 — [link](https://arxiv.org/abs/2606.13812)
  - **What it is:** Prompt an LLM to role-play as a specific company's CFO at a specific date; it reproduces individual responses to the Duke-Fed CFO Survey economic-optimism question (2002–2025), surviving firm and year-quarter fixed effects plus a control for the prior response. Accuracy rises with supplied history/firm characteristics.
  - **Why it matters for trading:** A path to scalable, high-frequency "expectations" data (business sentiment as a digital-twin panel) where real surveys are slow, sparse, and lagged — a candidate macro/sentiment overlay.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read / prototype a digital-twin expectations index, then shelve until validated out-of-sample.
- **Continuous-time Optimal Stopping through Deep RL (CARLOS)** — Cosmin Borsa, Michael Ludkovski (arXiv q-fin.CP / stat.ML), 16 Jun 2026 — [link](https://arxiv.org/abs/2606.17545)
  - **What it is:** An RL-inspired solver that learns a joint space-time exercise boundary at arbitrarily fine resolution, progressively refining the stopping grid with adaptive sampling concentrated near the boundary. Beats Bermudan solvers, approaches the American upper bound, high compute efficiency.
  - **Why it matters for trading:** Optimal-stopping = American/Bermudan exercise and, by analogy, discretized execution/exit timing — removes the coarse-grid undervaluation vs fine-grid error-accumulation tradeoff.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** replicate on a Bermudan benchmark; assess transfer to execution-timing.
- **Robust Transformer One-Step Stock Index Forecasting via Shifted Data Augmentation (SDA)** — Tien Thanh Thach (arXiv q-fin.ST), 14 Jun 2026 — [link](https://arxiv.org/abs/2606.15701)
  - **What it is:** Modified Transformer + cosine-annealing-with-warmup + a Shifted Data Augmentation scheme for one-step index forecasting (VN30, S&P 500). SDA cuts error and run-to-run variance and improves hyperparameter robustness; data augmentation mattered more than model size.
  - **Why it matters for trading:** Cheap, practical robustness recipe for noisy short-memory financial series — the SDA trick is directly portable to existing forecasting stacks.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest SDA as a drop-in augmentation on an existing index model.

### Microstructure & execution
- **Realtime price impact detection** — Ilija I. Zovko (arXiv q-fin.TR), 11 Jun 2026 — [link](https://arxiv.org/abs/2606.13419)
  - **What it is:** Per-action impact test based on timing *synchronicity* between a trader's action and the subsequent adverse event — "surprisingly fast" adverse moves as a signature of causation/leakage — instead of statistically expensive slippage estimation (which needs hundreds of fills and can't establish causality). Empirical validation tests are specified, not yet run.
  - **Why it matters for trading:** Directly addresses the execution dilemma: self-impact says "slow down," a competitor capturing the same alpha says "speed up" — opposite responses the conventional slippage monitor cannot distinguish.
  - **Scores:** Novelty 5/5 · Credibility 3/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read closely; replicate the timing-surprise test on internal execution data (the missing validation).
- **Revisiting Trade-sign Long-memory and Square-root Law Price Impact** — Chris Angstmann, Tim Gebbie (arXiv q-fin.TR), 15 Jun 2026 — [link](https://arxiv.org/abs/2606.16269)
  - **What it is:** A coupled reaction–diffusion model of lit + latent order books with non-uniform event times derives both Lillo–Mike–Farmer trade-sign long-memory and the square-root impact law from one framework, reducing to a Volterra equation under constant participation. Key reframe: LMF is an *event-time* sign-memory statement, the square-root law a *physical-time* viability statement.
  - **Why it matters for trading:** Unifies two cornerstone microstructure regularities and clarifies the event-time vs calendar-time mapping that governs how meta-order impact actually accrues during execution.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** read; useful theory grounding for impact models — not directly implementable yet.

### Risk & portfolio
- **Two Sides of Schur Damping: High-Dimensional Pseudo-Likelihoods and Portfolio Allocation** — Peter Cotton (arXiv q-fin.PM / q-fin.RM), 11 Jun 2026 — [link](https://arxiv.org/abs/2606.14798)
  - **What it is:** Shows that the Schur-complement damping spatial statisticians use to keep Gaussian (Vecchia) pseudo-likelihoods estimable is, term for term, the damping that interpolates hierarchical risk parity and the minimum-variance portfolio — one operation: reliability shrinkage of a conditional Gaussian, with a closed-form James-Stein / Ledoit-Wolf intensity. The optimal damping is a closed-form reliability; the spatial community's fitted intensity looks like the better recipe.
  - **Why it matters for trading:** A principled, closed-form way to set covariance/diversification shrinkage when assets outnumber returns — exactly the high-dimensional portfolio-construction regime.
  - **Scores:** Novelty 5/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** replicate the damping recipe; compare fitted-intensity vs Ledoit-Wolf on a live universe.
- **On Reference-Regulated Multiperiod Mean-Variance Portfolio Optimization in High Dimensions (RRMV)** — Yutao Deng, Jianjun Gao, Weichen Wang (arXiv q-fin.PM), 31 May 2026 — [link](https://arxiv.org/abs/2606.13697)
  - **What it is:** Multiperiod MV that penalizes deviation from a reference policy, combining dynamic strategies with reference portfolios; characterizes out-of-sample Sharpe under high-dimensional asymptotics with errors in *both* mean and covariance, showing how reference penalty + horizon jointly drive performance. Simulations + real data show materially higher OOS Sharpe and stability.
  - **Why it matters for trading:** Estimation-error-robust dynamic allocation with an explicit anchor (e.g., a benchmark or prior book) — practical for multiperiod rebalancing under turnover/tracking constraints.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; backtest RRMV vs single-period shrinkage on a multiperiod book.
- **A Multiplex Network Hawkes Model for Systemic Risk Measurement** — Mante Zelvyte, Jim E. Griffin (arXiv q-fin.ST / q-fin.RM), 14 Jun 2026 — [link](https://arxiv.org/abs/2606.15755)
  - **What it is:** Extends network Hawkes with multiple covariate-dependent excitation layers to separate contagion channels within one inferred transmission network; applied to a 99-firm cross-industry CDS dataset (2004–2022). Finds sparse contagion concentrated in outward flows from a few influential institutions; industry similarity the most consistent asset-similarity channel.
  - **Why it matters for trading:** Channel-resolved systemic-risk monitoring — identifies which institutions and which mechanisms (similarity/solvency/profitability) drive contagion, useful for credit/tail hedging and counterparty screens.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve / read — strong methodology, heavy to operationalize.

### Asset class / market
- **PIVOT: Bridging Black-Scholes Implied-Volatility and Price Objectives via Differentiable Jäckel Operator** — Raeid Saqur, Yannick Limmer, Anastasis Kratsios, Blanka Horvath, Hans Buehler (arXiv q-fin.CP), Jun 2026 — [link](https://arxiv.org/abs/2606.17065)
  - **What it is:** A differentiable layer that keeps Jäckel's "Let's Be Rational" IV solver intact in the forward pass and supplies the backward pass by implicit differentiation through the BS/Black-76 price map, with explicit gating for the low-vega singularity. Fused Triton kernel hits 1.79e9 IV/s at machine precision; PIVOT-augmented objectives cut held-out SPX price MAE by up to 43.4% and improve IV MAE jointly; cross-asset gains on RUT/VIX/NDX.
  - **Why it matters for trading:** Removes the price-space ↔ IV-space interface bottleneck in option-learning systems — lets models train in IV coordinates while enforcing no-arbitrage in price space, at production throughput.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** replicate; integrate the differentiable IV layer into an option surface / deep-hedging pipeline.
- **Crashing Together, Rallying Apart: Dynamic Conditional Tail Dependence in Cryptocurrency Markets** — Rama Siva Sarwari Mallela, Manuele Leonelli (arXiv q-fin.ST), 15 Jun 2026 — [link](https://arxiv.org/abs/2606.16840)
  - **What it is:** Dynamic Hüsler-Reiss graphical models of extremes over 89 overlapping windows (late 2021–2025) on the 13 largest cryptos, estimated separately for joint crashes and rallies vs a Gaussian benchmark. Lower-tail graph near-complete and stable; upper tail thins into sectoral structure; ordinary categories collapse into a Bitcoin-Ethereum-anchored block.
  - **Why it matters for trading:** Quantifies that intra-crypto diversification fails on the downside — standard covariance models understate market-wide crash probability ~8×; extremal graphs as a superior systemic-risk monitor for crypto books.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; consider tail-dependence graph as a crypto crash-risk monitor / sizing input.

## New resources & tooling
- **PIVOT differentiable Jäckel IV operator** — fused Triton kernel, machine-precision IV inversion at 1.79e9 IV/s (from 2606.17065). A reusable autograd layer for any option-learning / deep-hedging stack — [link](https://arxiv.org/abs/2606.17065).
- **CARLOS optimal-stopping solver** — adaptive RL exercise-boundary learner approaching the American upper bound (from 2606.17545); reference algorithm for Bermudan/American pricing experiments — [link](https://arxiv.org/abs/2606.17545).

## Watchlist updates
New players worth adding to `watchlist.md`:
- **John R. Graham & Campbell R. Harvey (Duke / Fuqua)** — LLM-as-expectations-data, CFO survey; Harvey is a foundational factor/asset-pricing name.
- **Tim Gebbie & Chris Angstmann (UCT / UNSW)** — reaction–diffusion microstructure, trade-sign memory, square-root impact, Epps effect in coupled LOBs.
- **Peter Cotton** — high-dimensional covariance shrinkage / portfolio damping, cross-pollinating spatial statistics.
- **Blanka Horvath & Hans Buehler** — deep hedging / volatility-surface learning (PIVOT, differentiable IV).
- **Michael Ludkovski (UCSB)** — computational finance, RL for optimal stopping.

## Open questions / threads to pull next run
- **Coupled-LOB Epps effect** (Angstmann & Gebbie, 2606.14182) — companion to the square-root-law paper; correlation emergence in two coupled order books. Worth a full read next run.
- **Beyond the Smile: Hybrid Convolutional VAE for Crypto Volatility Surfaces** (2606.16961) — generative crypto vol-surface modeling; pairs with PIVOT and the crypto tail-dependence finding.
- **Declining CVaR Glidepath for Target-Date Funds** (Muñoz, Suárez, Larré, Cifuentes, 2606.13618) — CVaR-based glidepath design; relevant to drawdown-aware allocation.
- **Martingale Doppelgänger-Eval** (2606.17423) — auditing candlestick understanding in vision-language models; probes whether VLMs actually "read" charts.
- **hftbacktest-class open-source LOB backtesters** — GitHub search surfaced a high-fidelity HFT/market-making backtester accounting for queue position and latency on L2/L3 tick data (Binance/Bybit), but a specific verified repo URL was not confirmed this run. Verify and capture the canonical repo next run rather than cite unverified.
