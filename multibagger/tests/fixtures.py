"""Builds a fully-populated, editable StockDossier for tests."""

from multibagger.models import (
    StockDossier, FinancialSeries, MarketData, MoatSourceEvidence, MoatTrajectory,
    GovernancePillars, IndustryContext, IndustryPhase, ReturnBridgeAssumptions,
    VariantPerception, G3State, SourceTier,
)


def make_financials(years=5, revenue_start=100.0, revenue_cagr=0.20, ebitda_margin=0.20,
                     tax_rate=0.25, capex_pct_revenue=0.06, payout=0.20, debt_equity=0.3):
    yrs = list(range(2019, 2019 + years))
    revenue = [revenue_start * (1 + revenue_cagr) ** i for i in range(years)]
    ebitda = [r * ebitda_margin for r in revenue]
    depreciation = [r * 0.03 for r in revenue]
    interest = [r * 0.01 for r in revenue]
    pat = [(e - d - it) * (1 - tax_rate) for e, d, it in zip(ebitda, depreciation, interest)]
    ocf = [e * 0.85 for e in ebitda]
    capex = [r * capex_pct_revenue for r in revenue]
    nfa = [revenue_start * 2 * (1.1 ** i) for i in range(years)]
    cwip = [revenue_start * 0.1 for _ in range(years)]
    nwc = [r * 0.15 for r in revenue]
    total_debt = [r * debt_equity * 0.5 for r in revenue]
    cash = [r * 0.05 for r in revenue]
    net_worth = [r * 0.8 for r in revenue]
    dividend = [p * payout for p in pat]
    taxes = [tax_rate] * years

    return FinancialSeries(
        years=yrs, revenue=revenue, ebitda=ebitda, depreciation=depreciation,
        interest_expense=interest, pat=pat, ocf=ocf, capex=capex,
        net_fixed_assets=nfa, cwip=cwip, net_working_capital=nwc,
        total_debt=total_debt, cash_equiv=cash, net_worth=net_worth,
        dividend_paid=dividend, tax_rate=taxes,
    )


def make_dossier(**overrides) -> StockDossier:
    financials = overrides.pop("financials", make_financials())
    market = overrides.pop("market", MarketData(
        price=1000.0, market_cap_cr=5000.0, adtv_cr=5.0,
        shares_outstanding=5.0, diluted_shares_outstanding=5.1,  # Crore of shares
        sector_median_pe=25.0, sector_median_pb=4.0,
        ten_year_gsec_yield=0.069, gsec_date="2026-09-01",
    ))
    moat_sources = overrides.pop("moat_sources", [
        MoatSourceEvidence("pricing_power", "GREEN", MoatTrajectory.BUILDING, SourceTier.T2_FILING, "5yr GM rising"),
        MoatSourceEvidence("switching_costs", "AMBER", MoatTrajectory.HOLDING, SourceTier.T3_AGGREGATOR, "moderate lock-in"),
    ])
    governance = overrides.pop("governance", GovernancePillars(
        related_party_conduct=8, board_audit_independence=8, ownership_transparency=8,
        capital_allocation_discipline=8, management_stability=8, leverage_pledge_legal=9,
        earnings_quality=8, promoter_holding_pct=55, promoter_holding_3y_direction="STABLE",
    ))
    industry_context = overrides.pop("industry_context", IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="capacity utilisation rising sector-wide",
        addressable_profit_pool_cr=2000.0, current_profit_share_pct=10.0,
    ))
    bridge_assumptions = overrides.pop("bridge_assumptions", ReturnBridgeAssumptions(
        target_multiple=5.0, horizon_years=5, assumed_exit_pe=25.0,
        own_10y_75th_pctile_pe=28.0, sector_10y_75th_pctile_pe=27.0, annual_dilution_rate=0.04,
    ))
    variant_perception = overrides.pop("variant_perception", VariantPerception(
        market_belief="market prices this as a mature cyclical",
        whats_wrong_with_belief="mix shift to higher-margin exports not yet in estimates",
        persistence_mechanism="small-cap, no institutional coverage",
        m3_edge="coverage_neglect",
        gap_closing_event="FY27 export segment disclosure",
        answered=True,
    ))
    g3_state = overrides.pop("g3_state", G3State.D)

    defaults = dict(
        symbol="TEST", name="Test Co", sector="Industrials", industry="Test Industry",
        financials=financials, market=market, moat_sources=moat_sources,
        governance=governance, industry_context=industry_context,
        bridge_assumptions=bridge_assumptions, variant_perception=variant_perception,
        g3_state=g3_state, m5_protocol_complete=True,
    )
    defaults.update(overrides)
    return StockDossier(**defaults)
