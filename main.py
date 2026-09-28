# Multibagger Engine — CLI entry point

"""Evaluates one or more stock dossiers (JSON) against the SR STOCK RESEARCH
Unified Framework v2.1/v2.2 and prints the Final Call Block for each.

Usage:
    python3 main.py multibagger/sample_data/*.json
    python3 main.py path/to/your_dossier.json
"""
import json
import sys

from multibagger.loader import load_dossier
from multibagger.composite import evaluate
from multibagger.report import final_call_block, gate_table_markdown


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python3 main.py <dossier.json> [more.json ...]")
        print("       python3 main.py multibagger/sample_data/*.json")
        return 1

    for path in argv:
        with open(path) as f:
            data = json.load(f)
        dossier = load_dossier(data)
        result = evaluate(dossier)

        print(f"\n{'='*70}")
        print(f"{dossier.name} ({dossier.symbol}) — {dossier.sector}")
        print("=" * 70)
        print(final_call_block(dossier, result))
        print()
        print(gate_table_markdown(result))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
