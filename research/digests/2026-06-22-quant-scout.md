# Quant Scout Digest — 2026-06-22

## TL;DR
- **Calibration validation is more than low RMSRE** — Mahler & Ruckdeschel recast interest-rate calibration as Weighted Least Squares, unlocking leverage diagnostics and confidence intervals; "low RMSRE is not sufficient" for model governance (highest-actionability item this run).
- **Multi-day equity tails need tempering** — Shao & Serota fit accumulated S&P500 returns (20–120d) with a tempered Skew-t (capped Inverse-Gamma stochastic vol), capturing finite power-law tails and gain/loss asymmetry — usable for horizon-scaled VaR.
- **CAP slope = Bayes' theorem** — Burakov unifies accuracy ratio, Somers' D and Gini as "one number three ways," with calibration-curve diagnostics for model validation.
- Thin Monday-after-weekend window: arXiv had no q-fin announcements for 20–22 Jun (weekend gap); findings are 16–19 Jun residue not yet captured.

## Findings by focus area

### ML / AI for alpha
_no notable new findings this run_

### Microstructure & execution
_no notable new findings this run_

### Risk & portfolio
- **Fitting Accumulated Stock Returns with Tempered Skew-t Distribution** — Siqi Shao, R. A. Serota, 17 Jun 2026 (q-fin.ST) — [arXiv:2606.19318](https://arxiv.org/abs/2606.19318)
  - **What it is:** Models multi-day S&P500 return distributions across 20–120-day accumulation windows. A "capped Inverse-Gamma" stochastic-vol prior generates a tempered Student-t for returns; a symmetry-breaking modification yields a tempered Skew-t that captures finite power-law tails plus the positive-mean / negative-skew gain–loss asymmetry. Mean and variance scale near-linearly with horizon.
  - **Why it matters for trading:** Direct input for horizon-scaled VaR / drawdown modeling and option-tail pricing where simple Gaussian or even plain Student-t understate accumulated-return tails.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** shelve (reference); replicate the capped-IG → tempered-Skew-t fit if building a multi-horizon tail model.
- **The Gini-Bayes Connection: The CAP Slope as Bayes' Theorem** — Denis Burakov, 16 Jun 2026 (q-fin.RM) — [arXiv:2606.18545](https://arxiv.org/abs/2606.18545)
  - **What it is:** Shows the cumulative accuracy profile (CAP) slope is Bayes' theorem in cumulative form, with standardized PD = rescaled posterior. Weight-of-evidence and information value fall out of the same geometry, and accuracy ratio / Somers' D_xy / Gini are proven to be "one number computed three ways." Calibration curves recover reliability diagrams in cumulative form.
  - **Why it matters for trading:** A clean, unified diagnostic toolkit for any score-based classifier — default screens, signal-quality ranking, ML-model validation — reducing three metrics and several ad-hoc checks to one geometric frame.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 2/5 · Actionability 3/5
  - **Next step:** shelve (model-validation reference for credit/score-based signals).

### Asset class / market
- **Advanced Calibration Analysis and Tools: Identifying Influential Observations in Stochastic Interest Rate Model Calibration** — Philipp Mahler, Peter Ruckdeschel, 18 Jun 2026 (q-fin.CP) — [arXiv:2606.20420](https://arxiv.org/abs/2606.20420)
  - **What it is:** Proves minimizing Root Mean Squared Relative Error is equivalent to a Weighted Least Squares problem, so standard WLS diagnostics — leverage analysis, confidence intervals — apply to rate-model calibration. Applied to Euro rates 2016–2025: leverage is boundary-dominated, parameters shifted after the 2022 regime break, and "low RMSRE is not sufficient for calibration validation."
  - **Why it matters for trading:** Concrete model-governance tooling for fixed-income/derivatives desks — identifies which quotes actually drive calibrated parameters and flags unstable fits a point-estimate error metric hides.
  - **Scores:** Novelty 2/5 · Credibility 3/5 · Relevance 3/5 · Actionability 4/5
  - **Next step:** replicate the WLS-leverage diagnostic on your own curve-calibration pipeline.

## New resources & tooling
- **QuantTradingOS** (GitHub org, 14 repos) — [github.com/QuantTradingOS](https://github.com/QuantTradingOS) — a modular, safety-first agentic "trading OS": `orchestrator` (regime → portfolio → allocation, FastAPI), `qtos-core` (event-driven backtest/execution), data-ingestion, plus intelligence agents (market-regime, sentiment-shift, insider) and control agents (capital-guardian, execution-discipline) with hard-limit circuit breakers and an MCP server. _Caveat: early-stage (0–3★, last updated Jan–Feb 2026, no proven adoption)_ — useful as an architecture reference for the agentic-finance thread alongside [[Vibe-Trading]].

## Watchlist updates
- _none added this run_ — Shao/Serota (tempered-t return distributions) and Mahler/Ruckdeschel (rate-model calibration governance) are credible but single-paper; revisit if they recur.

## Open questions / threads to pull next run
- **Optimal Order of Multi-Agent and General Many-Body Systems** — Jake J. Xia, 18 Jun 2026 ([arXiv:2606.20485](https://arxiv.org/abs/2606.20485)): physics-flavored framework deriving an "optimal degree of order" balancing collective output vs systemic fragility from agent power/response functions. Tagged q-fin.RM but not finance-validated — *potential* lens on crowding/synchronization risk in agentic markets. Below scoring bar as a finding; worth watching if the author applies it to markets.
- Catch the 22 Jun arXiv q-fin announcement (weekend gap) on the next run — 20–22 Jun were unannounced when scouted.
- Verify whether QuantTradingOS / HKUDS Vibe-Trading are converging on a shared agentic-trading-OS pattern worth a dedicated tracking note.
