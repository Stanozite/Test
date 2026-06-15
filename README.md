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
3. Run it on a recurring schedule (while a session is open):
   ```
   /loop 1d /quant-scout
   ```

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

## Tuning

Edit `research/watchlist.md` to add players (firms/authors/labs), sources, arXiv
categories, or focus areas. The scout reads it every run, so changes take effect
immediately.
