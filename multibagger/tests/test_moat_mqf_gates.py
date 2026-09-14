from multibagger.models import MoatSourceEvidence, MoatTrajectory, SourceTier, GovernancePillars, G3State
from multibagger.moat import classify_moat, moat_trajectory_gate_clears
from multibagger.mqf import evaluate_mqf
from multibagger import gates as G
from .fixtures import make_dossier


def test_moat_class_table():
    def src(rating, traj=MoatTrajectory.HOLDING):
        return MoatSourceEvidence("x", rating, traj, SourceTier.T2_FILING)

    assert classify_moat([]).moat_class == "NONE"
    assert classify_moat([src("GREEN")]).moat_class == "NARROW"
    assert classify_moat([src("GREEN"), src("GREEN")]).moat_class == "MODERATE"
    assert classify_moat([src("GREEN"), src("GREEN"), src("GREEN")]).moat_class == "WIDE"


def test_moat_eroding_caps_matm_at_1x_regardless_of_class():
    sources = [
        MoatSourceEvidence("a", "GREEN", MoatTrajectory.ERODING, SourceTier.T2_FILING),
        MoatSourceEvidence("b", "GREEN", MoatTrajectory.ERODING, SourceTier.T2_FILING),
        MoatSourceEvidence("c", "GREEN", MoatTrajectory.ERODING, SourceTier.T2_FILING),
    ]
    result = classify_moat(sources)
    assert result.moat_class == "WIDE"
    assert result.trajectory_conditioned_matm == 1.00


def test_moat_trajectory_gate_requires_tier123_building():
    tier4_building = [MoatSourceEvidence("a", "GREEN", MoatTrajectory.BUILDING, SourceTier.T4_MANAGEMENT)]
    assert moat_trajectory_gate_clears(tier4_building) is False
    tier2_building = [MoatSourceEvidence("a", "GREEN", MoatTrajectory.BUILDING, SourceTier.T2_FILING)]
    assert moat_trajectory_gate_clears(tier2_building) is True


def test_mqf_composite_formula():
    g = GovernancePillars(
        related_party_conduct=9, board_audit_independence=9, ownership_transparency=9,
        capital_allocation_discipline=8, management_stability=8, leverage_pledge_legal=9,
        earnings_quality=8,
    )
    result = evaluate_mqf(g)
    expected = (9*0.25 + 9*0.20 + 9*0.15 + 8*0.10 + 8*0.10 + 9*0.10 + 8*0.10) * 10
    assert round(result.raw_composite, 2) == round(expected, 2)
    assert result.effective_verdict == "HIGH-TRUST"


def test_mqf_kill_gate_forces_avoid_regardless_of_score():
    g = GovernancePillars(
        related_party_conduct=10, board_audit_independence=10, ownership_transparency=10,
        capital_allocation_discipline=10, management_stability=10, leverage_pledge_legal=10,
        earnings_quality=10, kill_gate_fired=True, kill_gate_reason="Forensic audit ordered by regulator",
    )
    result = evaluate_mqf(g)
    assert result.effective_verdict == "AVOID"


def test_mqf_single_pillar_floor_caps_high_trust():
    # management_stability carries only 10% weight, so tanking it alone still
    # leaves the weighted composite in HIGH-TRUST range -- the single-pillar
    # floor exists precisely to catch this case.
    g = GovernancePillars(
        related_party_conduct=10, board_audit_independence=10, ownership_transparency=10,
        capital_allocation_discipline=10, management_stability=2, leverage_pledge_legal=10,
        earnings_quality=10,
    )
    result = evaluate_mqf(g)
    assert result.raw_composite >= 85  # would be HIGH-TRUST on weighted score alone
    assert result.effective_verdict == "ACCEPTABLE"  # single-pillar floor caps it


def test_g0_liquidity_discard():
    d = make_dossier()
    d.market.adtv_cr = 0.4
    finding = G.g0_liquidity(d)
    assert finding.passed is False
    assert finding.band == "RED"


def test_g2_earnings_exempt_for_turnaround():
    d = make_dossier()
    d.financials.pat = [-10, -20, -5]
    d.is_turnaround = True
    finding = G.g2_earnings(d)
    assert finding.passed is True  # exempted


def test_g3_a_is_hard_discard():
    d = make_dossier()
    d.g3_state.__class__  # sanity
    from multibagger.models import G3State
    d.g3_state = G3State.A
    findings = G.run_all_gates(d)
    assert G.hard_discard(findings) is True
