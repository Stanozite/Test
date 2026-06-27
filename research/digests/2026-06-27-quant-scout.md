# Quant Scout Digest — 2026-06-27

## TL;DR
- **Neural nets beat econometric term-structure models on both RMSE and trading P&L** — US bonds favor Dynamic Nelson-Siegel + autoencoder; EU favors PCA-factor NNs *without* macro variables (Lausser/Vuolo/Zagst, TUM).
- **Pairwise risk-attribution checks miss a triple-level failure** — squared-Sharpe driver attribution has an order-three "immersion" obstruction (à la Bernstein's pairwise-independent-yet-dependent variables) invisible to 2-way diagnostics; permutation screening detects it, code released (Rodriguez Dominguez).
- **Conservative wins for commodity ETFs** — across 30 US commodity ETFs, min-risk / CVaR portfolios with Student-t copula + ARMA-GARCH marginals gave steadier cumulative returns than tangency, but tail exposure persists (Appiah/Jaffri/Rachev).
- **Leif Andersen & Itkin: ~10× faster American-option / flexible-forward pricing** under time-dependent Heston via Volterra early-exercise integral equation; DSINC scheme ~12× more accurate than COS, 1–2 s pricing.
- **Robust HVA framed as worst-case loss over a relative-entropy ball** around the no-trade-band loss distribution — quantifies the rebalancing-cost vs hedge-error trade-off under demand-liquidity stress (Sakuma).
- _Thin Friday window: arXiv announced only 26-Jun (no 25-Jun digest gap-filler, no Sat 27-Jun announce). Microstructure/execution had no fresh standalone this run._

## Findings by focus area

### ML / AI for alpha
- **Data-Driven Duration Management — Term Structure Forecasting Using Machine Learning** — Tobias Lausser, João Eduardo Vuolo, Rudi Zagst (TUM), 2026-06-26 — [link](https://arxiv.org/abs/2606.26815)
  - **What it is:** Compares econometric term-structure models vs neural nets for forecasting US & EU zero-coupon government yield curves, evaluated on statistical metrics (RMSE, MAE, directional accuracy) *and* an economic duration-trading strategy. Architectures: direct-forecast NN with Dynamic Nelson-Siegel factors, autoencoder macro-feature extraction, PCA-factor NN.
  - **Why it matters for trading:** Concrete, benchmarked recipe for duration/curve positioning. Notably the winning config differs by region (US: DNS+autoencoder; EU: PCA-factor NN, macro variables *hurt*), a directly testable design choice for a fixed-income desk.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest the DNS+autoencoder pipeline on a duration strategy vs DNS baseline.

### Microstructure & execution
_No notable new standalone findings this run — 26-Jun arXiv batch had no fresh execution/LOB/market-making paper. Carry the open threads below to next run._

### Risk & portfolio
- **A sharp order-three obstruction to the aggregation of conditional price-of-risk attribution** — Alejandro Rodriguez Dominguez, 2026-06-26 — [link](https://arxiv.org/abs/2606.26835)
  - **What it is:** Decomposes a portfolio's integrated conditional squared-Sharpe ("price-of-risk premium") into causal drivers and proves the decomposition is only valid when driver filtrations are properly *immersed* in the price filtration. Immersion can hold for every single and paired sub-portfolio yet fail at the triple — a clean Bernstein-type pairwise-vs-mutual analogue — splitting failure into "combinatorial masking" vs "anticipative coupling." Permutation-calibrated screening detects the leakage; reproducible code on GitHub/Zenodo.
  - **Why it matters for trading:** Risk-attribution / factor-leakage diagnostics that rely on pairwise checks can silently certify a broken decomposition. Direct relevance to anyone validating causal attribution or guarding against look-ahead in multi-driver risk models.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read; lift the permutation-screening test into existing attribution QA.
- **Portfolio Optimization for Commodity ETFs under Heavy-Tailed Returns** — Nicholas Appiah, Ali Jaffri, Dilmi C.W. Hettiachchi-Halpe-Kankanamalage, Svetlozar T. Rachev, 2026-06-26 — [link](https://arxiv.org/abs/2606.26625)
  - **What it is:** 30 US commodity ETFs (agriculture/energy/metals/broad), Bloomberg daily Dec-2018→Dec-2024. Rolling-window mean-variance and CVaR optimization with Student-t copula dependence + ARMA-GARCH marginals vs passive buy-and-hold.
  - **Why it matters for trading:** Empirical verdict that min-risk/CVaR portfolios deliver steadier cumulative performance than tangency in a heavy-tailed asset class — but optimized books *still* carry heavy downside tails, so explicit tail diagnostics remain mandatory. Useful template for a commodity-ETF sleeve.
  - **Scores:** Novelty 2/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve as reference / replicate the CVaR + t-copula sleeve if adding commodity ETF exposure.
- **Robust Hedging Valuation Adjustment under Liquidity–Demand Stress** — Takayuki Sakuma, 2026-06-26 — [link](https://arxiv.org/abs/2606.26731)
  - **What it is:** Builds a loss distribution from simulated rebalancing + maturity-unwind trades under each no-trade-band rule, then defines robust HVA as the worst-case expected loss over a relative-entropy neighborhood of that distribution. Contrasts fixed-radius vs fixed-benchmark-stress conventions.
  - **Why it matters for trading:** Quantifies the rebalancing-cost vs hedge-error trade-off in dynamic hedging under liquidity stress — directly relevant to XVA desks and anyone sizing no-trade bands / hedge frequency robustly.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read; map the worst-case-over-entropy-ball framing onto hedge-band sizing.

### Asset class / derivatives
- **Valuing American options and Flexible Forwards contracts in time-dependent models** — Leif Andersen, Andrey Itkin, Rakhymzhan Kazbek, 2026-06-26 — [link](https://arxiv.org/abs/2606.27335)
  - **What it is:** Prices American options and flexible-delivery FX forwards under *time-inhomogeneous* Heston via an integral-equation decomposition yielding a Volterra equation for the early-exercise surface. Two spectral evaluators — COS double-cosine expansion and a damped-Sinc (DSINC) local-basis scheme — with recursive Riccati solutions.
  - **Why it matters for trading:** 1–2 s pricing, ~10× faster than fine finite-difference grids; DSINC ~12× more accurate than COS. Finds the early-exercise boundary is strongly *nonlinear* in variance, contradicting prior linear approximations. High-credibility (Andersen/Itkin) production-grade pricing for FX hedging structures.
  - **Scores:** Novelty 3/5 · Credibility 5/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve as reference for any American/early-exercise pricing under stochastic-vol with term structure.

## New resources & tooling
- Reproducible code for the order-three attribution obstruction — [GitHub/Zenodo, linked from arXiv:2606.26835](https://arxiv.org/abs/2606.26835) — permutation-calibrated screening to detect triple-level immersion failures in risk-driver attribution.

## Watchlist updates
- **Leif Andersen & Andrey Itkin** — Authors — production-grade derivatives pricing (integral-equation / Volterra early-exercise methods, time-dependent stochastic vol). Worth tracking for execution/derivatives tooling.
- **Svetlozar T. Rachev** — Author — heavy-tailed / CVaR portfolio construction (Student-t copula + ARMA-GARCH). Track for risk & portfolio.
- **Rudi Zagst / TUM (Mathematical Finance)** — Author/lab — ML for fixed-income / term-structure forecasting and portfolio applications.

## Open questions / threads to pull next run
- Microstructure/execution gap: no fresh standalone this run — sweep q-fin.TR + cs.LG harder next run; revisit the queue-reactive RL execution lineage (2511.15262 etc.) if it surfaces a fresh follow-up.
- Region-asymmetry in the duration-ML result (macro variables help US, hurt EU) — is this robustly replicable, or a sample artifact? Candidate for a focused replication.
- Whether the order-three immersion obstruction generalizes to standard factor-attribution / Brinson-style decompositions used in practice.
