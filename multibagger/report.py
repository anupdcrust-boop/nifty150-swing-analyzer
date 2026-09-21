"""Part 6 — Final Call Block, formatted per the framework's mandatory template."""

from .models import StockDossier
from .composite import EvaluationResult


def final_call_block(d: StockDossier, r: EvaluationResult) -> str:
    eg = r.engine_growth
    rb = r.return_bridge
    lines = [
        f"FINAL CALL: {r.final_call}",
        f"Compounder tier: {r.compounder_tier}",
        f"Engine verdict: {r.engine_verdict} — consolidated gates passed [{r.gates_passed} of {r.gates_total}]",
        f"Return bridge (N1): {d.bridge_assumptions.target_multiple:.1f}x / {d.bridge_assumptions.horizon_years}yrs "
        f"= {rb.required_annualised_return*100:.1f}% p.a. -> EPS CAGR {rb.required_eps_cagr*100:.1f}% x "
        f"re-rating {rb.rerating_cagr*100:.1f}% | earnings share {rb.earnings_share_of_log_return*100:.1f}%",
        f"Engine growth (5e): ROIIC {_p(eg.roiic)} x RR {_p(eg.reinvestment_rate)} = {_p(eg.engine_growth_g)} "
        f"vs {rb.required_revenue_cagr*100:.1f}% required revenue-driven CAGR "
        f"(margin-delta term {rb.margin_delta_cagr_applied*100:.1f}% handled separately by 6A) — "
        f"{'CLEARS' if (eg.engine_growth_g or 0) >= rb.required_revenue_cagr else 'FAILS'}",
        f"Moat class (5b): {r.moat.moat_class} — MATM anchor applied {r.moat.trajectory_conditioned_matm:.2f}x",
        f"Runway/profit pool (6B): {r.runway.message}",
        f"Industry phase (6A): {r.industry_phase_detail}",
        f"MQF governance: {r.mqf.effective_verdict} ({r.mqf.raw_composite:.1f}/100) — {r.mqf.sizing_note}",
        f"Position: Reconciled {r.position_size_pct_range[0]:.1f}-{r.position_size_pct_range[1]:.1f}%  "
        f"| Market-cap band: {r.market_cap_band}",
        f"Price vs bridge: {r.price_vs_bridge}",
    ]
    if r.notes:
        lines.append("Notes: " + " | ".join(r.notes))
    hard_fail_rows = [g.name for g in r.gate_table if g.hard_fail]
    if hard_fail_rows:
        lines.append("Failed gates: " + ", ".join(hard_fail_rows))
    return "\n".join(lines)


def gate_table_markdown(r: EvaluationResult) -> str:
    out = ["| Gate | Source | Status | Detail |", "|---|---|---|---|"]
    for row in r.gate_table:
        status = "PASS" if row.passed else ("HARD FAIL" if row.hard_fail else "soft fail")
        out.append(f"| {row.name} | {row.source} | {status} | {row.detail} |")
    return "\n".join(out)


def _p(x):
    return f"{x*100:.1f}%" if x is not None else "n/a"
