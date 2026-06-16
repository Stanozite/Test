# Quant Scout Digest — 2026-06-16

_First run. Window: trailing ~30 days (mid-May → mid-June 2026), with a few
foundational items just outside the window where high-signal. All items below were
verified to exist (real arXiv IDs / repos, genuine authors and abstracts). Scholar
Gateway was not yet authorized this run — see "Open questions"._

## TL;DR
- **LLM-driven alpha research is the dominant 2026 theme** — reasoning models that *screen/mine* factors (Alpha-R1, QuantaAlpha), not just emit trades, are posting strong out-of-sample IC/Sharpe.
- **QuantaAlpha** (evolutionary LLM alpha mining, GPT-5.2): IC 0.1501, ARR 27.75%, MDD 7.98% — and it's open-source with a usable UI. Highest actionability this run.
- **ReCAP** (June 2026): regime-aware *continual learning* beats rolling-window retraining for portfolio management on 5 datasets — directly relevant to regime robustness.
- **Benchmarks matured**: AlphaForgeBench + BacktestBench give reproducible ways to evaluate "LLM-as-quant-researcher" pipelines, exposing severe run-to-run instability in naive LLM trading agents.
- **Informed-trading detection** went mainstream on decentralized prediction markets (ILS / order-flow skill screens) — a modern microstructure echo of the insider-trading seed paper.

## Findings by focus area

### ML / AI for alpha
- **QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining** — QuantaAlpha team (Tsinghua/PKU/CAS/CMU/HKUST), Feb 2026 — [arXiv:2602.07085](https://arxiv.org/abs/2602.07085) · [GitHub](https://github.com/QuantaAlpha/QuantaAlpha)
  - **What it is:** Treats each end-to-end alpha-mining run as a "trajectory" and improves factors via trajectory-level mutation/crossover, enforcing semantic consistency across hypothesis → factor expression → executable code while constraining complexity/redundancy.
  - **Why it matters for trading:** A working, open-source successor to "101 Formulaic Alphas" — automated factor discovery you can actually run. With GPT-5.2: IC 0.1501, ARR 27.75%, MDD 7.98%; factors mined on CSI 300 transferred to CSI 500 / S&P 500 (160% / 137% cumulative excess over 4y).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 5/5
  - **Next step:** replicate — stand up the repo, point it at your universe, sanity-check factors with purged CV.
- **Alpha-R1: Alpha Screening with LLM Reasoning via Reinforcement Learning** — Jiang, Zhao, Sun et al. (FinStep-AI), Dec 2025 — [arXiv:2512.23515](https://arxiv.org/abs/2512.23515) · [GitHub](https://github.com/FinStep-AI/Alpha-R1)
  - **What it is:** An 8B reasoning model RL-trained to *screen* alphas — reasons over factor logic + real-time news to activate/deactivate factors as regimes shift.
  - **Why it matters for trading:** Targets alpha decay directly (the core enemy of any factor book). On out-of-domain CSI 1000: cumulative return 42.49%, Sharpe 4.03. Open-source weights/code.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read + backtest the screening layer on top of an existing factor set; treat single-market results cautiously.
- **AlphaForgeBench: Benchmarking End-to-End Trading Strategy Design with LLMs** — Wentao Zhang et al., Feb 2026 (KDD'26) — [arXiv:2602.18481](https://arxiv.org/abs/2602.18481)
  - **What it is:** A benchmark that grades LLMs as *quant researchers synthesizing executable strategies*, decoupling reasoning from execution for deterministic, reproducible evaluation. Documents severe behavioral instability (run-to-run variance, action flipping) in LLMs that emit point-wise trades.
  - **Why it matters for trading:** The evaluation harness you'd want before trusting any LLM in the idea→strategy pipeline (your future component #2).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve as the standard to adopt when building the backtest pipeline.

### Microstructure & execution
- **Per-Market Information Leakage and Order-Flow Skill: Two Methodological Lenses on Informed Trading in Decentralized Prediction Markets** — Maksym Nechepurenko, May 2026 — [arXiv:2605.02287](https://arxiv.org/abs/2605.02287)
  - **What it is:** Introduces an Information Leakage Score (ILS) measuring per-market front-loading around public-event timestamps, and reviews three near-simultaneous informed-trading screens (Mitts–Ofir composite screen over 210k wallet-market pairs; Gomez-Cram et al. sign-randomization flagging ~3.14% "skilled winners" and 1,950 "insiders"; ILS).
  - **Why it matters for trading:** A modern, data-driven update to the insider/stealth-trading seed paper — detecting informed flow is the flip side of avoiding being adversely selected, and prediction markets are a tradeable venue.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; consider ILS-style leakage features as a signal/risk filter on event-driven books.

### Risk & portfolio
- **Regime-Adaptive Continual Learning for Portfolio Management (ReCAP)** — Chaofan Pan et al., Jun 2026 — [arXiv:2606.00143](https://arxiv.org/abs/2606.00143)
  - **What it is:** A continual-learning framework with an adaptive regime-detection module that segments history into variable-length regimes, learns regime-specific policy vectors, and builds a reusable policy library — avoiding both costly rolling-window retraining and naive online fine-tuning.
  - **Why it matters for trading:** Directly tackles non-stationarity / regime shifts (your watchlist priority). Reports consistent outperformance vs. popular baselines on five real-world datasets, with fast adaptation after shifts.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read; mine the regime-segmentation idea even if you don't adopt the full RL stack.
- **From Classical Optimization to Bayesian Integration: A Comprehensive Analysis of Systematic Portfolio Management** — May 2026 — [arXiv:2605.29413](https://arxiv.org/abs/2605.29413)
  - **What it is:** A consolidated walk through mean-variance / constrained optimization, Fama-French 5-factor regression, Monte Carlo, and Black-Litterman / Bayesian allocation.
  - **Why it matters for trading:** Useful reference scaffolding for the portfolio-construction layer; good for grounding terminology and baselines.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve as a reference.

### Asset class / market
- **Pricing options on the cryptocurrency futures contracts** — Julia Kończal (Wrocław Univ. of Sci. & Tech.), Jun 2025 — [arXiv:2506.14614](https://arxiv.org/abs/2506.14614)
  - **What it is:** Calibrates and compares Black-Scholes, Merton Jump-Diffusion, Variance Gamma, Kou, Heston, and Bates models on BTC and ETH vanilla options on futures.
  - **Why it matters for trading:** Concrete, actionable model selection for crypto-derivatives pricing: BS has the highest error; **Kou wins for BTC, Bates wins for ETH**. (Just outside the 30-day window but high-signal for the crypto/options focus.)
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** replicate calibration if you trade BTC/ETH options; use as the pricing baseline.

## New resources & tooling
- **BacktestBench + AutoBacktest** — [arXiv:2605.17937](https://arxiv.org/abs/2605.17937) — first large-scale benchmark for automated quant backtesting (18,246 annotated QA pairs over 6M+ market records) plus a multi-agent NL→backtest baseline (Summarizer/Retriever/Coder). Evaluates 23 LLMs. The yardstick for your future backtest pipeline.
- **QuantaAlpha** — [github.com/QuantaAlpha/QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha) — runnable LLM alpha-mining engine with a factor library + UI.
- **Alpha-R1** — [github.com/FinStep-AI/Alpha-R1](https://github.com/FinStep-AI/Alpha-R1) — open weights/code for RL alpha screening.
- **awesome-systematic-trading** — [github.com/wangzhe3224/awesome-systematic-trading](https://github.com/wangzhe3224/awesome-systematic-trading) — curated index of systematic-trading libraries (crypto/stock/futures/options/FX) to seed future watchlist sources.

## Watchlist updates
New players/sources worth adding to `watchlist.md`:
- **QuantaAlpha team** (academic consortium — LLM alpha mining) · **FinStep-AI** (Alpha-R1).
- **alphaXiv** (alphaxiv.org) and **Cool Papers / papers.cool** — fast arXiv discovery layers.
- Track the emerging **"LLM-as-quant-researcher" benchmark cluster**: AlphaForgeBench, BacktestBench, QuantCode-Bench (2604.15151), Market-Bench.

## Open questions / threads to pull next run
- **Authorize Scholar Gateway** to add peer-reviewed journal coverage (SSRN/journals) beyond arXiv — link is in the chat summary for this run.
- Chase a *fresh* (May–Jun 2026) optimal-execution / market-making paper — the strongest execution hit this run (2601.04896) was **withdrawn**, so the execution slot is thin and should be refilled.
- Verify QuantaAlpha / Alpha-R1 results aren't overfit to A-share universes before trusting transfer claims (apply purged/embargoed CV — cf. López de Prado).
- Pull the **AQR / Robeco** practitioner pipeline (factor timing, momentum-crash mitigation) which arXiv under-covers.

---

# Run 2 — same-day refresh (2026-06-16)

_Second scheduled pass. Window: items not already in the Run-1 ledger, prioritising
the **thin execution slot** and the **AQR/Robeco factor thread** flagged above. All
items verified against live arXiv abstracts (real IDs, authors, submission dates).
The strongest fresh execution + market-making hits are now captured. Scholar Gateway
still not authorized._

## TL;DR
- **Execution slot refilled, with depth**: a fresh RL execution agent (TT-DAC-PS, Jun 2026) and a market-making *unification theorem* (Avellaneda-Stoikov ≡ Cartea-Jaimungal, May 2026) — one practical, one foundational.
- **Sunshine-trading evidence on Hyperliquid** (Lillo, Jun 2026): visible TWAPs beat hidden metaorders on cost — transparency *lowers* adverse selection, and the cost shifts onto non-announcers. Directly actionable for DEX execution design.
- **DeePM** (Zohren/Oxford-Man, Jan 2026): regime-robust macro portfolio manager optimising an EVaR proxy nets ~2× classical trend-following over 50 futures, 2010–2025.
- **FactorEngine** (Mar 2026): LLM factor mining that ingests *financial documents* into executable factor code — a knowledge-infused complement to QuantaAlpha's evolutionary search.

## Findings by focus area

### ML / AI for alpha
- **FactorEngine: A Program-level Knowledge-Infused Factor Mining Framework for Quantitative Investment** — Lin, Feng, Feng, Huang et al., Mar 2026 — [arXiv:2603.16365](https://arxiv.org/abs/2603.16365)
  - **What it is:** Represents factors as executable code and separates *logic revision* from *parameter optimization*; a "knowledge-infused bootstrapping" module turns financial documents into factor code via a multi-agent extract→verify pipeline.
  - **Why it matters for trading:** A different attack on alpha discovery than QuantaAlpha's evolutionary mutation — it pulls priors from domain text, improving IC/ICIR stability and reported annualized return/Sharpe vs. baselines. Pairs naturally with the Run-1 alpha-mining stack.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read; compare its document→factor extraction against QuantaAlpha on the same universe before adopting either.

### Microstructure & execution
- **TT-DAC-PS: Twin-Target Deterministic Actor-Critic with Policy Smoothing for Optimal Trade Execution** — Zaznov, Badii, Kunkel, Dufour, Jun 2026 — [arXiv:2606.08379](https://arxiv.org/abs/2606.08379)
  - **What it is:** An RL execution agent combining twin critic targets + policy smoothing (a learned noise schedule, conservative Q-regularization) over Almgren-Chriss impact and limit-order-book features.
  - **Why it matters for trading:** Refills the execution slot the prior run flagged as thin. On 10 US stocks it consistently cuts mean implementation-shortfall % with competitive variance, beating TWAP/VWAP and PPO/SAC/A2C baselines.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** backtest as the execution layer; verify the IS gains hold out-of-sample on your own fills.
- **Avellaneda-Stoikov and Cartea-Jaimungal as One Framework: A Forced Uniqueness Theorem for Inventory Market Making** — Frank M. V. Feys, May 2026 — [arXiv:2606.01477](https://arxiv.org/abs/2606.01477)
  - **What it is:** Proves that under axioms on the preference functional (cash-additivity, normalization, concavity, strong dynamic consistency, law-invariance) Avellaneda-Stoikov is the *unique* solution, and Cartea-Jaimungal is its second-order approximation with a forced parameter link φ = γσ²/2.
  - **Why it matters for trading:** A clean theoretical consistency check for any inventory market-making book — the invertible relation γ = 2φ/σ² lets you sanity-check that your AS and CJ parameterizations agree.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; use the γ↔φ relation as a unit test on existing MM parameter calibration.
- **Trading in the Sunshine or in the Shade: Market Impact and Adverse Selection on Hyperliquid** — Davide Barone & Fabrizio Lillo, Jun 2026 — [arXiv:2606.15715](https://arxiv.org/abs/2606.15715)
  - **What it is:** Empirical study of "sunshine trading" on Hyperliquid (a blockchain perp DEX where TWAP orders publicly disclose terms): 4.3M hidden orders vs. 465k visible TWAPs.
  - **Why it matters for trading:** Visible TWAPs face *lower* execution cost than comparable hidden metaorders — transparency cuts adverse selection, the cost shifts to non-announcers, and book depth rises during announced execution. A concrete, tradeable execution-design lesson on a real DEX venue, from a top microstructure group (Lillo).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read; test announced-TWAP vs. hidden execution on your own DEX flow.

### Risk & portfolio
- **DeePM: Regime-Robust Deep Learning for Systematic Macro Portfolio Management** — Kieran Wood, Stephen J. Roberts, Stefan Zohren (Oxford-Man), Jan 2026 — [arXiv:2601.05975](https://arxiv.org/abs/2601.05975)
  - **What it is:** End-to-end deep portfolio manager with a Directed-Delay mechanism for asynchronous data, a macroeconomic graph prior for denoising, and a distributionally-robust objective (smooth worst-window penalty as a differentiable EVaR proxy).
  - **Why it matters for trading:** Directly targets the regime-robustness watchlist priority. Over 50 futures (2010–2025) it nets ~2× classical trend-following and passive benchmarks, ~+50% over the Momentum Transformer, holding up through CTA Winter and post-2020 vol.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read; the EVaR-proxy objective and macro-graph prior are portable even without the full stack.

### Asset class / market
- **Dynamic Multi-Pair Trading Strategy in Cryptocurrency Markets with Deep Reinforcement Learning** — Damian Lebiedź & Robert Ślepaczuk, Jun 2026 — [arXiv:2606.04574](https://arxiv.org/abs/2606.04574)
  - **What it is:** A "Filter-then-Rank" pair-selection method feeding a PPO-LSTM execution agent inside deterministic risk bounds, tested on Binance USD-M futures.
  - **Why it matters for trading:** Modernizes classic pair trading for crypto; out-of-sample it beat the heuristic baseline, but significance is only at the 10% level — treat as promising, not proven.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve / lightweight replication; the Filter-then-Rank selection idea is the reusable part.

## New resources & tooling
- **q-fin.TR June-2026 microstructure cluster** to mine next: market-making axiomatics (2606.09454), price-impact laws (2606.16269 square-root law; 2606.07059 "inconspicuous law of market impact"; 2606.13419 realtime impact detection), dealer internalisation (2606.06413), market-maker informedness (2606.05882). A dense, fresh microstructure reading list.

## Watchlist updates
- Add **Fabrizio Lillo** (Scuola Normale Superiore / microstructure, price impact, adverse selection) and **Stefan Zohren / Oxford-Man Institute** (deep learning for systematic macro, Momentum Transformer lineage) as tracked authors.
- **AQR/Robeco thread, partial close:** the canonical **Daniel & Moskowitz "Momentum Crashes"** (NBER w20439 / SSRN 2371227) was revised ~May 2026 — foundational reference for the momentum-crash-mitigation lead; still arXiv-under-covered, pull the practitioner version next run.

## Open questions / threads to pull next run
- A withdrawn-but-interesting lead: **"Not All Factors Crowd Equally" (2512.11913)** derived a hyperbolic alpha-decay model (momentum R²=0.65; crowded reversals 1.7–1.8× crash prob) but was **withdrawn pending major revision** — watch for a v2 before trusting it.
- Still un-authorized: **Scholar Gateway** for SSRN/journal coverage of the AQR/Robeco factor-timing pipeline.
- Chase the **square-root-law / price-impact** mini-cluster (2606.16269, 2606.07059) — recurring fresh microstructure theme worth one consolidated finding next run.
