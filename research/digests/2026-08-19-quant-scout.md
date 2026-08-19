# Quant Scout Digest — 2026-08-19

_7-day window since 08-12. Swept arXiv q-fin TR/PM/ST/CP/RM `/recent` above ceiling
2608.10852 → leading edge 2608.18022. Batch is unusually **equity/portfolio-heavy**;
no crypto-native directional signal surfaced (the crypto-touching papers this window
are infrastructure/censorship/on-chain-credit, not tradable price signals). The
sharpest theme is a **risk-measure upgrade** (Choi's Entropic VaR) — which becomes
today's backtest target on the heaviest-tailed liquid asset._

## TL;DR
- **Choi "Entropic VaR for tempered-stable Lévy" (2608.18022)** derives closed-form
  portfolio EVaR from asset/component parameters (no portfolio-level refitting) and
  several entropic reward–risk sector-ETF portfolios **beat CVaR-matched and standard
  benchmarks OOS 2000–2026** — a coherent heavy-left-tail measure that is an upper
  bound on CVaR. → backtested (below).
- **Aste group HNN (2608.14323):** a Maximally-Filtered-Clique-Forest fixes a neural
  net's depth/width/sparsity *before training* from firm-characteristic dependence —
  **80× fewer params, better cross-sectional ranking**, multiple-testing-robust. The
  architecture *is* the dependence graph.
- **"Buy the Rumor, Sell the News" (2608.14014):** 4.57M articles, 1.68M events —
  the move concentrates **before/at publication (2.8× the +20d value)**; markets
  **underreact to numbers (drift), overreact to stories (reversal)**. Ships a per-tag
  drift table usable as a forecasting prior.
- **AgonAlpha (2608.11250):** first alpha-miner to combine verified-artifact search +
  a fresh-context adversarial reviewer with **re-execution veto** + pending-aware
  budget allocation; live WorldQuant BRAIN Fitness 9.50 / Sharpe 3.48 (self-reported).
- **Backtest: evar_regime on BTC-USD → MIXED (leans REJECT).** EVaR tail-gate OOS
  Sharpe **0.032**, CAGR **−2.55%**, fails deflated-SR — and unlike `vol_regime` it
  bought **no drawdown insurance** (in-sample MaxDD −70% ≈ B&H). Even the "better"
  coherent tail measure adds nothing on single-series BTC. **12th straight daily-BTC
  reject-lean.**

## Findings by focus area

### ML / AI for alpha

- **AgonAlpha: Autonomous Alpha Discovery via Prompt Economy and Scalable Agentic Search** — Ye, Sun, Ren, Yu, Yi, Yang, 2026-08-04 — [arXiv:2608.11250](https://arxiv.org/abs/2608.11250)
  - **What it is:** an agentic alpha-miner that searches over *frozen research
    artifacts* (hypotheses, executable expressions, platform evidence, rationales,
    review status) rather than formulas; adds a fresh-context adversarial reviewer with
    re-execution + veto authority and pending-aware parallel budget allocation, with a
    full public evidence trail. Live BRAIN deployments hit Fitness 9.50 / Sharpe 3.48.
  - **Why it matters for trading:** the interesting bit isn't the (self-reported,
    platform-graded) Sharpe — it's the *governance* pattern: a re-executing adversarial
    reviewer with veto is exactly the anti-overfitting scaffold our own gates enforce.
    Provenance-per-submission is the reproducibility discipline others skip.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** read — mine the reviewer/veto design; alphas themselves are BRAIN-bound.

- **Dependence-Informed Sparse Neural Architecture for Stock Return Prediction** — Lin, Chen, Wang, Briola, Aste, 2026-08-14 — [arXiv:2608.14323](https://arxiv.org/abs/2608.14323)
  - **What it is:** estimate dependence among firm characteristics with a Maximally
    Filtered Clique Forest (MFCF), map its clique structure to a Homological Neural
    Network — the max clique size K is the *only* complexity knob and bounds interaction
    order. The filtered graph fixes depth/width/sparse-connections before training. On
    US excess returns 1987–2016 (94 characteristics): matches a 3-layer MLP on pooled
    accuracy, **ranks the cross-section better with ~80× fewer parameters**; both the
    sparsity and the grouping contribute, significant after multiple-testing correction.
  - **Why it matters for trading:** a principled, interpretable answer to "how big a net"
    — architecture derived from the correlation graph, not hyperparameter search. Fewer
    params = less overfit surface, the recurring failure mode in our audits.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** replicate — MFCF→HNN is reusable for any cross-sectional characteristic panel (equity-first; needs a multi-asset feed for crypto).

- **Self-Supervised Auxiliary Task Discovery for Stable RL in Stock Trading** — Orra, Choudhary, Thakur, 2026-08-16 — [arXiv:2608.15841](https://arxiv.org/abs/2608.15841)
  - **What it is:** auxiliary tasks for a trading RL agent are *discovered* (not hand-
    designed) as General Value Functions; a secondary net learns their cumulants and
    discount factors via meta-gradient on long-term trading impact. Tested on DJI, FTSE,
    Sensex, TAIEX indices — more robust learning vs fixed-auxiliary baselines.
  - **Why it matters for trading:** addresses RL instability under non-stationarity — the
    core reason RL-trading papers rarely survive OOS. Meta-learned auxiliaries adapt
    across regimes instead of assuming a fixed horizon.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve — index-level, heavy infra; watch the meta-gradient auxiliary idea.

- **LLM-Driven Small-Capitalization Trading (news sentiment + macro + technical)** — Kargarzadeh, Khaledian, Parvini, Khaledian, 2026-08 — [arXiv:2608.12283](https://arxiv.org/abs/2608.12283)
  - **What it is:** fuses LLM news-sentiment, macro indicators, and technical signals for
    small-cap US equity selection (same author cluster as the news-drift study below).
  - **Why it matters for trading:** small-caps are where slow information diffusion should
    leave the most alpha; a data point on whether multimodal LLM fusion beats each channel.
  - **Scores:** Novelty 2/5 · Credibility 2/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve — low-differentiation genre; verify claims before trusting.

### Microstructure & execution

- **Buy the Rumor, Sell the News: When Is News Priced In?** — Kargarzadeh, Khaledian, Parvini, Ghatak, Khaledian, 2026-08-14 — [arXiv:2608.14014](https://arxiv.org/abs/2608.14014)
  - **What it is:** 4.57M US financial-news articles (2023–26, ~3,000 stocks); an LLM
    teacher distilled into a compact classifier tags 17 event types + 5 attributes,
    articles are clustered into stories (first-report vs follow-up), beta-adjusted
    abnormal returns measured on 1.68M stock-day events vs 364k neutral placebos.
    Results: (1) the move concentrates **before/at publication — 2.8× its +20d value**;
    for rumor-flagged events the rumor day captures the *entire* move, confirmation adds
    nothing. (2) **Underreaction to numbers** (earnings/dividends/guidance/analyst drift
    for weeks) vs **overreaction to stories** (launches/macro/leadership give it back).
    (3) volatility rises pre-publication, falls once out (uncertainty resolves).
  - **Why it matters for trading:** a clean, large-sample event taxonomy with a shipped
    per-tag drift table — a ready prior for news-conditioned forecasting and for sizing
    post-event drift-vs-reversal. The magnitude≫sign asymmetry echoes Portnaya's
    "bounce has no direction" (2606.29591) on the microstructure side.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read — the drift-by-tag table is directly usable; needs a news feed (equity).

- **FlowLOB: Controllable Limit Order Book Generation with Flow Matching** — Wang, Bacalum, Olby, Ventre, Stillman, 2026-08-13 — [arXiv:2608.13096](https://arxiv.org/abs/2608.13096) · companion eval **LOB-ID** (inception distances) — [arXiv:2608.13082](https://arxiv.org/abs/2608.13082)
  - **What it is:** a conditional flow-matching generator for LOB trajectories (HKEX,
    multi-symbol, 0.1/1/10s). At matched data/architecture/compute vs diffusion, flow
    matching reaches best quality in **only 10 ODE steps** (diffusion needs many more),
    beats two learned + two agent-based baselines on distributional metrics at fine
    frequencies, and **transfers zero-shot to held-out symbols** with controllable
    counterfactual scenarios. LOB-ID gives a standardized Inception-Distance metric.
  - **Why it matters for trading:** a fast, controllable market simulator is the missing
    substrate for training/stress-testing execution and market-making agents — and a
    principled synthetic-data evaluator stops "looks realistic" hand-waving.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve as tooling — track the Ventre/Stillman LOB-generation line.

### Risk & portfolio

- **Entropic Value-at-Risk portfolio optimization for tempered stable Lévy processes** — Jaehyung Choi, 2026-08-18 — [arXiv:2608.18022](https://arxiv.org/abs/2608.18022)
  - **What it is:** parametric EVaR portfolio optimization under tempered-stable Lévy
    returns. Derives portfolio cumulant-generating functions and weight-dependent
    admissible MGF domains under two multivariate constructions (multivariate normal
    tempered stable; independent-component factorization), so portfolio EVaR is
    evaluated from fitted asset/component parameters **without repeated portfolio-level
    distribution fitting**. Builds min-EVaR + two entropic reward–risk portfolios;
    rolling 2000–2026 US sector-ETF OOS test — several **beat CVaR-matched and standard
    benchmarks on realized Sharpe.**
  - **Why it matters for trading:** EVaR is a coherent risk measure, an upper bound on
    CVaR, that weights the worst losses exponentially — the natural control for
    heavy-left-tailed books. The closed-form CGF makes it computationally practical
    where CVaR needs scenario simulation.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** **backtested** — adapted to a single-series EVaR exposure gate on
    BTC-USD (see below). Cross-sectional replication is the higher-value path but blocked
    on a multi-asset crypto feed.

- **Simulating Stress Laws under Extremal Dependence (SSGEN)** — Mantu Gupta, Anand Deo, 2026-08-13 — [arXiv:2608.13056](https://arxiv.org/abs/2608.13056)
  - **What it is:** continuation of the tracked SS-GEN line. In regions where several
    losses are simultaneously extreme, both the conditional law of risk factors and the
    most-plausible stress configurations are governed by the **same limiting tail law**;
    preserving its measure recovers rare-event probabilities and scaled conditional stress
    laws, while its density governs reverse-stress optimization. SSGEN learns extremal
    dependence from intermediate exceedances and extrapolates with a Pareto radial
    component, with convergence guarantees even when the target event is absent from data.
  - **Why it matters for trading:** tells you *what a generative stress model must
    preserve* (extremal dependence) to be trustworthy — a spec sheet for validating any
    synthetic-scenario / tail-risk generator, including the LOB/diffusion tools above.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** reference — a checklist for stress-generator validation.

- **Regime-Gated Residual Mixture-of-Experts for Cross-Sectional Volatility Forecasting** — Junyi Ye, Gargi Vijay Borde, 2026-08-12 — [arXiv:2608.12251](https://arxiv.org/abs/2608.12251)
  - **What it is:** asks *where* regime information should enter a neural vol model. On
    5-day realized-vol forecasts for 1,027 US equities (walk-forward, matched info/
    capacity/tuning/seeds): RG-ResMoE routes residual corrections via a regime-gated MoE
    but keeps regime vars out of the direct forecast path. Feeding regime vars into the
    *input* degrades accuracy and stability; restricting them to the *routing gate*
    improves accuracy **and VaR calibration**; soft routing beats hard. Replicates on a
    Japanese panel.
  - **Why it matters for trading:** a concrete, generalizable finding — regime info is
    best used to *gate* not to *predict*. Directly informs how we build vol-target and
    exposure overlays (the exact axis today's backtest probes).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read — "gate, don't feed" is a reusable design rule for our overlays.

- **Scalable constrained dynamic portfolio choice via Pontryagin/adjoint methods** — Jeon, Huh, Koo, Lim (2608.15667) + Huh, Kim, Jeong (2608.17808), 2026-08-15/18 — [arXiv:2608.15667](https://arxiv.org/abs/2608.15667) · [arXiv:2608.17808](https://arxiv.org/abs/2608.17808)
  - **What it is:** two same-week papers on constrained dynamic portfolio choice —
    "Scalable Pontryagin-Guided Adjoint-to-Control Recovery" and "Self-Consistent Adjoint
    Policy Iteration" — recover optimal controls under constraints via adjoint/BSDE
    machinery rather than dynamic-programming grids that explode in dimension.
  - **Why it matters for trading:** adjoint/Pontryagin methods scale multi-period
    allocation with realistic constraints (leverage, no-short, turnover) to high
    dimension — the practical bottleneck in dynamic portfolio construction.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve — method reference for constrained multi-period allocation.

### Asset class / derivatives

- **Beyond the Skew-Stickiness Ratio: Transport Geometry of Spot-Driven Variance Surface Dynamics** — Charlie Che, Pradeepta Das, 2026-08-12 — [arXiv:2608.12493](https://arxiv.org/abs/2608.12493)
  - **What it is:** a geometric theory of arbitrage-free implied-variance-surface dynamics.
    Spot moves generate transport vector fields; the transport velocity v(k) unifies all
    stickiness regimes — the **SSR is just the zeroth-order coefficient**, higher orders
    govern ATM skew, curvature, and higher smile derivatives. Sticky-strike/-delta, local
    vol, and rough vol all fall out as special cases. On 5y of SPX across 7 tenors: SPX is
    "super-skew" (SSR 1.44 at 1m → 1.01 at 2y), self-similar transport is rejected at all
    tenors (skew-transport coefficient flips sign between 6–9m), and the full 3-parameter
    model **beats SSR on OOS curvature dynamics by 17–21%** at medium tenors.
  - **Why it matters for trading:** a nonparametric, arbitrage-consistent way to forecast
    how the whole smile moves with spot — the core object for vol trading, hedging, and
    barrier/exotic risk. Generalizes the ad-hoc SSR practitioners use.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read — options-desk tool; SPX-first, adaptable to any liquid surface.

## New resources & tooling
- **Diffusion Models in Finance: A Survey** — Wang & Ventre — [arXiv:2608.12583](https://arxiv.org/abs/2608.12583). First survey dedicated to diffusion-family generative models in finance (time series, LOBs, tabular); open-source companion repo. A map for the fast-growing generative-finance stack (and context for FlowLOB above).
- **Forma / ProForma-20Q** — Johnson, Jiang, Chaudhuri, Chen, Falvey, O'Cofaigh — [arXiv:2608.11327](https://arxiv.org/abs/2608.11327). First reproducible benchmark for jointly forecasting **complete** financial statements (78 line items, 1–20 quarters ahead) scored by change-space R²; Forma (a masked-tuple Gaussian transformer reading statements as (account, quarter, value) sets) beats classical ML, chained GBMs, a zero-shot TS foundation model, and frontier LLMs — lead **widens with horizon**, intervals never under-cover, forecasts nearly satisfy accounting identities. Directly relevant to DCF-driven fundamental valuation.
- **LOB-ID** — Bacalum, Wang, Olby, Garaj, Stillman — [arXiv:2608.13082](https://arxiv.org/abs/2608.13082). Standardized Inception-Distance evaluator for synthetic LOB data (paired with FlowLOB).

## Watchlist updates
New players/authors worth tracking (added to `watchlist.md`):
- **Jaehyung Choi** — Entropic-VaR / tempered-stable Lévy portfolio construction; closed-form EVaR CGF.
- **Antonio Briola / Tomaso Aste (UCL)** — network-filtered (MFCF→HNN) interpretable neural architectures for cross-sectional return prediction.
- **Weicheng Ye / Haizhao Yang** — agentic alpha discovery with adversarial re-execution veto (AgonAlpha).
- **Carmine Ventre / Namid Stillman (King's College London)** — flow-matching / diffusion LOB generation + synthetic-data evaluation (FlowLOB, LOB-ID, diffusion survey).
- **Junyi Ye** — where-to-inject-regime-information neural vol forecasting (RG-ResMoE); quantization for financial TS.
- **Alireza Kargarzadeh / Arman Khaledian et al.** — large-scale LLM news-event taxonomy + abnormal-return drift/reversal mapping.
- **Charlie Che / Pradeepta Das** — transport-geometry theory of implied-variance-surface dynamics (generalized SSR).
- **Travis L. Johnson** — long-horizon complete-financial-statement forecasting (Forma / ProForma-20Q).

## Open questions / threads to pull next run
- **Cross-sectional crypto remains the blocked frontier.** Three+ independent lines now
  point off single-series BTC (Choi EVaR, MINGLE, MFCCA, Halperin three-matrices, Aste
  MFCF→HNN) — all are *cross-sectional* by construction. The pipeline is single-symbol;
  a BTC/ETH/alts multi-asset feed is the highest-value unblock. Until then, single-series
  daily BTC is empirically tapped out (12 straight rejects).
- **"Gate, don't feed" (RG-ResMoE):** could a regime-*routed* (not regime-conditioned)
  version of any prior overlay behave differently OOS? Worth a controlled re-test.
- **News drift-by-tag table (2608.14014)** is a ready prior — but needs a crypto news
  feed to port off equities; is there a crypto-native event taxonomy with abnormal-return
  drift measured?
- **Signed Optimal Transport for order flow** (Weng 2608.17363) is pure theory (no
  financial data yet) — watch for an empirical follow-up on flow conservation in LOBs.
- Next ceiling: **2608.18022**.
