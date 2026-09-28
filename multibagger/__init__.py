"""Multibagger Engine — a computable implementation of the SR STOCK RESEARCH
Unified Framework (Part 7 / Section 5e / Section 6 / N1 / N8 gates).

This package implements every RULE in the framework that the source PDF states
as a formula or a numeric threshold. Rules that the framework itself leaves to
analyst judgement (moat-source evidence, MQF pillar scores, industry-phase
classification) are exposed as *inputs*, not computed — the engine never
invents a judgement call the framework requires a human, Tier 1-3 evidence for.
"""

from .models import StockDossier
from .composite import evaluate

__all__ = ["StockDossier", "evaluate"]
