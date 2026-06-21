# Quant Scout Digest — 2026-06-21

_Window: items newer than the 2026-06-20 run. Sunday window is thin — the latest
arXiv q-fin batch is Fri 19 Jun, and the strongest 19-Jun items were already
captured yesterday (Schmidhuber lattice-gas, Portnaya prediction-markets,
DeXposure-Claw, ensemble anomaly detection). This run harvests the verified
16–17 Jun residue those sweeps left behind, plus the freshest ML/alpha-method
and agentic-risk work._

## TL;DR
- **Novelty ≠ discovery (Li Xia):** a geometric theory shows LLM-guided factor search only beats generic search in *weakly-represented but target-aligned* directions — random orthogonal exploration widens coverage with zero yield. A diagnostic for when to spend on LLM alpha mining.
- **Vision-LLMs can't actually read candlesticks (Ziyao Wang):** a martingale-null benchmark shows commercial + open VLMs assign chart evidence coefficients near zero or *opposite* the rule-implied sign — they trend-extrapolate, they don't see the chart. Hard caution for chart-image alpha.
- **Epps effect decomposed (Angstmann/Gebbie, tracked players):** correlation emergence across two coupled limit-order books resolves into three mechanisms — async event clocks, finite coupling response, and their interaction. Microstructure foundation for cross-asset lead-lag estimation.
- **Agentic-AI model risk gets a VaR (Dixon):** treat the LLM as a noisy observation model in a POMDP, run Bayesian belief filtering, and read out posterior entropy, calibration error, and a belief-driven VaR — auditable model risk for autonomous trading agents.
- **Microsecond, error-bounded option pricing (van den Berg):** a mixture-density-network surrogate prices GJR-GARCH options arbitrage-free in microseconds with a *distribution-free error bound* (OOS CDF error 1.4e-4). Replaces Monte Carlo for vol-surface/Greeks at scale.

## Findings by focus area

### ML / AI for alpha
- **Discovery under Hypothesis Redundancy: A Geometric Theory of Discovery Bottlenecks** — Li Xia, Baoxun Wang, 12 Jun 2026 (cs.LG / cs.AI / q-fin.PM) — [link](https://arxiv.org/abs/2606.14386)
  - **What it is:** A "Search Compression Hypothesis" giving three geometric conditions under which hybrid discovery (local search + LLM proposals) succeeds: spectral compression, orthogonal escape from the explored span, and residual alignment with the target signal. Gains vanish once the hypothesis space reaches full rank.
  - **Why it matters for trading:** Direct theory for LLM-driven factor/alpha mining (the QuantaAlpha / AlphaPROBE line). It says *when* directed LLM exploration pays — only in under-represented, target-bearing directions — and when it is wasted compute. A go/no-go diagnostic before throwing an LLM at factor discovery.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** read — use the rank/alignment diagnostics to gate the existing alpha-mining harness.
- **Martingale Doppelgänger-Eval: An Identification Framework for Auditing Candlestick Understanding in Vision-Language Models** — Ziyao Wang, 16 Jun 2026 (q-fin.CP) — [link](https://arxiv.org/abs/2606.17423)
  - **What it is:** A benchmark that isolates whether VLMs actually read candlestick charts vs. trend-extrapolate, using martingale-null markets and trend-label swaps. Finding: across commercial and open models, evidence coefficients are ~zero or opposite the rule-implied sign.
  - **Why it matters for trading:** Hard caution against any pipeline feeding chart *images* to a VLM for signal. The models look at the trend label, not the bars. Validates a numeric/structured-feature path over screenshot-to-LLM.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve chart-image VLM ideas; reuse the martingale-null protocol to audit any internal model.

### Microstructure & execution
- **Correlation emergence and the Epps effect in two coupled limit order books** — Chris Angstmann, Tim Gebbie, 12 Jun 2026 (q-fin.TR / q-fin.ST) — [link](https://arxiv.org/abs/2606.14182)
  - **What it is:** A discrete order-flow random walk (creation/cancellation/diffusion) with pair-trader coupling at order creation, taken to coupled reaction–diffusion equations with a moving transaction-price boundary. Yields closed-form realized correlation vs. aggregation time; the Epps effect arises from three mechanisms — asynchronous event clocks (subordination), finite coupling response time, and their interaction.
  - **Why it matters for trading:** Mechanistic model of why measured cross-asset correlation collapses at high frequency. Directly informs sampling-frequency choice and lead-lag / pairs estimation, and extends this duo's reaction–diffusion microstructure program (square-root impact, trade-sign memory).
  - **Scores:** Novelty 4/5 · Credibility 5/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read — calibrate the aggregation-time correction into any HF correlation estimator.

### Risk & portfolio
- **Sharpe Ratio and Return-VaR Ratio Maximization for Option Portfolios with Skew-Elliptical t Underlying Returns** — Kyle Sung, Traian A. Pirvu, 15 Jun 2026 (q-fin.PM) — [link](https://arxiv.org/abs/2606.17032)
  - **What it is:** Explicit closed-form portfolio weights that maximize Sharpe and Return-VaR ratios for option portfolios when the underlying follows a skew-elliptical t (heavy tails + skew), not Gaussian. Optimal portfolios differ materially by objective.
  - **Why it matters for trading:** Implementable weight formulas for options under realistic return distributions, and a clean demonstration that Sharpe- vs. tail-objective optimization diverge — relevant to anyone sizing option books.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest — implement the weight formulas and compare Sharpe vs. Return-VaR allocations on a small option book.
- **Belief at Risk: Quantifying Agentic AI Model Risk with LLM-Inferred Bayesian State Filters** — Matthew Francis Dixon, 13 Jun 2026 (q-fin.RM) — [link](https://arxiv.org/abs/2606.15473)
  - **What it is:** Models an agentic AI as a POMDP where the LLM is a *semantic observation model* mapping evidence to a distribution over latent regimes; Bayesian filtering enforces temporal consistency and auditable beliefs. Separates uncertainty (posterior entropy, belief drift, calibration error) from risk (loss distribution → VaR). Empirical equity-return case study.
  - **Why it matters for trading:** A concrete, regulator-friendly way to put a number on the model risk of LLM/agentic trading systems — exactly the governance layer needed before any agentic harness touches live capital. Companion paper, same author, formalizes the validation side: *Model Validation of Agentic AI Systems: A POMDP-Based Framework* ([2606.17383](https://arxiv.org/abs/2606.17383)).
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read — adopt posterior-entropy / belief-VaR as the monitoring layer over any LLM-driven decision agent.
- **An extendable, integrated, and dynamic approach to forecasting and stress-testing credit risk** — Marcel Muller, Arno Botha, Conrad Beyers, 17 Jun 2026 (q-fin.CP / q-fin.RM) — [link](https://arxiv.org/abs/2606.19052)
  - **What it is:** A multistate probabilistic framework that simulates loan cash flows and computes portfolio-level credit metrics, integrating risk-metric forecasting with receipt generation and embedding correlation structures that classical stress tests omit.
  - **Why it matters for trading:** Useful for any credit/loan-book or fixed-income exposure where stress scenarios need cross-loan correlation rather than independent defaults. Niche vs. the equities/derivatives focus, but a clean stress-testing template.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve unless credit exposure becomes in-scope.

### Asset class / market
- **Fast, Reliable, and Error-Bounded Option Pricing with Pretrained Neural Networks: A GJR–GARCH Study** — Thijs van den Berg, 13 Jun 2026 (q-fin.CP) — [link](https://arxiv.org/abs/2606.15502)
  - **What it is:** A Mixture Density Network maps (parameters, maturity) to the terminal return density as a Gaussian mixture, giving arbitrage-free option prices, IVs, and Greeks in closed form — microseconds on CPU, sub-microsecond on GPU — with a *distribution-free* error bound (OOS CDF error 1.4e-4, within 10% of the noise floor). Demonstrated on GJR-GARCH.
  - **Why it matters for trading:** Drop-in replacement for slow Monte Carlo when you need vol surfaces / Greeks at scale, and rare among NN pricers in shipping a verifiable accuracy guarantee instead of "trust the net." Practical execution-/risk-engine tooling.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** replicate — train the MDN surrogate on a known model and validate the error bound before any production use.

## New resources & tooling
- **nittygritty-zzy/quantlab** — [link](https://github.com/nittygritty-zzy/quantlab) — quant research platform built on Microsoft Qlib: ML-powered backtesting, multi-source options analysis, portfolio management, Plotly dashboards, CLI. _Lead only — star count/maturity not yet verified; evaluate against existing Qlib workflow before adopting._
- No clearly-new high-signal library release this run beyond the awesome-* indexes already in the watchlist; GitHub surface was generic.

## Watchlist updates
- **Matthew Francis Dixon** — author, agentic-AI model risk for finance (POMDP belief-VaR, agentic validation frameworks; [2606.15473](https://arxiv.org/abs/2606.15473), [2606.17383](https://arxiv.org/abs/2606.17383)). Worth tracking as agentic trading governance matures.
- **Li Xia** — author, geometric theory of LLM-guided discovery / factor mining bottlenecks ([2606.14386](https://arxiv.org/abs/2606.14386)).
- Angstmann & Gebbie (already tracked) extended their reaction–diffusion microstructure line to coupled order books — keep following.

## Open questions / threads to pull next run
- **Dixon's validation companion (2606.17383)** captured here as a lead but not fully scored — chase next run if agentic governance stays relevant.
- **Scholar Gateway MCP / SSRN** not driven this run (no auth + thin weekend) — run a dedicated SSRN factor/microstructure sweep on the next weekday batch.
- The fresh 19-Jun arXiv items are mostly captured; the next real refresh of candidates lands with the **Mon 22 Jun** announce batch — re-sweep q-fin.TR/PM/ST then.
- Verify **quantlab** (stars, activity, license) before promoting from lead to tooling.
