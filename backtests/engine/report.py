"""Render a BacktestResult to a Markdown report matching the repo schema."""
from __future__ import annotations

from .pipeline import BacktestResult


def render(res: BacktestResult, date: str, idea_source: str = "") -> str:
    synth_banner = ""
    if res.is_synthetic:
        synth_banner = (
            "> ⚠️ **SYNTHETIC DATA — NOT A REAL RESULT.** Yahoo/data feed was "
            "unreachable, so this run used a generated series purely to verify the "
            "pipeline. Allowlist a data domain (see backtests/README.md) for real "
            "numbers.\n\n")

    def row(label, m):
        return (f"| {label} | {m.get('sharpe','-')} | {m.get('cagr','-')} | "
                f"{m.get('max_drawdown','-')} | {m.get('deflated_sharpe_prob','-')} | "
                f"{m.get('n_periods','-')} |")

    lines = [
        f"# Backtest Report — {res.strategy} on {res.symbol} — {date}",
        "",
        synth_banner.rstrip(),
        "" if not synth_banner else "",
        f"**Idea source:** {idea_source or 'manual'}  ",
        f"**Verdict:** {res.verdict}  ",
        f"**Best params (stage-1 winner):** `{res.best_params}`  ",
        f"**Data source:** {res.source}",
        "",
        "## Metrics",
        "| Split | Sharpe | CAGR | MaxDD | Deflated-SR prob | Periods |",
        "| --- | --- | --- | --- | --- | --- |",
        row("Train (in-sample, best of grid)", res.train),
        row("Test (out-of-sample, realistic costs)", res.test),
        row("Full sample (winner)", res.full),
        "",
        "## Stage-1 sweep (top configurations on train)",
        "| Rank | Params | Sharpe | CAGR | MaxDD | Deflated-SR prob |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    # Stage-1 leaderboard lives on res.train only as the winner; include if attached.
    leaderboard = getattr(res, "leaderboard", None)
    if leaderboard:
        for i, r in enumerate(leaderboard[:5], 1):
            lines.append(f"| {i} | `{r['params']}` | {r['sharpe']} | {r['cagr']} | "
                         f"{r['max_drawdown']} | {r['deflated_sharpe_prob']} |")
    else:
        lines.append(f"| 1 | `{res.best_params}` | {res.train.get('sharpe','-')} | "
                     f"{res.train.get('cagr','-')} | {res.train.get('max_drawdown','-')} | "
                     f"{res.train.get('deflated_sharpe_prob','-')} |")

    lines += [
        "",
        "## Notes & caveats",
        *[f"- {n}" for n in res.notes],
        "",
        "## Interpretation",
        "- **Deflated-SR prob** is the probability the true Sharpe > 0 after "
        "penalising for the number of configurations tested. Treat < 0.95 as "
        "\"not convincingly better than luck.\"",
        "- A result is only worth advancing if it **survives the out-of-sample "
        "split** with positive Sharpe *and* passes the deflated-SR gate.",
    ]
    return "\n".join(l for l in lines if l is not None)
