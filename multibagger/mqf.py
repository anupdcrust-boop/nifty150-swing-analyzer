"""Part 4 — Management Quality & Forensic Governance, MQF v1.1.

Pillar scores (0-10) are analyst judgement from Tier 1-3 evidence; this
module applies the framework's weighting formula, kill-gates and the two
caps (Section 20A pattern escalation, single-pillar floor) mechanically.
"""

from dataclasses import dataclass

from .models import GovernancePillars

_WEIGHTS = {
    "related_party_conduct": 0.25,
    "board_audit_independence": 0.20,
    "ownership_transparency": 0.15,
    "capital_allocation_discipline": 0.10,
    "management_stability": 0.10,
    "leverage_pledge_legal": 0.10,
    "earnings_quality": 0.10,
}


@dataclass
class MQFResult:
    raw_composite: float  # 0-100
    effective_verdict: str  # HIGH-TRUST / ACCEPTABLE / ELEVATED / AVOID
    kill_gate_fired: bool
    single_pillar_floor_applied: bool
    section_20a_cap_applied: bool
    sizing_note: str


def evaluate_mqf(g: GovernancePillars) -> MQFResult:
    composite = sum(getattr(g, k) * w for k, w in _WEIGHTS.items()) * 10

    if g.kill_gate_fired:
        return MQFResult(composite, "AVOID", True, False, False, f"Kill-gate: {g.kill_gate_reason} — not investable")

    verdict = _band_from_score(composite)

    single_pillar_floor = min(getattr(g, k) for k in _WEIGHTS) <= 3
    if single_pillar_floor and verdict == "HIGH-TRUST":
        verdict = "ACCEPTABLE"

    section_20a = g.section_20a_pattern_escalation
    if section_20a and verdict in ("HIGH-TRUST", "ACCEPTABLE"):
        verdict = "ELEVATED"

    sizing = {
        "HIGH-TRUST": "No governance-based size constraint",
        "ACCEPTABLE": "Position size capped; re-run RPT/pledge/litigation every 2Q",
        "ELEVATED": "Stage 2 sizing capped at WATCHLIST. Tracking position at most",
        "AVOID": "Not investable irrespective of valuation, growth or engine score",
    }[verdict]

    return MQFResult(composite, verdict, False, single_pillar_floor, section_20a, sizing)


def _band_from_score(score: float) -> str:
    if score >= 85:
        return "HIGH-TRUST"
    if score >= 65:
        return "ACCEPTABLE"
    if score >= 45:
        return "ELEVATED"
    return "AVOID"


def clears_engine_compounder_mos_gate(result: MQFResult) -> bool:
    return result.effective_verdict == "HIGH-TRUST"


def clears_any_multibagger_sizing_gate(result: MQFResult) -> bool:
    return result.effective_verdict in ("HIGH-TRUST", "ACCEPTABLE")
