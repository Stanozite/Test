# Quant Scout

An AI research-scouting system that augments trading by regularly surveying the
quant world — research papers, advanced techniques, skills, and open-source
resources that top global players use — and turning them into a durable, growing,
cited knowledge base.

This is **component #1** of a larger trading-augmentation system: the *intelligence
gathering* layer.

## Quickstart

1. Open this repo in Claude Code.
2. Run the scout on demand:
   ```
   /quant-scout
   ```
   Or target one focus area:
   ```
   /quant-scout microstructure
   ```
3. Run it on a recurring schedule — see **Recurring runs** below.

Each run reads `research/watchlist.md` + `research/INDEX.md`, performs deep
multi-source research (arXiv, SSRN, Scholar Gateway, GitHub, quant blogs),
deduplicates against past findings, and writes a dated digest to
`research/digests/YYYY-MM-DD-quant-scout.md`, then commits & pushes.

## Layout

```
.claude/skills/quant-scout/SKILL.md   # the /quant-scout command (core prompt)
.claude/loop.md                        # default recurring prompt
research/watchlist.md                  # tunable config: focus areas, sources, players
research/INDEX.md                      # log of all digests + dedupe ledger
research/digests/                      # one dated digest per run
CLAUDE.md                              # persistent project context
```

## Recurring runs

The scout is meant to run *regularly*. Pick the path that matches how you run Claude Code:

### A. Scheduled session on Claude Code web (recommended — hands-off)
A scheduled trigger spins up a fresh container on a schedule and runs a prompt, with
**no session left open**. This survives container reclamation, so it's the right fit for
a daily scout.

1. In the Claude Code web app, open this repo's environment / automation settings.
2. Create a **scheduled session** (recurring trigger) with the prompt:
   ```
   /quant-scout
   ```
3. Set the cadence (e.g. daily) and target branch
   `claude/trading-ai-research-prompt-e3v01m`.

Each scheduled run reads `research/watchlist.md` + `research/INDEX.md`, dedupes, writes a
dated digest, and commits/pushes on its own. Docs:
https://code.claude.com/docs/en/claude-code-on-the-web

### B. Local `/loop` (session must stay open)
If you run Claude Code locally (desktop/CLI) and keep a session running:
```
/loop 1d /quant-scout
```
Note: `/loop` only fires while the session is open, and each loop task auto-expires after
7 days — so this needs a long-lived local session, not a remote web session.

## Tuning

Edit `research/watchlist.md` to add players (firms/authors/labs), sources, arXiv
categories, or focus areas. The scout reads it every run, so changes take effect
immediately.
