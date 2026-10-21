# Quant Scout Digest — 2026-10-21

_14-day window since 2026-10-07. Swept arXiv q-fin TR/PM/ST/RM/CP for October 2026 IDs above the last ceiling **2610.08631** → top fresh ID this run **2610.28075**. All items below are verified to exist on arXiv (real IDs, titles, authors); numeric results are quoted only where an abstract was read, and flagged otherwise. Deduped against the INDEX ledger._

## TL;DR
- **The honest-evaluation thread gets its most concrete artifact yet — from live trading, not theory.** Vidovich & Zerjal "Where Backtests and Live Trading Part Ways" (2610.21846) ran one intraday US-equity system live, diffed it against a backtest replay, and catalogued **six specific defects** (a default feed carrying a fraction of true opening volume; dividend-adjusted history live orders never see; a live-only data download; a sizing step over the live account limit; UTC read as New-York time; config flags toggled but never reaching the order code) — none visible in summary statistics. This is the field manual for every reject this repo has logged.
- **Smerlak closes the loop on *why* our rejects reject (and anchors this week's backtest).** "Optimal Trading Filters and the Value of Predictive Signals" (2610.24558) proves via Wiener-Hopf factorization that the optimal policy is a forecast + explicit causal linear filter (= the Gârleanu-Pedersen aim-portfolio under exponential impact resilience); frictionless value depends only on instantaneous predictive strength, but **net-of-cost value depends on the *friction-weighted* forecast** — the filter prices a signal under costs, it does not create one.
- **Bouchaud pushes back on a clean derivation of the square-root impact law** (2610.10053, w/ Mastromatteo & Tóth): Bonart's diffusivity route gives the SRIL only if the market can whiten *each participant's whole stream* of metaorders and attribute trades to their issuers — "formidable and implausible"; isolated well-separated metaorders should then *not* obey SRIL, which the authors say the data does not support. Microstructure's cleanest law is still contested.
- **Zohren lands twice.** Attribution-propagation that turns portfolio-metric explanations into out-of-sample Sharpe gains *without retraining* (Liang/Zohren/Cucuringu 2610.15144), and a generative-LOB **market-impact benchmark** (2610.27100) measuring emergent impact in LOB generators.
- **Backtest: gp_aim on BTC-USD → MIXED** — the Gârleanu-Pedersen / Smerlak optimal filter (2610.24558). **Strongest OOS in 19 runs (Sharpe 0.404, CAGR +7.6%) and the first to CONFIRM a paper's mechanism in-sample** (the top-3 configs are all the optimal low-pass filter `phi=0.1`, beating naive full-chase `phi=1.0`), **but** it fails deflated-SR (0.65 full) and its full-sample Sharpe 0.656 trails BTC buy-and-hold 0.769 — the "edge" is a −12.5% MaxDD (vs B&H −76.6%), i.e. de-risked smoothing, not alpha. Confirms Smerlak; does not falsify "daily single-series is tapped out."

## Findings by focus area

### ML / AI for alpha
- **From Economic Explanation to Performance Improvement in Machine-Learning Portfolios** — Liang, Zohren, Cucuringu (Oxford-Man), 2026-10-10 — [2610.15144](https://arxiv.org/abs/2610.15144)
  - **What it is:** a local first-order attribution-propagation framework linking each feature's exposure in the allocation function to sensitivities of *sequential portfolio* metrics; ties propagated attributions to Shapley values defined on the portfolio objective and derives inference for **Sharpe-ratio attributions**. An attribution-guided intervention then adjusts feature exposures *post-training, without retraining*.
  - **Why it matters for trading:** turns "explainability" from a reporting afterthought into an OOS decision lever; the abstract reports statistically significant net-Sharpe gains across model classes (effect sizes not in abstract). A rare explanation→action loop.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read (method, then consider as an overlay on an existing ML allocator)
- **AlphaRLM: Aligning Language Models for Literature-Grounded Symbolic Factor Discovery** — Huang, Hong, Chen, Zhong, et al., 2026-10 — [2610.14959](https://arxiv.org/abs/2610.14959)
  - **What it is:** RL-aligned LMs that mine *symbolic* factors grounded in the research literature (not free-form generation), extending the LLM-alpha-mining lineage (QuantaAlpha → AlphaPADI).
  - **Why it matters for trading:** literature-grounding is the proposer-side answer to the "no paradigm dominates / honest-eval" findings — constrain the search to economically-motivated forms before the frozen referee judges.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** shelve (watch for code + an honest OOS eval)
- **Conflicting History in Foundation Model Return Forecasts** — Levent Bulut, 2026-10 — [2610.25822](https://arxiv.org/abs/2610.25822)
  - **What it is:** probes how time-series foundation models' return forecasts depend on (and conflict across) the history window they are shown — a direct successor to the "base-rate-honest benchmark guts fine-tuned FMs" thread (Cheung/Kwon, 07-15).
  - **Why it matters for trading:** more evidence that FM "forecast skill" is an artifact of conditioning/leakage; a must-read guardrail before trusting any FM return signal.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (methods/guardrail)
- **The Buffett Effect** — Smolinski, Saridevi, 2026-10 — [2610.17231](https://arxiv.org/abs/2610.17231)
  - **What it is:** an empirical "effect" paper (q-fin.ST) on the return signature associated with Buffett-style exposures/signals; title-level only this run.
  - **Why it matters for trading:** potential quality/value factor refinement; needs the abstract read to score the claim.
  - **Scores:** Novelty 2/5 · Credibility 2/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** read (verify the actual claim before any weight)

### Microstructure & execution
- **Optimal Trading Filters and the Value of Predictive Signals** — Matteo Smerlak, 2026-10-17 — [2610.24558](https://arxiv.org/abs/2610.24558) · **← this run's backtest anchor**
  - **What it is:** solves the stationary quadratic trading problem with transient impact via Wiener-Hopf factorization → optimal policy = conditional forecast + explicit **causal linear filter**. Exponential impact resilience ⇒ Gârleanu-Pedersen aim-portfolio; power-law decay ⇒ *fractional* filters needing memory finite-dimensional LQR cannot provide. Frictionless value depends only on instantaneous predictive strength; net value depends on the **mean square of the friction-weighted forecast**; for OU signals with power-law impact there is an *intermediate* optimal mean-reversion rate.
  - **Why it matters for trading:** the precise theory of *when a signal is worth trading after costs* — exactly the question under every one of this repo's cost-band / "the edge is not-trading" rejects.
  - **Scores:** Novelty 5/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** **backtested this run** (gp_aim · BTC-USD · MIXED — see below)
- **Where Backtests and Live Trading Part Ways: Six Defects from One Intraday System** — Vidovich, Zerjal, 2026-10-15 — [2610.21846](https://arxiv.org/abs/2610.21846)
  - **What it is:** a live-vs-replay post-mortem of one intraday US-equity system; six concrete data/code/config defects (see TL;DR) + a ten-point reconciliation checklist; makes **no** profitability claim.
  - **Why it matters for trading:** the practitioner complement to deflated-Sharpe — the divergences that kill a "validated" strategy live are plumbing, not statistics, and invisible in summary metrics. Fold the checklist into the backtest engine's data-integrity notes.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 5/5
  - **Next step:** read + adopt the checklist as an engine gate
- **On Bonart's interpretation of the Square-Root Impact Law** — Bouchaud, Mastromatteo, Tóth (CFM), 2026-10-07 — [2610.10053](https://arxiv.org/abs/2610.10053)
  - **What it is:** rebuts a diffusivity-based derivation of SRIL — it would require whitening *each participant's whole metaorder stream* and attributing trades to issuers ("formidable and implausible"); predicts isolated well-separated metaorders should violate SRIL, which the authors say the data does not support. (Companion: Bonart "Diffusive Market Impact," [2610.11691](https://arxiv.org/abs/2610.11691).)
  - **Why it matters for trading:** impact modelling sits under every execution cost estimate; the clean law is conditional on market structure, not universal — matters for anyone sizing by a √-impact cost model.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (theory; informs the engine's cost layer)
- **From Alpha to Execution: Trading Horizons, Regimes, and Schedules under Concave Impact and Hurst Scaling** — Kulkarni, Nayar, 2026-10-16 — [2610.23749](https://arxiv.org/abs/2610.23749)
  - **What it is:** optimal execution under concave power-law impact + Hurst-scaled cost envelope `w ∝ t^H`; interior horizon optimum exists only when duration-elasticity `a = β−H` and net urgency `ν` are both positive, else trade fastest/slowest; KKT schedule `φ ∝ (λ−w(t))₊^{1/β}` is front-loaded, saves 10–17% of envelope cost vs equal-duration TWAP. **Execution only — takes alpha as given, no signal rule** (hence not the backtest target).
  - **Why it matters for trading:** a clean, implementable schedule generator and a crisp "when is horizon even a free choice" condition; pairs with Smerlak's filter as the execution layer.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (execution layer; revisit when trading a real signal)
- **Neural Estimation of Irreversibility in Real and Simulated Limit Order Book Paths** — Yeo, Cha, Hwang, 2026-10 — [2610.16151](https://arxiv.org/abs/2610.16151)
  - **What it is:** learns a time-irreversibility measure on LOB paths (real vs simulated) — extends the crypto time-irreversibility thread (Kim/Cho/Lee 2608.10852) down to the order-book path level.
  - **Why it matters for trading:** irreversibility is the structural reason CSD/critical-slowing-down crash predictors failed here (cascade_warning REJECT); a learned estimator is a candidate regime/stress feature.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (needs LOB data)
- **Market Impact Estimation via Causal Foundation Models** — Thumm, Ying Chen, 2026-10 — [2610.12537](https://arxiv.org/abs/2610.12537)
  - **What it is:** estimates market impact with causal foundation models rather than parametric propagators.
  - **Why it matters for trading:** impact estimation is the input to any cost-aware sizing; a causal-FM approach is the counterpoint to the Bouchaud/Bonart parametric debate above.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

### Risk & portfolio
- **Conditional value-at-risk under a reward-penalty mechanism, with applications to robust portfolio management** — Cai, Mao (Tiantian Mao), Zhiqiao Song, 2026-10 — [2610.09246](https://arxiv.org/abs/2610.09246)
  - **What it is:** a CVaR variant under a reward-penalty mechanism for robust portfolio construction, from the Mao/Wang risk-measure-theory lineage already tracked here.
  - **Why it matters for trading:** continues the coherent-risk-measure thread (EVaR, weighted-VaR-superadditivity) — a robust objective for allocation under tail uncertainty.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read
- **E-Backtesting Expected Shortfall without Value-at-Risk Forecasts under Time-series Models** — Ruodu Wang, Jingcheng Yu, 2026-10 — [2610.17681](https://arxiv.org/abs/2610.17681)
  - **What it is:** anytime-valid **e-value** backtesting of Expected Shortfall that does *not* require a paired VaR forecast, under time-series models (ES was long thought not directly backtestable).
  - **Why it matters for trading:** an e-process ES backtest is the risk-measurement analogue of the frozen-referee / anytime-valid evaluation thread (Qu/Chen 09-30) — a sequentially-valid risk gate.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (evaluation methods)
- **Regime-Aware Interpretable Ranking for Sector Rotation** — Koa, Liu, Li, Feng, et al., 2026-10 — [2610.26456](https://arxiv.org/abs/2610.26456)
  - **What it is:** interpretable, regime-conditioned cross-sectional *ranking* for sector rotation, from tracked player Kelvin Koa (self-evolving symbolic discovery lineage).
  - **Why it matters for trading:** cross-sectional ranking is the axis this repo is blocked on for crypto (daily single-series is exhausted); a clean regime-aware ranker is a template to port once a multi-asset feed exists.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (cross-sectional; blocked on multi-asset data)
- **Regime Detection in Latent Factor Models — A Bayesian Decision-Theoretic Approach** — Karl Kristian Engelund, 2026-10 — [2610.20366](https://arxiv.org/abs/2610.20366)
  - **What it is:** casts regime detection in latent-factor models as a Bayesian decision problem (loss-aware, not just likelihood-aware) — kin to the BOCPD-on-order-flow thread (Jebali 2609.07989).
  - **Why it matters for trading:** regime detection is the one component that has survived every reject here as a secondary (crash-insurance) effect; a decision-theoretic framing is the right way to make it load-bearing.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read
- **Deep catastrophic-risk-aware reinforcement learning** — Pérez, Mendoza, Godin, 2026-10 — [2610.27214](https://arxiv.org/abs/2610.27214)
  - **What it is:** RL with an explicit catastrophic-/tail-risk-aware objective (distortion/CVaR-style) in the reward.
  - **Why it matters for trading:** the RL counterpart to the coherent-risk-measure thread; directly relevant to drawdown-controlled allocation.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

### Asset class / market (crypto, derivatives)
- **Market Efficiency in a Changing Asset Population: Mobility, Entry, and Survival over Cryptocurrency's Full History** — Ballis, Ioannidis, 2026-10 — [2610.23283](https://arxiv.org/abs/2610.23283)
  - **What it is:** studies efficiency across the *entire surviving-and-dead* crypto universe (entry/exit/mobility), not a survivorship-biased panel.
  - **Why it matters for trading:** survivorship bias is the silent killer of crypto cross-sectional backtests; a full-population efficiency map calibrates how much apparent alpha is survivorship.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** read (data-hygiene reference for the eventual multi-coin loader)
- **GROMM: Generative Risk-neutral Option Market Models** — Wiese, Buehler, Horvath, 2026-10 — [2610.16732](https://arxiv.org/abs/2610.16732)
  - **What it is:** generative, arbitrage-aware risk-neutral *option-market* models (full surface dynamics), from the deep-hedging / differentiable-IV lineage already tracked.
  - **Why it matters for trading:** the generator needed to stress-test and train option-hedging policies; connects to the ETH-options-lab exploration.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (options infra)
- **A GLE-LSV model with state-dependent leverage and colored noise** — Andrey Itkin, 2026-10 — [2610.18706](https://arxiv.org/abs/2610.18706)
  - **What it is:** a generalized-Langevin-equation local-stochastic-vol model with state-dependent leverage and colored noise — continues Itkin's "Beyond Rough Volatility" GLE program (2609.20293) that explained this repo's two long-memory-vol nulls.
  - **Why it matters for trading:** the GLE decoupling of memory from scaling is the theory under volterra_signal / asym_longmem_vol — a real-but-non-tradable vol-memory channel.
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 2/5 · Actionability 1/5
  - **Next step:** shelve (derivatives theory)
- **Algorithmic Collusion Without Deterrence: Auditing the Punishment Mechanism in Q-Learning Pricing Agents** — Lopes de Moraes, De-Losso, 2026-10 — [2610.21867](https://arxiv.org/abs/2610.21867)
  - **What it is:** audits *why* Q-learning pricing agents sustain collusive prices — the punishment mechanism — finding collusion without genuine deterrence. Pairs with Campajola RL-execution collusion (2610.00619, last run).
  - **Why it matters for trading:** the "learned collusion / correct-reward-is-not-enough" diagnosis is a standing caution for any RL execution/market-making agent.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** read (RL-agent caution)
- **Agentic AI in Automated Markets** — Irene Aldridge et al. (33 authors), 2026-10 — [2610.22522](https://arxiv.org/abs/2610.22522)
  - **What it is:** a large-team survey/framework on agentic AI operating in automated markets, from tracked player Aldridge.
  - **Why it matters for trading:** maps the agentic-market landscape; mostly orientation, low direct actionability.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 2/5 · Actionability 1/5
  - **Next step:** shelve

## Backtest run this cycle
- **gp_aim · BTC-USD → MIXED** (anchored to Smerlak 2610.24558). New strategy `gp_aim` = the Gârleanu-Pedersen aim-portfolio / Smerlak optimal linear filter: EWMA-momentum forecast → vol-normalized Markowitz target → **partial-adjustment low-pass filter** with trade rate `phi` (`phi=1` naive full-chase control, `phi<1` the optimal filter). Real cached BTC-USD (2922 bars). **Train Sharpe 1.093 (span=40, phi=0.1) → OOS Sharpe 0.404, CAGR +7.6%** — the strongest OOS in 19 runs. **First-ever in-sample confirmation of an anchored paper's mechanism:** the stage-1 top three are all `phi=0.1` (optimal filter), beating the `phi=1.0` controls at ranks 4–5 — the low-pass filter genuinely adds value (≈0.15 Sharpe + ~6× less turnover + −12.5% MaxDD). **But it fails deflated-SR (full 0.648) and does not beat buy-and-hold** (gp_aim full Sharpe 0.656 / CAGR 5.6% / MaxDD −12.5% vs BTC B&H **0.769 / 32.5% / −76.6%**, reconciled by direct computation). The Sharpe is low-exposure *smoothing*, not alpha — exactly Smerlak's thesis (the filter prices a signal under costs; it does not manufacture one). Confirms Smerlak; does **not** falsify "daily single-series is tapped out." Report: [2026-10-21-gp_aim-BTC-USD.md](../../backtests/reports/2026-10-21-gp_aim-BTC-USD.md).

## New resources & tooling
- **4Cast Lab** — open-source app for ML & statistical analysis (Gogas), [2610.16800](https://arxiv.org/abs/2610.16800) — a GUI/toolkit for forecasting + stats workflows.
- **LOB-Impact Benchmark** — emergent market impact in generative LOB models (Nigmatulin, …, Zohren), [2610.27100](https://arxiv.org/abs/2610.27100) — a benchmark to check whether a generative LOB reproduces realistic impact (quality gate for synthetic-LOB training data).
- **CorrFlow** — exact, permutation-equivariant flow matching on the correlation elliptope (Gautier Marti), [2610.13606](https://arxiv.org/abs/2610.13606) — generates valid correlation matrices; useful for covariance-cleaning / scenario simulation.
- **AuDQ** — auditable data quality via agentic rule discovery (BlackRock-adjacent authors), [2610.26031](https://arxiv.org/abs/2610.26031) — automated data-integrity rule mining; pairs directly with the Vidovich/Zerjal backtest-vs-live checklist.

## Watchlist updates (new players/sources to add)
- **Matteo Smerlak** — optimal trading filters / Wiener-Hopf conversion of forecasts to positions under transient impact; the theory of *the value of a signal after costs* (anchor of this run's backtest).
- **Alex Vidovich & Zivana Zerjal** — practitioner honest-negatives; backtest-vs-live reconciliation, data/code/config defect taxonomies.
- **Julius F. Bonart** — diffusive market impact; the SRIL-from-diffusivity program Bouchaud et al. engage with.
- **Minkey Chang** — amortized neural filtering for calibrated posteriors in statistical arbitrage ([2610.25802]).

## Open questions / threads to pull next run
- **The one unblock, now ~8× overdue: an hourly / multi-coin OHLCV loader.** gp_aim this run is the sharpest case yet — even the *mathematically optimal* cost-aware filter finds no daily return signal, only a better exposure dial. The GP/Smerlak filter is the right *implementation* layer to carry onto an intraday feed where short-horizon persistence actually lives (Kitron-Wengrowicz 15-min reversal, quarter-hour effects, Koa cross-sectional ranking).
- **Adopt the Vidovich/Zerjal 10-point checklist as an engine data-integrity gate** — low effort, directly hardens every future backtest.
- **Smerlak's fractional filter under power-law impact** needs memory finite-dimensional LQR cannot provide — a concrete reason fixed-lag strategies underperform; worth a dedicated fractional-filter test once there is a signal with genuine long persistence.
- **Did Smerlak run any empirics?** The abstract is theory-only (OU signals); if the full text has a calibrated example, it would sharpen the gp_aim mapping — check the PDF next run.
