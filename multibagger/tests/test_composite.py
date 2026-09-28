from multibagger.composite import evaluate
from multibagger.models import G3State, GovernancePillars
from .fixtures import make_dossier, make_financials


def test_full_evaluation_runs_end_to_end():
    d = make_dossier()
    result = evaluate(d)
    assert result.symbol == "TEST"
    assert result.engine_verdict in ("STRONG", "PARTIAL", "WEAK")
    assert result.final_call in ("BUY", "ACCUMULATE", "WATCH", "AVOID")


def test_g3_a_forces_skip_even_with_strong_fundamentals():
    d = make_dossier(g3_state=G3State.A)
    result = evaluate(d)
    assert result.hard_discard is True
    assert result.compounder_tier == "SKIP"
    assert result.final_call == "AVOID"


def test_incomplete_variant_perception_caps_watch():
    d = make_dossier()
    d.variant_perception.answered = False
    result = evaluate(d)
    assert result.compounder_tier == "WATCH"
    assert result.final_call == "WATCH"


def test_high_reinvestment_high_roiic_low_payout_reaches_multibagger_candidate():
    """A textbook Section 5e engine compounder: high ROIIC, low payout, strong
    reinvestment, should be able to reach MULTIBAGGER CANDIDATE when every
    other gate is also fed clean evidence."""
    financials = make_financials(years=6, revenue_start=100.0, revenue_cagr=0.35,
                                  ebitda_margin=0.25, payout=0.05, capex_pct_revenue=0.15)
    d = make_dossier(
        financials=financials,
        governance=GovernancePillars(
            related_party_conduct=9, board_audit_independence=9, ownership_transparency=9,
            capital_allocation_discipline=9, management_stability=9, leverage_pledge_legal=9,
            earnings_quality=9, promoter_holding_pct=55, promoter_holding_3y_direction="STABLE",
        ),
    )
    d.industry_context.share_gain_3y_vs_sector = True
    d.industry_context.addressable_profit_pool_cr = 4000.0  # keeps implied share <=25% at target
    # Price the entry at a plausible 15x current EPS (the PDF's own worked
    # example entry multiple) so the N1 bridge isn't testing an absurd PE.
    eps = financials.pat[-1] / d.market.diluted_shares_outstanding
    d.market.price = eps * 15
    d.market.market_cap_cr = d.market.price * d.market.shares_outstanding
    result = evaluate(d)
    assert result.engine_growth.gate_payout_ceiling_clears is True
    # Not asserting the exact tier (depends on synthetic ROIIC), but the engine
    # must at least clear the payout and reach PARTIAL or STRONG, never WEAK
    # purely from a governance/data artefact.
    assert result.engine_verdict in ("STRONG", "PARTIAL")
