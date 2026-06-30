# Watchlist — Quant Scout config

This is the tunable control file for the scout. Edit freely; it is re-read on every
run. Add players, sources, categories, or keywords to steer what gets surfaced.

---

## Focus areas (priorities)
1. **ML / AI for alpha** — machine learning, deep learning, RL, LLMs for signal
   generation, forecasting, alpha mining, feature engineering.
2. **Microstructure & execution** — market microstructure, order flow, Kyle/PIN-type
   models, optimal execution, market making, HFT, transaction-cost analysis.
3. **Risk & portfolio** — factor models, portfolio construction, risk management,
   regime detection, drawdown/crash mitigation.
4. **Asset class / market** — equities, futures, FX, crypto, options & derivatives.
   *(User to refine which markets matter most — add notes here.)*

---

## Sources to scan (in priority order)
- **arXiv** q-fin categories: `q-fin.TR` (trading & microstructure), `q-fin.PM`
  (portfolio mgmt), `q-fin.ST` (statistical finance), `q-fin.CP` (computational),
  `q-fin.RM` (risk), plus `econ.GN`, `cs.LG`, `stat.ML` when finance-applied.
- **SSRN** — finance working papers (factor research, microstructure).
- **Scholar Gateway (MCP)** — academic search across journals.
- **GitHub** — high-star quant repos, new strategy/library releases.
- **Quant blogs / newsletters** — practitioner writeups, firm research notes.
- **Discovery layers** — alphaXiv (alphaxiv.org), Cool Papers (papers.cool), and curated
  indexes like `wangzhe3224/awesome-systematic-trading` (added 2026-06-16).

---

## Global players to track
Firms, labs, and authors whose output is worth following. Grow this list over time.

| Player | Type | Why track |
| --- | --- | --- |
| Zura Kakushadze (Quantigic Solutions) | Author/firm | Alpha formulas, factor models |
| Guido Baltussen / Robeco | Author/firm | Factor & momentum research |
| AQR Capital | Firm | Factor investing, academic-grade research |
| Two Sigma / Jane Street / Jump | Firm | ML, microstructure, execution (public writeups) |
| Marcos López de Prado | Author | ML for finance, backtesting pitfalls |
| QuantaAlpha team (Tsinghua/PKU/CAS/CMU/HKUST) | Academic consortium | LLM-driven alpha mining (added 2026-06-16) |
| FinStep-AI | Lab | RL alpha screening — Alpha-R1 (added 2026-06-16) |
| Fabrizio Lillo (Scuola Normale Superiore) | Author | Market microstructure, price impact, adverse selection (added 2026-06-16) |
| Stefan Zohren / Oxford-Man Institute | Author/lab | Deep learning for systematic macro; Momentum Transformer lineage (added 2026-06-16) |
| John Graham & Campbell Harvey (Duke/Fuqua) | Authors | LLM-as-expectations-data; foundational factor/asset-pricing (added 2026-06-17) |
| Tim Gebbie & Chris Angstmann (UCT/UNSW) | Authors | Reaction–diffusion microstructure; trade-sign memory, square-root impact, Epps effect (added 2026-06-17) |
| Peter Cotton | Author | High-dimensional covariance shrinkage / portfolio damping (added 2026-06-17) |
| Blanka Horvath & Hans Buehler | Authors | Deep hedging / volatility-surface learning; differentiable IV (added 2026-06-17) |
| Michael Ludkovski (UCSB) | Author | Computational finance; RL for optimal stopping (added 2026-06-17) |
| Christoph Schmidhuber (ZHAW) | Author | Econophysics; trend-conditioned vol/correlation forecasting, critical phenomena (added 2026-06-20) |
| HKU Data Science Lab (HKUDS) | Lab | Agentic-finance frameworks & open-source tooling — Vibe-Trading (added 2026-06-20) |
| Cathy Yi-Hsuan Chen / Fengxiang He | Authors | LLM-agent on-chain/DeFi risk supervision — DeXposure-Claw (added 2026-06-20) |
| Matthew Francis Dixon | Author | Agentic-AI model risk for finance — POMDP belief-VaR, agentic validation frameworks (added 2026-06-21) |
| Li Xia | Author | Geometric theory of LLM-guided discovery / factor-mining bottlenecks (added 2026-06-21) |
| Sebastien Lleo & Wolfgang Runggaldier | Authors | Risk-sensitive stochastic control + RL for allocation; continuous-time q-learning, fractional Kelly (added 2026-06-23) |
| Bruce Mizrach (Rutgers) | Author | Market microstructure economist; on-chain/L2 transaction-cost mapping (added 2026-06-23) |
| Luca Capriotti | Author | Fast/semi-analytical pricing (path integrals, AAD) for credit & XVA (added 2026-06-23) |
| Fabio Sigrist (HSLU) | Author | Gradient boosting + spatio-temporal mixed models (gpboost); bounded-ratio credit targets (added 2026-06-23) |
| Mao Guan / Qian Chen | Authors | Leakage-aware LLM forecasting & macro-factor ranking; rigorous decision-time evaluation protocol (added 2026-06-24) |
| Useong Shin | Author | Factor-model diagnostics — construction-dependence & body-tail tests of pricing models (added 2026-06-24) |
| Ruodu Wang (Waterloo) | Author | Risk-measure theory; VaR (super)additivity, diversification limits under heavy tails (added 2026-06-24) |
| Jakub Michańków / Paweł Sakowski (UW QFRG) | Authors | ML for derivatives pricing / XVA — randomized neural networks (added 2026-06-24) |
| Diego Klabjan (Northwestern) | Author | ML for futures stat-arb; hierarchical graph learning on term structure / calendar spreads (added 2026-06-25) |
| C. Evans Hedges | Author | Scaling-laws + latency-efficient ML architectures for LOB microstructure prediction (added 2026-06-25) |
| Claudio J. Tessone / UZH Blockchain Center | Author/lab | Empirical crypto & Ethereum economics — staking, validator dynamics, on-chain carry (added 2026-06-25) |
| Leif Andersen & Andrey Itkin | Authors | Production-grade derivatives pricing — integral-equation / Volterra early-exercise methods under time-dependent stochastic vol (added 2026-06-27) |
| Svetlozar T. Rachev | Author | Heavy-tailed / CVaR portfolio construction — Student-t copula + ARMA-GARCH (added 2026-06-27) |
| Rudi Zagst / TUM Mathematical Finance | Author/lab | ML for fixed-income / term-structure forecasting & portfolio applications (added 2026-06-27) |
| Thibaut Mastrolia (UC Berkeley IEOR) | Author | Optimal control / market making; signature methods, Sig-REINFORCE quoting (added 2026-06-28) |
| Ruimeng Hu (UCSB) | Author | Mean-field games; finite-player↔MF convergence for insurance & financial markets (added 2026-06-28) |
| Xavier Fonseca | Author | Decision-theoretic covariance/portfolio estimation; exact regret geometry for GMV under heavy tails (added 2026-06-29) |
| Matloob Khushi / Josiah Poon (Univ. of Sydney) | Authors | ML for crypto forecasting; cross-asset graph-attention models — CryptoGAT (added 2026-06-29) |
| Daniele Angelini | Author | Fractional-calculus market-efficiency / rough-volatility detection; Grünwald–Letnikov Hurst regime tests (added 2026-06-29) |
| Andrei Bysik & Robert Ślepaczuk (Univ. of Warsaw QFRG) | Authors/lab | Execution-realistic crypto ML; cost-aware filters, rigorous walk-forward backtesting (added 2026-06-30) |
| _add your own…_ | | |

---

## Seed examples — the quality bar
These are reference items the user flagged as the *kind* of research that is
beneficial. New findings should be at least this useful, novel, or actionable.

1. **101 Formulaic Alphas** — Zura Kakushadze (Quantigic Solutions), Dec 2015.
   Explicit alpha formulas that double as executable code. *Focus: ML/alpha.*
   arXiv: https://arxiv.org/abs/1601.00991
2. **Momentum factor investing: Evidence and evolution** — Baltussen, Dom, Van Vliet,
   Vidojevic, Oct 2025. Momentum's evolution from price-based to fundamental/
   network-based trends; risk-managed momentum. *Focus: risk/portfolio.*
3. **je-suis-tm/quant-trading** — GitHub, ~10k★. Python implementations of many
   strategies (Bollinger, MACD, pair trading, Monte Carlo, London Breakout, etc.).
   *Focus: resources/code/skills.* https://github.com/je-suis-tm/quant-trading
4. **Insider and stealth trading with dynamic legal risk** — Qiao & Xia, 2026
   (arXiv econ.GN). Continuous-time Kyle-type model with dynamic legal risk.
   *Focus: microstructure/execution.*

---

## Keywords to boost
`alpha mining`, `optimal execution`, `market making`, `factor timing`, `regime
detection`, `reinforcement learning trading`, `limit order book`, `transaction cost`,
`deflated Sharpe`, `combinatorial purged CV`, `Kyle model`, `cross-sectional momentum`.

## Exclusions / noise to drop
Marketing/listicle content, paywalled-with-no-abstract items, get-rich-quick blogs,
re-posts of already-captured papers (see `INDEX.md` ledger).
