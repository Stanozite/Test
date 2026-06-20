# Quant Scout Digest — 2026-06-20

_Window: items since the last digest (2026-06-17). This was a short, weekend-spanning
window (Thu–Sat), so the fresh-paper pool is thin — q-fin.PM had no new submissions
18–20 Jun, and q-fin.TR had effectively no new execution/microstructure work. Where the
strongest unrecorded items sit just outside the window (15–17 Jun, not in the ledger),
they are included with their true dates flagged. Alpha and microstructure were lean; see
Open questions._

## TL;DR
- **Trend-conditioned risk forecasting beats mean-reversion** (Safari & Schmidhuber): vol and correlations *rise* day-after-day inside strong trends, more so in downturns — a usable risk-up signal, with markets modeled as a lattice gas near criticality.
- **Factor-model "winners" are an artifact of test-portfolio construction** (Shin): FF3 is the most construction-robust; q5 posts high Sharpes but construction-sensitive pricing errors — benchmark across weighting/rebalancing rules, not one set.
- **A persistent 5.6pp cross-venue mispricing** between Polymarket BTC-threshold contracts and Binance option-implied probabilities that slowly mean-reverts (Portnaya) — a measurable, slow-information arbitrage thread.
- **Crypto IV surfaces compress ~8× better** with a convolutional VAE that also flags regime anomalies unsupervised (Singh et al.) — a denoising/anomaly layer for crypto options desks.
- **Agentic risk supervision that doesn't cry wolf** (DeXposure-Claw): routing LLM decisions through forecasts + confidence gates cuts false alarms vs. naive LLM monitoring, validated on 5 years of on-chain data.

## Findings by focus area

### ML / AI for alpha
- **AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph Biased Evolution** — Taian Guo, Haiyang Shen, Junyu Luo et al. (PKU), Feb 2026 — [link](https://arxiv.org/abs/2602.11917)
  - **What it is:** Models formulaic-alpha discovery as navigation over a directed acyclic graph: a Bayesian retriever picks promising seed factors, a DAG-aware generator uses ancestral relationships to avoid re-deriving redundant alphas. Beats 8 baselines on Chinese-equity datasets for predictive accuracy, return stability, and training efficiency.
  - **Why it matters for trading:** Directly extends the LLM/evolutionary alpha-mining line already in the ledger (QuantaAlpha, Alpha-R1, FactorEngine) with an explicit redundancy-avoidance mechanism — the practical pain point in automated factor search is duplicate/decayed alphas.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Date note:** Feb 2026, outside the 17–20 Jun window — included as an unrecorded catch-up because in-window alpha work was absent and it complements captured items.
  - **Next step:** read → compare DAG-dedup against AlphaForge/FactorEngine; consider replicating the retriever on US equities.

_Otherwise: no notable **new** alpha findings in the 17–20 Jun window._

### Microstructure & execution
_No notable new findings this run — q-fin.TR produced no new execution/market-making work in the window; the recent batch (TT-DAC-PS, AS≡CJ, Hyperliquid sunshine-trading, Angstmann–Gebbie) was already captured 16–17 Jun._

### Risk & portfolio
- **Trends, Volatility, Correlations, and Critical Phenomena in Financial Markets** — Sara A. Safari, Christoph Schmidhuber, 18 Jun 2026 — [link](https://arxiv.org/abs/2606.20145)
  - **What it is:** Shows volatilities and correlations *increase day-after-day* during strong up- or down-trends (stronger in downturns); quadratic-polynomial trend models outperform mean-reversion for predicting market risk. Frames markets as a lattice-gas system near a critical point.
  - **Why it matters for trading:** A forward-looking, trend-conditioned input for vol/correlation forecasting → position sizing, de-grossing triggers, and crash-mitigation overlays. The downturn asymmetry is directly tradable as a risk-budget rule.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** backtest — replace EWMA/mean-reversion vol estimate with a trend-conditioned predictor in a risk-parity sleeve.
- **Which Portfolios? The Construction Dependence of Factor Model Performance** — Useong Shin, 17 Jun 2026 — [link](https://arxiv.org/abs/2606.19550)
  - **What it is:** Forms randomly constructed CRSP test portfolios while varying weighting and rebalancing, then re-ranks CAPM / FF3 / FF5 / Carhart / FF6 / q5. FF3 is most construction-robust; q5 hits high max-Sharpe but with construction-sensitive pricing errors.
  - **Why it matters for trading:** Cautions that factor-model selection and reported alphas are partly a construction artifact — benchmark across multiple weighting/rebalancing schemes before trusting a model in live, constraint-bound portfolios.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** read → adopt as a robustness checklist for in-house factor evaluation.
- **How to Spot Outliers: an Ensemble Anomaly Detection Framework** — Daniil Peysakhovich, Rafał Sieradzki, 18 Jun 2026 — [link](https://arxiv.org/abs/2606.20079)
  - **What it is:** Unsupervised ensemble to detect anomalies in *risk-calculation outputs* (incl. stale/frozen-feed values), validated on proprietary IB credit-derivatives data (183 trades, 129 days), F1 61–79%, beating single methods. Aimed at Basel III / FRTB operational risk.
  - **Why it matters for trading:** A practical data-quality / model-risk guardrail — stale-feed and outlier detection on PnL and risk vectors is exactly the silent failure mode that corrupts live signals and risk reports.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** shelve/replicate — lightweight to prototype as a monitor over daily risk outputs.

### Asset class / market
- **Do Prediction Markets Match Option Prices? Bitcoin Threshold Evidence from Binance and Polymarket** — Victoria Portnaya, 17 Jun 2026 — [link](https://arxiv.org/abs/2606.19517)
  - **What it is:** Compares Polymarket BTC-threshold contract prices to risk-neutral probabilities from Binance call options. Finds a persistent ~5.6pp mean pricing gap that *slowly reverts* — evidence of slow information diffusion across segmented venues, not noise.
  - **Why it matters for trading:** A concrete, measurable cross-venue mispricing with a reversion structure — the basis of a prediction-market vs. options relative-value / convergence trade in crypto.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest the gap-reversion as a tradable spread, net of Polymarket/Binance frictions.
- **Beyond the Smile: A Hybrid Convolutional VAE for Crypto Volatility Surfaces** — Sadanand Singh, Allam Reddy, Manan Chopra, 15 Jun 2026 — [link](https://arxiv.org/abs/2606.16961)
  - **What it is:** Convolutional VAE for BTC/ETH implied-vol surfaces (hourly options data) hybridized with classical smile-fitting; ~8× lower reconstruction error than conventional methods, robust to missing data, and flags regime anomalies (e.g. Aug-2023 flash crash) without labels.
  - **Why it matters for trading:** A denoising + low-dimensional latent representation of crypto IV surfaces → surface interpolation/repair, anomaly detection, and a feature source for vol trading and deep hedging.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Date note:** 15 Jun, just outside the window; unrecorded and strong, so included.
  - **Next step:** read → evaluate latent factors as inputs to a crypto vol-carry or dispersion strategy.
- **DeXposure-Claw: An Agentic System for DeFi Risk Supervision** — Aijie Shu, Bowei Chen, Wenbin Wu, Cathy Yi-Hsuan Chen, Fengxiang He, 17 Jun 2026 — [link](https://arxiv.org/abs/2606.19501)
  - **What it is:** A forecast-grounded agentic supervision system that routes LLM decisions through structured evidence and confidence gates, with a graph time-series model predicting exposure networks. Validated on ~5 years of on-chain data; cuts the over-reaction/false-alarm failure mode of general-purpose LLM monitoring.
  - **Why it matters for trading:** Template for *auditable* LLM-in-the-loop risk monitoring — pairing deterministic forecasts + confidence gates with an LLM is transferable to any live-risk surveillance stack, not just DeFi.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read → mine the forecast-gate architecture for an internal risk-alert agent.

## New resources & tooling
- **HKUDS/Vibe-Trading** — [link](https://github.com/HKUDS/Vibe-Trading) — natural-language multi-agent trading/research framework from the HKU Data Science Lab: 6 backtest engines (ChinaA, GlobalEquity, Crypto, ChinaFutures, GlobalFutures, Forex + options) with Monte-Carlo permutation, bootstrap Sharpe CI, and walk-forward validation, plus an MCP server exposing `backtest`, `factor_analysis`, `analyze_options`, `pattern_recognition` etc. (v0.1.0, Apr 2026). Credible group; good harness for agentic strategy prototyping with built-in statistical validation.
- **FinStressTS** — [link](https://arxiv.org/abs/2606.03184) — Sun, Koa, Ni et al.: a parametric *synthetic* benchmark for time-series forecasting in finance, generating controllable stress/regime scenarios (cs.LG + q-fin.CP/ST, 3 Jun 2026). Useful for stress-testing forecasting models against tail regimes without overfitting to one historical path.

## Watchlist updates
- **Christoph Schmidhuber (ZHAW)** — econophysics / critical-phenomena approach to vol & correlation forecasting; trend-conditioned risk. Worth tracking for risk/regime work.
- **HKU Data Science Lab (HKUDS)** — prolific agentic-finance + open-source tooling group (Vibe-Trading); track their releases for new strategy/agent frameworks.
- **Cathy Yi-Hsuan Chen / Fengxiang He** — agentic DeFi risk supervision; intersection of LLM agents and on-chain risk.

## Open questions / threads to pull next run
- **Alpha + microstructure were thin this window.** Re-sweep q-fin.TR and the LLM-alpha line (AlphaPROBE, FactorEngine, AlphaForge) once the post-weekend submission backlog clears (≈23–25 Jun).
- **Portnaya BTC mispricing:** is the 5.6pp gap robust net of Polymarket resolution risk and Binance options liquidity? Worth a dedicated data pull.
- **Trend-conditioned vol (Safari & Schmidhuber):** does the downturn asymmetry survive out-of-sample on non-equity assets (FX, crypto, futures)?
- **Vibe-Trading:** verify whether its backtest statistical-validation suite (deflated/bootstrap Sharpe, walk-forward) is rigorous enough to trust, or just cosmetic.
