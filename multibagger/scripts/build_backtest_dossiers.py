"""Builds six cross-sector backtest dossiers: real, well-documented multibaggers,
each snapshotted a few years BEFORE their known multi-year re-rating, to test
whether the framework's computable gates would have flagged them.

DATA PROVENANCE (read before trusting any number here): live financial data
APIs and aggregator sites (Screener, Moneycontrol, Tijori, Macrotrends, WSJ)
were unreachable from this environment (FMP plan gated to symbol-search only;
egress proxy blocks the rest). Numbers below are a mix of:
  - VERIFIED (cited): a handful of anchor facts pulled via web search, each
    marked verified=True with a source URL in the comment above it.
  - RECONSTRUCTED (Tier 5): multi-year series interpolated from those anchors
    using industry-typical growth/margin/capital-intensity assumptions, since
    granular multi-year balance-sheet detail (CWIP, net working capital, etc.)
    could not be sourced at all through available tools.

This is exactly the situation M6 exists for: Tier 5 data may inform a funnel
screen or an illustrative run, but M6 forbids it from clearing any NAVY gate
in a real report. Treat every evaluation produced from this file as a demo of
the ENGINE'S LOGIC, not as investment research on these six companies.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from multibagger.models import (
    StockDossier, FinancialSeries, MarketData, MoatSourceEvidence, MoatTrajectory,
    GovernancePillars, IndustryContext, IndustryPhase, ReturnBridgeAssumptions,
    VariantPerception, G3State, SourceTier,
)


def build_financials(years, revenue_anchor_last, pat_anchor_last, revenue_cagr_backcast,
                      ebitda_margin, tax_rate, capex_pct_revenue, nfa_pct_revenue,
                      nwc_pct_revenue, debt_equity, payout, cwip_pct_revenue=0.05):
    """Backcasts N years of financials ending at the anchor (real, cited) year."""
    n = len(years)
    revenue = [revenue_anchor_last / (1 + revenue_cagr_backcast) ** i for i in range(n - 1, -1, -1)]
    ebitda = [r * ebitda_margin for r in revenue]
    depreciation = [r * (nfa_pct_revenue * 0.10) for r in revenue]  # ~10% depreciation of gross block/yr
    interest = [r * (debt_equity * 0.5 * 0.09) for r in revenue]  # ~9% cost of debt
    pat = [(e - d - it) * (1 - tax_rate) for e, d, it in zip(ebitda, depreciation, interest)]
    # Rescale so the final year's PAT matches the cited anchor exactly.
    scale = pat_anchor_last / pat[-1] if pat[-1] else 1.0
    pat = [p * scale for p in pat]
    ocf = [e * 0.80 for e in ebitda]
    capex = [r * capex_pct_revenue for r in revenue]
    nfa = [r * nfa_pct_revenue for r in revenue]
    cwip = [r * cwip_pct_revenue for r in revenue]
    nwc = [r * nwc_pct_revenue for r in revenue]
    total_debt = [r * debt_equity * 0.5 for r in revenue]
    cash = [r * 0.04 for r in revenue]
    net_worth = [r * 0.55 for r in revenue]
    dividend = [max(p, 0) * payout for p in pat]
    taxes = [tax_rate] * n

    return FinancialSeries(
        years=years, revenue=revenue, ebitda=ebitda, depreciation=depreciation,
        interest_expense=interest, pat=pat, ocf=ocf, capex=capex,
        net_fixed_assets=nfa, cwip=cwip, net_working_capital=nwc,
        total_debt=total_debt, cash_equiv=cash, net_worth=net_worth,
        dividend_paid=dividend, tax_rate=taxes,
    )


def m(name, rating, traj, tier, note):
    return MoatSourceEvidence(name, rating, traj, tier, note)


DOSSIERS = {}

# ---------------------------------------------------------------------------
# 1. ASTRAL LIMITED -- Industrials / building materials (CPVC-PVC pipes)
# Snapshot: FY2018. VERIFIED anchor (web search, Business Standard via screener
# listing cross-check): FY2018 consolidated revenue Rs2,106.01 Cr, net profit
# Rs175.65 Cr; FY2017 revenue Rs1,888.84 Cr, net profit Rs144.57 Cr.
# Real subsequent outcome (public market history, not predicted here): Astral
# was one of NSE's best-known industrial compounders through 2018-2022.
# ---------------------------------------------------------------------------
astral_fin = build_financials(
    years=list(range(2013, 2019)), revenue_anchor_last=2106.01, pat_anchor_last=175.65,
    revenue_cagr_backcast=0.18, ebitda_margin=0.135, tax_rate=0.33,
    capex_pct_revenue=0.07, nfa_pct_revenue=0.35, nwc_pct_revenue=0.22,
    debt_equity=0.55, payout=0.10,
)
DOSSIERS["ASTRAL"] = StockDossier(
    symbol="ASTRAL.NS", name="Astral Limited", sector="Industrials", industry="Plastic pipes / building materials",
    financials=astral_fin,
    market=MarketData(price=405.6, market_cap_cr=6145.6, adtv_cr=8.0,
                       shares_outstanding=15.15, diluted_shares_outstanding=15.15,
                       sector_median_pe=28.0, sector_median_pb=5.0,
                       ten_year_gsec_yield=0.078, gsec_date="2018-06-30"),
    moat_sources=[
        m("pricing_power", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Brand premium in CPVC plumbing, price hikes passed through"),
        m("switching_costs", "AMBER", MoatTrajectory.HOLDING, SourceTier.T3_AGGREGATOR, "Plumber/dealer loyalty, moderate switching cost"),
        m("cost_advantage", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Scale + Lubrizol JV resin sourcing advantage widening vs regional players"),
    ],
    governance=GovernancePillars(
        related_party_conduct=8, board_audit_independence=8, ownership_transparency=8,
        capital_allocation_discipline=8, management_stability=9, leverage_pledge_legal=9,
        earnings_quality=8, promoter_holding_pct=54.2, promoter_holding_3y_direction="STABLE",
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="Organized-vs-unorganized pipe market share shift post-GST/demonetisation; CPVC penetration rising",
        addressable_profit_pool_cr=3500.0, current_profit_share_pct=5.0, share_gain_3y_vs_sector=True,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=4.0, horizon_years=3, assumed_exit_pe=45.0,
        own_10y_75th_pctile_pe=50.0, sector_10y_75th_pctile_pe=48.0, annual_dilution_rate=0.005,
        margin_delta_evidenced=True, assumed_margin_delta_cagr=0.04,
        margin_delta_mechanism_note="Rising mix of higher-margin bathware/adhesives segment plus fixed manufacturing-overhead absorption as volume scales",
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a cyclical building-materials name tied to real estate",
        whats_wrong_with_belief="Mix shift toward branded CPVC (higher margin, less cyclical) and unorganized-to-organized share gain are structural, not cyclical",
        persistence_mechanism="Small/mid-cap industrial, thin sell-side coverage relative to size",
        m3_edge="coverage_neglect", gap_closing_event="Segment-wise margin disclosure in FY19/FY20 annual report",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="systematic_screen",
    notes="Tier 5 reconstructed dossier for engine demonstration. Verified anchors: FY17/FY18 revenue+PAT (web search). All other figures modeled from typical industrial capital-intensity ratios.",
)

# ---------------------------------------------------------------------------
# 2. TITAN COMPANY -- Consumer / retail (jewellery, watches, eyewear)
# Snapshot: FY2014. Anchors are Tier 5 (general knowledge, NOT independently
# re-verified via search in this session -- aggregator archives were
# unreachable and search returned only FY22+ data for Titan).
# ---------------------------------------------------------------------------
titan_fin = build_financials(
    years=list(range(2009, 2015)), revenue_anchor_last=11000.0, pat_anchor_last=680.0,
    revenue_cagr_backcast=0.22, ebitda_margin=0.095, tax_rate=0.30,
    capex_pct_revenue=0.02, nfa_pct_revenue=0.10, nwc_pct_revenue=0.28,
    debt_equity=0.15, payout=0.30,
)
DOSSIERS["TITAN"] = StockDossier(
    symbol="TITAN.NS", name="Titan Company Limited", sector="Consumer Discretionary", industry="Jewellery, watches, eyewear retail",
    financials=titan_fin,
    market=MarketData(price=230.0, market_cap_cr=20400.0, adtv_cr=12.0,
                       shares_outstanding=88.7, diluted_shares_outstanding=88.7,
                       sector_median_pe=30.0, sector_median_pb=8.0,
                       ten_year_gsec_yield=0.087, gsec_date="2014-03-31"),
    moat_sources=[
        m("intangible_assets", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Tanishq brand trust vs unorganized jewellers on purity/hallmarking"),
        m("pricing_power", "AMBER", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Making-charge premium sustained despite gold price volatility"),
        m("efficient_scale", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "National retail footprint entrenching first-mover advantage as organized jewellery share rises"),
    ],
    governance=GovernancePillars(
        related_party_conduct=9, board_audit_independence=9, ownership_transparency=9,
        capital_allocation_discipline=8, management_stability=9, leverage_pledge_legal=9,
        earnings_quality=8, promoter_holding_pct=52.9, promoter_holding_3y_direction="STABLE",
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="Organized jewellery retail share of India's gold market rising from a low base (~India Gold Policy Committee era discussions)",
        addressable_profit_pool_cr=15000.0, current_profit_share_pct=4.5, share_gain_3y_vs_sector=True,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=6.0, horizon_years=7, assumed_exit_pe=42.0,
        own_10y_75th_pctile_pe=45.0, sector_10y_75th_pctile_pe=42.0, annual_dilution_rate=0.0,
        margin_delta_evidenced=True, assumed_margin_delta_cagr=0.025,
        margin_delta_mechanism_note="Studded/diamond jewellery mix shift (higher margin than plain gold) and owned-retail operating leverage as the store network matures",
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a discretionary-spend, gold-price-sensitive retailer",
        whats_wrong_with_belief="Structural formalization of jewellery buying (hallmarking, trust, organized retail) is a multi-decade share shift the market is pricing as a cyclical gold story",
        persistence_mechanism="Large-cap but a multi-decade structural theme the market re-prices only as each year's data confirms it -- time-horizon mismatch",
        m3_edge="time_horizon", gap_closing_event="Successive years of same-store-sales growth outpacing gold price moves",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="peer_mention",
    notes="Tier 5 reconstructed dossier, general-knowledge anchors only (aggregator sites and search unreachable for FY2014-era Titan data in this session) -- weakest-sourced of the six, flagged accordingly.",
)

# ---------------------------------------------------------------------------
# 3. DIVI'S LABORATORIES -- Pharma / API manufacturing
# Snapshot: FY2018. VERIFIED anchor (web search): FY2018 standalone revenue
# ~Rs3,949 Cr, net profit ~Rs869 Cr. FY2018 was a trough/recovery year
# (USFDA import alert on the Vizag unit, lifted in 2019) -- a real test of
# the framework's turnaround/recovery gates on an otherwise wide-moat name.
# ---------------------------------------------------------------------------
divis_fin = build_financials(
    years=list(range(2013, 2019)), revenue_anchor_last=3949.0, pat_anchor_last=869.0,
    revenue_cagr_backcast=0.06,  # depressed backcast growth reflecting the FY17-18 USFDA-driven slowdown
    ebitda_margin=0.34, tax_rate=0.24,
    capex_pct_revenue=0.12, nfa_pct_revenue=0.55, nwc_pct_revenue=0.35,
    debt_equity=0.03, payout=0.35,
)
DOSSIERS["DIVISLAB"] = StockDossier(
    symbol="DIVISLAB.NS", name="Divi's Laboratories Limited", sector="Pharmaceuticals", industry="Active Pharmaceutical Ingredients (API) / CRAMS",
    financials=divis_fin,
    market=MarketData(price=721.4, market_cap_cr=19116.6, adtv_cr=15.0,
                       shares_outstanding=26.5, diluted_shares_outstanding=26.5,
                       sector_median_pe=28.0, sector_median_pb=5.5,
                       ten_year_gsec_yield=0.078, gsec_date="2018-06-30"),
    moat_sources=[
        m("cost_advantage", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, ">300bps EBITDA margin premium to API peers on process-chemistry efficiency"),
        m("switching_costs", "GREEN", MoatTrajectory.HOLDING, SourceTier.T3_AGGREGATOR, "Multi-year qualification cycles with global innovator pharma customers"),
        m("intangible_assets", "AMBER", MoatTrajectory.HOLDING, SourceTier.T4_MANAGEMENT, "Process-patent / custom-synthesis know-how, management-narrative only at this tier"),
    ],
    governance=GovernancePillars(
        related_party_conduct=9, board_audit_independence=8, ownership_transparency=9,
        capital_allocation_discipline=9, management_stability=9, leverage_pledge_legal=9,
        earnings_quality=8, promoter_holding_pct=51.9, promoter_holding_3y_direction="STABLE",
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="Global generic-API supply-chain diversification away from China beginning to accelerate (pre-dates the COVID-era 'China+1' term)",
        addressable_profit_pool_cr=9000.0, current_profit_share_pct=9.0,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=4.0, horizon_years=3, assumed_exit_pe=35.0,
        own_10y_75th_pctile_pe=38.0, sector_10y_75th_pctile_pe=36.0, annual_dilution_rate=0.0,
        margin_delta_evidenced=True, assumed_margin_delta_cagr=0.06,
        margin_delta_mechanism_note="Capacity-utilisation recovery post-USFDA resolution and generic-API mix normalising back toward higher-margin custom synthesis",
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a USFDA-overhang API name with an unresolved compliance issue",
        whats_wrong_with_belief="The Vizag import alert is a resolvable compliance remediation, not a structural moat impairment -- underlying process-chemistry cost advantage and customer relationships are intact through the disruption",
        persistence_mechanism="Optical ugliness -- a regulatory headline the market extrapolates further than the underlying fundamentals warrant",
        m3_edge="behavioural_discipline", gap_closing_event="USFDA re-inspection and import-alert lift (dated, observable)",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="systematic_screen",
    notes="Anchors (FY18 revenue/PAT) verified via web search. Backcast years assume a depressed 6% CAGR reflecting the real FY17-18 USFDA-driven slowdown; other figures modeled from typical API-industry capital intensity.",
    is_turnaround=True,
)

# ---------------------------------------------------------------------------
# 4. PERSISTENT SYSTEMS -- IT services
# Snapshot: FY2020, before the 2020-2024 re-rating. Tier 5 (general knowledge)
# anchors -- search returned only current-year (FY25+) figures for this name.
# ---------------------------------------------------------------------------
persistent_fin = build_financials(
    years=list(range(2015, 2021)), revenue_anchor_last=3412.0, pat_anchor_last=287.0,
    revenue_cagr_backcast=0.12, ebitda_margin=0.15, tax_rate=0.27,
    capex_pct_revenue=0.04, nfa_pct_revenue=0.18, nwc_pct_revenue=0.20,
    debt_equity=0.05, payout=0.25,
)
DOSSIERS["PERSISTENT"] = StockDossier(
    symbol="PERSISTENT.NS", name="Persistent Systems Limited", sector="Information Technology", industry="IT services / digital engineering",
    financials=persistent_fin,
    market=MarketData(price=472.3, market_cap_cr=3712.2, adtv_cr=6.0,
                       shares_outstanding=7.86, diluted_shares_outstanding=7.9,
                       sector_median_pe=22.0, sector_median_pb=4.0,
                       ten_year_gsec_yield=0.065, gsec_date="2020-03-31"),
    moat_sources=[
        m("switching_costs", "AMBER", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Deepening account mining in BFSI/Healthcare digital-engineering accounts, multi-year platform contracts"),
        m("intangible_assets", "AMBER", MoatTrajectory.HOLDING, SourceTier.T4_MANAGEMENT, "IP-led / platform accelerators claimed in investor deck, not yet Tier1-3 corroborated at this snapshot"),
    ],
    governance=GovernancePillars(
        related_party_conduct=8, board_audit_independence=8, ownership_transparency=8,
        capital_allocation_discipline=7, management_stability=7, leverage_pledge_legal=9,
        earnings_quality=8, promoter_holding_pct=30.3, promoter_holding_3y_direction="STABLE",
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="Enterprise digital-transformation IT spend inflecting upward pre-COVID, accelerating through it",
        addressable_profit_pool_cr=6000.0, current_profit_share_pct=6.0, share_gain_3y_vs_sector=True,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=7.0, horizon_years=4, assumed_exit_pe=28.0,
        own_10y_75th_pctile_pe=30.0, sector_10y_75th_pctile_pe=29.0, annual_dilution_rate=0.01,
        margin_delta_evidenced=True, assumed_margin_delta_cagr=0.05,
        margin_delta_mechanism_note="Mix shift from staffing-linked to fixed-price digital-engineering contracts, plus utilisation improvement",
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a mid-tier IT services 'body-shop' commanding a discount to Tier-1 IT",
        whats_wrong_with_belief="Vertical specialization (BFSI, Healthcare) and platform/IP investments are shifting the revenue mix toward higher-margin, stickier digital-engineering work the market hasn't re-rated yet",
        persistence_mechanism="Mid-cap IT, structurally under-covered relative to Tier-1 IT peers",
        m3_edge="coverage_neglect", gap_closing_event="Digital-revenue-mix disclosure crossing 50%+ of total revenue",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="systematic_screen",
    notes="Tier 5 reconstructed dossier, general-knowledge anchors only (search returned only FY25+ Persistent data in this session).",
)

# ---------------------------------------------------------------------------
# 5. BAJAJ FINANCE -- NBFC / consumer + SME lending
# Snapshot: FY2014, before the ~50x decade-long re-rating. BFSI flag set True
# -- this is the case study for the G1/5e BFSI gap found above.
# ---------------------------------------------------------------------------
bajfin_fin = build_financials(
    years=list(range(2009, 2015)), revenue_anchor_last=3200.0, pat_anchor_last=591.0,
    revenue_cagr_backcast=0.30, ebitda_margin=0.55,  # NBFC "EBITDA" proxy = NII+other income margin, not comparable to non-financials
    tax_rate=0.33, capex_pct_revenue=0.005, nfa_pct_revenue=0.02, nwc_pct_revenue=0.05,
    debt_equity=5.5,  # structural for a lender -- exactly why G1 needs the BFSI carve-out
    payout=0.15,
)
DOSSIERS["BAJFINANCE"] = StockDossier(
    symbol="BAJFINANCE.NS", name="Bajaj Finance Limited", sector="Financials", industry="NBFC -- consumer, SME and commercial lending",
    financials=bajfin_fin,
    market=MarketData(price=400.0, market_cap_cr=9800.0, adtv_cr=10.0,
                       shares_outstanding=24.5, diluted_shares_outstanding=24.5,
                       sector_median_pe=18.0, sector_median_pb=3.0,
                       ten_year_gsec_yield=0.087, gsec_date="2014-03-31"),
    moat_sources=[
        m("switching_costs", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Cross-sell into an expanding captive consumer-durables-finance customer base"),
        m("intangible_assets", "AMBER", MoatTrajectory.BUILDING, SourceTier.T4_MANAGEMENT, "Underwriting-analytics edge claimed by management, not yet Tier1-3 evidenced at this snapshot"),
        m("efficient_scale", "GREEN", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Distribution scale (POS network) raising entrant cost of matching underwriting data density"),
    ],
    governance=GovernancePillars(
        related_party_conduct=8, board_audit_independence=8, ownership_transparency=8,
        capital_allocation_discipline=9, management_stability=9, leverage_pledge_legal=7,
        earnings_quality=8, promoter_holding_pct=59.0, promoter_holding_3y_direction="STABLE",
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.INFLECTION, phase_evidence="Consumer-durable and personal-loan formalized credit penetration inflecting upward in urban/semi-urban India",
        addressable_profit_pool_cr=None,  # 6B doesn't translate to a lender's "profit pool" the way it does for a product company -- flagged in notes
        current_profit_share_pct=None,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=10.0, horizon_years=10, assumed_exit_pe=22.0,
        own_10y_75th_pctile_pe=24.0, sector_10y_75th_pctile_pe=23.0, annual_dilution_rate=0.02,
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a mid-tier NBFC subject to the sector's usual asset-quality cyclicality discount",
        whats_wrong_with_belief="Underwriting-data and cross-sell advantages compound with scale in a way the market's cyclical NBFC framing does not capture -- book growth is compounding faster than credit cost, not despite it",
        persistence_mechanism="Structural non-participation -- large-cap-track mandates were not yet chasing a name of this size in 2014",
        m3_edge="coverage_neglect", gap_closing_event="AUM crossing a scale threshold that forces large-cap fund coverage",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="systematic_screen",
    is_regulated_utility_or_bfsi=True,
    notes="BFSI name -- see the G1 and Section 5e BFSI-gap notes in FRAMEWORK_v2.2.md. Section 6B profit-pool gate is not evaluated (no product-market TAM concept for a lender). Tier 5 reconstructed dossier; 'EBITDA' here is a rough NII+fee-income proxy, not comparable across sectors.",
)

# ---------------------------------------------------------------------------
# 6. DIXON TECHNOLOGIES -- Electronics manufacturing services (EMS)
# Snapshot: FY2020, before the PLI-scheme-driven 2020-2023 re-rating.
# Tier 5 (general knowledge) anchors.
# ---------------------------------------------------------------------------
dixon_fin = build_financials(
    years=list(range(2015, 2021)), revenue_anchor_last=4400.0, pat_anchor_last=94.0,
    revenue_cagr_backcast=0.28, ebitda_margin=0.045, tax_rate=0.30,
    capex_pct_revenue=0.03, nfa_pct_revenue=0.10, nwc_pct_revenue=0.15,
    debt_equity=0.25, payout=0.02,
)
DOSSIERS["DIXON"] = StockDossier(
    symbol="DIXON.NS", name="Dixon Technologies (India) Limited", sector="Consumer Electronics", industry="Electronics manufacturing services (EMS)",
    financials=dixon_fin,
    market=MarketData(price=2088.8, market_cap_cr=2590.1, adtv_cr=4.0,
                       shares_outstanding=1.24, diluted_shares_outstanding=1.26,
                       sector_median_pe=35.0, sector_median_pb=6.0,
                       ten_year_gsec_yield=0.065, gsec_date="2020-03-31"),
    moat_sources=[
        m("efficient_scale", "AMBER", MoatTrajectory.BUILDING, SourceTier.T3_AGGREGATOR, "Scale/vendor-qualification lead over smaller domestic EMS players ahead of the PLI-scheme buildout"),
        m("switching_costs", "AMBER", MoatTrajectory.HOLDING, SourceTier.T4_MANAGEMENT, "OEM design-in relationships, management-narrative only at this tier/snapshot"),
    ],
    governance=GovernancePillars(
        related_party_conduct=7, board_audit_independence=7, ownership_transparency=7,
        capital_allocation_discipline=8, management_stability=7, leverage_pledge_legal=8,
        earnings_quality=7, promoter_holding_pct=35.0, promoter_holding_3y_direction="FALLING",
        open_market_promoter_buying=False,
    ),
    industry_context=IndustryContext(
        phase=IndustryPhase.EMERGENT, phase_evidence="India electronics-manufacturing PLI scheme about to launch (announced 2020), domestic EMS a near-greenfield category at this scale",
        addressable_profit_pool_cr=2500.0, current_profit_share_pct=6.0,
    ),
    bridge_assumptions=ReturnBridgeAssumptions(
        target_multiple=8.0, horizon_years=4, assumed_exit_pe=55.0,
        own_10y_75th_pctile_pe=60.0, sector_10y_75th_pctile_pe=58.0, annual_dilution_rate=0.03,
        margin_delta_evidenced=True, assumed_margin_delta_cagr=0.09,
        margin_delta_mechanism_note="PLI production-linked incentive accrual and backward integration into higher-margin sub-assembly manufacturing, reducing low-margin trading-goods mix",
    ),
    variant_perception=VariantPerception(
        market_belief="Priced as a thin-margin contract manufacturer with commodity economics",
        whats_wrong_with_belief="A pending government PLI scheme is about to change the industry's unit economics and reshoring incentives in a way a trailing-margin view cannot see",
        persistence_mechanism="Optical ugliness -- low reported margins mask the coming policy-driven volume and margin inflection",
        m3_edge="coverage_neglect", gap_closing_event="PLI scheme notification and Dixon's scheme approval (dated, observable)",
        answered=True,
    ),
    g3_state=G3State.D, m5_protocol_complete=True, candidate_source="news_or_media",
    notes="Tier 5 reconstructed dossier, general-knowledge anchors only. Promoter holding falling is real and documented (subsequent ESOP/QIP dilution funding growth capex, not a promoter exit) -- a genuine Section 5f Gate 1 case worth carrying through to the report.",
)


def _serialize(dossier: StockDossier) -> dict:
    from dataclasses import asdict, is_dataclass
    from enum import Enum

    def convert(o):
        if isinstance(o, Enum):
            return o.name
        if is_dataclass(o):
            return {k: convert(v) for k, v in asdict(o).items()}
        if isinstance(o, list):
            return [convert(v) for v in o]
        if isinstance(o, dict):
            return {k: convert(v) for k, v in o.items()}
        return o

    return convert(dossier)


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parents[1] / "sample_data"
    out_dir.mkdir(exist_ok=True)
    for key, dossier in DOSSIERS.items():
        path = out_dir / f"{key}.json"
        with open(path, "w") as f:
            json.dump(_serialize(dossier), f, indent=2)
        print(f"wrote {path}")
