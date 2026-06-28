# Quant Scout Digest — 2026-06-28

## TL;DR
- **AlphaMemo** records *which edit-motifs work under which parent-factor context* as structured search-process memory + a veto on known-failure patterns — LLM alpha-mining agents get faster discovery and less overfit reuse on CSI 500 / S&P 500 (Yu/Zheng/Pan/Liu/Wang/**He**).
- **Signature methods for optimal market making** — signature linearization turns mean-variance MM into a *pseudo-linear* program over the expected signature of the augmented market path; `Sig-REINFORCE` learns bid/ask quotes and beats a PPO baseline under both Poisson and Hawkes order flow (Gennaro/**Mastrolia**/Primavera).
- **Endogenous reinsurance pricing** as a Stackelberg mean-field game exposes a feedback loop standard models miss: premium hikes act through *both* direct cost and indirect aggregate-risk channels; relative-performance concerns sustain retention even when reinsurance is financially attractive (Hu/Kong).
- _Thin Sunday window (2026-06-28): arXiv weekend announce gap — only one genuinely-new ID above the 2606.27 ceiling (reinsurance). Remaining two are mid-June residue not previously surfaced. GitHub "Alpha Skills"/"QuantGPT" tooling leads dropped — no verifiable canonical repo URL._

## Findings by focus area

### ML / AI for alpha
- **AlphaMemo: Structured Search-Process Memory for Self-Evolving Alpha Mining Agents** — Hang Yu, Zifan Zheng, Jeff Z. Pan, Tongliang Liu, Zhiyong Wang, Fengxiang He, Jun 2026 — [arXiv:2606.20625](https://arxiv.org/abs/2606.20625)
  - **What it is:** An LLM alpha-mining agent that stores not final factors but the *process*: AST-diff "edit motifs" tagged by parent-factor context, with confidence-gated residual memory and a veto mechanism filtering known-failure patterns. Tackles the combinatorial search space, noisy non-stationary feedback, redundant discovery, and overfit-from-reuse failure modes.
  - **Why it matters for trading:** Directly addresses the alpha-decay/overfit trap that kills naive LLM factor mining (cf. AlphaAgent, AlphaPROBE, FactorMiner). Memory-of-process is the upgrade over memory-of-results — fewer wasted GPU-hours per usable factor, validated OOS on CSI 500 + S&P 500.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read — extract the veto + confidence-gating design as a bolt-on for any existing LLM-agent factor loop; full replication is infra-heavy.

### Microstructure & execution
- **Signature Methods for Optimal Market Making** — Alberto Gennaro, Thibaut Mastrolia, Francesca Primavera, Jun 2026 — [arXiv:2606.19772](https://arxiv.org/abs/2606.19772)
  - **What it is:** Reformulates mean-variance market making via signature linearization into a *pseudo-linear optimization over the expected signature* of an augmented market path. Introduces `Sig-REINFORCE` to learn optimal bid/ask quotes; tested under Poisson and self-exciting Hawkes order arrivals against a PPO baseline.
  - **Why it matters for trading:** A tractable, model-light route to optimal quoting that sidesteps hand-specifying intensity dynamics — and the Hawkes case captures order-flow clustering that Avellaneda-Stoikov ignores. Beating PPO suggests the signature structure is a genuine inductive-bias win, not just reparametrization.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read / replicate — signature-transform tooling (e.g. `signatory`/`iisignature`) makes a small-scale Sig-REINFORCE quoting prototype feasible.

### Risk & portfolio
- **Endogenous Reinsurance Pricing in Large Competitive Insurance Markets: Finite-Player and Mean Field Analysis** — Ruimeng Hu, Byungdoo Kong, Jun 2026 — [arXiv:2606.27150](https://arxiv.org/abs/2606.27150)
  - **What it is:** A Stackelberg game where one strategic reinsurer sets premium + investment policy as leader, and many heterogeneous insurers choose retention + investment under absolute, relative-performance, and common-risk concerns. Characterizes equilibrium retention via a scalar fixed point, proves monotone premium response and a full-cession → partial → full-retention threshold, and establishes finite-player ↔ mean-field convergence.
  - **Why it matters for trading:** Tangential to systematic trading but directly relevant to the insurance pillar — the "feedback loop absent from standard models" (premiums move aggregate risk, which moves equilibrium premiums) is the kind of reflexivity that also shows up in crowded-factor and dealer-inventory settings. Relative-performance concerns sustaining uneconomic retention is a transferable behavioral lesson.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 2/5 · Actionability 2/5
  - **Next step:** shelve — read for the insurance book; no direct trading action.

## New resources & tooling
- _No verifiable new repos this run. "Alpha Skills" and a 2026-vintage "QuantGPT" (8-MCP-tool A-share factor engine, anti-overfit) surfaced in search summaries but neither resolved to a confirmable canonical GitHub URL — omitted pending verification next run._

## Watchlist updates
- **Thibaut Mastrolia (UC Berkeley IEOR)** — optimal control / market-making theorist; signature methods for MM. Worth adding to Global players.
- **Ruimeng Hu (UCSB)** — mean-field games, finite-player↔MF convergence for insurance/financial markets. Candidate add.

## Open questions / threads to pull next run
- "Alpha Skills" and the 2026 "QuantGPT" MCP factor engine — chase canonical repos + star counts; if real, both are directly usable agentic factor-research tooling.
- Signature-method MM vs. the captured Feys forced-uniqueness AS≡CJ axiomatization (2606.01477) — do signature quotes recover the AS/CJ inventory-skew form in the Poisson limit?
- Next arXiv announce (Mon 2026-06-29) should clear the weekend backlog — expect a fuller 2606.27–28 batch; re-scan microstructure + alpha first.
