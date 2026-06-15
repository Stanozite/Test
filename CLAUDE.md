# CLAUDE.md — Quant Scout

## What this repo is
A research-scouting system that augments trading. It regularly surveys the quant
world (papers, techniques, skills, open-source resources used by top global
players) and accumulates a cited, deduplicated knowledge base under `research/`.

This is component #1 (intelligence gathering). Later components (idea→backtest
pipeline, strategy library, alerting) will build on the digest output.

## How to run
- `/quant-scout` — full sweep across all focus areas.
- `/quant-scout <focus>` — target one area (e.g. `microstructure`, `alpha`, `risk`, `asset-class`).
- `/loop 1d /quant-scout` — recurring daily scout (requires an open session; 7-day expiry per loop task).

## Conventions
- **Digests**: `research/digests/YYYY-MM-DD-quant-scout.md`, one per run, following
  the schema defined in `.claude/skills/quant-scout/SKILL.md`.
- **Scoring rubric** (each finding, 1–5): Novelty · Credibility · Relevance-to-focus · Actionability.
- **Dedupe**: before adding a finding, check it is not already in `research/INDEX.md`'s
  ledger. Fingerprint = normalized title + primary author/source (or canonical URL).
- **Config**: `research/watchlist.md` is the single tunable source of focus areas,
  sources, and tracked players. Read it every run.
- **Recency bias**: prefer items newer than the last digest date, or within a trailing ~30 days.

## Git
- Work on branch `claude/trading-ai-research-prompt-e3v01m`.
- Commit each digest run with message `research: quant-scout digest <date>`.
- Push with `git push -u origin claude/trading-ai-research-prompt-e3v01m` (retry with
  backoff on network errors). Do not open a PR unless explicitly asked.

## Reused capabilities (do not rebuild)
- `deep-research` bundled skill — fan-out search / fetch / verify / synthesize engine.
- `Scholar_Gateway` MCP — academic paper search (may need a one-time `authenticate`).
- `WebSearch` / `WebFetch` — general web + source fetching.
- `/loop` bundled skill — recurring scheduling.
