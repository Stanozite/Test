# Quant Scout Digest — 2026-07-01

## TL;DR
- **The lag-1 "mean reversion" everyone trades is bid-ask bounce, not direction** (Portnaya): SPY lag-1 autocorrelation is magnitude-shrinkage (full test p<10⁻¹²), but the *sign* test is insignificant (p=0.11) — a big move predicts a smaller move, not a reversal. Crypto in her 21-asset panel is indistinguishable from a random walk. **→ this run's backtest target on BTC-USD.**
- **When building return models, spend your engineering budget on the output head, not the backbone** (He/Zhang): swapping backbone (TimesNet/DLinear/N-BEATS/iTransformer) buys <1.5%; a 4-component Gaussian-mixture head buys ~3.7% and +13.9% in high-vol regimes.
- **Signature methods unify the alpha *and* the execution schedule** (Morbelli/Karbach/Derksen): both modeled as linear functionals of the truncated path signature; a quadratic-reduction theorem collapses stat-arb execution to finite-dim optimization, beating z-score thresholds on return-to-turnover.
- **Hidden (non-linear) dependence is where aggregate tail risk actually lives** (De Vecchi/Nendel/Vanduffel): correlation-blind risk aggregation understates portfolio tails when dependence is concealed.
- **Thin mid-week window** — July-1 arXiv batch is sparse (q-fin.PM/CP announced 0 on 07-01); fresh IDs 2606.29xxx–2606.31xxx sit cleanly above last run's 2606.28063 ceiling.

## Findings by focus area

### ML / AI for alpha
- **Heads, Not Backbones: Output Heads Dominate Architectures on Fat-Tailed Returns** — Sichao He, Yansong Zhang, Jun 30 2026 — [link](https://arxiv.org/abs/2606.30037)
  - **What it is:** Factorial study crossing 4 backbones (TimesNet, DLinear, N-BEATS, iTransformer) × 3 output heads (point, single-Gaussian, 4-component Gaussian mixture) on S&P 500 monthly returns 1871–2023. Head choice dominates: point→Gaussian ≈ +1.3%, →mixture ≈ +2.4% more; backbone swaps <1.5%. Mixture gains concentrate in high-vol regimes (+13.9% in 1970s stagflation).
  - **Why it matters for trading:** Direct prior for any forecasting stack — a probabilistic mixture head on a *simple* backbone captures tail risk better than an exotic architecture with a point head. Cheaper, less overfit-prone.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read → shelve as a modeling prior for future signal work
- **When Summaries Distort Decisions: Information Fidelity in LLM-Compressed Financial Analysis** — Lee, Park, Lopez-Lira, Sabanis, et al., Jun 30 2026 — [link](https://arxiv.org/abs/2606.29251)
  - **What it is:** Large author panel measures how LLM summarization of financial documents degrades downstream investment decisions — information-fidelity loss, not just factual error.
  - **Why it matters for trading:** Anyone piping news/filings through an LLM into a signal is silently exposed to summary-induced distortion; this quantifies the leak.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (guardrail reference for any LLM-in-the-loop pipeline)
- **CLQT: A Closed-Loop, Cost-Aware, Strategy-Consistent Benchmark for Diagnostic Evaluation of LLM Portfolio-Management Agents** — Bo Qu, Mingguang Chen, Jun 30 2026 — [link](https://arxiv.org/abs/2606.29771)
  - **What it is:** Benchmark that scores LLM PM agents in a closed loop with transaction costs and strategy-consistency constraints, rather than one-shot recommendation accuracy.
  - **Why it matters for trading:** Extends the LLM-backtest-benchmark line (BacktestBench, AlphaForgeBench in ledger) toward cost-realistic, path-consistent evaluation — the honest way to grade agentic PM.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (evaluation infra, not a signal)

### Microstructure & execution
- **The Bounce Has No Direction: Sign, Magnitude, and the Microstructure of Equity Return Predictability** — Victoria Portnaya, Jun 28 2026 — [link](https://arxiv.org/abs/2606.29591)
  - **What it is:** Decomposes lag-1 return autocorrelation into a *sign* channel and a *magnitude* channel across 6 US instruments (1993–2026) plus a 21-asset cross-asset panel (equities, bonds, credit, commodities, FX, crypto). SPY: full autocorrelation test p<10⁻¹² but the sign test is insignificant (p=0.11) → yesterday's large move predicts a *smaller* move today regardless of direction — bid-ask bounce / staleness, not mean reversion. A weak directional reversal reappears at lag-3 (p=0.02). Mean reversion is confined to exchange-traded equities and sovereign bonds; other classes (incl. crypto) ≈ random walk.
  - **Why it matters for trading:** Falsifies naive "fade the big move" strategies: the sign is not predictable, so a lag-1 reversal rule has no directional edge and just churns the spread. Clean, cheap, falsifiable on crypto.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 5/5
  - **Next step:** **replicate / backtest** — lag-1 mean-reversion rule on BTC-USD; expect no directional edge (this run's backtest)
- **Signature-Based Optimal Execution for Statistical Arbitrage with Path-Dependent Trading Signals** — Gianmarco Morbelli, Sven Karbach, Mike Derksen, Jun 30 2026 — [link](https://arxiv.org/abs/2606.31387)
  - **What it is:** Models both the alpha process and trading speed as linear functionals of the truncated signature of a time-augmented market path; a "quadratic reduction theorem" turns execution into finite-dimensional optimization under impact + inventory constraints. Beats z-score-threshold benchmark on return-to-turnover in synthetic mean-reverting-spread tests and on historical equity pairs data.
  - **Why it matters for trading:** Unifies signal and execution in one basis, so the trade schedule reacts to realized signal history instead of a static threshold — directly relevant to any pairs/stat-arb book.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (implementation is signature-machinery heavy; shelve for a stat-arb sprint)
- **Liquidity-Based Audit of Algorithmic Trading Strategies** — Irene Aldridge, Jun 30 2026 — [link](https://arxiv.org/abs/2606.29018)
  - **What it is:** Audit methodology that stress-tests algo strategies against the liquidity actually available, exposing execution risk hidden by frictionless backtests.
  - **Why it matters for trading:** A concrete checklist for the exact failure mode our own pipeline guards against (synthetic-data / cost-blind backtests). Reference for the backtest harness.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (methods reference for backtests/ realism checks)
- **Settlement Manipulation in Prediction Markets** — David Dai, Ruizhe Jia, Shihao Yu, Jul 1 2026 — [link](https://arxiv.org/abs/2606.31675)
  - **What it is:** Models how participants can distort prediction-market outcomes by manipulating the settlement/resolution procedure.
  - **Why it matters for trading:** Extends the Polymarket↔Binance mispricing thread (Portnaya 06-20) — a structural risk to treat prediction-market prices as clean signal.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve (risk awareness, not tradeable)

### Risk & portfolio
- **Hidden Dependence and Aggregate Tail Risk** — Corrado De Vecchi, Max Nendel, Steven Vanduffel, Jun 30 2026 — [link](https://arxiv.org/abs/2606.30193)
  - **What it is:** Shows how concealed (beyond-correlation) dependence between assets amplifies aggregate tail losses that correlation-based aggregation misses.
  - **Why it matters for trading:** Reinforces the Chen/Lin/Wang VaR-superadditivity thread (06-24) — diversification can backfire in the tail; sizing off linear correlation understates crash risk.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (portfolio-construction caution)
- **Generating Plausible Stress Scenarios via Large Deviations** — Anand Deo, Jul 1 2026 — [link](https://arxiv.org/abs/2606.31122)
  - **What it is:** Uses large-deviation theory to construct realistic (not arbitrary) stress scenarios for portfolio risk assessment.
  - **Why it matters for trading:** Principled scenario generation for drawdown/stress testing — an upgrade over hand-picked shocks.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (stress-test tooling)
- **Regime-Conditional Distributional Comparison of Trading Strategies: A GAMLSS/ZAGA Framework Applied to the S&P 500** — Krzysztof Ozimek, Jul 1 2026 — [link](https://arxiv.org/abs/2606.31251)
  - **What it is:** Compares full return *distributions* of trading strategies conditional on market regime using a GAMLSS/zero-adjusted-gamma framework, rather than comparing point Sharpe ratios.
  - **Why it matters for trading:** A more honest strategy-comparison protocol (distribution + regime, not a single moment) — relevant to how we adjudicate backtest verdicts.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (evaluation-protocol reference)

## New resources & tooling
- _no notable new open-source repos this run — findings are papers._

## Watchlist updates
- **Victoria Portnaya** — already effectively tracked (06-20 Polymarket↔Binance); now a second high-signal microstructure paper (sign/magnitude decomposition of return predictability). Confirm as a tracked author.
- **Sichao He / Yansong Zhang** — output-head-dominance finding; worth watching for follow-on fat-tail forecasting work.

## Open questions / threads to pull next run
- **Real-time identification of the onset of financial rogue waves** (Hayward/Lennon/Biancalana, 2606.31475) — pattern-formation early-warning; not chased this run, potential regime-detection lead.
- **Adaptive AI Delegation under Uncertainty** (Dixon, 2606.29406) — continues Dixon's agentic-AI model-risk line (belief-VaR, POMDP validation already in ledger); Bayesian governance for delegating decision authority.
- Portnaya's lag-3 directional-reversal channel (p=0.02) — if lag-1 has no sign edge but lag-3 does, is there a tradeable multi-lag structure on crypto? Follow-up backtest candidate.
