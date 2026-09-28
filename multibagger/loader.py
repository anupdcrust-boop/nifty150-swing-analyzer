"""Loads a StockDossier from a plain JSON dict (see sample_data/*.json)."""

from .models import (
    StockDossier, FinancialSeries, MarketData, MoatSourceEvidence, MoatTrajectory,
    GovernancePillars, IndustryContext, IndustryPhase, ReturnBridgeAssumptions,
    VariantPerception, G3State, SourceTier,
)


def load_dossier(data: dict) -> StockDossier:
    fin = data["financials"]
    financials = FinancialSeries(
        years=fin["years"], revenue=fin["revenue"], ebitda=fin["ebitda"],
        depreciation=fin["depreciation"], interest_expense=fin["interest_expense"],
        pat=fin["pat"], ocf=fin["ocf"], capex=fin["capex"],
        net_fixed_assets=fin["net_fixed_assets"], cwip=fin["cwip"],
        net_working_capital=fin["net_working_capital"], total_debt=fin["total_debt"],
        cash_equiv=fin["cash_equiv"], net_worth=fin["net_worth"],
        dividend_paid=fin["dividend_paid"], tax_rate=fin["tax_rate"],
    )

    mkt = data["market"]
    market = MarketData(
        price=mkt["price"], market_cap_cr=mkt["market_cap_cr"], adtv_cr=mkt["adtv_cr"],
        shares_outstanding=mkt["shares_outstanding"],
        diluted_shares_outstanding=mkt["diluted_shares_outstanding"],
        sector_median_pe=mkt["sector_median_pe"], sector_median_pb=mkt["sector_median_pb"],
        ten_year_gsec_yield=mkt["ten_year_gsec_yield"], gsec_date=mkt["gsec_date"],
        forward_eps=mkt.get("forward_eps"), book_value_per_share=mkt.get("book_value_per_share"),
    )

    moat_sources = [
        MoatSourceEvidence(
            name=m["name"], rating=m["rating"],
            trajectory=MoatTrajectory[m["trajectory"]],
            evidence_tier=SourceTier[m["evidence_tier"]],
            evidence_note=m.get("evidence_note", ""),
        )
        for m in data["moat_sources"]
    ]

    gov = data["governance"]
    governance = GovernancePillars(
        related_party_conduct=gov["related_party_conduct"],
        board_audit_independence=gov["board_audit_independence"],
        ownership_transparency=gov["ownership_transparency"],
        capital_allocation_discipline=gov["capital_allocation_discipline"],
        management_stability=gov["management_stability"],
        leverage_pledge_legal=gov["leverage_pledge_legal"],
        earnings_quality=gov["earnings_quality"],
        kill_gate_fired=gov.get("kill_gate_fired", False),
        kill_gate_reason=gov.get("kill_gate_reason", ""),
        section_20a_pattern_escalation=gov.get("section_20a_pattern_escalation", False),
        promoter_pledge_pct=gov.get("promoter_pledge_pct", 0.0),
        promoter_holding_pct=gov.get("promoter_holding_pct", 0.0),
        promoter_holding_3y_direction=gov.get("promoter_holding_3y_direction", "STABLE"),
        open_market_promoter_buying=gov.get("open_market_promoter_buying", False),
    )

    ind = data["industry_context"]
    industry_context = IndustryContext(
        phase=IndustryPhase[ind["phase"]], phase_evidence=ind["phase_evidence"],
        addressable_profit_pool_cr=ind.get("addressable_profit_pool_cr"),
        current_profit_share_pct=ind.get("current_profit_share_pct"),
        is_consolidating_duopoly_leader=ind.get("is_consolidating_duopoly_leader", False),
        share_gain_3y_vs_sector=ind.get("share_gain_3y_vs_sector"),
    )

    ba = data["bridge_assumptions"]
    bridge_assumptions = ReturnBridgeAssumptions(
        target_multiple=ba["target_multiple"], horizon_years=ba["horizon_years"],
        assumed_exit_pe=ba["assumed_exit_pe"],
        own_10y_75th_pctile_pe=ba.get("own_10y_75th_pctile_pe"),
        sector_10y_75th_pctile_pe=ba.get("sector_10y_75th_pctile_pe"),
        annual_dilution_rate=ba.get("annual_dilution_rate", 0.0),
        margin_delta_evidenced=ba.get("margin_delta_evidenced", False),
        assumed_margin_delta_cagr=ba.get("assumed_margin_delta_cagr", 0.0),
        margin_delta_mechanism_note=ba.get("margin_delta_mechanism_note", ""),
    )

    vp = data.get("variant_perception", {})
    variant_perception = VariantPerception(
        market_belief=vp.get("market_belief", ""),
        whats_wrong_with_belief=vp.get("whats_wrong_with_belief", ""),
        persistence_mechanism=vp.get("persistence_mechanism", ""),
        m3_edge=vp.get("m3_edge", ""),
        gap_closing_event=vp.get("gap_closing_event", ""),
        reverse_dcf_implied_growth=vp.get("reverse_dcf_implied_growth"),
        answered=vp.get("answered", False),
    )

    return StockDossier(
        symbol=data["symbol"], name=data["name"], sector=data["sector"], industry=data["industry"],
        financials=financials, market=market, moat_sources=moat_sources, governance=governance,
        industry_context=industry_context, bridge_assumptions=bridge_assumptions,
        variant_perception=variant_perception, g3_state=G3State[data["g3_state"]],
        candidate_source=data.get("candidate_source", "systematic_screen"),
        is_turnaround=data.get("is_turnaround", False),
        is_regulated_utility_or_bfsi=data.get("is_regulated_utility_or_bfsi", False),
        m5_protocol_complete=data.get("m5_protocol_complete", False),
        notes=data.get("notes", ""),
    )
