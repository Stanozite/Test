# Watchlist — Quant Scout config

This is the tunable control file for the scout. Edit freely; it is re-read on every
run. Add players, sources, categories, or keywords to steer what gets surfaced.

---

## Focus areas (priorities)
1. **ML / AI for alpha** — machine learning, deep learning, RL, LLMs for signal
   generation, forecasting, alpha mining, feature engineering.
2. **Microstructure & execution** — market microstructure, order flow, Kyle/PIN-type
   models, optimal execution, market making, HFT, transaction-cost analysis.
3. **Risk & portfolio** — factor models, portfolio construction, risk management,
   regime detection, drawdown/crash mitigation.
4. **Asset class / market** — equities, futures, FX, crypto, options & derivatives.
   *(User to refine which markets matter most — add notes here.)*

---

## Sources to scan (in priority order)
- **arXiv** q-fin categories: `q-fin.TR` (trading & microstructure), `q-fin.PM`
  (portfolio mgmt), `q-fin.ST` (statistical finance), `q-fin.CP` (computational),
  `q-fin.RM` (risk), plus `econ.GN`, `cs.LG`, `stat.ML` when finance-applied.
- **SSRN** — finance working papers (factor research, microstructure).
- **Scholar Gateway (MCP)** — academic search across journals.
- **GitHub** — high-star quant repos, new strategy/library releases.
- **Quant blogs / newsletters** — practitioner writeups, firm research notes.

---

## Global players to track
Firms, labs, and authors whose output is worth following. Grow this list over time.

| Player | Type | Why track |
| --- | --- | --- |
| Zura Kakushadze (Quantigic Solutions) | Author/firm | Alpha formulas, factor models |
| Guido Baltussen / Robeco | Author/firm | Factor & momentum research |
| AQR Capital | Firm | Factor investing, academic-grade research |
| Two Sigma / Jane Street / Jump | Firm | ML, microstructure, execution (public writeups) |
| Marcos López de Prado | Author | ML for finance, backtesting pitfalls |
| _add your own…_ | | |

---

## Seed examples — the quality bar
These are reference items the user flagged as the *kind* of research that is
beneficial. New findings should be at least this useful, novel, or actionable.

1. **101 Formulaic Alphas** — Zura Kakushadze (Quantigic Solutions), Dec 2015.
   Explicit alpha formulas that double as executable code. *Focus: ML/alpha.*
   arXiv: https://arxiv.org/abs/1601.00991
2. **Momentum factor investing: Evidence and evolution** — Baltussen, Dom, Van Vliet,
   Vidojevic, Oct 2025. Momentum's evolution from price-based to fundamental/
   network-based trends; risk-managed momentum. *Focus: risk/portfolio.*
3. **je-suis-tm/quant-trading** — GitHub, ~10k★. Python implementations of many
   strategies (Bollinger, MACD, pair trading, Monte Carlo, London Breakout, etc.).
   *Focus: resources/code/skills.* https://github.com/je-suis-tm/quant-trading
4. **Insider and stealth trading with dynamic legal risk** — Qiao & Xia, 2026
   (arXiv econ.GN). Continuous-time Kyle-type model with dynamic legal risk.
   *Focus: microstructure/execution.*

---

## Keywords to boost
`alpha mining`, `optimal execution`, `market making`, `factor timing`, `regime
detection`, `reinforcement learning trading`, `limit order book`, `transaction cost`,
`deflated Sharpe`, `combinatorial purged CV`, `Kyle model`, `cross-sectional momentum`.

## Exclusions / noise to drop
Marketing/listicle content, paywalled-with-no-abstract items, get-rich-quick blogs,
re-posts of already-captured papers (see `INDEX.md` ledger).
