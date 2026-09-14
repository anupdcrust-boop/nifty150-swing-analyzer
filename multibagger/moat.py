"""Section 5 (moat class), Section 5b-T (trajectory -> MATM conditioning),
Section 5c (Rule #27 decay scorecard).

Moat SOURCE ratings (GREEN/AMBER/RED per source) are analyst judgement backed
by Tier 1-3 evidence — this module never assigns them. It only applies the
framework's own counting/classification rules once those ratings exist.
"""

from dataclasses import dataclass

from .models import MoatSourceEvidence, MoatTrajectory


@dataclass
class MoatClassResult:
    moat_class: str  # NONE / NARROW / MODERATE / WIDE
    green_or_amber_count: int
    base_matm_anchor: float
    trajectory_conditioned_matm: float
    building_source_with_tier123: bool


_CLASS_TABLE = [
    (0, 1, "NONE", 1.00),
    (1, 2, "NARROW", 1.10),
    (2, 3, "MODERATE", 1.25),
    (3, 99, "WIDE", 1.50),
]


def classify_moat(sources: list[MoatSourceEvidence]) -> MoatClassResult:
    qualifying = [s for s in sources if s.rating in ("GREEN", "AMBER")]
    count = len(qualifying)

    moat_class, base_anchor = "NONE", 1.00
    for lo, hi, name, anchor in _CLASS_TABLE:
        if lo <= count < hi:
            moat_class, base_anchor = name, anchor
            break
    else:
        moat_class, base_anchor = "WIDE", 1.50

    # Section 5b-T: 1.10/1.25/1.50 anchors only apply where trajectory is
    # BUILDING or HOLDING on the sources backing the class; ERODING caps at 1.00x.
    eroding_dominant = qualifying and all(s.trajectory == MoatTrajectory.ERODING for s in qualifying)
    trajectory_matm = 1.00 if eroding_dominant else base_anchor

    building_source_tier123 = any(
        s.trajectory == MoatTrajectory.BUILDING and s.evidence_tier.value <= 3 for s in sources
    )

    return MoatClassResult(
        moat_class=moat_class,
        green_or_amber_count=count,
        base_matm_anchor=base_anchor,
        trajectory_conditioned_matm=trajectory_matm,
        building_source_with_tier123=building_source_tier123,
    )


def moat_trajectory_gate_clears(sources: list[MoatSourceEvidence]) -> bool:
    """Multibagger Candidate tier requires BUILDING on >=1 source, Tier 1-3 evidence."""
    return any(s.trajectory == MoatTrajectory.BUILDING and s.evidence_tier.value <= 3 for s in sources)
