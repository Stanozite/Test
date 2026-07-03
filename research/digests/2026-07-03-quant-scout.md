# Quant Scout Digest — 2026-07-03

## TL;DR
- **Short-term trend is dead — and tick size is the tell** (Kurth/Eisler/Rej/**Bouchaud**, CFM, 2607.01550): on ~100 liquid futures 1995–2025, short-term trend PnL broke ~2009 and the *only* cross-sectional variable that separates degraded from surviving trends is **volatility-normalised tick size** — trend collapsed on small-tick contracts at every signal horizon, stayed intact on large-tick ones. Capacity, electronification, and CTA/order-flow regime shifts all fail on timing/magnitude. → **backtest target**: short-term trend on BTC-USD (small effective tick) should show no reliable edge.
- **Kyle's λ predicts the cross-section** (Aldridge, 2607.01377): daily signed order flow → firm-month λ̂ (impact regression + Amihud) predicts contemporaneous and 1-month-ahead equity returns on CRSP 2020–25; resolves the Constantinides illiquidity-premium puzzle as adverse selection (low flow widens λ, depresses price today, normalisation reverts) — no risk compensation needed.
- **Factor models can raise max-Sharpe yet still misprice a fixed subspace** (Shin, 2607.01765): a cap-rank "bridge-alpha" curve exposes zero-alpha violations along the market-cap axis that Sharpe gain hides; q5's daily negative bridge attenuates under lead-lag correction, FF/Carhart more visible monthly, across 154 factors the cap-axis norm is distinct from Sharpe gain and size.
- Thin July batch again — only three IDs above the 07-02 ceiling (2607.01198) are genuinely fresh trading/risk work; q-fin.RM shows no 2607 entries, cs.LG July-3 finance-empty.

## Findings by focus area

### ML / AI for alpha
_no notable new findings this run_ (July-3 cs.LG batch had no finance-applied ML above ceiling; LLM/alpha-mining items all previously captured).

### Microstructure & execution
- **Is Trend Still Your Friend?: A Microstructural Account of the Demise of Short-Term Trend-Following** — Jutta G. Kurth, Zoltan Eisler, Adam Rej, Jean-Philippe Bouchaud (CFM / Capital Fund Management), 2 Jul 2026 — [arXiv:2607.01550](https://arxiv.org/abs/2607.01550)
  - **What it is:** Cross-section of ~100 liquid futures (1995–2025) + an industry CTA proxy documents a ~2009 break in short-term trend profitability. Tests four explanations (capacity, electronification, CTA-vs-order-flow regime change, microstructure) and rejects the first three. Central result: the discriminating variable is **volatility-normalised tick size** — post-2008 trend PnL collapsed on small-tick contracts at all signal speeds while surviving on large-tick ones; asset class and liquidity do *not* replicate the split.
  - **Why it matters for trading:** A concrete, testable microstructural law for *where* trend still works. Says the death of short-term trend is a tick-size / discreteness effect, not a crowding or capacity story — so screening trend universes by vol-normalised tick becomes an ex-ante edge filter. Directly frames a BTC test: crypto trades at a tiny effective tick relative to vol, so the thesis predicts short-term trend on BTC should be structurally weak.
  - **Scores:** Novelty 5/5 · Credibility 5/5 · Relevance 5/5 · Actionability 4/5
  - **Next step:** backtest — short-term trend-following on BTC-USD, expect no reliable OOS edge (confirmatory test of the small-tick prediction).

- **Liquidity Premium and Investment Horizons** — Irene Aldridge, 1 Jul 2026 — [arXiv:2607.01377](https://arxiv.org/abs/2607.01377)
  - **What it is:** Estimates Kyle (1985) price-impact λ directly from daily equity order flow (within-month impact regression + Amihud-style ratio) on CRSP 2020–2025. Signed order flow predicts contemporaneous and one-month-ahead returns; volume volatility predicts *lower* subsequent returns. Fama-MacBeth + Newey-West confirm cross-sectional signal. Resolves Constantinides (1986) illiquidity premium via adverse selection: low flow widens λ, depresses price today, later normalisation reverts.
  - **Why it matters for trading:** A cheap, daily-data λ estimator that carries cross-sectional return information — a liquidity/impact signal buildable without tick data. The "normalisation reversion" mechanism is a directional reversal signal tied to a measurable impact state, adjacent to the Portnaya/bounce work already in the ledger.
  - **Scores:** Novelty 3/5 · Credibility 4/5 · Relevance 4/5 · Actionability 3/5
  - **Next step:** shelve (equities/CRSP-specific; revisit if a daily crypto order-flow λ proxy is available).

### Risk & portfolio
- **A Cap-Axis Integral Diagnostic of Factor Models** — Useong Shin, 2 Jul 2026 — [arXiv:2607.01765](https://arxiv.org/abs/2607.01765)
  - **What it is:** A factor-model diagnostic that lifts pricing errors into a "bridge-alpha" curve along the market-cap rank axis. Low-dim factor models can improve the max-Sharpe frontier while leaving zero-alpha violations on economically fixed subspaces; under an aggregate-market gate a zero bridge curve ≡ pricing the market's internal cap-rank subspace. CRSP 1967–2024: q5's daily negative bridge attenuates under lead-lag correction, FF/Carhart bridges more visible monthly; across 154 factors the cap-axis norm is distinct from Sharpe gain and size exposure.
  - **Why it matters for trading:** Extends Shin's earlier construction-dependence / body-tail factor diagnostics (already tracked) with a cap-rank test that catches mispricing a Sharpe-max screen misses — a validation gate before trusting a factor set for portfolio tilts.
  - **Scores:** Novelty 4/5 · Credibility 4/5 · Relevance 3/5 · Actionability 2/5
  - **Next step:** shelve (methods reference; useful when auditing a factor library, not a standalone signal).

### Asset class / market
_no notable new findings this run_

## New resources & tooling
_none new this run_ (no fresh high-signal repo/dataset above the ledger).

## Watchlist updates
- No new players to add — Bouchaud/CFM, Aldridge, and Shin are already tracked (Shin added 2026-06-24; Aldridge appears as execution-risk reference since 2026-07-01). Consider promoting **Jean-Philippe Bouchaud / CFM** to an explicit tracked-player row given the strength of 2607.01550.

## Open questions / threads to pull next run
- **Bouchaud tick-size thesis on crypto:** does the small-tick prediction extend to perp funding / large-tick altcoins? A cross-crypto tick-normalised trend screen would be the natural replication.
- **Aldridge daily-λ signal on crypto:** can signed daily order flow → λ̂ be reconstructed from public crypto trade prints as a reversal signal?
- July arXiv volume remains thin (RM 2607-empty, PM/CP light) — monitor for the mid-July batch; ceiling now 2607.01765.
