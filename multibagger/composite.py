"""Orchestration layer: runs Stage 1 gates, Section 5/5b-T/5e/5f/6A/6B, Part 7
N1/N7, MQF, and the consolidated Multibagger Candidate Gate table, then
resolves the Part 6 Engine x Price matrix placement and a sizing figure.

Where the source PDF leaves a judgement call to the analyst (e.g. exactly how
"price vs the bridge" is measured), this module makes an explicit, documented
choice rather than silently guessing — see the docstring on `price_vs_bridge`.
"""

from dataclasses import dataclass, field

from .models import StockDossier, MoatTrajectory
from . import gates as G
from . import engine as E
from . import moat as M
from . import mqf as MQF


@dataclass
class GateRow:
    name: str
    source: str
    passed: bool
    detail: str
    hard_fail: bool  # RED row: caps below Steady Compounder / at WATCH


@dataclass
class EvaluationResult:
    symbol: str
    stage1_findings: list
    hard_discard: bool
    moat: M.MoatClassResult
    moat_trajectory_gate: bool
    engine_growth: E.EngineGrowthResult
    return_bridge: E.ReturnBridgeResult
    industry_phase_clears: bool
    industry_phase_detail: str
    runway: E.RunwayResult
    mqf: MQF.MQFResult
    gate_table: list[GateRow]
    gates_passed: int
    gates_total: int
    engine_verdict: str  # STRONG / PARTIAL / WEAK
    compounder_tier: str
    price_vs_bridge: str  # BELOW / AT / ABOVE
    final_call: str  # BUY / ACCUMULATE / WATCH / AVOID / SKIP
    position_size_pct_range: tuple[float, float]
    market_cap_band: str
    notes: list[str] = field(default_factory=list)


def price_vs_bridge(entry_pe: float, revenue_cagr_3y: float | None) -> str:
    """Implementation choice (not specified verbatim by the PDF): the PDF's
    Engine x Price matrix treats "engine strength" and "price vs what the
    engine can deliver" as two INDEPENDENT axes. v2.2 fix (found via
    cross-sector backtest -- see FRAMEWORK_v2.2.md): an earlier version of
    this function reused the same engine-growth-vs-N1-target ratio for both
    axes, which made them perfectly correlated and silently deleted the
    "ENGINE WEAK, price BELOW bridge -> value candidate, up to 3%" cell the
    PDF's matrix explicitly keeps open. This version scores price against
    what the business has ALREADY demonstrated (a Peter Lynch PEG=1 style
    heuristic: fair PE ~= trailing 3yr revenue CAGR in percentage points,
    bounded to a sane range) rather than against an aspirational N1 target,
    so a name can be "cheap" on this axis independent of whether its engine
    clears an ambitious multi-year bridge.
    """
    if revenue_cagr_3y is None:
        return "ABOVE"
    fair_pe = min(max(revenue_cagr_3y * 100, 8.0), 60.0)
    ratio = entry_pe / fair_pe
    if ratio <= 0.85:
        return "BELOW"
    if ratio <= 1.15:
        return "AT"
    return "ABOVE"


def build_gate_table(
    engine_growth: E.EngineGrowthResult,
    required_revenue_cagr: float,
    moat_trajectory_gate: bool,
    runway: E.RunwayResult,
    industry_phase_clears: bool,
    industry_phase_detail: str,
    promoter_alignment_clear: bool,
    return_bridge: E.ReturnBridgeResult,
    variant_perception_complete: bool,
    mqf_result: MQF.MQFResult,
) -> list[GateRow]:
    rows = []

    # v2.2 (PILOT, found via cross-sector backtest -- see FRAMEWORK_v2.2.md):
    # this row was a binary hard-fail, unlike G3/MQF elsewhere in the suite
    # which grade on multi-state bands. Backtesting six real, hindsight-
    # confirmed multibaggers showed several land within a modest margin of
    # clearing (ratio 0.80-1.00) -- close enough that treating it identically
    # to a name with no engine at all (ratio near zero) throws away signal.
    # A near-miss now soft-fails (routes to Steady Compounder, same as an
    # ORANGE moat-trajectory miss) rather than hard-failing to WEAK/IGNORE.
    g = engine_growth.engine_growth_g
    engine_ratio = (g / required_revenue_cagr) if (g is not None and required_revenue_cagr > 0) else 0.0
    engine_clears = engine_ratio >= 1.0
    engine_near_miss = 0.80 <= engine_ratio < 1.0
    rows.append(GateRow(
        "Engine growth clears requirement", "5e", engine_clears,
        f"g={_pct(g)} vs required revenue-driven CAGR {_pct(required_revenue_cagr)} "
        f"(margin-delta term handled separately by 6A)"
        + (" -- NEAR-MISS (>=80% of requirement): soft-fail, caps at Steady Compounder" if engine_near_miss else ""),
        hard_fail=not engine_clears and not engine_near_miss,
    ))

    roiic_floor = not engine_growth.roiic_below_cost_of_capital_2y
    rows.append(GateRow("ROIIC floor", "5e", roiic_floor,
                         "ROIIC above cost of capital, 2 consecutive years" if roiic_floor else "ROIIC below cost of capital 2yrs — hard fail", not roiic_floor))

    rows.append(GateRow("Payout ceiling", "5e", engine_growth.gate_payout_ceiling_clears,
                         f"3yr avg payout {_pct(engine_growth.payout_3y_avg)}", not engine_growth.gate_payout_ceiling_clears))

    rows.append(GateRow("Moat trajectory", "5b-T", moat_trajectory_gate,
                         "BUILDING on >=1 source, Tier 1-3" if moat_trajectory_gate else "No qualifying BUILDING source", not moat_trajectory_gate))

    rows.append(GateRow("Runway / profit pool", "6B", runway.clears, runway.message, not runway.clears))

    rows.append(GateRow("Industry phase", "6A", industry_phase_clears, industry_phase_detail, not industry_phase_clears))

    rows.append(GateRow("Promoter alignment", "5f", promoter_alignment_clear,
                         "No open Gate 1/2 flag" if promoter_alignment_clear else "Open alignment flag unexplained", not promoter_alignment_clear))

    bridge_clears = (
        return_bridge.earnings_dominance_clears
        and return_bridge.dilution_honesty_clears
        and return_bridge.exit_multiple_ceiling_clears
    )
    rows.append(GateRow("Return bridge closes", "N1", bridge_clears,
                         f"earnings share {_pct(return_bridge.earnings_share_of_log_return)}, dominance {'OK' if return_bridge.earnings_dominance_clears else 'FAIL'}, exit ceiling {'OK' if return_bridge.exit_multiple_ceiling_clears else 'FAIL'}", not bridge_clears))

    rows.append(GateRow("Variant perception complete", "N7", variant_perception_complete,
                         "All four questions answered, reverse DCF run" if variant_perception_complete else "Incomplete — caps at WATCH", not variant_perception_complete))

    mqf_clears = MQF.clears_engine_compounder_mos_gate(mqf_result)
    rows.append(GateRow("MQF governance", "Part 4", mqf_clears,
                         f"{mqf_result.effective_verdict} ({mqf_result.raw_composite:.1f}/100) — HIGH-TRUST required for Engine Compounder tier", not mqf_clears))

    return rows


def _pct(x: float | None) -> str:
    return f"{x*100:.1f}%" if x is not None else "n/a"


def evaluate(d: StockDossier, target_market_cap_multiplier_from_entry: float | None = None) -> EvaluationResult:
    stage1 = G.run_all_gates(d)
    discard = G.hard_discard(stage1)

    moat_result = M.classify_moat(d.moat_sources)
    moat_traj_gate = M.moat_trajectory_gate_clears(d.moat_sources)

    engine_growth = E.compute_engine_growth(d)

    entry_pe = d.market.price / (d.financials.pat[-1] / d.market.diluted_shares_outstanding) if d.financials.pat[-1] > 0 else d.bridge_assumptions.assumed_exit_pe
    bridge = E.compute_return_bridge(d, entry_pe)

    phase_clears, phase_detail = E.industry_phase_gate_clears(d, d.industry_context.share_gain_3y_vs_sector)

    target_mcap = d.market.market_cap_cr * d.bridge_assumptions.target_multiple
    runway = E.compute_runway_gate(d, target_mcap)

    mqf_result = MQF.evaluate_mqf(d.governance)

    promoter_alignment_clear = d.governance.promoter_holding_3y_direction != "FALLING" or d.governance.open_market_promoter_buying

    gate_table = build_gate_table(
        engine_growth,
        bridge.required_revenue_cagr,
        moat_traj_gate,
        runway,
        phase_clears,
        phase_detail,
        promoter_alignment_clear,
        bridge,
        d.variant_perception.answered,
        mqf_result,
    )

    gates_passed = sum(1 for r in gate_table if r.passed)
    gates_total = len(gate_table)
    hard_fails = [r for r in gate_table if r.hard_fail]

    if gates_passed == gates_total:
        engine_verdict = "STRONG"
    elif len(hard_fails) == 0:
        engine_verdict = "PARTIAL"
    else:
        engine_verdict = "WEAK"

    pvb = price_vs_bridge(entry_pe, d.financials.revenue_cagr_3y)

    compounder_tier, final_call, size_range = _resolve_tier_and_sizing(
        discard, engine_verdict, pvb, mqf_result, moat_result, d
    )

    notes = []
    if d.is_regulated_utility_or_bfsi:
        notes.append(
            "GAP (v2.2): Section 5e's ROIIC/RR formula (net fixed assets + CWIP + NWC as invested "
            "capital) is a manufacturing/services model and does not describe a BFSI balance sheet, "
            "where the 'invested capital' that compounds is the loan book funded by borrowings. "
            "The engine-growth figures below are computed for completeness but should not be trusted "
            "for this name — see FRAMEWORK_v2.2.md for the proposed BFSI-variant test (incremental "
            "spread income / incremental AUM, book-value-per-share CAGR, credit-cost-adjusted ROE)."
        )
    if discard:
        notes.append("Stage 1 hard discard fired (G0/G1/G2/G3-A/G3-C) — no tier above SKIP is reachable regardless of Part 7 results.")
    if mqf_result.kill_gate_fired:
        notes.append(f"MQF kill-gate fired: {d.governance.kill_gate_reason}")
    if not d.variant_perception.answered:
        notes.append("N7 variant perception incomplete — capped at WATCH per M3 regardless of composite.")

    return EvaluationResult(
        symbol=d.symbol,
        stage1_findings=stage1,
        hard_discard=discard,
        moat=moat_result,
        moat_trajectory_gate=moat_traj_gate,
        engine_growth=engine_growth,
        return_bridge=bridge,
        industry_phase_clears=phase_clears,
        industry_phase_detail=phase_detail,
        runway=runway,
        mqf=mqf_result,
        gate_table=gate_table,
        gates_passed=gates_passed,
        gates_total=gates_total,
        engine_verdict=engine_verdict,
        compounder_tier=compounder_tier,
        price_vs_bridge=pvb,
        final_call=final_call,
        position_size_pct_range=size_range,
        market_cap_band=E.market_cap_band(d.market.market_cap_cr),
        notes=notes,
    )


def _resolve_tier_and_sizing(
    discard: bool,
    engine_verdict: str,
    pvb: str,
    mqf_result: MQF.MQFResult,
    moat_result: M.MoatClassResult,
    d: StockDossier,
) -> tuple[str, str, tuple[float, float]]:
    if discard or mqf_result.effective_verdict == "AVOID":
        return "SKIP", "AVOID", (0.0, 0.0)

    if not d.variant_perception.answered:
        return "WATCH", "WATCH", (0.0, 1.0)

    if not MQF.clears_any_multibagger_sizing_gate(mqf_result):
        return "WATCHLIST — GOVERNANCE-CAPPED", "WATCH", (0.0, 1.0)

    # Engine x Price matrix (Part 6)
    if engine_verdict == "STRONG":
        if pvb == "BELOW":
            return "MULTIBAGGER CANDIDATE", "BUY", (5.0, 8.0)
        if pvb == "AT":
            return "STEADY COMPOUNDER", "ACCUMULATE", (3.0, 5.0)
        return "WATCH", "WATCH", (0.0, 1.0)

    if engine_verdict == "PARTIAL":
        if pvb == "BELOW":
            return "STEADY COMPOUNDER", "ACCUMULATE", (2.0, 4.0)
        return "WATCH", "WATCH", (0.0, 1.0)

    # WEAK
    if pvb == "BELOW":
        return "SPECULATIVE / VALUE PATH ONLY", "WATCH", (0.0, 2.0)
    return "IGNORE", "AVOID", (0.0, 0.0)
