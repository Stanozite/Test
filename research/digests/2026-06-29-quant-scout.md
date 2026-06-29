# Quant Scout Digest — 2026-06-29

## TL;DR
- **CryptoGAT** recasts crypto price forecasting as a *cross-asset graph* problem (graph-attention over coins), arguing temporal models (LSTM/GRU/Transformer) that work on equities fail on crypto's wild swings — a structural reframe with public code (Peng/Khushi/Poon). *→ backtest target this run.*
- **Fonseca** gives a *decision-geometry* of GMV-portfolio covariance estimation: an exact regret identity proving estimation error only matters through its action on the weights, plus a (p−1)-dim invariance and sharper heavy-tail (κ∈(2,4)) constants — choose the estimator by decision regret, not matrix-norm loss.
- **Angelini** builds a regime-adaptive KS / Grünwald–Letnikov fractional-derivative test that keeps Hurst-exponent estimation valid for H>1/2, classifying persistent / anti-persistent / efficient states and detecting rough volatility on equity indices.
- Thin Monday window — arXiv weekend gap (no Sat 27 / Sun 28 announcements); the genuinely fresh items are the 06-29 batch (IDs > 2606.27150 ceiling). A risk-management systematic review (Kutej/Rass) rounds it out as reference material.

## Findings by focus area

### ML / AI for alpha
- **CryptoGAT: Are Time Series Models Effective for Cryptocurrency Forecasting?** — Yu Peng, Matloob Khushi, Josiah Poon (Univ. of Sydney group), 26 Jun 2026 — [link](https://arxiv.org/abs/2606.27670)
  - **What it is:** A lightweight Graph Attention Network that treats crypto price prediction as a *cross-asset* graph problem (attention across coins) rather than per-series temporal modeling. The thesis: standard temporal architectures (LSTM/GRU/Transformer) that suit equities underperform on crypto's extreme volatility; modeling cross-asset structure beats modeling the time axis. Claims outperformance over SOTA by a "notable margin"; GitHub code referenced.
  - **Why it matters for trading:** Directly about a tradable universe (crypto). If the cross-asset frame genuinely dominates, it argues against the naive temporal-trend baselines most retail crypto systems lean on — and gives a falsifiable claim we can probe with our own engine.
  - **Scores:** Novelty 4/5 · Credibility 3/5 · Relevance 4/5 · Actionability 4/5
  - **Next step:** backtest (test the converse temporal baseline on BTC/ETH; see backtest report)

### Microstructure & execution
- **(In)Efficient Market States and Rough Volatility Detected via Grünwald–Letnikov Fractional Derivative** — Daniele Angelini, 26 Jun 2026 — [link](https://arxiv.org/abs/2606.27932)
  - **What it is:** A regime-adaptive KS / GL–KS framework using the discrete Grünwald–Letnikov fractional derivative to estimate the Hurst exponent robustly. Standard KS self-similarity tests break down for H>1/2; the GL filter strips low-frequency artifacts while preserving self-similarity, letting the method classify persistent / anti-persistent / efficient market states and flag rough volatility. Validated with Monte Carlo, applied to realized volatility and equity-index prices (36 pp).
  - **Why it matters for trading:** A clean efficiency/regime detector. Persistent (H>0.5) states are where trend/momentum has statistical footing; anti-persistent states favor mean-reversion. A robust H-estimator that doesn't fall apart above 0.5 is a usable regime switch for turning trend rules on/off.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 3/5
  - **Next step:** read / shelve (regime overlay candidate for a future trend backtest)

### Risk & portfolio
- **The Decision Geometry of Covariance Estimation for the Global Minimum-Variance Portfolio under Heavy Tails** — Xavier Fonseca, 26 Jun 2026 — [link](https://arxiv.org/abs/2606.27462)
  - **What it is:** Reframes covariance-estimator evaluation around the *decision* (the GMV weights), not matrix-norm loss. Proves an exact regret identity and a non-asymptotic bound showing decision regret depends on estimation error only through its action on the weights; GMV regret is invariant to a (p−1)-dim projection of the p²-dim error matrix (scale-invariance as a special case). Under heavy tails (tail index κ∈(2,4)) the decision-focused view yields sharper constants — the gain shows up as concentration improvements, not faster rates. Pre-registered skew-t / t-copula simulations confirm it.
  - **Why it matters for trading:** Tells you *which* covariance estimator actually matters for a min-variance book and why two estimators with identical Frobenius error can give very different portfolios. The (p−1)-projection invariance means effort spent shrinking error directions the weights ignore is wasted — a concrete estimator-selection rule for heavy-tailed (read: crypto, single-name equity) returns.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 5/5 · Actionability 3/5
  - **Next step:** read (estimator-selection guidance for portfolio construction)
- **Methods for Uncertainty Representation in Risk Management: A Comparative Review and Decision-Oriented Framework** — Albert Kutej, Stefan Rass, 26 Jun 2026 — [link](https://arxiv.org/abs/2606.27804)
  - **What it is:** Systematic literature review of 370 publications, classifying uncertainty-representation methods into five families (probabilistic; evidence-based / fuzzy; qualitative elicitation; graphical / visual; hybrid). Finds probabilistic methods dominate for rigor but practical integration into operational risk workflows stays limited; calls for structured method-selection guidance. Map, not a new method.
  - **Why it matters for trading:** Reference material for how to *represent* model/parameter uncertainty in a risk stack — useful when deciding between probabilistic VaR, scenario/elicitation, or hybrid approaches. Low novelty, high as a survey.
  - **Scores:** Novelty 2/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (reference)

### Asset class / market
_Covered above — CryptoGAT (crypto) and Angelini (equity-index rough vol)._

## New resources & tooling
- **CryptoGAT code** — GitHub repo referenced in arXiv:2606.27670 (graph-attention crypto forecaster). Unverified link contents this run; worth pulling next run to confirm reproducibility before trusting the "notable margin" claim.

## Watchlist updates
- **Xavier Fonseca** — decision-theoretic covariance / portfolio estimation; exact regret geometry for GMV under heavy tails. *(add — risk/portfolio)*
- **Matloob Khushi / Josiah Poon (Univ. of Sydney)** — ML for crypto forecasting; cross-asset graph models. *(add — ML/alpha, crypto)*
- **Daniele Angelini** — fractional-calculus market-efficiency / rough-volatility detection. *(add — stat finance / microstructure)*

## Open questions / threads to pull next run
- Does CryptoGAT's cross-asset graph actually beat a simple cross-sectional momentum/relative-strength baseline, or just LSTM/GRU? The abstract withholds numbers — verify against the repo.
- Angelini's GL–KS Hurst switch as a live regime overlay: would gating an MA-crossover on H>0.5 cut the drawdowns trend-following eats in choppy crypto?
- Fonseca's (p−1)-projection invariance applied to a real crypto covariance: how much shrinkage effort is being wasted on weight-irrelevant directions?
