# Quant Scout Digest — 2026-07-02

## TL;DR
- **AI portfolio policies beat simple rules only non-uniformly** (Pollok/Robik, 2607.00475): end-to-end differentiable-Sharpe policies on the 16 most liquid CME futures rank above equal-weight / risk-parity / time-series-momentum on the *pooled* cross-asset book and in some sub-classes but **not everywhere**; a transformer beats an LSTM mainly because it *trades far less* and survives costs — the edge is a turnover story, not a forecasting one. Backtest target: does the TSMOM benchmark itself have standalone edge on BTC (an asset class they don't test)?
- **Large trades stop being "news" when liquidity has fat tails** (Çetin/Lin/Livieri, 2607.01198): in a sequential competitive LOB with Student-t uninformed flow, heavy-tailed liquidity demand *flattens and concavifies* price impact, *slows* learning from order flow, and *delays* the decay of the adverse-selection premium — impact becomes tail-dependent, Gaussian-calibrated impact models understate it in rare-liquidity regimes.
- **A physics crash-detector on vol indices** (Hayward/Lennon/Biancalana, 2606.31475): treat extreme vol spikes as nonlinear-Schrödinger "rogue waves"; the gradient of the system's minimum eigenvalue spikes at onset, giving an 87.5% out-of-sample early-warning hit rate on VIX/VXO/VSTOXX.
- **Governance-aware POMDP for delegating to AI** (Dixon, 2606.29406): sequential Bayesian allocation of decision authority to an AI beats five static/heuristic governance policies across heterogeneous AI-quality regimes — a model-risk control layer for agentic trading stacks.
- Thin early-July window — only three genuinely fresh IDs above the 06-30/07-01 ceiling (2607.01198 / 2607.00475 / 2607.00856); the July-2 arXiv batch is small and PM/CP-light. Fresh IDs verified above the ledger's 2606.31675 top.

## Findings by focus area

### ML / AI for alpha
- **End-to-End Parametric Portfolio Policies for Cross-Asset Futures Timing: When Do AI Models Beat Simple Rules?** — Austin Pollok, Kevin Robik, 1 Jul 2026 (q-fin.ST/PM/TR) — [link](https://arxiv.org/abs/2607.00475)
  - **What it is:** Skips the "forecast-then-optimize" pipeline and learns a policy that maps market state directly to portfolio weights, trained on the 16 most liquid CME futures with a *differentiable Sharpe-ratio loss*, benchmarked against equal weight, risk parity, and time-series momentum. Learned policies rank above the rules on the pooled book and in several sub-asset classes but not uniformly; LSTM ≈ transformer gross, but the transformer trades far less and so wins net of costs.
  - **Why it matters for trading:** A clean, honest statement of where end-to-end AI actually adds value over cheap rules (answer: pooled diversification + cost-efficient turnover, not universal forecasting skill). The differentiable-Sharpe objective is directly reusable, and TSMOM is confirmed as a hard-to-beat baseline — which is exactly what makes it worth stress-testing on crypto.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** backtest — replicate the *time-series-momentum benchmark* (the simple rule) on BTC-USD to check whether it has standalone OOS edge in an asset class outside their 16-future panel.
- **Shapley in Context: Explaining Financial Language with Domain Expertise** — Dangxing Chen, Pengzhan Guo, 1 Jul 2026 (q-fin.CP) — [link](https://arxiv.org/abs/2607.00856)
  - **What it is:** Tests whether Shapley-value attributions over LLM outputs on financial text line up with genuine financial reasoning rather than generic token importance, arguing domain-aware attribution is needed before trusting LLM explanations.
  - **Why it matters for trading:** Interpretability gate for any LLM-in-the-loop signal (news/filings sentiment) — a check that the model is reasoning from finance-relevant features, not artifacts, before you size on it.
  - **Scores:** Novelty 3/5 · Credibility 3/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (reference for LLM-signal validation, not a standalone strategy).

### Microstructure & execution
- **When Large Trades Are Not News: Liquidity Tail Risk and Price Discovery** — Umut Çetin, Mingwei Lin, Giulia Livieri, 1 Jul 2026 (q-fin.TR) — [link](https://arxiv.org/abs/2607.01198)
  - **What it is:** A sequential competitive limit-order-book model with asymmetric information where liquidity suppliers cannot separate informed from uninformed demand. Modeling uninformed flow with Student-t tails of varying index creates "liquidity-tail ambiguity" that flattens and concavifies price impact, slows learning from order flow, and delays the decline of the adverse-selection premium; impact follows tail-dependent asymptotic laws with polynomial-order pricing relevance absent under Gaussian flow.
  - **Why it matters for trading:** Says the informativeness of a large trade is *state-dependent on liquidity tails* — in fat-tailed regimes a big print is more likely liquidity than information, so Gaussian-calibrated impact/adverse-selection models mis-price execution risk exactly when it matters. Directly relevant to sizing, impact estimation, and reading order flow.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** read (theory; a tail-index-conditioned impact model is a longer build).

### Risk & portfolio
- **Real-time identification of the onset of financial rogue waves** — Rosie Hayward, Orla Lennon, Fabio Biancalana, 30 Jun 2026 (q-fin.ST / nlin.PS) — [link](https://arxiv.org/abs/2606.31475)
  - **What it is:** Maps extreme volatility spikes to nonlinear-Schrödinger (Kerr-nonlinearity) "rogue waves." Detection monitors the numerical gradient of the system's minimum eigenvalue over a moving window; it reliably spikes at the onset of an extreme event, giving an 87.5% out-of-sample hit rate on VIX, VXO, and VSTOXX.
  - **Why it matters for trading:** A candidate crash / vol-spike early-warning that keys off the volatility surface rather than price, usable as a de-risking / hedge-on overlay. The eigenvalue-gradient machinery is heavier than a simple filter, so treat the 87.5% as a claim to reproduce, not a fact.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** replicate (reproduce the eigenvalue-gradient signal on VIX before trusting the hit rate; possible risk overlay later).
- **Adaptive AI Delegation under Uncertainty: A Bayesian Governance Policy for Sequential Decision Authority** — Matthew Francis Dixon, 28 Jun 2026 (q-fin.RM) — [link](https://arxiv.org/abs/2606.29406)
  - **What it is:** Formulates AI governance as a Governance-Aware POMDP: Bayesian inference tracks the informational state and sequential optimization sets how much decision authority to delegate to the AI. Across heterogeneous AI-quality regimes the sequential Bayesian policy beats five heuristic governance strategies, with stress-tests and an early-warning layer.
  - **Why it matters for trading:** A principled human-in-the-loop control for agentic trading stacks — how much to trust an LLM/agent's recommendation as its measured reliability drifts. Extends Dixon's belief-VaR / agentic-model-risk line (already tracked).
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read (governance/model-risk reference for the agentic layer).

### Asset class / market
- _no notable new findings this run_ — the July-2 batch surfaced no fresh crypto/FX/options empirical paper above the ledger ceiling; the closest crypto-relevant thread is testing the TSMOM benchmark (2607.00475) on BTC, done in today's backtest.

## New resources & tooling
- **nkaz001/hftbacktest** — [link](https://github.com/nkaz001/hftbacktest) — free HFT / market-making backtester that models feed + order latency and queue position on full L2/L3 tick data (Binance/Bybit crypto examples). The right tool if we ever act on the microstructure/impact findings (Çetin et al., Aldridge audit) at the order-book level — our current daily-bar pipeline can't represent queue/impact effects. Established repo, surfaced this run as the fit-for-purpose option; not new-this-week.

## Watchlist updates
- **Austin Pollok & Kevin Robik** — end-to-end differentiable-Sharpe portfolio policies; cross-asset futures timing; honest AI-vs-rules benchmarking. (add to players)
- **Umut Çetin / Giulia Livieri** — asymmetric-information LOB theory; liquidity-tail-dependent price impact and adverse selection. (add to players)
- **Fabio Biancalana (+ Hayward/Lennon)** — nonlinear-physics (NLS/rogue-wave) methods for extreme-event / vol-spike early warning. (add to players)

## Open questions / threads to pull next run
- Does the eigenvalue-gradient "rogue-wave" onset signal (2606.31475) survive on crypto vol (DVOL / BTC realized vol) as well as it does on VIX? Reproducibility of the 87.5% claim.
- Pollok/Robik's differentiable-Sharpe *end-to-end weight policy* — worth a proper multi-asset replication (out of scope for the single-symbol daily pipeline; needs a cross-asset engine).
- SSRN factor-momentum 1-month-lag lead (5333744) still deferred — 403 on prior runs, date unverified. Retry.
- July arXiv numbering has rolled to 2607.xxxxx — reset recency ceiling; watch for the fuller Mon/Tue July batch next runs.
