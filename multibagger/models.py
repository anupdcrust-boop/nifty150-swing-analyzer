"""Data model for a single stock's dossier.

Every field carries an implicit M6 source-tier expectation: numeric financial
series should come from Tier 1/2 (audited statements, exchange filings); the
`*_tier` fields let a caller record which tier actually backed a figure, and
the report layer refuses to let a Tier-3-only figure clear a gate that the
framework marks NAVY/binding.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SourceTier(Enum):
    T1_AUDITED = 1
    T2_FILING = 2
    T3_AGGREGATOR = 3
    T4_MANAGEMENT = 4
    T5_MEDIA = 5


class MoatTrajectory(Enum):
    BUILDING = "BUILDING"
    HOLDING = "HOLDING"
    ERODING = "ERODING"
    NOT_RATED = "NOT_RATED"


class IndustryPhase(Enum):
    EMERGENT = "EMERGENT"
    INFLECTION = "INFLECTION"
    MATURE = "MATURE"
    DECLINING = "DECLINING"


class G3State(Enum):
    A = "A"  # siphoning / fraud — full discard
    B = "B"  # pledge 10-25%, promoter holding <15%, settled enforcement
    C = "C"  # active SEBI PFUTP on sitting MD/CMD/CFO/WTD
    D = "D"  # clean


@dataclass
class FinancialSeries:
    """Annual figures, oldest first. All in Rs Crore unless noted."""

    years: list[int]
    revenue: list[float]
    ebitda: list[float]
    depreciation: list[float]
    interest_expense: list[float]
    pat: list[float]
    ocf: list[float]
    capex: list[float]
    net_fixed_assets: list[float]
    cwip: list[float]
    net_working_capital: list[float]
    total_debt: list[float]
    cash_equiv: list[float]
    net_worth: list[float]
    dividend_paid: list[float]
    tax_rate: list[float]  # effective, e.g. 0.25

    def _last(self, series: list[float], n: int = 1) -> float:
        return series[-n]

    @property
    def ebit(self) -> list[float]:
        return [e - d for e, d in zip(self.ebitda, self.depreciation)]

    @property
    def interest_coverage(self) -> float:
        ebit = self.ebit[-1]
        interest = self.interest_expense[-1]
        return ebit / interest if interest else float("inf")

    @property
    def debt_to_equity(self) -> float:
        nw = self.net_worth[-1]
        return self.total_debt[-1] / nw if nw else float("inf")

    @property
    def net_debt_to_equity(self) -> float:
        nw = self.net_worth[-1]
        net_debt = self.total_debt[-1] - self.cash_equiv[-1]
        return net_debt / nw if nw else float("inf")

    @property
    def pat_negative_years_trailing(self) -> int:
        count = 0
        for p in reversed(self.pat):
            if p < 0:
                count += 1
            else:
                break
        return count

    @property
    def revenue_cagr_3y(self) -> Optional[float]:
        return _cagr(self.revenue, 3)

    @property
    def payout_ratio_3y_avg(self) -> Optional[float]:
        if len(self.pat) < 3 or len(self.dividend_paid) < 3:
            return None
        pats = self.pat[-3:]
        divs = self.dividend_paid[-3:]
        total_pat = sum(pats)
        if total_pat <= 0:
            return None
        return sum(divs) / total_pat

    @property
    def ocf_to_ebitda_3y_avg(self) -> Optional[float]:
        if len(self.ocf) < 3 or len(self.ebitda) < 3:
            return None
        ocfs, ebitdas = self.ocf[-3:], self.ebitda[-3:]
        if sum(ebitdas) == 0:
            return None
        return sum(ocfs) / sum(ebitdas)

    @property
    def roce_series(self) -> list[float]:
        """ROCE = EBIT / (Net worth + Total debt - Cash), per-year."""
        out = []
        for ebit, nw, debt, cash in zip(
            self.ebit, self.net_worth, self.total_debt, self.cash_equiv
        ):
            capital_employed = nw + debt - cash
            out.append(ebit / capital_employed if capital_employed else 0.0)
        return out

    @property
    def gross_margin_proxy_series(self) -> list[float]:
        """EBITDA margin used as pricing-power proxy where COGS breakup is unavailable."""
        return [e / r if r else 0.0 for e, r in zip(self.ebitda, self.revenue)]


@dataclass
class MoatSourceEvidence:
    """One of the six Section 5 moat sources, analyst-rated."""

    name: str  # pricing_power | switching_costs | network_effects | cost_advantage | intangible_assets | efficient_scale
    rating: str  # GREEN / AMBER / RED
    trajectory: MoatTrajectory
    evidence_tier: SourceTier
    evidence_note: str = ""


@dataclass
class GovernancePillars:
    """MQF v1.1 — each pillar scored 0-10 by the analyst from Tier 1-3 evidence."""

    related_party_conduct: float
    board_audit_independence: float
    ownership_transparency: float
    capital_allocation_discipline: float
    management_stability: float
    leverage_pledge_legal: float
    earnings_quality: float
    kill_gate_fired: bool = False
    kill_gate_reason: str = ""
    section_20a_pattern_escalation: bool = False
    promoter_pledge_pct: float = 0.0
    promoter_holding_pct: float = 0.0
    promoter_holding_3y_direction: str = "STABLE"  # RISING / STABLE / FALLING
    open_market_promoter_buying: bool = False


@dataclass
class MarketData:
    price: float
    market_cap_cr: float
    adtv_cr: float  # 30-day average daily traded value, Rs Cr
    # Share counts are in CRORE of shares (e.g. 5.1 = 5.1 Crore = 51 million
    # shares) — the same unit convention as revenue/PAT (Rs Crore), so
    # EPS = PAT(Cr) / shares(Cr) needs no separate scaling factor.
    shares_outstanding: float
    diluted_shares_outstanding: float
    sector_median_pe: float
    sector_median_pb: float
    ten_year_gsec_yield: float  # e.g. 0.069
    gsec_date: str
    forward_eps: Optional[float] = None
    book_value_per_share: Optional[float] = None


@dataclass
class IndustryContext:
    phase: IndustryPhase
    phase_evidence: str
    addressable_profit_pool_cr: Optional[float] = None
    current_profit_share_pct: Optional[float] = None
    is_consolidating_duopoly_leader: bool = False
    share_gain_3y_vs_sector: Optional[bool] = None  # revenue CAGR > sector for 3 consecutive years


@dataclass
class ReturnBridgeAssumptions:
    """N1 — analyst-stated target for the return bridge."""

    target_multiple: float  # e.g. 5.0 for "5x"
    horizon_years: int
    assumed_exit_pe: float
    own_10y_75th_pctile_pe: Optional[float] = None
    sector_10y_75th_pctile_pe: Optional[float] = None
    annual_dilution_rate: float = 0.0  # fully diluted share count growth p.a.
    # Section 6A cross-reference (v2.2 fix — see FRAMEWORK_v2.2.md): if the N1
    # bridge's required EPS CAGR relies partly on margin expansion rather than
    # pure reinvestment-driven volume growth, that margin-delta CAGR must be
    # named and evidenced here. Per 6A's own rule, an unevidenced margin delta
    # is set to zero and the bridge re-run entirely on revenue-driven growth.
    margin_delta_evidenced: bool = False
    assumed_margin_delta_cagr: float = 0.0
    margin_delta_mechanism_note: str = ""


@dataclass
class VariantPerception:
    """N7 — four mandatory questions, answered before verdict."""

    market_belief: str = ""
    whats_wrong_with_belief: str = ""
    persistence_mechanism: str = ""  # must map to an M3 edge
    m3_edge: str = ""  # time_horizon | coverage_neglect | behavioural_discipline
    gap_closing_event: str = ""
    reverse_dcf_implied_growth: Optional[float] = None
    answered: bool = False


@dataclass
class StockDossier:
    symbol: str
    name: str
    sector: str
    industry: str
    financials: FinancialSeries
    market: MarketData
    moat_sources: list[MoatSourceEvidence]
    governance: GovernancePillars
    industry_context: IndustryContext
    bridge_assumptions: ReturnBridgeAssumptions
    variant_perception: VariantPerception
    g3_state: G3State
    candidate_source: str = "systematic_screen"  # M8
    is_turnaround: bool = False
    is_regulated_utility_or_bfsi: bool = False
    m5_protocol_complete: bool = False
    notes: str = ""


def _cagr(series: list[float], years: int) -> Optional[float]:
    if len(series) <= years:
        return None
    start, end = series[-years - 1], series[-1]
    if start <= 0 or end <= 0:
        return None
    return (end / start) ** (1 / years) - 1
