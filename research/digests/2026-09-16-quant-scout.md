# Quant Scout Digest — 2026-09-16

_7-day window since 2026-09-09 (ceiling 2609.04917). Swept q-fin.TR / PM / ST / CP / RM
+ finance-applied cs.LG on the 2609.05xxx–2609.12xxx band. All items below have a
verified arXiv abstract; deduped against `research/INDEX.md`._

## TL;DR
- **Fabrizio Lillo lands two this week.** (1) *Explainable DL for price-trade dynamics*
  (Naviglio & Lillo, 2609.06085) trains a deep net on HF returns + signed volume, then
  uses SHAP to reverse-engineer it into a **parsimonious parametric impact model** that
  matches the net — signed-volume effect is "sign-preserving and saturating" (nonlinear
  impact), lagged returns act as a **state variable deciding continuation vs reversal**.
  (2) *Robust RL market making under regime-switching flow* (Moret & Lillo, 2609.11614):
  a C51 distributional DQN beats Guéant-Lehalle-Fernandez-Tapia in stationary flow but
  **blows up under persistent directional imbalance** until a Bayesian change-point
  filter + queue-imbalance signal restore it — the edge is *regime detection*, not the
  RL core.
- **Backtest of the week (ALM-GARCH → BTC): MIXED, leans REJECT — 16th straight
  daily-crypto reject-lean.** Sign-asymmetric long-memory vol gate: train Sharpe 1.026 →
  **OOS 0.069, CAGR −0.88%**, deflated-SR **0.435** (fail). Two confirming tells inside
  the sweep — the **asymmetry buys ~0.05 Sharpe** (symmetric control nearly ties) and the
  **winner is the shortest-memory config** (long memory carries no edge, echoing last
  week's Volterra result). Only survivor: crash insurance (OOS MaxDD −34% vs B&H ≈ −77%).
- **A signal-library caution with teeth (da Costa Nunes, 2609.12477):** ~3,000 signals
  on 20 assets all ~90% correlated with PC1 — but the paper proves **crowding alone
  imposes neither a nonzero mean nor PC1 agreement**; apparent alignment is a
  *research-design artifact* (combining design weights shrinks angle to PC1 by
  √(λ₂/λ₁)), not evidence the library captures return structure. Theory only, no data.
- **Boyd ships a boringly strong baseline (Devanathan/Tzikas/Boyd, 2609.07946):** on
  stock/bond/gold/cash 2006–2026, **simple vol-targeting improves every risk & drawdown
  metric**, and convex-optimization allocation adds substantial further return — all from
  public data with conservative costs. A clean, replicable overlay benchmark.
- **Choi returns (2609.11905)** with EVaR risk-parity for tempered-stable returns
  (recovers vanilla vol-parity under Gaussian, positive Sharpe vs equal-weight across 3
  universes) — a portfolio-level sibling of the EVaR gate we already found *doesn't*
  transfer to single-asset BTC timing.

## Findings by focus area

### ML / AI for alpha
- **Explainable Deep Learning for Price-Trade Dynamics: From Black-Box Forecasts to
  Effective Parametric Models** — Naviglio & Fabrizio Lillo, 2026-09-05 —
  [2609.06085](https://arxiv.org/abs/2609.06085)
  - **What it is:** train a deep FFN on HF returns + signed volumes vs a linear VAR
    baseline, then use Shapley attributions as a *structural-discovery* tool to distill a
    small interpretable parametric model that matches the net.
  - **Why it matters for trading:** recovers nonlinear price impact (signed volume
    sign-preserving + saturating) and shows **lagged returns are a regime/state variable**
    switching order flow between continuation and reversal — a directly usable impact
    parameterization from a tracked player.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read (impact-model spec for the execution cost layer)
- **Large Signal Libraries: Equal-Weight Limits and the Divergent Spectra of Signals and
  PnL** — Marc da Costa Nunes, 2026-09-11 — [2609.12477](https://arxiv.org/abs/2609.12477)
  - **What it is:** distinguishes four objects (equal-weight signals, signal PCs,
    equal-weight PnL, PnL PCs) and proves crowding alone forces neither a nonzero mean nor
    PC1 alignment; combining design weights shrinks angular deviation to PC1 by √(λ₂/λ₁).
  - **Why it matters for trading:** a rigorous warning that "all my signals load on PC1"
    can be a construction artifact, not captured structure — bears on how alpha libraries
    are aggregated and deflated. **Explicitly presents no market-data results.**
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (theory; revisit if an empirical companion appears)
- **Nyström Attention Matches Full Attention for Cross-Sectional Stock Prediction** —
  Kunhan Guo, 2026-09-07 — [2609.08106](https://arxiv.org/abs/2609.08106)
  - **What it is:** linear-complexity Nyström attention reaches full-attention accuracy on
    cross-sectional equity return prediction.
  - **Why it matters for trading:** efficiency, not edge — relevant only when scaling a
    cross-sectional transformer to a large universe; no standalone alpha claim.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Microstructure & execution
- **Deep Learning of Robust Market Making under Regime-Switching Order Flow** — Felipe
  Moret & Fabrizio Lillo, 2026-09-10 — [2609.11614](https://arxiv.org/abs/2609.11614)
  - **What it is:** C51 distributional DQN market maker in a zero-intelligence LOB vs the
    GLFT benchmark; augmented with a Bayesian online change-point filter on directional
    flow bias + a queue-adjusted quote-exposure imbalance, plus scenario-bandit
    reweighting for stress robustness.
  - **Why it matters for trading:** confirms the recurring lesson — a bare RL MM is fragile
    to non-stationary flow; **the durable value is the regime/change-point detector**, not
    the policy network. Same moral as the exec-cost-filter and vol-gate threads.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read
- **Regimes in the Order Flow** — Ramzi Jebali (ENSTA / Scuola Normale Superiore),
  2026-09-07 — [2609.07989](https://arxiv.org/abs/2609.07989)
  - **What it is:** Bayesian Online Change-Point Detection (BOCPD) + two literature
    extensions applied to signed order flow of NASDAQ equities to flag structural breaks
    (stable↔unstable) in real time. 59pp, 48 figs — a thorough methods survey.
  - **Why it matters for trading:** the change-point-on-flow primitive that Moret & Lillo
    plug into their MM this same week; a reference implementation of the detector both the
    execution and vol-gate threads keep converging on.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read
- **The Privacy Subsidy in Market Microstructure** — Yuki Nakamura, 2026-09 (cs.GT
  cross-list) — [2609.10543](https://arxiv.org/abs/2609.10543)
  - **What it is:** a maker pricing on a signal *strictly coarser* than the flow it settles
    must cede a closed-form welfare transfer to traders — proven across single-period Kyle,
    Glosten-Milgrom, and continuous Kyle-Back; structurally parallel to Loss-Versus-
    Rebalancing (LVR). _(arXiv v1 metadata shows a June date under a 2609 ID — flagged.)_
  - **Why it matters for trading:** a Kyle-family theory bound linking information
    coarsening to adverse-selection cost; conceptual, ties AMM LVR to classic microstructure.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve
- **The Double-Edged Sword of Short-Selling Bans** — Della Corte, Kosowski,
  Papadimitriou & Rapanos, 2026-09-08 — [2609.08881](https://arxiv.org/abs/2609.08881)
  - **What it is:** empirical analysis of short-selling-ban effects on liquidity and price
    efficiency (credible author roster — Imperial/AQR-adjacent).
  - **Why it matters for trading:** regime/regulatory-risk context for liquidity provision
    and shorting-based strategies; not a directly tradable single-name signal.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read

### Risk & portfolio
- **Simple Dynamic Stock/Bond/Gold Portfolios** — Devanathan, Tzikas & Stephen P. Boyd,
  2026-09-07 — [2609.07946](https://arxiv.org/abs/2609.07946)
  - **What it is:** on stocks/bonds/gold/cash, 2006–2026 monthly with conservative costs,
    compares 60/40 & 50/30/20 fixed benchmarks against (a) vol-controlled mixing with cash
    and (b) convex-optimization allocation with return forecasts. Vol control alone
    improves every risk-adjusted & drawdown metric; convex opt adds substantial further
    return.
  - **Why it matters for trading:** an authoritative, fully replicable baseline for the
    vol-target overlay this repo keeps testing — and a reminder that on *multi-asset*
    books vol control *does* help (vs the single-series BTC null).
  - **Scores:** Novelty 2/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** replicate (multi-asset overlay benchmark; needs a stock/bond/gold feed)
- **Entropic Value-at-Risk Parity for Tempered Stable Returns** — Jaehyung Choi,
  2026-09-10 — [2609.11905](https://arxiv.org/abs/2609.11905)
  - **What it is:** EVaR-deviation risk contributions (IRP/ERC) under multivariate normal
    tempered-stable + ICA components; recovers conventional vol IRP/ERC under Gaussian, and
    EVaR-based ERC beats equal-weight on Sharpe across three universes.
  - **Why it matters for trading:** the portfolio-construction sibling of Choi's earlier
    EVaR work (2608.18022) that we tested as `evar_regime` — where the tail measure added
    nothing to *single-asset* BTC timing. This confirms EVaR's value is **cross-sectional
    allocation**, not single-series exposure gating.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (needs a multi-asset universe to test as intended)
- **Market-Informed Networks for Modeling and Forecast Evaluation of Financial
  Extremes** — Jungbluth, Lederer & Simon Trimborn, 2026-09-10 —
  [2609.11575](https://arxiv.org/abs/2609.11575)
  - **What it is:** network-structured models for tail/extreme-event modeling and forecast
    evaluation across assets.
  - **Why it matters for trading:** tail-risk plumbing; sits with the extreme-value /
    stress-simulation thread (SS-GEN, IlliQaR) rather than offering a direct entry signal.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

### Asset class / market (crypto, vol, derivatives)
- **Asymmetric Long-Memory GARCH: Sign-Dependent Kernel Injection in a 2D Markov
  Chain (ALM-GARCH)** — Kennedy Titus Kayaki & Kyungsub Lee, 2026-09-06 —
  [2609.06422](https://arxiv.org/abs/2609.06422) — **← backtested this run**
  - **What it is:** GARCH with sign-dependent *level* (injection amplitude) and *memory*
    (persistence/kernel offset) channels, Foster-Lyapunov stability. On 5 equity indices +
    **Bitcoin**, joint symmetry strongly rejected (level-driven); the **memory channel is
    significant for Nikkei, KOSPI & BTC**; OOS variance forecasts only *match* benchmarks.
  - **Why it matters for trading:** the vol-model of the week that explicitly covers BTC —
    natural daily replicate. See backtest below: the two channels are real in-sample but
    non-tradable for single-series timing.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** backtest → **done (MIXED, leans REJECT)**
- **The Log S-fBM Model: Statistical Analysis** — Zarhali, Emmanuel Bacry &
  Jean-François Muzy, 2026-09-08 — [2609.09405](https://arxiv.org/abs/2609.09405)
  - **What it is:** log-volatility as a *stationary* fractional Brownian motion bridging
    rough (H≈0.1) and multifractal (H≈0) regimes; derives scaling/deviation inequalities,
    a **rough-vs-multifractal hypothesis test**, and small-intermittency GMM calibration
    (empirical intermittency ≈ 0.02 across assets).
  - **Why it matters for trading:** rigorous estimation/testing scaffold for rough-vol
    modeling (Bacry/Muzy Hawkes lineage) — foundational for anyone calibrating H on crypto.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (calibration reference)

## New resources & tooling
- **dexamine** — Magnus Hansson, [2609.10407](https://arxiv.org/abs/2609.10407) — a Python
  package for pulling and parsing Uniswap event data on Ethereum; on-chain DEX microstructure feed.
- **Deep Learning for Reflected BSDEs: Regularization and Error Analysis** — Ruimeng Hu &
  Yihan Zou, [2609.05434](https://arxiv.org/abs/2609.05434) — numerical method for
  American-option-style optimal stopping (tracked player Ruimeng Hu).

## Watchlist updates
New authors/players surfaced this run worth tracking:
- **Kyungsub Lee** — asymmetric long-memory volatility (ALM-GARCH), sign-dependent kernels.
- **Emmanuel Bacry & Jean-François Muzy** — rough/multifractal vol, stationary-fBM, Hawkes lineage.
- **Stephen P. Boyd (Stanford)** — convex-optimization portfolio construction (CVXPY); simple, replicable dynamic allocation baselines.
- **Ramzi Jebali** — Bayesian online change-point detection on order flow.
- **Marc da Costa Nunes** — geometry of large signal libraries (signal-vs-PnL spectra, crowding artifacts).
- **Pasquale Della Corte / Robert Kosowski (Imperial)** — short-selling bans, liquidity & efficiency.
- **Simon Trimborn** — market-informed networks for financial extremes.
- **Magnus Hansson** — on-chain DEX data tooling (dexamine).

## Open questions / threads to pull next run
- **The daily single-series vol axis is now triple-exhausted** (plain RV, EVaR tail,
  sign-asymmetric long-memory) — all crash-insurance, no alpha. Stop swapping vol
  statistics on daily BTC.
- **Highest-leverage unblock, now 5× overdue: an hourly / multi-coin OHLCV loader.** Every
  live crypto signal (Kitron-Wengrowicz 15-min reversal, Zhai on-chain identity,
  Quarter-Hour effects, and this week's order-flow-regime detectors) lives at intraday or
  cross-sectional resolution the daily cache can't reach.
- **Multi-asset overlay is now testable in spirit** (Boyd 2609.07946, Choi 2609.11905 both
  want a cross-asset universe) — but the repo only has BTC/ETH daily CSVs; a stock/bond/gold
  or multi-coin feed would unlock both.
- **Later-dated items to check next run** (IDs 2609.13xxx–15xxx, likely just past today's
  ceiling): Angstmann & Gebbie event-time order-flow memory (2609.13715); Han/Xu diffusion
  vol-surface hedging (2609.13402); Peng/Khushi/Poon CAST cross-asset drawdown-control
  (2609.14205); Bhaskara/Jerfy prediction-markets crypto-vol hedge (2609.14267).
