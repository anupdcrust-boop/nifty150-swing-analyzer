"""Loads every sample_data/*.json dossier, runs the full evaluation, and
prints a markdown report to stdout (redirect to reports/BACKTEST_REPORT.md)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from multibagger.loader import load_dossier
from multibagger.composite import evaluate
from multibagger.report import final_call_block, gate_table_markdown

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample_data"

KNOWN_OUTCOME = {
    "ASTRAL": "Real subsequent history (public record, not predicted by this run): Astral re-rated sharply through 2018-2022, among NSE's best-known industrial compounders of that period.",
    "TITAN": "Real subsequent history: one of NSE's largest cap-weighted multibaggers of the 2010s, driven by the organized-jewellery share shift this dossier's N7 names.",
    "DIVISLAB": "Real subsequent history: re-rated strongly 2019-2021 once the USFDA import alert was resolved and API/CRAMS demand accelerated.",
    "PERSISTENT": "Real subsequent history: ~7x re-rating 2020-2024 on digital-engineering demand and vertical (BFSI/Healthcare) mix shift.",
    "BAJFINANCE": "Real subsequent history: one of India's best-documented compounders, ~50x+ from 2014 through its 2024 peak before growth normalized.",
    "DIXON": "Real subsequent history: ~15-20x re-rating 2020-2023 on the PLI electronics-manufacturing scheme this dossier's N7 names as the closing event.",
}

def main():
    print("# Multibagger Engine v2.1 — Cross-Sector Backtest Report\n")
    print("Each name below is evaluated using ONLY the data available as of the stated snapshot")
    print("date — i.e. as if this framework had been run at that point in time, with no knowledge")
    print("of what happened next. See `multibagger/scripts/build_backtest_dossiers.py` for exact")
    print("data provenance and tier tags on every figure.\n")
    print("---\n")

    rows = []
    for path in sorted(SAMPLE_DIR.glob("*.json")):
        key = path.stem
        data = json.loads(path.read_text())
        dossier = load_dossier(data)
        result = evaluate(dossier)

        print(f"## {dossier.name} ({dossier.symbol}) — {dossier.sector}\n")
        print(f"Snapshot date: {dossier.market.gsec_date}\n")
        print("```")
        print(final_call_block(dossier, result))
        print("```\n")
        print(gate_table_markdown(result))
        print()
        print(f"**Known subsequent outcome:** {KNOWN_OUTCOME.get(key, 'n/a')}\n")
        print("---\n")

        rows.append((dossier.name, dossier.sector, result.engine_verdict, result.compounder_tier, result.final_call))

    print("## Summary table\n")
    print("| Name | Sector | Engine verdict | Compounder tier | Final call |")
    print("|---|---|---|---|---|")
    for name, sector, ev, tier, call in rows:
        print(f"| {name} | {sector} | {ev} | {tier} | {call} |")


if __name__ == "__main__":
    main()
