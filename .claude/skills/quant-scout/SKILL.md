---
name: quant-scout
description: Scout the quant world for new research, techniques, skills, and open-source resources used by top global players, then write a dated, cited, deduplicated digest into research/digests/ and commit it. Use when the user wants to survey recent quant/trading research or refresh the knowledge base.
argument-hint: "[focus-area]   (alpha | microstructure | risk | asset-class; empty = all)"
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Bash(git *), mcp__Scholar_Gateway__authenticate, mcp__Scholar_Gateway__complete_authentication
model: claude-opus-4-8
---

# Quant Scout

You are the research-scouting engine for a trading-augmentation system. Your job is
to find the **most beneficial new quant research, techniques, skills, and resources**
that top global players are producing, then record them as a structured, cited,
deduplicated digest.

`$ARGUMENTS` (optional) = a single focus area to target this run. If empty, sweep all
focus areas. Accepted values: `alpha`, `microstructure`, `risk`, `asset-class`.

## Step 1 — Load state
1. Read `research/watchlist.md` — focus areas, sources, tracked players, keywords,
   exclusions, and the seed examples that define the quality bar.
2. Read `research/INDEX.md` — the digest log (to find the last run date for recency)
   and the dedupe ledger (so you never re-surface a captured item).
3. Set the time window: prefer items newer than the last digest date; if this is the
   first run, use a trailing ~30 days (but seed examples in the watchlist may be older
   and are allowed as foundational references).

## Step 2 — Scout (deep, multi-source)
Run **deep, fanned-out research**. If a `deep-research` skill/harness is available,
use it; otherwise drive `WebSearch` + `WebFetch` + the Scholar Gateway MCP directly.
For each focus area in scope, search across the watchlist sources, in priority order:
- **arXiv** q-fin categories (q-fin.TR / PM / ST / CP / RM), plus econ.GN, cs.LG, stat.ML when finance-applied.
- **SSRN** finance working papers.
- **Scholar Gateway (MCP)** — academic search. If it returns an auth error, call
  `mcp__Scholar_Gateway__authenticate` once, surface the link to the user, and continue
  with other sources rather than blocking the whole run.
- **GitHub** — new/updated high-star quant repos, libraries, datasets.
- **Quant blogs / newsletters / firm research notes.**

Follow the watchlist **players** first (e.g. Kakushadze/Quantigic, Baltussen/Robeco,
AQR, López de Prado). Use the boosted keywords. Aim for ~8–15 strong candidates total.

## Step 3 — Filter & verify
For each candidate:
- **Dedupe**: skip if its fingerprint (normalized title + primary author/source, or
  canonical URL) already appears in the `research/INDEX.md` ledger.
- **Verify**: confirm the source is real — a working link, a genuine abstract, real
  authors. Drop items you cannot verify.
- **Score 1–5** on each axis: **Novelty · Credibility · Relevance-to-focus · Actionability.**
- Drop low-signal items (sum clearly below the bar) and anything in the watchlist exclusions.

## Step 4 — Write the digest
Create `research/digests/<TODAY>-quant-scout.md` (date = `YYYY-MM-DD`, today's date)
using exactly this schema:

```markdown
# Quant Scout Digest — YYYY-MM-DD

## TL;DR
- (top 3–5 findings, one line each, with the single sharpest takeaway)

## Findings by focus area

### ML / AI for alpha
- **Title** — authors/source, date — [link](url)
  - **What it is:** key idea in 1–2 sentences.
  - **Why it matters for trading:** concrete relevance.
  - **Scores:** Novelty x/5 · Credibility x/5 · Relevance x/5 · Actionability x/5
  - **Next step:** read / replicate / backtest / shelve

### Microstructure & execution
(same item format)

### Risk & portfolio
(same item format)

### Asset class / market
(same item format)

## New resources & tooling
- repos / datasets / libraries — [link](url) — one line on what it gives you.

## Watchlist updates
- new players/sources/authors discovered this run worth adding to watchlist.md

## Open questions / threads to pull next run
- promising leads not fully chased this run.
```

Only include focus-area sections that are in scope for this run; omit empty sections
or write `_no notable new findings this run_`.

## Step 5 — Update the ledger
Edit `research/INDEX.md`:
- Prepend a row to the **Digest log** table: date, digest filename (as a link),
  number of findings, and a short highlights phrase.
- Append one line per captured finding to the **Dedupe ledger**:
  `- [YYYY-MM-DD] <fingerprint> | <url>`

If you discovered strong new players/sources, also append them to
`research/watchlist.md` (Global players table or Sources list).

## Step 6 — Commit & push
```bash
git add research/ && \
git commit -m "research: quant-scout digest <TODAY>" && \
git push -u origin claude/trading-ai-research-prompt-e3v01m
```
On network failure, retry with exponential backoff (2s, 4s, 8s, 16s). Do **not** open
a PR. Then report a short summary to the user: how many findings, the top 2–3, and the
digest path.

## Quality bar
Match or exceed the seed examples in `research/watchlist.md` (101 Formulaic Alphas;
Momentum factor evolution; je-suis-tm/quant-trading; Kyle-type microstructure with
legal risk). Prefer specific, implementable, credible work over generic commentary.
Never fabricate a paper, author, link, or result — if unsure, omit it.
