"""Part 2 — Stage 1 discard gates G0-G5 and the Irani governance flags.

Each function returns a Finding: (band, passed, message). RED findings from
G0-G2 are absolute discards per the framework ("never outvoted by score").
"""

from dataclasses import dataclass

from .models import StockDossier, G3State


@dataclass
class Finding:
    rule_id: str
    band: str  # GREEN / TEAL / ORANGE / RED / NAVY
    passed: bool
    message: str


def g0_liquidity(d: StockDossier) -> Finding:
    if d.market.adtv_cr < 1.0:
        return Finding("G0", "RED", False, f"30-day ADTV Rs{d.market.adtv_cr:.2f}Cr < Rs1Cr floor — DISCARD")
    return Finding("G0", "GREEN", True, f"ADTV Rs{d.market.adtv_cr:.2f}Cr clears G0 floor")


def g1_leverage(d: StockDossier) -> Finding:
    # GAP FOUND IN APPLICATION (v2.2): the PDF's G1 text carries no BFSI/utility
    # carve-out, unlike G2's explicit one. Applied literally, a lend-to-earn
    # NBFC's structural 4-8x D/E would auto-discard every healthy lender,
    # Bajaj Finance included. Borrowed borrowing costs, not equity gearing, is
    # the actual risk signal for BFSI; this gate is not the right lens there.
    if d.is_regulated_utility_or_bfsi:
        return Finding("G1", "TEAL", True, "G1 D/E test does not apply to a BFSI/regulated-utility balance sheet — needs a sector-specific leverage test (see v2.2 notes), not scored here")
    de = d.financials.debt_to_equity
    icr = d.financials.interest_coverage
    if de > 2.0 and icr < 1.5:
        return Finding("G1", "RED", False, f"D/E {de:.2f}x AND interest coverage {icr:.2f}x — DISCARD")
    return Finding("G1", "GREEN", True, f"D/E {de:.2f}x, interest coverage {icr:.2f}x")


def g2_earnings(d: StockDossier) -> Finding:
    neg_years = d.financials.pat_negative_years_trailing
    exempt = d.is_regulated_utility_or_bfsi or d.is_turnaround
    if neg_years >= 3 and not exempt:
        return Finding("G2", "RED", False, f"PAT negative {neg_years} consecutive years — DISCARD unless turnaround")
    return Finding("G2", "GREEN", True, f"PAT negative-year streak: {neg_years}")


def g3_promoter_integrity(d: StockDossier) -> Finding:
    caps = {
        G3State.A: (0.0, "RED", "Siphoning/fraud — full discard"),
        G3State.B: (1.5, "ORANGE", "Pledge 10-25%, promoter holding <15%, settled enforcement — max 1.5%"),
        G3State.C: (1.0, "RED", "Active SEBI PFUTP on sitting MD/CMD/CFO/WTD — max 1%"),
        G3State.D: (100.0, "GREEN", "Clean — standard sizing"),
    }
    cap_pct, band, msg = caps[d.g3_state]
    return Finding("G3", band, d.g3_state == G3State.D, f"G3-{d.g3_state.value}: {msg}")


def g4_objectivity(d: StockDossier) -> Finding:
    if not d.m5_protocol_complete:
        return Finding("G4", "ORANGE", False, "M5 adversarial protocol incomplete — cannot lock verdict")
    return Finding("G4", "GREEN", True, "M5 adversarial protocol complete")


def g5_valuation_sanity(d: StockDossier) -> Finding:
    pe = _trailing_pe(d)
    if pe is None:
        return Finding("G5", "TEAL", True, "PE undefined (no positive TTM EPS) — sanity check skipped")
    ratio = pe / d.market.sector_median_pe if d.market.sector_median_pe else float("inf")
    if ratio > 3.0:
        return Finding("G5", "ORANGE", False, f"PE {pe:.1f}x is {ratio:.1f}x sector median — REVIEW")
    return Finding("G5", "GREEN", True, f"PE {pe:.1f}x is {ratio:.1f}x sector median")


def _trailing_pe(d: StockDossier) -> float | None:
    pat = d.financials.pat[-1]
    shares = d.market.diluted_shares_outstanding
    if pat <= 0 or shares <= 0:
        return None
    eps = pat / shares
    return d.market.price / eps


def irani_flags(d: StockDossier) -> list[Finding]:
    """Section-3 Irani governance flags. Returns only flags that fired."""
    out: list[Finding] = []
    f = d.financials

    if len(f.pat) >= 3 and len(f.ocf) >= 3:
        pat_over_ocf_years = sum(1 for p, o in zip(f.pat[-3:], f.ocf[-3:]) if p > o)
        if pat_over_ocf_years >= 3:
            out.append(Finding("Accounting Gap", "RED", False, "PAT > OCF for 3+ consecutive years — Layer C EQ zeroed"))

    de_rising = len(f.total_debt) >= 2 and f.debt_to_equity > 1.5 and f.total_debt[-1] > f.total_debt[-2]
    if de_rising and f.interest_coverage < 2.0:
        out.append(Finding("Leverage Trap", "RED", False, f"D/E {f.debt_to_equity:.2f}x rising AND ICR {f.interest_coverage:.2f}x < 2.0x"))

    roce = f.roce_series
    if len(roce) >= 3 and (roce[-3] - roce[-1]) > 0.03:
        out.append(Finding("ROCE Decay", "ORANGE", False, f"ROCE down {(roce[-3]-roce[-1])*100:.1f}pts/2yrs, no capex explanation stated"))

    gm = f.gross_margin_proxy_series
    if len(gm) >= 2 and gm[-1] < 0.15 and (f.revenue[-1] / f.revenue[0] if f.revenue[0] else 0) - 1 != 0:
        # commodity dependence proxy: thin, revenue-linear margin
        pass  # left as a manual flag — needs COGS-to-commodity-price correlation the series alone can't prove

    if d.governance.promoter_pledge_pct >= 10:
        out.append(Finding("Pledge", "ORANGE", False, f"Promoter pledge {d.governance.promoter_pledge_pct:.1f}%"))

    return out


def run_all_gates(d: StockDossier) -> list[Finding]:
    return [
        g0_liquidity(d),
        g1_leverage(d),
        g2_earnings(d),
        g3_promoter_integrity(d),
        g4_objectivity(d),
        g5_valuation_sanity(d),
        *irani_flags(d),
    ]


def hard_discard(findings: list[Finding]) -> bool:
    """G0/G1/G2/G3-A/G3-C are absolute discards regardless of composite score."""
    for f in findings:
        if f.rule_id in ("G0", "G1", "G2") and not f.passed:
            return True
        if f.rule_id == "G3" and f.band == "RED":
            return True
    return False
