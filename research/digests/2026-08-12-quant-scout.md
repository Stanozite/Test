# Quant Scout Digest — 2026-08-12

_7-day window since 2026-08-05. Swept arXiv q-fin (TR/PM/ST/CP/RM) plus finance-applied
cs.LG, IDs 2608.03616 → 2608.10852 (above last ceiling 2608.03616). 11 findings, all
verified against live abstracts._

## TL;DR
- **Public wallet identity beats anonymity on a DEX** (Zhai, 2608.04373): a decentralized
  venue publishes the counterparty on every order; ranking 147k wallets by post-order price
  move is a *persistent* attribute (rank-corr 0.52 across 10-day windows) and adding the top
  wallets' live flow lifts 1-second-return OOS R² to 12.3% (+13.2%, t=9.2, 1.6× the best of
  200 placebos). Identity carries short-horizon alpha that anonymous LOB data misses.
- **Order imbalance = a closed-form skew/width adjustment** (Cotton, 2608.07690): under
  exponential competing quotes, OTC imbalance is absorbed *exactly* by translating the maker's
  skew, widening quotes, and scaling cost-of-carry — no free parameter beyond observed width;
  even zero-inventory makers should skew; "constant width, linear skew" is the small-skew limit.
- **Strategy capacity is a causal question you can't answer with the usual proxies**
  (Rodriguez Dominguez & Noguer i Alonso, 2608.08405): the same-date comparison that makes a
  capacity experiment robust to market shocks *also* cancels the strategy's own crowding — so
  it can't measure the thing capacity is about; recovering aggregate crowding needs deliberate
  exposure variation or time-variation, and a fixed holding period understates the eventual edge decay.
- **Crypto's "statistical maturity" is skin-deep** (Kim/Cho/Lee, 2608.10852): conventional
  stylized facts converge with equities, but complexity–entropy + directed-visibility-graph
  diagnostics show crypto is more locally random in calm periods yet far more time-irreversible
  around big moves — large fluctuations begin abruptly and stay elevated. Different dynamics.
- **Backtest — `cascade_warning` on BTC-USD → REJECT** (tests Garcia Seuma 2608.03616): a
  critical-slowing-down overlay (de-risk on rising variance+autocorrelation) has train Sharpe
  0.658 → **OOS −0.827, CAGR −15.5%**, fails deflated-SR, and — unlike every prior overlay —
  gives **no crash-insurance drawdown edge** (train MaxDD −80% ≈ B&H). Confirms the paper's
  claim that no scalar pre-state measure grades a first-order cascade. **10th straight daily-BTC reject.**

## Findings by focus area

### ML / AI for alpha
- **Objective-Oriented Quantitative Investment (OOQI): specification-driven synthesis of strategy pipelines** — Liangliang Zhang, 2026-08-11 — [2608.10410](https://arxiv.org/abs/2608.10410)
  - **What it is:** reframes automated quant from "which pipeline scores highest on one metric"
    to "which pipeline satisfies an *identity*" — pure selection alpha, resilient in declines,
    within turnover/capacity budgets. Models the full pipeline as a typed design space (8.85×10⁸
    assemblies), formalizes investor intent as falsifiable spec clauses (8 requirement families,
    hard/soft, interaction algebra), and a compiler verifies clause-by-clause. Crucially treats
    the *satisfaction rate itself* as a statistical object with deflation for search width, temporal
    holdout, and random-assembly nulls; anytime-valid rolling re-certification via e-processes.
  - **Why it matters for trading:** a rigorous alternative to Sharpe-chasing AutoQuant; the
    deflation-for-search-width discipline is exactly our deflated-Sharpe gate, generalized to a
    whole spec. Directly useful as a *design template* for how we score and re-certify strategies.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (adopt the "satisfaction rate as deflatable statistic" idea into our gate)

- **When the Fed Speaks: Dynamics and Forecasts of the Volatility Surface** — Lukasz Adamski & Robert Słepaczuk (UW QFRG), 2026-08-11 — [2608.10693](https://arxiv.org/abs/2608.10693)
  - **What it is:** forecasts the full implied-vol surface around scheduled FOMC dates with a
    convolutional 2D-LSTM applied *directly to the surface* (no dimensionality reduction), augmented
    with an FOMC-date feature. Confirms IV rises pre-announcement, strongest for short-dated OTM
    options in high-vol regimes; the ML edge over a random-walk benchmark exists but is "limited by
    the noisy characteristics of the IV surface."
  - **Why it matters for trading:** honest, cost-of-the-noise-aware take on ML vol-surface
    forecasting from a tracked group; the "scheduled-event feature helps, but noise caps the edge"
    result is a useful calibration for any event-driven options overlay.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (options-surface data we don't hold) — file as methods reference

### Microstructure & execution
- **Public Trader Identity: Adverse Selection and Return Predictability** — Daojing Zhai, 2026-08-05 — [2608.04373](https://arxiv.org/abs/2608.04373)
  - **What it is:** reconstructs a full-depth DEX LOB from 17.1B messages / 14.3M aggressive orders
    by 147,113 wallets ($84.3B taker notional). Three results: (1) informativeness is a *persistent
    wallet attribute* (rank-corr 0.52 across adjacent 10-day windows); (2) adding top-ranked wallets'
    live activity to an anonymous price/quote/flow benchmark raises 1-second-return OOS R² to 12.31%
    (+13.2%, t=9.2, = 1.6× the largest of 200 activity-matched placebos); (3) the increment grows
    from 1.43 to 2.47 pp of R² when measured at realized trades.
  - **Why it matters for trading:** transparent on-chain venues break the "informed traders need
    anonymity" assumption — wallet reputation is a directly exploitable, short-horizon alpha source
    unavailable in any anonymized feed. A concrete new crypto-microstructure signal family.
  - **Scores:** Novelty 5/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** replicate (needs wallet-tagged DEX message data — highest-value new axis this run)

- **On a Simple Relationship Between Order Imbalance, Skew and Width in OTC Trading** — Peter Cotton, 2026-08-07 — [2608.07690](https://arxiv.org/abs/2608.07690)
  - **What it is:** a sealed-bid RFQ market maker facing imbalanced buy/sell intent. Under
    exponentially-distributed best competing quotes, a steady-state symmetry compresses the
    imbalanced problem onto the balanced one: imbalance is absorbed *exactly* by a translation of
    skew, a widening of quotes, and a multiplication of effective cost-of-carry — with no free
    parameter beyond observed width. Consequences: zero-inventory makers should still skew; skew
    responds to imbalance at *first* order, width only at *second*; "constant width, linear skew"
    is recovered as the small-skew limit.
  - **Why it matters for trading:** closed-form, calibratable quoting rule for OTC/RFQ making; the
    first-order-skew / second-order-width split is an implementable market-making heuristic and a
    clean theoretical anchor for the Barzykin RFQ lineage we already track.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (market-making reference; not directly backtestable on OHLCV)

- **Measuring the engine of a liquidation cascade: subcritical branching inside a first-order transition** — Ramon Marc Garcia Seuma, 2026-08-04 — [2608.03616](https://arxiv.org/abs/2608.03616)
  - **What it is:** measures the branching ratio of the Oct-2025 crypto crash *in flight* from a
    transparent venue's on-chain fill log — it ran deeply **subcritical** (λ̂≈0.1–0.2, no free
    constants). Across 7 cascades (2022-25), at onset the order parameter (mean inter-asset coupling)
    jumps 1.6–4.4σ into a near-fully-ordered phase while the susceptibility proxy χ *collapses* in 5/7
    and diverges in none. The Galton–Watson critical-cascade account is eliminated at power ≥0.96:
    the transition is **abrupt/first-order, not critical**, so "none of the scalar pre-state measures
    grades it." Severity = shock × map-in-path × liquidity-withdrawal.
  - **Why it matters for trading:** kills the folk belief that critical-slowing-down (rising
    variance/autocorrelation) front-runs crypto crashes — a strong prior for any de-risking overlay.
    Directly implies our early-warning axis should fail on price-only pre-state data. **Backtested this run (below).**
  - **Scores:** Novelty 5/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** backtest ✔ (done — `cascade_warning`, REJECT, confirms the paper)

- **Velocity- and Regime-Aware Detection of Intraday Options Market Manipulation** — Alex Chen & Maria Hybinette, 2026-08-05 — [2608.05373](https://arxiv.org/abs/2608.05373)
  - **What it is:** manipulation leaves a signature in the *velocity* of market state, not its level.
    A minute-level, strictly time-partitioned autoencoder on smoothed state-velocity (option-Delta
    velocity for index options, price velocity for equities) recovers 10/10 regulator-flagged
    BANKNIFTY manipulation days OOS with thresholds fixed beforehand; a pump-reversal shape score
    transfers to thin US equities (AUC 0.91/0.81 on SEC-complaint names). Instructive negative:
    HMM-regime conditioning trades recall for precision (~25%), and SHAP shows "unconfirmed" alerts
    share the confirmed days' profile (cos-sim 0.99) — the precision ceiling is *incomplete labels*,
    not detector failure.
  - **Why it matters for trading:** a velocity-of-state anomaly detector is a reusable surveillance
    /risk primitive; the "high AUC ≠ actionable precision under incomplete labels" lesson echoes our
    07-15 base-rate-honesty thread.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (surveillance/risk reference)

- **When Cross-Venue Agreement Is Not Price Discovery: Disclosure Frontiers for 24/7 Equity-Perpetual Oracles** — Seo, Cha, Son, Lee, Lee & Sung, 2026-08-10 — [2608.09188](https://arxiv.org/abs/2608.09188)
  - **What it is:** crypto-listed equity perpetuals trade while the cash market is closed but still
    need a mark. Models the closed-window mark as the fixed point of an oracle operator (external
    anchoring + self/peer reference); from marks alone the two blocks are *observationally equivalent*
    — every reduced form admits infinitely many topology decompositions, so lead-lag and
    information-share estimators have power = size. Only *disclosure* (diagonal adjustment, forbidden
    anchors) or the cash reopen breaks the equivalence class; empirically a disclosed OKX row survives
    pre-open falsification.
  - **Why it matters for trading:** a caution for anyone using cross-venue agreement or
    information-share as a price-discovery signal on 24/7 wrapped-equity/perp products — agreement can
    be pure self-reference. Matters as these instruments (tokenized stocks, xStocks) proliferate.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (structural/identification result; watch the instrument class)

### Risk & portfolio
- **Robustness or Crowding: Experimental Design for Trading Strategy Capacity** — Alejandro Rodriguez Dominguez & Miquel Noguer i Alonso, 2026-08-09 — [2608.08405](https://arxiv.org/abs/2608.08405)
  - **What it is:** treats "how much capital before the edge disappears" as a *causal* question and
    shows two features conspire against the usual proxies: deployed capital erodes edge gradually (a
    fixed-length trial understates the eventual effect), and parallel implementations trade the same
    securities (not independent units). The same-date comparison that removes market-wide shocks
    *also* absorbs the strategy's own accumulated-position crowding exactly — so the robust design
    can't measure the crowding capacity is about. Recovering the aggregate effect needs deliberate
    exposure variation across implementations or variation over time; the paper prices what each route
    identifies and costs.
  - **Why it matters for trading:** the definitive statement of *why* naive capacity/decay estimates
    mislead — essential before scaling any live edge. A design checklist for capacity studies and a
    warning that in-sample capacity numbers are systematically optimistic.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (capacity-design reference for any strategy we advance to sizing)

- **MINGLE: Mutually-Informed Graph-Locality and Exposures for portfolio diversification** — Chehab, Iacovides, Yazdanparast & Mandic, 2026-08-06 — [2608.06618](https://arxiv.org/abs/2608.06618)
  - **What it is:** joins factor models (blind to latent structure) and graph methods (blind to
    idiosyncratic shocks) by redefining graph *locality via systematic factor-exposure profiles*
    rather than observed co-movement. An ADMM framework jointly learns a latent factor representation
    and its induced graph topology from returns; the resulting exposure-similarity graph aligns with
    economic sectors better than correlation graphs, and portfolios from it beat correlation-based
    counterparts across vol regimes and cost levels (confirmed by paired tests).
  - **Why it matters for trading:** a cleaner covariance/diversification backbone that sidesteps
    finite-sample correlation artefacts — the same problem the Lehalle CD-DFM and Bongiorno/Mantegna
    compact-NN cleaning work (already tracked) attack from other angles. Cross-sectional, so it feeds
    the crypto-basket axis we keep flagging.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** shelve (needs a cross-asset panel; candidate once multi-asset feed exists)

- **Portfolio Allocation under Heterogeneous Scales and Multifractality** — Shinji Kakinaka & Ken Umeno, 2026-08-05 — [2608.04987](https://arxiv.org/abs/2608.04987)
  - **What it is:** builds a risk functional from the *signed* fluctuation function of multifractal
    cross-correlation analysis (MFCCA), indexed by scale s and order q. Unlike MFDCCA it keeps the
    sign, so co-moving and counter-moving components enter risk with opposite signs; at q=2 it recovers
    mean-variance as a scale-dependent limit. On real multi-asset data it lowers drawdown, VaR, and
    expected shortfall vs mean-variance *at every required return, in and out of sample, with no loss
    in realized return* — and sign preservation matters more for tail reduction than aggregating over q.
  - **Why it matters for trading:** a scale- and amplitude-aware risk measure that dominates
    mean-variance on tails without a return cost — directly relevant to crypto's heterogeneous-scale,
    amplitude-dependent coupling. A concrete upgrade path for portfolio construction.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (multi-asset, needs MFCCA tooling; strong candidate for the cross-sectional axis)

### Asset class / market (crypto)
- **Universality and Heterogeneity of Stylized Facts in Cryptocurrency and Equity Markets** — Jaesung Kim, Changhee Cho & Jae Woo Lee, 2026-08-11 — [2608.10852](https://arxiv.org/abs/2608.10852)
  - **What it is:** asks whether crypto's macroscopic "statistical maturity" means dynamical
    equivalence with equities. Using the Complexity–Entropy Causality Plane and directed horizontal
    visibility graphs on 2020-25 high-frequency data: conventional stylized facts converge across all
    assets, but structurally crypto is *more locally random* in ordinary periods yet shows
    *significantly stronger directional time-irreversibility* around high-visibility return events —
    large crypto fluctuations begin abruptly and stay elevated (shared on the upside, asset-specific
    on the downside). "Statistical maturity is only skin-deep."
  - **Why it matters for trading:** empirical backing for why equity-calibrated models mis-fire on
    crypto tails, and — converging with Garcia Seuma this run — that crypto extremes are *abrupt and
    time-irreversible*, not smoothly-approached critical transitions. Reinforces: don't expect
    early-warning predictability in crypto crashes.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (stylized-facts evidence; informs model choice, not a strategy)

## New resources & tooling
- _No standalone new repos/datasets verified this run._ Zhai's DEX study (2608.04373) implies a
  wallet-tagged full-depth LOB dataset exists but the paper does not link a public release — flagged
  as an open thread below.

## Watchlist updates
- **Daojing Zhai** — author — DEX/on-chain microstructure; persistent wallet-informativeness as a
  return-predictive signal (public-identity adverse selection). *Add.*
- **Peter Cotton** — already tracked (added 2026-06-17); confirmed active — two new items this run
  (2608.07690 OTC skew/width, 2608.07479 conformal-prediction information gap).
- **Alejandro Rodriguez Dominguez & Miquel Noguer i Alonso** — authors — causal experimental design
  for strategy capacity/crowding; also prior causal-portfolio-choice work (2607.06702). *Add.*
- **Danilo Mandic (Imperial) team** — author/lab — graph-signal-processing portfolio construction
  (MINGLE factor-graph diversification). *Add.*
- **Robert Słepaczuk (UW QFRG)** — already tracked implicitly via Bysik/Ślepaczuk; confirmed — Fed
  vol-surface ML (2608.10693).

## Open questions / threads to pull next run
- **Wallet-reputation alpha (Zhai 2608.04373) is the standout** — but needs wallet-tagged DEX message
  data (Hyperliquid / dYdX / a transparent perp venue). Can we source even a sample? This is the first
  genuinely *new-data* alpha axis in weeks and sidesteps the tapped-out daily-BTC problem.
- **Cross-sectional crypto is now triple-flagged** (Halperin rank-Markov 2607.27461 · MINGLE
  2608.06618 · MFCCA signed-risk 2608.04987) but blocked on a multi-asset feed. Priority infra task:
  allowlist Yahoo or drop a BTC/ETH/+alts CSV panel into `backtests/data/` so the cross-sectional axis
  can finally run. **10 straight single-series daily-BTC rejects say the single-series well is dry.**
- **Convergence signal:** Garcia Seuma (2608.03616) and Kim/Cho/Lee (2608.10852) independently say
  crypto extremes are *abrupt / first-order / time-irreversible*, not critically-approached — so
  early-warning / critical-slowing-down strategies are structurally dead on crypto. Treat as a settled
  prior; stop testing pre-state crash predictors.
- Next ceiling: **2608.10852**.
