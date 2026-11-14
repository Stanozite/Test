# Quant Scout Digest — 2026-11-14

10-day window since 2026-11-04. Swept the fresh November batch above the prior ceiling (2611.05310) across q-fin.TR / PM / ST / CP / RM `/2026-11` plus the finance-applied cs.LG / cs.AI / econ.EM cross-lists — a heavy run (submissions out to 2611.17xxx). The **honest-evaluation thread lands its two sharpest artifacts yet** (a *bounded* LLM research loop that reports every failure; an analytic exploit of moving deflation *inside* the search loop), **the square-root/propagator-impact debate gets a no-go theorem from a tracked physicist (Kanazawa)**, and a practitioner trio (ReSolve-style Butlers) ships **two genuinely tradable global-futures factors** — the first after-cost-positive directional findings in weeks, both cross-sectional/multi-asset. Crypto's own tradable signals remain sub-daily (wallet identity, 5-min realized measures). The backtest anchor is a crypto-native negative: Baquero & Menezes show BTC's power-law trend is **not statistically identifiable** under persistent noise.

## TL;DR
- **"Hard to Fool" (Henry Zhang, 2611.06607)** — a *bounded* agentic quant-research loop (model proposes strict JSON, only trusted code decides; hash-chained ledger, single-use holdout): across ~two dozen campaigns, almost everything fails, and an LM survivor at **Sharpe ≈3 in validation collapses to 0.26 on its one holdout use**. The loop's value is "how hard it makes false reporting," not what it finds.
- **Gençay "Can a search hold its own bar?" (2611.14539, tracked player)** — moving the deflated-Sharpe correction *inside* the LLM search loop creates a new exploit (**variance dilution**: near-duplicate mediocre candidates lower the bar); gated search reports **no certifiable discovery in 36/37 runs** vs 16/16 for ungated, 100 nominal trials ≈ 6–8 independent streams.
- **Kanazawa et al no-go theorem (2611.10574)** — asymptotic price-impact decay is **not identifiable by propagator estimation**: Wiener-Hopf deconvolution under long-memory flow forces the inferred kernel to be transient and "fine-balance"-tuned *even when true impact is permanent* → fitted propagator decay is an estimation artifact; the square-root law is compatible with permanent impact.
- **Butler et al "Global Seasonality Factor Investing" (2611.15657, tradable)** — five calendar seasonality anomalies across bond/commodity/equity futures; **slow patterns (day-of-year, day-of-half-year) are net-positive after costs**, fast ones die on turnover; an ensemble lifts a global factor portfolio's OOS Sharpe ~30%, largely uncorrelated with carry/momentum/skew.
- **Backtest: `powerlaw_trend` on BTC-USD → REJECT.** New strategy fading the deviation from a log(price)~log(days-since-genesis) corridor (the Santostasi/Baquero-Menezes object). Barely an in-sample edge (train Sharpe **0.393**) → **OOS −0.343, CAGR −10.9%**, full **−0.255 / CAGR −18.5% / MaxDD −93.3% / deflated-SR 0.003**; the short leg (shorting "rich" vs the corridor = shorting BTC's up-drift) is ruinous, and tighter bands are monotonically worse. Trails BTC B&H (0.639 / 21.4% / −76.6%) on every axis. **Confirms, not falsifies** Baquero & Menezes (2611.13962): the power law is not identifiable and reversion-to-trend "cannot be decided," so a corridor-reversion trade has no edge. **21st straight daily-crypto non-advance** — a genuinely new trend object still fails; the blocker is data *resolution*, not the model.

## Findings by focus area

### ML / AI for alpha

- **Hard to Fool: A Bounded LLM Research Loop for Quantitative Finance** — Henry Zhang, 2026-11-04 — [2611.06607](https://arxiv.org/abs/2611.06607)
  - **What it is:** An open-source "Autonomous Quant Researcher" built on the reverse of the usual agentic loop — the model proposes changes as strict declarative JSON over a fixed vocabulary (no model-written code to sandbox), and **only immutable trusted code decides**. Acceptance requires a *conjunction* of absolute gates (positive net-of-cost P&L, positive bootstrap lower bound on weekly clusters, survival at elevated costs, per-year stability, sample-size floors) on chronologically split discovery/validation/**single-use** holdout data, with every proposal/refusal/crash/result in a hash-chained append-only ledger. ~Two dozen campaigns: 0DTE, overnight SPX verticals, daily ETF rules, TA premises, Kalshi crypto binaries, earnings options, off-exchange volume, alt-data.
  - **Why it matters for trading:** The most complete *practitioner* instantiation of the honest-evaluation thread (Gençay / Benhamou / Giesecke). Headline cautionary tale: an LM strategy passed discovery+validation at Sharpe ≈3, then **fell to 0.26 on its one holdout use** — exactly the deflation-gate failure mode. Only two survivors across all campaigns. Mirrors this repo's own 20-straight-non-advance record.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read (adopt the single-use-holdout + conjunction-of-gates discipline into the backtest pipeline's own verdict logic)

- **Can a search hold its own bar? In-loop deflation and its exploits** — Eray Gençay, 2026-11 — [2611.14539](https://arxiv.org/abs/2611.14539)
  - **What it is:** Tracked player; direct successor to his 2608.27734 / honest-eval line. Asks what happens when the deflated-Sharpe correction moves *inside* the LLM search loop (threshold tied to the running count + dispersion of the search's own trials). Shows analytically the search can game its own bar via **variance dilution** (near-duplicate mediocre candidates shrink dispersion faster than the trial-count penalty grows). Defenses: a pre-registered variance floor + a monotone high-water-mark bar. 53 audited searches ×100 candidates: gated reports **no certifiable discovery in 36/37**, ungated in **16/16**, every arm's OOS CI includes zero; 100 nominal trials ≈ **6–8 effectively independent** streams; state-based stopping matches at ~1/12 the budget.
  - **Why it matters for trading:** Quantifies that a nominal "100 backtests" is ~6–8 real bets — a direct discipline for any LLM-agent alpha pipeline, and the reason ungated agentic search always "finds" something.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read

- **Tabular Foundation Models in Financial Predictions** — Ed deHaan, Allen H. Huang, 2026-11-10 — [2611.13550](https://arxiv.org/abs/2611.13550)
  - **What it is:** Introduces tabular foundation models (Google Research's TabFM) to financial/accounting prediction — pretrained on *synthetic* tabular data (no memorized firm outcomes → no look-ahead), learns in-context with no fine-tuning. On next-year earnings-change prediction it beats a fine-tuned open-weight LLM and several tree models on accuracy, faster and cheaper than the LLM (though some trees predict faster).
  - **Why it matters for trading:** A credible, leakage-safe challenger to gradient boosting for cross-sectional tabular signals; the synthetic-pretraining angle sidesteps the memorization critique that dogs LLM-as-forecaster work. Single-task so far.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (watch for a cross-sectional-returns benchmark)

- **Also (lighter):** **Honest Small Decision Models for Finance** (Ajitabh Kumar, 2611.03755) — scale/specialization-collapse + mixed-corpus remediation, honest-eval adjacent; **Diversification Across Predictors** (Danning Li, 2611.12389) — heterogeneous ensemble learning for cross-sectional return prediction; **Point-in-Time Encoders for Earnings Calls** (Alessio Brini, 2611.14325) — leakage-safe PiT text encoders; **CosmosAlpha** (Wang et al, 2611.04555) — Pareto-guided multi-relational graph search alpha mining (proposer-side; captured 11-04 as a related ID); **FINCOSMOS** (Cao et al, 2611.07464) — open-world agent-in-finance evaluation paradigm.

### Microstructure & execution

- **Is price-impact decay statistically identifiable by propagator estimation?** — Shunta Fujiwara, Yuki Sato, Kiyoshi Kanazawa, 2026-11-07 — [2611.10574](https://arxiv.org/abs/2611.10574)
  - **What it is:** A **no-go theorem** (Kanazawa — tracked econophysicist). Market-order flow has long memory yet prices stay diffusive (the "diffusivity puzzle"); the propagator model explains it by impact that *decays* and is finely balanced against flow memory, and fitted propagators seem to confirm this. The authors prove via Wiener-Hopf deconvolution under long-memory flow that **asymptotic impact decay cannot be identified**: the inferred propagator is *necessarily transient even when true impact is permanent*, and decays with a "fine-balance" exponent set by order-flow autocorrelation alone. An exactly-solvable null with *strictly permanent* impact (keeping order-splitting + the square-root law) still yields a fine-tuned inferred decay.
  - **Why it matters for trading:** Guts a load-bearing empirical claim in execution cost modeling — fitted propagator decay is a deconvolution artifact, not evidence that impact decays, so transient-impact cost models (and the aim-portfolio/`gp_aim` resilience assumption) rest on an unidentified kernel. Pairs directly with the 2610.10053/11691 Bouchaud-vs-Bonart exchange; the square-root law is shown compatible with *permanent* impact.
  - **Scores:** Novelty 5/5 · Credibility 5/5 · Relevance 4/5 · Actionability 2/5
  - **Next step:** read

- **Does a Trading Policy Need to Know What It Trades? Microstructure Invariance and Zero-Shot Transfer** — Hieu Tran, Hong Yu, 2026-11-05 — [2611.08701](https://arxiv.org/abs/2611.08701)
  - **What it is:** Trains execution policies (wait-in-queue vs cross-the-spread) *once* on 954 stocks (2019, exact order-by-order Nasdaq replay), then evaluates them unchanged on 1,964 unseen stocks (2020–21), 2,629 stocks (2025–26), crypto pairs, and a second exchange. A policy seeing a stock only through normalized microstructure features (trade rate, size, spread, tick) performs within **0.015 spreads/share** of one trained on that very stock — the stock's own history "adds nothing." But invariant units beat raw units/z-scores by **<1 bp**, no representation generalizes to **unseen spread regimes**, and the authors warn a near-zero pooled-comparator transfer gap is weak evidence a representation is correct.
  - **Why it matters for trading:** Strong evidence that a *single* execution policy can be deployed zero-shot across assets/venues/epochs via Kyle-style microstructure invariance — a real engineering win — balanced by an honest ceiling (the invariant normalization's marginal value is tiny and spread-regime transfer is unsolved).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read

- **Risk-Sensitive RL for an Options Market Maker: Empirical Study with Real S&P 500 Options** — J. Chen, Cheng, **John Hull**, Li, Poulos, Shi, Veneris, Wang, 2026-11-07 — [2611.10956](https://arxiv.org/abs/2611.10956)
  - **What it is:** A distributional TD3 hedging agent trained on 1996–2017 real SPX options, tested OOS 2018–2023 against delta hedging, hedge-ratio rules, and the *same agent trained in simulators* (GBM / SABR / Black-Scholes-on-historical-paths). Empirically-trained agent cuts CVaR tail loss **3.1%** vs delta hedging (**8.9%** in volatile falling markets) and beats every simulator-trained variant — but the gain **reverses to a 7–10% cost in rising markets** (it learns a state-dependent short-net-delta tilt), and the evidence rests on a single test path.
  - **Why it matters for trading:** Clean apples-to-apples demonstration that *training distribution* (empirical vs simulated) is the dominant lever for RL hedging, with honest regime-conditionality — the deep-hedging negative-result lineage (Kumar 2608.29025) now with a conditional positive.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

- **Also (lighter):** **Deep Learning for Operator Maps in Optimal Liquidation** (Donnelly et al, 2611.14245); **Optimal execution in a fractional setting with RL** (Garcin/Pu/Verrier, 2611.11373); **Fine-Tuning an Order-Flow Foundation Model for Sub-Second Forecasting** (Shabashev, 2611.14117); **Towards Robust RL Market Making: Lessons from Loss-Function Experimentation** (Nand/Guney, 2611.09012); **Optimal Trading Speed on Blockchain** (Jia/Yu, 2611.13616, crypto execution); **Price-Volume Correlations Are Always Zero** (Olkhov, 2611.08528 — provocative identity-level claim that price-volume correlation is definitionally zero under his framework).

### Risk & portfolio

- **Global Seasonality Factor Investing** — Andrew Butler, Adam Butler, Maciej Zawadzki, 2026-11-11 — [2611.15657](https://arxiv.org/abs/2611.15657)
  - **What it is:** Documents **five** calendar-seasonality anomalies (day-of-week → day-of-year) that jointly appear across bond, commodity, and equity futures, modeled nonlinearly *per market*. Walk-forward OOS splits cleanly by speed: **fast patterns (day-of-week, day-of-month) are strong gross but negative after costs** (turnover); **slow patterns (day-of-quarter/half-year/year) are positive gross and — except day-of-quarter — positive net.** An equal-weight ensemble has an OOS Sharpe competitive with and largely uncorrelated to global carry/momentum/skew; adding it lifts a global factor portfolio's OOS Sharpe **~30%**.
  - **Why it matters for trading:** A rare after-cost-positive *directional* factor finding, incremental to the standard global-futures factor set, with an honest fast-vs-slow cost boundary — the kind of multi-asset futures overlay a systematic book can actually run. (The exact Sharpes/sample/cost assumptions need the full PDF.)
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest (slow-seasonal overlay — but needs the multi-asset global-futures panel this repo still lacks)

- **Idiosyncratic Market Effects in Global Time Series Momentum** — Andrew Butler, Maciej Zawadzki, Adam Butler, 2026-11-11 — [2611.15646](https://arxiv.org/abs/2611.15646)
  - **What it is:** Extends Moskowitz-style nonlinear TSMOM: instead of one global nonlinear factor model, fit the momentum→forward-return response *market by market*. Per-market response curves are "distinct from the global model," and despite much smaller samples, market-by-market nonlinear fits give a small but robust OOS improvement.
  - **Why it matters for trading:** The companion to the seasonality paper — says the momentum response is idiosyncratic, not universal, so a single global TSMOM curve under-fits. Relevant to this repo's six rejected single-series trend tests (the daily-BTC curve is one idiosyncratic market, not the global one).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (multi-asset; single-series TSMOM already rejected)

- **The Logic of Factor Portfolios: Boolean Rules, Interactions, and Trading Costs** — Ziyao Wang, Svetlozar T. Rachev, Frank J. Fabozzi, 2026-11 — [2611.09834](https://arxiv.org/abs/2611.09834)
  - **What it is:** Tracked players (Rachev/Fabozzi). Recasts factor portfolio construction as **Boolean rules over factor signals** with explicit interaction terms and trading-cost penalties — an interpretable, rule-based alternative to linear factor weighting.
  - **Why it matters for trading:** Rule-logic factor combination is directly implementable and cost-aware; interaction terms capture the nonlinearity the Butler papers also chase, in a transparent form.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve

- **Also (lighter):** **Dynamic Scenario-Based Portfolio Optimization for Multi-Asset ETFs** (Mensah/Rachev/Fabozzi, 2611.16540); **Conformal Risk Certificates for Portfolio Optimization — Gated RL** (Zarei et al, 2611.14699) + sibling **Safe Portfolio Learning from Untrusted Predictions** (MohammadpourAzari et al, 2611.04826, signed-trust/abstention); **Diversified-Risk-Perception Risk Measures** (Yang Liu et al, 2611.11803); **Robust distortion riskmetrics over Bregman-Wasserstein balls** (Peng Liu/Vanduffel/Bernard, 2611.04021 — captured 11-04); **Interpretable Allocation & MPC Rebalancing** (Varner, 2611.03022).

### Asset class / market (crypto & derivatives)

- **Deceleration without identification: a power-law trend in Bitcoin prices under persistent noise** — Carlos Baquero, Raquel Menezes, 2026-11-10 — [2611.13962](https://arxiv.org/abs/2611.13962)  *(this run's backtest anchor)*
  - **What it is:** A pre-registered, publicly-hashed test of whether BTC's price follows a log(price)~log(age-since-genesis) **power law**. Verdict is a careful negative: constant drift is rejected only *fragilely* (survives once persistence beyond a random walk is allowed), the log-age exponent **~5.7** is not rejected but not identified, a **Gompertz ceiling fits about as well** (the data do not single out the power law), and **"reversion to trend cannot be decided."** A good log-log fit / high R² is weak evidence because random-walk-like deviations manufacture trends. No trading claim; forecasts registered for 2027–2030.
  - **Why it matters for trading:** Directly adjudicates the popular retail "Bitcoin power-law corridor" (Santostasi) timing model and the Molnar "runs on a clock" lineage (`halving_clock`, 08-05): if the trend is unidentifiable and reversion undecidable, a corridor-reversion timing rule should carry no reliable edge.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest *(done this run — `powerlaw_trend` on BTC-USD → **REJECT**: train Sharpe 0.393 → OOS −0.343, full −0.255 / MaxDD −93.3% / deflated-SR 0.003, the short leg ruinous; confirms non-identifiability — the corridor-reversion trade has no edge)*

- **AFNO: Universal Certifiably-Arbitrage-Free Operator Learning for European Call-Price Surfaces** — Kratsios, Limmer, **Buehler, Horvath**, Saqur, 2026-11 — [2611.12899](https://arxiv.org/abs/2611.12899)
  - **What it is:** Tracked players (Buehler/Horvath). A neural operator for call-price surfaces that is **arbitrage-free by construction** (maps an RKHS input to convex combinations of arbitrage-free surfaces via a continuous nearest-neighbour solve), plus a negative result: a *nearest* arbitrage-free correction to an unconstrained surface may not exist, so post-hoc projection can't restore no-arbitrage — standard FNO/encoder-decoder NOs can emit arbitrage-violating prices that produce negative PnL downstream.
  - **Why it matters for trading:** A fast surrogate for option-surface pricing with a built-in no-arbitrage guarantee — removes a real failure mode (negative-PnL from arbitrageable model prices) in risk/vol trading systems.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve

- **Neural Realized Measures: Forecast-Supervised Intraday Aggregation for Volatility Forecasting** — Brian Sing Fan Chan, Jennifer So Kuen Chan, 2026-11-05 (ICAIF 2026) — [2611.07287](https://arxiv.org/abs/2611.07287)
  - **What it is:** Learns the intraday-aggregation weights of a realized measure *from the forecast objective* (positive, mean-normalized, context-dependent weights; uniform weights exactly recover the raw realized measure — so the classical RM is a special case). On **six crypto assets at 5-min**, NRM improves QLIKE in **all 54 paired OOS comparisons** (mean gains 7–9% over the raw RM under SF/HAR/MIDAS); Heston simulations confirm lower RMSE.
  - **Why it matters for trading:** A drop-in, interpretable upgrade to the realized-vol input that every vol-gate/vol-target overlay consumes — and it is validated *on crypto 5-min data*, the exact intraday resolution this repo's backtests keep being blocked from.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (needs the 5-min feed; natural companion to the pending intraday loader)

- **The End-of-Day Reversal After 2019: A Pre-Registered Test on S&P 500 Stocks** — Alex Vidovich, Zivana Zerjal, 2026-11-06 — [2611.09286](https://arxiv.org/abs/2611.09286)
  - **What it is:** Tracked players (the backtest-vs-live defect-taxonomy pair). Pre-registered out-of-sample test of Baltussen-Da-Soebhag's last-half-hour reversal (prior-session losers beat gainers), S&P 500 ex-~80 heavily-traded names. Dollar-vol-weighted reversal is **3.13 bps/day (t=7.5) in 2016–19** and **3.05 bps (t=3.0) in 2023–26**, but **~0 in 2020–22** and **1.69 bps (t=2.3) from 2020 on**; on the full index it falls 3.40→0.74 bps (change t=−1.83, short of the pre-registered −3 bar). **Gross only — makes no claim net of costs, proposes no strategy; no mechanism test passes.**
  - **Why it matters for trading:** A model of pre-registration discipline (private reproduction of the published sign before computing outcomes) on a real microstructure anomaly — the effect is window-dependent and much smaller on the liquid index, i.e. not obviously tradeable after costs.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (gross-only, equities, sub-bp)

## New resources & tooling
- **Autonomous Quant Researcher** — open-source bounded LLM research loop with hash-chained ledger + single-use holdout (Zhang, 2611.06607) — the reference implementation of a fraud-resistant discovery pipeline.
- **FINCOSMOS** (2611.07464) — open-world evaluation paradigm for finance agents; **JUBILEE** (2611.10972) — off-policy-evaluation benchmark environment for debt collections; **RiskReason** (2611.01236, captured 11-04) — verifiable financial-risk-reasoning benchmark.
- **TabFM-for-finance** harness (deHaan/Huang, 2611.13550) — synthetic-pretrained tabular foundation model applied to earnings-change prediction (leakage-safe baseline).

## Watchlist updates
New players/authors worth tracking, added to `watchlist.md`:
- **Kiyoshi Kanazawa (Kyoto) + Shunta Fujiwara / Yuki Sato** — econophysics microstructure; propagator/impact *identifiability* no-go theorems (diffusivity puzzle, square-root law under permanent impact).
- **Henry Zhang** — bounded agentic quant-research loops; conjunction-of-gates + single-use-holdout honest evaluation (Autonomous Quant Researcher).
- **Andrew Butler / Adam Butler / Maciej Zawadzki** — practitioner global-futures factor research (idiosyncratic nonlinear TSMOM, global seasonality factor); after-cost-honest walk-forward.
- **John Hull / Zissis Poulos / Andreas Veneris (Toronto)** — RL options market making / hedging on real SPX options; training-distribution effects.
- **Hieu Tran / Hong Yu** — microstructure-invariance zero-shot transfer of RL execution policies.
- **Anastasis Kratsios** — certifiably-arbitrage-free neural operators for option surfaces (with Buehler/Horvath).
- **Ed deHaan / Allen H. Huang** — tabular foundation models for financial/accounting prediction.
- **Carlos Baquero / Raquel Menezes** — pre-registered identifiability testing of BTC power-law / long-run trend claims.
- **Brian Sing Fan Chan / Jennifer So Kuen Chan** — forecast-supervised learned realized measures (neural RM).

## Open questions / threads to pull next run
- **The intraday/multi-coin loader is now the single highest-leverage unblock, ~10× overdue.** Three findings *this run alone* live at a resolution the daily cache can't reach: Neural Realized Measures (crypto 5-min), wallet-identity return prediction (ms-grid, captured 11-04), and the Butler seasonality/idiosyncratic-TSMOM factors (multi-asset global-futures panel).
- **Adopt the "Hard to Fool" conjunction-of-gates + single-use-holdout and Gençay's variance-floor** into this repo's own verdict logic — the backtest pipeline currently uses deflated-SR as a single gate, which both papers show is necessary-not-sufficient and gameable in a search.
- **The Kanazawa no-go theorem undercuts the transient-impact assumption** behind the `gp_aim` filter (2610.24558): if impact-decay is unidentifiable, the exponential-resilience/aim-portfolio resilience parameter is fit to an artifact. Worth a note when that filter is carried onto an intraday feed.
- **Butler's "idiosyncratic market effects"** reframe this repo's six single-series trend rejects: daily-BTC is one idiosyncratic momentum curve, not the global one — a cross-sectional multi-coin panel (still blocked) is where the nonlinear per-market fit could pay.

Next ceiling: 2611.17170
