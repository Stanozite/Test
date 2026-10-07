# Quant Scout Digest — 2026-10-07

_Window: since the 2026-09-30 run (7 days). Swept arXiv q-fin.TR / PM / ST / CP / RM
October batch 2610.00005 → 2610.08631 (above last ceiling 2609.35744). October is
thin and heavily **agentic-evaluation / microstructure-theory** weighted — no new
tradable single-asset daily directional signal, consistent with the standing thread.
Deduped against the INDEX ledger; all items verified against live abstracts._

## TL;DR
- **The honest-evaluation thread hardens again — now at the implementation and
  attribution layers.** **Policy-Value Audit (2610.04040)** proves an LLM earnings
  agent's +15.2 bps/event is **+25.8 passive composition minus −10.6 selection**:
  once you hold the action-change counts fixed and reshuffle them across events, the
  agent **does not beat random** — a zero-centered paired test falsely credits skill
  in 11.6% of no-skill runs. **MintEval (2610.03080)** shows even a frontier model
  (Claude Opus 5.5) **silently mis-implements 27.5%** of plain-English strategies on
  BTCUSDT-15m, and *the LLM judge accepts every one*. **FactorBench (Ventre, 2610.06947)**
  benchmarks ~5,000 mined factors × 9 methods × 5 markets: **no paradigm dominates.**
  Three independent "who judges / what survives" results in one week.
- **AlphaPADI (2610.04959)** is the proposer-side counterweight: pool-aware hierarchical
  discrete diffusion that generates whole alpha *pools* (not one formula at a time),
  beating RL/GFlowNet baselines on CN+US — the strongest new alpha-mining architecture
  this window, but a cross-sectional-equity method, not a single-series signal.
- **Crypto-native work is execution/honest-negative, not a daily edge:** MoE for
  BTC/USDT order execution (**2610.03369**) finds **no RL config beats TWAP**, and that
  MoE "masks a training-specification failure"; the failure attribution **flips between
  30 and 100 seeds** → the RL analogue of grid-overfitting.
- **Tracked players land four:** Angstmann/Diana/**Gebbie** reaction-diffusion finite
  spread (2610.07985); **Rodriguez Dominguez** admissible-information portfolio pair
  (2610.00147/00158, "causal identification has an oracle price"); **da Costa Nunes**
  "Cities of Signals" signal-geometry (2610.04122); **Ventre** FactorBench.
- **Backtest: weak_meanrev on BTC-USD → REJECT** (anchored to Hoffmann & Rasonyi
  2610.08631). The single-asset *level* OU-gap trade has **no in-sample edge to begin
  with** (best-of-grid train Sharpe 0.177) → OOS 0.019, full −0.551, short leg ruinous
  (MaxDD −97.6%). **The mean-reversion axis is now exhausted on daily crypto from all
  three angles** (horizon-1 / ratio / single-asset level). 18th straight reject-lean.

## Findings by focus area

### ML / AI for alpha
- **Agent Policy-Value Audit: Separating Transition Composition from Event Selection in Financial LLM Agents** — Chen, Xu, Chen, Lu & Jin, 2 Oct 2026 — [arXiv:2610.04040](https://arxiv.org/abs/2610.04040)
  - **What it is:** An audit that decomposes a financial LLM agent's realized return into a *composition benchmark* (hold the observed count of each ordered action-change type fixed, randomly reassign them across eligible events) and *selection value* (observed − composition). On 723 earnings events / 44 US consumer firms, +15.2 bps/event = +25.8 composition − 10.6 selection; the agent **does not detectably beat matched random assignment**. A zero-centered paired test mislabels passive exposure as skill 11.6% of the time; the audit cuts that to 5.3%.
  - **Why it matters for trading:** This is the exact failure mode behind every "my agent made money" claim — an up-drifting event pool makes a position-churning random agent look skilled. It operationalizes the repo's recurring "who/what judges" lesson at the *attribution* layer and gives a drop-in correction (report deployment value and selection value separately). Direct successor to Gençay (2608.27734) and Qu/Chen/Wang (2609.27051).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 5/5
  - **Next step:** read (adopt the composition/selection split in the repo's own backtest gate)

- **MintEval: Do LLMs Implement the Trading Strategy You Asked For?** — S. Wang, Y. Wang & He, 2 Oct 2026 — [arXiv:2610.03080](https://arxiv.org/abs/2610.03080)
  - **What it is:** A behavioural-equivalence benchmark for natural-language→strategy-code. 800 tasks on BTCUSDT 15-minute data; reference strategies are built from composable blocks, back-translated to colloquial instructions, re-implemented by the model, then compared **bar-by-bar on actions** (alpha is differenced away). Low-cost models reach ActionMatch ≤ 0.544 / exact ≤ 0.087; a frontier model (Claude Opus 5.5) reaches 0.889 but **still fails silently on 27.5%** of tasks; 79.2% of correctly-*specified* implementations diverge on >10% of active bars. **The LLM judge of a recent strategy-gen benchmark accepts every one of these silent failures.**
  - **Why it matters for trading:** The silent code-level failure is the layer *below* signal quality — the backtest plots, but the executed risk logic isn't what you described. Must-read for any LLM-authored backtest harness (including this repo's).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read

- **FactorBench: A Portfolio-Aware Benchmark for Automated Factor Mining** — Zhuohan Wang & Carmine Ventre, 3 Oct 2026 — [arXiv:2610.06947](https://arxiv.org/abs/2610.06947)
  - **What it is:** A shared data/evaluation contract comparing ~5,000 mined factors from **nine** automated methods (genetic programming, RL, generative, LLM agents) across **five** equity markets, tracing validity → temporal generalization → predictiveness beyond risk/style → pool distinctness (incl. similarity to Alpha101) → after-cost long-only / long–short portfolio performance. Headline: **no paradigm consistently dominates.**
  - **Why it matters for trading:** The portfolio-aware, cross-paradigm "so does any of this actually translate to after-cost PnL" audit the field lacked — and the answer continues the repo's "no AI architecture delivers persistent net alpha" thread (2609.04917). Tracked player (Ventre/Stillman lineage).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read

- **AlphaPADI: Formulaic Alpha Discovery via Pool-Aware Hierarchical Discrete Diffusion** — Jin, Shao, Ma, Pan, Zhai, Song, Shen & Kawaguchi, 4 Oct 2026 — [arXiv:2610.04959](https://arxiv.org/abs/2610.04959)
  - **What it is:** Generates whole alpha *pools* instead of formulas one at a time, via grammar-constrained buffer init + pool-aware hierarchical discrete diffusion (reconstructs complete pools at multiple structural scales under current pool context) + reward-guided refinement on joint predictive performance *and* inner diversity. Beats RL/GFlowNet baselines on Chinese and US equities in both predictive and portfolio performance.
  - **Why it matters for trading:** The proposer-side counterpart to FactorBench/Policy-Value-Audit — the first alpha-miner to put inter-formula complementarity *inside* the generative state (addressing the redundancy that PC1-crowding papers keep flagging, da Costa Nunes). Cross-sectional equity, not single-series.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (cross-sectional equity; revisit if/when a multi-asset crypto feed exists)

### Microstructure & execution
- **A Finite Bid–Ask Spread from Replenishment Displaced from the Quote** — Angstmann, Diana & Gebbie, 6 Oct 2026 — [arXiv:2610.07985](https://arxiv.org/abs/2610.07985)
  - **What it is:** A two-field (bid/ask) reaction–diffusion order book in operational time. A market-making source is introduced by **withholding placement over a finite interval around the reaction boundary** (round-trip replenishment displaced from the quote); the quoted spread emerges as the sub-threshold core of that placement-free interval, with a delayed, attenuated quote-level response. Finite spread and price impact arise from **distinct response sectors**, and their calendar-time appearance needs a separate observation clock.
  - **Why it matters for trading:** Continues the tracked Angstmann/Gebbie subordinated-microstructure lineage (2609.13715 event-time order-flow memory). The "spread and impact are different response sectors, visible only under the right clock" result is the structural reason daily-close signals keep washing out in this repo.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read

- **Mixture-of-Experts for Cryptocurrency Order Execution: Training Stability, Tail Risk, and Failure Modes** — Ardaiz, Budati & Habibnia, 2 Oct 2026 — [arXiv:2610.03369](https://arxiv.org/abs/2610.03369)
  - **What it is:** On 5-minute BTC/USDT Binance LOB data, compares vanilla Double-DQL, K-means MoE experts (K∈{2,4,8}), and parameter-matched dense nets. **No learned config significantly beats DDQL, and all have higher mean shortfall than TWAP (0.39 bps) and immediate liquidation (0.21 bps).** The MoE's apparent benefit (suppressing the 11/100 "wait-until-forced-liquidation" collapse) is reproduced by **annealed exploration alone**; MoE "masks a training-specification failure rather than confer an intrinsic benefit." Within-policy tail risk worsens monotonically with K, and **the failure attribution reverses between 30 and 100 seeds.**
  - **Why it matters for trading:** The crypto-native honest-negative of the week and a methods must-read: seed-dispersion is the RL analogue of grid-overfitting, and a baseline (TWAP / annealed exploration) beats the architecture. Reinforces "the edge people claim is usually a training/selection artifact."
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read

- **Beyond Supra-Competitive Outcomes: Collusive Behaviour in Deep RL for Optimal Execution Games** — Koulouris & Campajola, 30 Sep 2026 — [arXiv:2610.00619](https://arxiv.org/abs/2610.00619)
  - **What it is:** Two independent PPO agents in an Almgren–Chriss liquidation game learn a **punitive mechanism** — when one deviates, the opponent accelerates liquidation, and the punishment reliably exceeds the deviation gain while preserving the punisher's payoff. Both formal collusion conditions hold → the supra-competitive outcome is **collusion, not Nash**.
  - **Why it matters for trading:** A clean behavioural test for whether multi-agent "edge" is cooperative-equilibrium rather than skill; relevant to anyone deploying RL execution against other algos, and a caution that shared training dynamics can manufacture apparent profitability.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read

- **Event History Over Scale: Compact Transformers for Low-Latency LOB Forecasting (MBOFormer)** — Schaurecker, Strand, O'Sullivan & Jakob, 2 Oct 2026 — [arXiv:2610.02917](https://arxiv.org/abs/2610.02917)
  - **What it is:** A 7,203-parameter causal transformer (plus a 14,371-param fusion variant) that consumes **level-3 market-by-order** histories (submissions/cancels/executions) rather than L2 snapshots. Highest macro-F1 in 11 of 12 market×horizon settings, **sub-millisecond** inference on one M2 CPU thread, <70 kB serialized — 5–8× faster than million-param baselines at comparable quality.
  - **Why it matters for trading:** The latency-efficient-architecture / "fine-grained event history beats model size" lineage (Hedges). Confirms the actionable crypto frontier is message-level and intraday — the exact data this repo's daily cache can't reach.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (needs L3 MBO data)

### Risk & portfolio
- **Exponential investors with weakly mean-reverting prices** — Hoffmann & Rasonyi, 6 Oct 2026 — [arXiv:2610.08631](https://arxiv.org/abs/2610.08631)
  - **What it is:** For an exponential-utility investor in a market whose (log) price is **weakly** (sublinear) mean-reverting with nonzero drift, the certainty equivalent grows as O(T^{2β+1}), 0<β<1, and an explicit asymptotically optimal strategy is given (position driven by the current gap to the mean-reverting level). Complements earlier strong-mean-reversion work.
  - **Why it matters for trading:** The cleanest price-buildable daily anchor this window and the direct premise for a single-asset OU-gap trade — the one mean-reversion angle this repo had not yet tested on a single crypto series (lag-1 and the BTC/ETH ratio were done).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** **backtest** → done this run (`weak_meanrev` on BTC-USD → REJECT; see below)

- **Admissible Portfolio Optimization: Information Constraints, Conditional Efficient Frontiers, and the Price of Causal Identification** (+ companion *Causal Price-of-Risk Mandates under Overlapping Information*) — Alejandro Rodriguez Dominguez — [arXiv:2610.00147](https://arxiv.org/abs/2610.00147) / [2610.00158](https://arxiv.org/abs/2610.00158)
  - **What it is:** Treats the *conditioning information* in mean-variance optimization as a decision variable subject to admissibility constraints (availability at decision time, no-arbitrage preservation, statistical separation, interventional invariance). Proves existence of optimal information classes and a value-of-admissible-information theorem; key result — **requiring causal identification carries an explicit oracle price traded against search complexity.** Empirically (127 candidate drivers) it helps for individual equities but **not pre-diversified portfolios**, where minimum-variance matches it at lower turnover.
  - **Why it matters for trading:** Tracked player (capacity-as-causal-inference lineage). Formalizes why "use only decision-time, causally-identified signals" has a measurable cost — and why the easy wins are at the single-name, not the already-diversified, level.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read

- **Cities of Signals: Compression, Separation, and the Geometry of Novelty** — Marc da Costa Nunes, 2 Oct 2026 — [arXiv:2610.04122](https://arxiv.org/abs/2610.04122)
  - **What it is:** A cross-sectional signal (demeaned/normalized) is a point on a sphere; its **"city"** is the direction of its time-averaged vector in a target-aligned frame — a compressed summary. For independent uniform histories, a city angle ≤ 90° implies the *history* angle meets-or-exceeds it with probability →1 at O(T^{-1/2}) error, dimension-independent. Tested on AlphaNova competition data (May 2026, 266,815 signal pairs): city angles ≥ 60° identify high-quality signal pairs at 94.3% success while retaining 72.5% of candidates.
  - **Why it matters for trading:** A cheap, dimension-free screen for *distinctness/novelty* of signals before pooling them — the crowding problem da Costa Nunes has been formalizing (2609.12477, 2609.17609), now with an operational angle threshold.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read

- **Adversarial Training for Deep Hedging in Nonstationary Markets (WRAP)** — Schneider, Looser, Garin, Liu & Kuhn, 5 Oct 2026 — [arXiv:2610.07162](https://arxiv.org/abs/2610.07162)
  - **What it is:** A drift-aware adversarial training framework from a **two-budget DRO** formulation: around a weighted empirical reference (baseline weights balancing sampling uncertainty vs temporal drift), an adversary may *reweight* trajectories (φ-divergence budget) and *perturb* paths (optimal-transport budget). A joint first-order expansion yields a tractable finite-dimensional attack; across stationary/nonstationary Heston and a generalized affine diffusion, joint adversarial training gives the largest gains under nonstationarity.
  - **Why it matters for trading:** Directly targets the problem every backtest in this repo lives with — training paths that don't represent the future. The reweight-vs-perturb decomposition is a clean template for stress-testing any learned policy. Daniel Kuhn (DRO) is a top name worth tracking.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read

### Asset class / market
- _No new tradable single-asset daily directional signal this window._ The crypto-native
  output is execution and on-chain microstructure, not price timing: MoE BTC/USDT
  execution (2610.03369, above), the RED-2400 Solana/DeFi corpus (below), and
  **Priority Gas Auction Cadence / Flashblocks on Base** (2610.03922, searcher-competition
  MEV). This is the same pattern the standing thread records — the actionable crypto
  frontier sits at intraday/on-chain resolution the daily cache cannot reach.

## New resources & tooling
- **RED-2400 family v2** — [arXiv:2610.00005](https://arxiv.org/abs/2610.00005) — five public, record-level Solana/DeFi microstructure benchmark datasets over one 57-day 2026 window (ORACLE: Pyth-vs-CEX staleness, 164k obs; LIQ: Aave liquidations + 4-chain utilization; BASIS: spot-perp basis/funding, 245k obs; ARB: Solana CEX-vs-DEX spread + realized impact, 328k obs; BRIDGE: Wormhole cross-chain flow, 361k messages), fixed-seed reproducibility scripts, SHA-256 manifests, CC-BY-4.0. On-chain microstructure, not OHLCV — but the most on-point public feed yet for the repo's intraday/multi-venue blocker.
- **AlphaPADI / FactorBench / MintEval** are methods+benchmarks (above) rather than drop-in libraries; MintEval's block-composed BTCUSDT-15m task set is a reusable harness pattern if code is released.

## Watchlist updates
- **Carlo Campajola** — RL execution games + honest diagnosis of reward/behaviour (collusion 2610.00619; broker-trader PPO "correct reward is not enough" 2610.03598). Add.
- **Daniel Kuhn (EPFL)** — distributionally-robust optimization / adversarial deep hedging (WRAP 2610.07162); foundational DRO name. Add.
- **Ali Habibnia / Alexander Ardaiz** — crypto RL execution honest-negatives, seed-robustness discipline (2610.03369). Add.
- **Mingyang Chen / Wei Jin (group)** — financial-agent evaluation (Policy-Value Audit 2610.04040), the attribution-layer extension of the honest-eval lineage. Add.

## Open questions / threads to pull next run
- **The data-resolution blocker is now triple-pointed-at within one week:** MintEval and
  MoE-execution both work on **BTCUSDT 15-minute**, and RED-2400 ships record-level
  on-chain tapes — every live crypto result this window lives at a resolution the daily
  cache can't reach. The hourly/multi-coin OHLCV loader is the single highest-leverage
  build and is now ~7× overdue.
- **Mean-reversion axis closed on daily crypto** (horizon-1 / ratio / single-asset level all
  rejected). The remaining single-series experiments worth running are not new signals but
  *overlays on the exhaustion itself* (e.g. a principled bounded-drawdown control, Hsieh
  2609.23272) — or move off daily entirely.
- **Adopt the Policy-Value-Audit composition/selection split and MintEval's
  behavioural-equivalence check** into the repo's own backtest gate — both are methods this
  system should *use*, not just catalog.

---
_Backtest run this cycle: see `backtests/reports/2026-10-07-weak_meanrev-BTC-USD.md`.
`weak_meanrev` (single-asset OU level band, anchored to Hoffmann & Rasonyi 2610.08631) on
real cached BTC-USD (2922 bars) → **REJECT**: best-of-grid train Sharpe 0.177 (no in-sample
edge to begin with), OOS Sharpe 0.019 / CAGR −2.0%, full-sample Sharpe −0.551 / MaxDD −97.6%
(short leg ruinous). Confirms — does not falsify — the paper: a single trending crypto is not
weakly mean-reverting at the level. 18th straight daily-crypto reject-lean._
