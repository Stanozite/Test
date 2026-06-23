# Quant Scout Digest — 2026-06-23

## TL;DR
- **Risk-sensitive RL portfolio allocation gets an explicit-solution backbone** (Lleo & Runggaldier): free-energy/entropy duality turns benchmarked allocation into an LQG stochastic game, solved by continuous-time q-learning, with allocations reading as fractional-Kelly decompositions.
- **A clean, growth-optimal AMM fee rule** (Ghasemlu): under loss-versus-rebalancing the optimal fee is independent of LP wealth/risk-aversion, strictly increasing in instantaneous variance (pro-cyclical), and weakly dominates every static/vol-linked heuristic on every simulated path.
- **GPU market-simulator that's ~3,400× faster than NumPy** (KineticSim): persistent shared-memory clearing cuts depth from Θ(L+A) to Θ(log L + ⌈A/L⌉), 54.7B agent-events/s — infrastructure for fast RL/backtest loops.
- **On-chain execution cost map** (Mizrach): Ethereum mainnet median fee fell $2 → <$0.02, L2 fees down >95%; mainnet projected to reach Solana-level pricing by Aug 2027 but throughput stays constrained.

## Findings by focus area

### ML / AI for alpha
- **Reinforcement Learning for Risk-Sensitive Investment Management: a Free Energy–Entropy Duality Approach** — Sebastien Lleo & Wolfgang Runggaldier, 18 Jun 2026 — [link](https://arxiv.org/abs/2606.20903)
  - **What it is:** Continuous-time risk-sensitive benchmarked asset allocation reformulated via free-energy/entropy duality into an LQG stochastic differential game with explicit solutions; solved with a continuous-time q-learning actor-critic (one actor for the portfolio, one adversarial), with allocations interpretable as fractional-Kelly decompositions. Validated on U.S. equity data.
  - **Why it matters for trading:** Bridges the gap between elegant risk-sensitive control theory (Bielecki–Pliska lineage) and learnable policies — you get a principled RL allocator whose output you can sanity-check against a closed-form Kelly benchmark, rather than a black-box agent.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read → replicate the q-learning critic on a small equity universe

### Microstructure & execution
- **Optimal Dynamic Fees for Automated Market Makers: A Stochastic Control Approach to Loss-Versus-Rebalancing** — Farbod Ghasemlu, 19 Jun 2026 — [link](https://arxiv.org/abs/2606.21769)
  - **What it is:** Models constant-product AMM LP wealth relative to a rebalanced benchmark (LVR) as a controlled process; fees trade revenue against deterred volume. Result: growth-optimal fee is independent of LP wealth and CRRA, strictly increasing in instantaneous variance (pro-cyclical); under stochastic vol it solves an HJB. Empirically weakly dominates every static and vol-linked heuristic on each simulated path.
  - **Why it matters for trading:** A concrete, implementable fee schedule for liquidity provision — and the "fee ∝ instantaneous variance" rule is a directly testable market-making heuristic, on-chain or off.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest the pro-cyclical fee against a fixed-fee baseline on a liquid pair
- **Transaction Costs and Speed in the Ethereum Ecosystem: Scalability of the Mainnet and Layer 2s** — Meghan Ambrosia & Bruce Mizrach, 20 Jun 2026 — [link](https://arxiv.org/abs/2606.22206)
  - **What it is:** Empirical study (Jan 2024–Mar 2026) of fees and speed across Ethereum mainnet, L2s, and Solana. Mainnet median fee fell from >$2 to <$0.02; L2 median fees down >95%. Forecasts mainnet fee parity with Solana by ~Aug 2027 with throughput still constrained; L2s projected to outpace Solana throughput at lower cost; EIP-7938 only modestly helps capacity.
  - **Why it matters for trading:** A grounded transaction-cost map for any on-chain execution or DeFi strategy — sizes the cost wedge by venue and the trajectory, which feeds directly into where on-chain TCA pays off.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read → fold venue cost curves into any on-chain execution model

### Risk & portfolio
- **A Censored Transformed Model for Proportional Outcomes with Boundary Mass, with an Application to Loss Given Default Modeling** — Yuan Christopher Qiang & Fabio Sigrist, 19 Jun 2026 — [link](https://arxiv.org/abs/2606.21515)
  - **What it is:** The zero-one censored transformed normal (ZOC-TN) model for proportional responses with probability mass at 0 and 1 (a censored Gaussian for boundaries + a transformation for interior). Captures more density shapes than benchmarks while staying parsimonious; extended with ML (tree boosting) and spatio-temporal effects. On U.S. residential mortgage LGD, the tree-boosted spatio-temporal version wins.
  - **Why it matters for trading:** A better-calibrated tool for any bounded-ratio target (LGD, recovery rates, fill ratios, hit rates) — boundary mass is exactly where naive Beta/OLS models misbehave. Sigrist's boosting framework (gpboost-adjacent) makes it practical.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve → revisit if modeling a bounded-ratio target

### Asset class / derivatives
- **Semi-Analytical Pricing for General Default Intensity Models** — Ryan Parker, Mark Stedman & Luca Capriotti, 19 Jun 2026 — [link](https://arxiv.org/abs/2606.21800)
  - **What it is:** Path-integral method giving an accurate, easy-to-compute semi-analytical approximation for a general class of default-intensity models; demonstrated on Black-Karasinski with strong precision at high vol and long horizons. Computationally competitive with fully numerical schemes for econometrics, derivatives, and XVA; worked example prices a quanto CDS with stochastic intensity + FX devaluation.
  - **Why it matters for trading:** Fast, accurate credit-intensity pricing matters for XVA desks and credit-FX hybrids; the path-integral approximation is a reusable trick to replace slow PDE/MC grids where speed gates the book.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read → assess vs current intensity-model pricing where latency binds

## New resources & tooling
- **KineticSim** — Jayakody & Jayakody, 19 Jun 2026 — [link](https://arxiv.org/abs/2606.21784) — GPU execution engine for real-time market simulators: a persistent, state-carrying shared-memory clearing pattern cuts computational depth from Θ(L+A) to Θ(log L + ⌈A/L⌉), hitting >54.7B agent-events/s (3,406× NumPy, 27.8× PyTorch-GPU, 42.8× JAX-GPU) with bitwise-identical outputs and lower GPU memory. Infrastructure for fast multi-agent RL/backtest loops.

## Watchlist updates
- **Sebastien Lleo & Wolfgang Runggaldier** — risk-sensitive stochastic control + RL for portfolio management (continuous-time q-learning, fractional Kelly). Worth tracking as the rigorous end of RL-for-allocation.
- **Bruce Mizrach (Rutgers)** — market microstructure economist now mapping on-chain (Ethereum/L2/Solana) transaction costs; useful for DeFi execution cost grounding.
- **Luca Capriotti** — fast/semi-analytical pricing (path integrals, AAD lineage) for credit and XVA.
- **Fabio Sigrist (HSLU)** — gradient-boosting + spatio-temporal mixed models (gpboost) applied to bounded-ratio credit targets.

## Open questions / threads to pull next run
- arXiv batch this run topped out around 2606.22xxx (submissions through 20 Jun, announced ~22–23 Jun). The 23 Jun evening batch may add fresh q-fin.TR/PM — re-sweep next run for IDs above 2606.222xx.
- Did not chase: 2606.22162 (multi-sector default-count copulas, Mori), 2606.21871 (On Prudence of Risk Measures — risk-measure theory), 2606.21539 (forecast-gap attribution across model suites). Pull if a risk-theory or model-attribution thread is in scope.
- GitHub/tooling sweep was light this run — next run, scan for new releases tied to the agentic-trading frameworks already tracked (Vibe-Trading, QuantTradingOS).
