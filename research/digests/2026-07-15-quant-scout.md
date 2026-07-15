# Quant Scout Digest — 2026-07-15

_First run since 2026-07-04 — an 11-day gap, so this sweeps the whole 2607.xxxxx
q-fin window above the prior ceiling 2607.01765 (through the current top ID 2607.12990).
All items below are new against the INDEX dedupe ledger._

## TL;DR
- **Crypto's tradeable edge this window is intraday, not daily.** Kim & Hansen's "Quarter-Hour Effect" (2607.09426) shows periodic *algorithmic* order flow predicts 4–12h crypto returns at quarter-hour/5-min/1-min clocks — invisible at the daily close. Jeon (2607.09230) independently finds order flow only matters *state-dependently* on L2 liquidity regimes, and for ETH more than BTC. Backtested the daily analogue (day-of-week seasonality) on BTC → **REJECT**, confirming the boundary.
- **A base-rate-honest benchmark guts fine-tuned foundation models for equity forecasting** (Cheung & Kwon, 2607.12248): LoRA-adapted TimesFM's "~80% directional accuracy" was the rising-market base rate — *no* directional skill over "always up" at any horizon; per-sector specialization loses to one pooled model (p<0.001). A methods must-read for our own honesty gates.
- **Kyle's model goes multi-asset with stochastic liquidity** (Ekren/Nikitopoulos/Vy, 2607.10934): matrix-valued martingale depth process, causal-optimal-transport primal-dual — the cleanest theoretical extension of our recurring Kyle-λ thread.
- **OTC market making becomes a reputation game** (Barzykin, 2607.11328): RFQ win-ratios feed back into future flow → optimal quoting cycles between reputation-building and monetization, with multiple stable client-flow equilibria.
- **Dynamic causal portfolio choice** (Rodriguez Dominguez, 2607.06702): when the *conditioning driver set itself rotates*, hedging that rotation becomes first-order; complexity scales with #drivers not #assets, and set-changes create unspannable (incomplete-market) risk.

## Findings by focus area

### ML / AI for alpha
- **When Directional Accuracy Lies: A Base-Rate-Honest Benchmark for LoRA-Adapted TimesFM on Equity Forecasting** — Taizhen Cheung, SA Kwon, Jul 14 2026 — [link](https://arxiv.org/abs/2607.12248)
  - **What it is:** A fine-tuned time-series foundation model (TimesFM + LoRA) appeared to hit ~80% directional accuracy on stocks; a naive "always predict up" matched it in a rising market. Under expanding walk-forward folds + stratified held-out-ticker splits + honest baselines, the pooled model shows *no directional skill over the base rate* at any horizon (negative at 6-month), and per-sector adapters underperform one pooled model (p<0.001). Fine-tuning cut point-forecast error but that never became tradeable direction.
  - **Why it matters for trading:** This is the exact failure mode our own pipeline's deflated-Sharpe/OOS gates exist to catch, applied to the hottest tool (TS foundation models). Directional-accuracy headlines are base-rate mirages; adopt their protocol before trusting any FM signal.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read (methods reference — fold its base-rate test into our verdict rubric)
- **Augmenting Fundamental Analysis with Large Language Models: A RAG-Based System for Generating Investor Briefs** — Bartosz Ziółko, Kacper Dobrzeniewski, Jul 2026 — [link](https://arxiv.org/abs/2607.09121)
  - **What it is:** A retrieval-augmented pipeline that assembles fundamental-analysis investor briefs from filings/news. Engineering-systems paper more than an alpha claim.
  - **Why it matters for trading:** Template for a research-brief layer over a fundamental corpus; adjacent to our own scout tooling. No demonstrated return edge.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 2/5 · Actionability 3/5
  - **Next step:** shelve (tooling reference)

### Microstructure & execution
- **The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures** — Chan Kim, Peter Reinhard Hansen, Jul 10 2026 — [link](https://arxiv.org/abs/2607.09426)
  - **What it is:** Six Binance perpetual futures, trade-level data. Periodic volatility/volume bursts cluster at quarter-hour, 5-min and 1-min marks; "trade-size roundness" evidences algorithmic participation; an "Autocorrelation Map" shows *order imbalance forecasts 4–12h returns*. Effect is exclusively intraday — daily aggregation erases it.
  - **Why it matters for trading:** A concrete, credible (Hansen) intraday crypto predictability claim tied to algorithmic clock-periodicity. Directly the backtest target this run — see the daily-analogue result below.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 5/5 · Actionability 3/5 _(needs sub-hour + order-flow data)_
  - **Next step:** backtest (intraday — daily pipeline can only test a degraded analogue; done this run, REJECT)
- **Multidimensional Stochastic Liquidity in Kyle's Model of Informed Trading** — Ibrahim Ekren, Evangelos A. Nikitopoulos, Lu Vy, Jul 12 2026 — [link](https://arxiv.org/abs/2607.10934)
  - **What it is:** Extends classical Kyle to *multiple assets with stochastic liquidity*: a matrix-valued martingale depth process supports equilibrium with stochastic, cross-asset price impact, solved via a causal-optimal-transport primal-dual (plus a general non-symmetric matrix Doob–Meyer decomposition).
  - **Why it matters for trading:** The theoretical backbone for cross-asset impact/adverse-selection modeling — connects our Kyle-λ empirical thread (Aldridge 2607.01377) to a multi-asset equilibrium.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (theory reference)
- **When Does Order Flow Matter? State-Dependent L2 Liquidity-State Transitions in Crypto Futures** — Joohyoung Jeon, Jul 10 2026 — [link](https://arxiv.org/abs/2607.09230)
  - **What it is:** Binance BTCUSDT/ETHUSDT futures 2023–2026, top-20 L2 book + trade flow + macro-event windows. Pre-event L2 liquidity *state* strongly predicts post-event liquidity regime; order flow only adds value layered on top of the state model. ETH holds across regimes; BTC shows only isolated 5-min passes, no regime clearing both horizons.
  - **Why it matters for trading:** Reinforces Kim/Hansen — the crypto edge is microstructural/state-dependent, and BTC is *harder* than ETH. Argues signals should condition on liquidity state, not fire unconditionally.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (needs L2 data; informs a future hourly track)
- **Strategic OTC Market Making with Reputation Feedback** — Alexander Barzykin, Jul 13 2026 — [link](https://arxiv.org/abs/2607.11328)
  - **What it is:** Stochastic-control model where RFQ win-ratios and fill rates feed back into future client flow via performance gates. Optimal MM cycles between reputation-building and monetization; multiple stable client-flow equilibria emerge within a single-dealer problem.
  - **Why it matters for trading:** Barzykin (HSBC) is a leading electronic-FX MM researcher; formalizes the franchise-value-vs-spread tradeoff that pure inventory models miss — relevant to any RFQ/flow-internalization desk.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (MM theory reference)
- **Herding and Liquidity in Order-Book Markets. I. A Robust Liquidity-Stress Crossover and its Reflexive Mechanism** — Jan Novotny, Jul 2026 — [link](https://arxiv.org/abs/2607.08907)
  - **What it is:** Identifies a robust liquidity-stress crossover in order-book markets with a self-reinforcing (reflexive) herding mechanism. Part I of a series.
  - **Why it matters for trading:** A candidate early-warning marker for liquidity regime shifts; pairs with the crash/stress-detection thread (Biancalana 2606.31475, Deo below).
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve
- **Volatility in Prediction Markets: A Structural Approach** — Weiye Xi, Ciamac C. Moallemi, Mallesh Pai, Shouqiao Wang, Jul 2026 — [link](https://arxiv.org/abs/2607.08199)
  - **What it is:** A structural model of volatility dynamics in prediction markets (Polymarket-class bounded-payoff instruments).
  - **Why it matters for trading:** Continues our prediction-market microstructure thread (Portnaya 2606.19517/29591); Moallemi (Columbia) is a credible market-design/MM theorist. Useful if we ever price/hedge event contracts.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Risk & portfolio
- **An Extreme Value Perspective on Learning Stress Laws (SS-GEN)** — Mantu Gupta, Anand Deo, Jul 12 2026 — [link](https://arxiv.org/abs/2607.10700)
  - **What it is:** Self-Similar Generative Estimation decomposes a multivariate tail into an explicit radial component + a nonparametric angular component, reducing rare-event learning to a compact domain that off-the-shelf deep generative models can handle — with asymptotic-exactness guarantees for regularly-varying and Weibull-type tails.
  - **Why it matters for trading:** A principled, architecture-agnostic way to simulate multi-asset tail/stress scenarios — directly useful for stress-testing a book and estimating rare-drawdown probabilities. Extends Deo's stress-scenario line (2606.31122).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (stress-testing method)
- **Dynamic Causal Portfolio Choice: Hedging the Rotation of the Common-Driver Manifold** — Alejandro Rodriguez Dominguez, Jul 7 2026 — [link](https://arxiv.org/abs/2607.06702)
  - **What it is:** Portfolio choice when assets are conditionally independent given a few observable drivers. Optimal policy splits into a static allocation along the conditioning geometry + a dynamic hedge for *predictable rotation of that geometry*; complexity scales with #drivers not #assets; a changing conditioning set creates unspannable risk (market incompleteness).
  - **Why it matters for trading:** Reframes intertemporal hedging around a low-dimensional driver manifold — a tractable route to multi-asset allocation when a handful of macro/factor drivers dominate. Same author as the order-three risk-attribution obstruction (2606.26835).
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (portfolio-theory reference)
- **Estimating the Stochastic Discount Factor from Option Prices and Predicting the Equity Premium** — Kenichiro Shiraya, Tomohisa Yamakami, Akira Yamazaki, Jul 2026 — [link](https://arxiv.org/abs/2607.08500)
  - **What it is:** Recovers the SDF from option prices and uses it to forecast the equity premium.
  - **Why it matters for trading:** Options-implied equity-premium timing is a classic but hard signal; worth a read for the recovery methodology, not an obvious standalone edge.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve

### Asset class / market (crypto & DeFi)
- **Causal Effects of Protocol-Fee Changes on Liquidity Provision in Automated Market Makers** — Wen-Ting Wang, Jul 2026 — [link](https://arxiv.org/abs/2607.08525)
  - **What it is:** A causal-inference study of how AMM protocol-fee changes shift LP behavior; companion to the same author's RL-execution-under-dynamic-fees DEX simulator (2607.10960).
  - **Why it matters for trading:** Directly relevant to DeFi LP/execution economics — continues the AMM-fee thread (Di Nosse/Lillo 2606.23070, Ghasemlu 2606.21769). Fee-timing over fee-level keeps recurring.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (DeFi LP reference)

## Backtest run this cycle
- **dow_seasonality on BTC-USD → REJECT** ([report](../../backtests/reports/2026-07-15-dow_seasonality-BTC-USD.md)). Daily-frequency test of Kim & Hansen's periodic-predictability theme (day-of-week = the daily clock's analogue of their intra-hour clock). Best grid pick (52-week look-back, long-flat) earns train Sharpe 0.32 → **OOS Sharpe −0.93** (CAGR −24%), fails deflated-SR (0.30). Confirms the boundary the paper draws — the periodicity is a high-frequency algorithmic artifact that aggregates away by the daily close; a REJECT here does **not** falsify Kim/Hansen. 7th consecutive daily BTC single-series signal to die OOS in this repo. Moves the program OFF the trend axis, as the 2026-07-04 capstone directed.

## New resources & tooling
- **Reinforcement Learning for Execution under Dynamic Fees in a Closed-Loop DEX Simulator** — Wen-Ting Wang — [link](https://arxiv.org/abs/2607.10960) — an RL execution testbed for AMM/DEX venues with fee feedback; a simulator to reuse rather than rebuild for DeFi execution studies.
- **tsbootstrap: Distribution-Free Uncertainty Quantification and Conformal Prediction for Time Series** — Sankalp Gilda — [link](https://arxiv.org/abs/2607.06690) — a time-series bootstrap / conformal-prediction library; useful for honest interval estimates and block-bootstrap Sharpe CIs in our own backtests.

## Watchlist updates
New players/authors worth adding to `watchlist.md`:
- **Peter Reinhard Hansen (UNC)** — econometrician; intraday/periodic return predictability & realized-volatility methods (Quarter-Hour Effect).
- **Alexander Barzykin (HSBC)** — electronic FX/OTC market making; RFQ pricing, reputation-feedback MM.
- **Ibrahim Ekren / Evangelos Nikitopoulos** — multi-asset Kyle equilibria under stochastic liquidity; optimal-transport methods in microstructure.
- **Anand Deo & Mantu Gupta** — extreme-value / generative rare-event simulation for stress laws (SS-GEN); tail-risk estimation.
- **Ciamac C. Moallemi (Columbia)** — market design / market making; prediction-market volatility structure.

## Open questions / threads to pull next run
- **Hourly track.** The two most credible crypto findings this window (2607.09426, 2607.09230) are structurally intraday — the daily pipeline can only falsify their daily shadows. Real replication needs an hourly/sub-hourly bar loader + an order-flow/imbalance proxy. Scope that as component upgrade #2.
- **Cross-sectional crypto.** Seven straight single-series daily BTC timing rejects. Jeon's "ETH > BTC" asymmetry suggests the daily edge, if any, is *relative-value* (BTC vs ETH vs alts), not single-series timing — a cleaner next daily backtest axis.
- **Novotny "Herding and Liquidity" Part I** — watch for Part II; the liquidity-stress crossover could join the crash-detection ensemble (Biancalana NLS, Deo SS-GEN) as a live early-warning panel.
- **Ceiling for next run:** highest ID seen this sweep = **2607.12990** (q-fin.CP, quantum CVA). Start the next recency window above it.
