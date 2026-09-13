"""Part 7 — The Multibagger Engine: Section 5e compounding engine, the N1
return bridge, Section 6B runway/profit-pool gate, and the N8 funnel screen.

These are the framework's *quantitative* core — every formula here is taken
directly from the PDF text, not inferred. Where the PDF gives a worked
example (N1, 5x/5yr), the unit tests reproduce it exactly.
"""

from dataclasses import dataclass
from typing import Optional

from .models import StockDossier, IndustryPhase, MoatTrajectory


# ---------------------------------------------------------------------------
# Section 5e — The Compounding Engine
# ---------------------------------------------------------------------------


@dataclass
class EngineGrowthResult:
    roiic: Optional[float]
    reinvestment_rate: Optional[float]
    engine_growth_g: Optional[float]
    roiic_below_cost_of_capital_2y: bool
    payout_3y_avg: Optional[float]
    gate_payout_ceiling_clears: bool  # 3-yr avg payout <= 40%


def _nopat(financials, index: int) -> float:
    ebit = financials.ebit[index]
    tax_rate = financials.tax_rate[index]
    return ebit * (1 - tax_rate)


def _invested_capital(financials, index: int) -> float:
    return (
        financials.net_fixed_assets[index]
        + financials.cwip[index]
        + financials.net_working_capital[index]
    )


def compute_engine_growth(d: StockDossier, cost_of_capital: float = 0.11) -> EngineGrowthResult:
    f = d.financials
    n = len(f.revenue)
    if n < 4:
        return EngineGrowthResult(None, None, None, False, f.payout_ratio_3y_avg, False)

    nopat_now, nopat_3y_ago = _nopat(f, -1), _nopat(f, -4)
    ic_now, ic_3y_ago = _invested_capital(f, -1), _invested_capital(f, -4)
    delta_ic = ic_now - ic_3y_ago

    roiic = (nopat_now - nopat_3y_ago) / delta_ic if delta_ic else None

    capex = f.capex[-1]
    delta_wc = f.net_working_capital[-1] - f.net_working_capital[-2] if n >= 2 else 0.0
    depreciation = f.depreciation[-1]
    rr = (capex + delta_wc - depreciation) / nopat_now if nopat_now else None

    g = roiic * rr if (roiic is not None and rr is not None) else None

    # Gate 2: ROIIC below cost of capital for 2 consecutive years
    roiic_series = []
    for i in range(-1, -3, -1):
        if abs(i) + 3 <= n:
            roiic_series.append((_nopat(f, i) - _nopat(f, i - 3)) / (_invested_capital(f, i) - _invested_capital(f, i - 3) or 1e-9))
    below_2y = len(roiic_series) == 2 and all(r < cost_of_capital for r in roiic_series)

    payout = f.payout_ratio_3y_avg
    payout_clears = payout is not None and payout <= 0.40

    return EngineGrowthResult(roiic, rr, g, below_2y, payout, payout_clears)


# ---------------------------------------------------------------------------
# Part 7, N1 — The Multibagger Return Bridge
# ---------------------------------------------------------------------------


@dataclass
class ReturnBridgeResult:
    required_annualised_return: float
    rerating_cagr: float
    required_eps_cagr: float
    required_net_profit_cagr_diluted: float
    required_revenue_cagr: float  # v2.2: required_eps_cagr net of the evidenced margin-delta term
    margin_delta_cagr_applied: float  # 0.0 unless evidenced per 6A
    earnings_share_of_log_return: float
    earnings_dominance_clears: bool  # N1-1: earnings share >= 60%
    exit_multiple_ceiling_clears: bool  # N1-2
    dilution_honesty_clears: bool  # N1-3


def required_annualised_return(target_multiple: float, horizon_years: int) -> float:
    return target_multiple ** (1 / horizon_years) - 1


def compute_return_bridge(d: StockDossier, entry_pe: float) -> ReturnBridgeResult:
    ba = d.bridge_assumptions
    r_total = required_annualised_return(ba.target_multiple, ba.horizon_years)

    rerating_cagr = (ba.assumed_exit_pe / entry_pe) ** (1 / ba.horizon_years) - 1 if entry_pe > 0 else 0.0
    required_eps_cagr = (1 + r_total) / (1 + rerating_cagr) - 1

    earnings_share = _log(1 + required_eps_cagr) / _log(1 + r_total) if r_total > 0 else 0.0
    dominance_clears = earnings_share >= 0.60

    required_net_profit_cagr = (1 + required_eps_cagr) * (1 + ba.annual_dilution_rate) - 1

    # v2.2 fix: Section 5e's g (ROIIC x RR) is a pure reinvestment/volume growth
    # concept -- it says nothing about margin expansion. Gating it against the
    # FULL required_eps_cagr silently demands reinvestment alone deliver any
    # margin-delta contribution too, double-counting the bar Section 6A already
    # gates separately. Per 6A's own rule, an unevidenced margin delta is zero.
    margin_delta_used = ba.assumed_margin_delta_cagr if (ba.margin_delta_evidenced and ba.margin_delta_mechanism_note) else 0.0
    required_revenue_cagr = (1 + required_eps_cagr) / (1 + margin_delta_used) - 1

    ceiling = None
    if ba.own_10y_75th_pctile_pe is not None and ba.sector_10y_75th_pctile_pe is not None:
        ceiling = min(ba.own_10y_75th_pctile_pe, ba.sector_10y_75th_pctile_pe)
    exit_ceiling_clears = ceiling is None or ba.assumed_exit_pe <= ceiling

    # no exit multiple above entry where trajectory is ERODING (checked by caller with moat data)
    dilution_honesty = ba.annual_dilution_rate is not None

    return ReturnBridgeResult(
        required_annualised_return=r_total,
        rerating_cagr=rerating_cagr,
        required_eps_cagr=required_eps_cagr,
        required_net_profit_cagr_diluted=required_net_profit_cagr,
        required_revenue_cagr=required_revenue_cagr,
        margin_delta_cagr_applied=margin_delta_used,
        earnings_share_of_log_return=earnings_share,
        earnings_dominance_clears=dominance_clears,
        exit_multiple_ceiling_clears=exit_ceiling_clears,
        dilution_honesty_clears=dilution_honesty,
    )


def _log(x: float) -> float:
    import math

    return math.log(x)


# ---------------------------------------------------------------------------
# Section 6A — Industry Phase & Operating-Leverage Inflection
# ---------------------------------------------------------------------------


def industry_phase_gate_clears(d: StockDossier, share_gain_3y: Optional[bool]) -> tuple[bool, str]:
    phase = d.industry_context.phase
    if phase in (IndustryPhase.EMERGENT, IndustryPhase.INFLECTION):
        return True, f"{phase.value} — clears"
    if phase == IndustryPhase.MATURE and share_gain_3y:
        return True, "MATURE + documented 3yr share-gainer — clears"
    if phase == IndustryPhase.MATURE:
        return False, "MATURE + share-flat — caps at Steady Compounder"
    return False, "DECLINING — caps at WATCH irrespective of valuation"


# ---------------------------------------------------------------------------
# Section 6B — Runway & Profit Pool
# ---------------------------------------------------------------------------


@dataclass
class RunwayResult:
    implied_share_at_target_pct: Optional[float]
    clears: bool
    message: str


def compute_runway_gate(d: StockDossier, target_market_cap_cr: float) -> RunwayResult:
    ic = d.industry_context
    pool = ic.addressable_profit_pool_cr
    if pool is None or pool <= 0:
        return RunwayResult(None, False, "No addressable profit pool stated — cannot evidence gate")

    # Implied share = target market cap's implied profit (at current exit multiple)
    # divided by the addressable pool. Caller passes an already PE-implied profit figure
    # via target_market_cap_cr / assumed_exit_pe upstream if needed; here we take profit share directly.
    implied_profit_share_pct = (target_market_cap_cr / d.bridge_assumptions.assumed_exit_pe) / pool * 100

    if implied_profit_share_pct > 25 and not ic.is_consolidating_duopoly_leader:
        return RunwayResult(
            implied_profit_share_pct,
            False,
            f"Implied profit-pool share at target {implied_profit_share_pct:.1f}% > 25% and not a consolidating-duopoly leader — RED",
        )
    return RunwayResult(implied_profit_share_pct, True, f"Implied profit-pool share at target {implied_profit_share_pct:.1f}% — clears")


def market_cap_band(market_cap_cr: float) -> str:
    if market_cap_cr < 1000:
        return "micro"
    if market_cap_cr < 10000:
        return "small"
    if market_cap_cr < 50000:
        return "mid"
    return "large"


# ---------------------------------------------------------------------------
# N8 — The Multibagger Funnel Screen
# ---------------------------------------------------------------------------


@dataclass
class FunnelScreenResult:
    passed: bool
    failed_filters: list[str]
    rank_score: Optional[float]  # ROIIC x (1 - payout), for ranking passers


def run_funnel_screen(d: StockDossier, engine: EngineGrowthResult) -> FunnelScreenResult:
    f = d.financials
    m = d.market
    g = d.governance
    failed = []

    if not (300 <= m.market_cap_cr <= 15000):
        failed.append(f"market_cap {m.market_cap_cr:.0f}Cr outside 300-15000Cr")

    rev_cagr = f.revenue_cagr_3y
    if rev_cagr is None or rev_cagr < 0.15:
        failed.append(f"revenue 3yr CAGR {rev_cagr}" if rev_cagr is not None else "revenue 3yr CAGR unavailable")

    roce = f.roce_series
    if not roce or roce[-1] < 0.15:
        failed.append(f"ROCE {roce[-1]*100:.1f}% < 15%" if roce else "ROCE unavailable")

    if engine.roiic is None or engine.roiic < 0.18:
        failed.append(f"ROIIC {engine.roiic} < 18%")

    if engine.payout_3y_avg is None or engine.payout_3y_avg > 0.40:
        failed.append(f"payout {engine.payout_3y_avg} > 40%")

    if f.debt_to_equity >= 1.0:
        failed.append(f"D/E {f.debt_to_equity:.2f}x >= 1.0x")

    if f.interest_coverage <= 3.0:
        failed.append(f"interest coverage {f.interest_coverage:.2f}x <= 3.0x")

    if g.promoter_holding_pct < 40 or g.promoter_holding_3y_direction == "FALLING":
        failed.append(f"promoter holding {g.promoter_holding_pct}% / {g.promoter_holding_3y_direction}")

    ocf_ebitda = f.ocf_to_ebitda_3y_avg
    if ocf_ebitda is None or ocf_ebitda <= 0.60:
        failed.append(f"OCF/EBITDA 3yr avg {ocf_ebitda}")

    if m.adtv_cr < 1.0:
        failed.append(f"ADTV {m.adtv_cr:.2f}Cr < 1Cr")

    rank_score = None
    if engine.roiic is not None and engine.payout_3y_avg is not None:
        rank_score = engine.roiic * (1 - engine.payout_3y_avg)

    return FunnelScreenResult(passed=len(failed) == 0, failed_filters=failed, rank_score=rank_score)
