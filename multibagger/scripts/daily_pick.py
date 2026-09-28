"""Picks one random, not-recently-repeated ticker from each market-cap band
for the daily coverage routine. Maintains a coverage log so a name doesn't
recur until its whole band has cycled through once.

Usage: python3 multibagger/scripts/daily_pick.py
Prints one "Band: TICKER" line per band and updates the coverage log.
"""
import json
import random
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from multibagger.data.universe import UNIVERSES

LOG_PATH = Path(__file__).resolve().parents[1] / "data" / "coverage_log.json"


def load_log() -> dict:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text())
    return {}


def save_log(log: dict) -> None:
    LOG_PATH.write_text(json.dumps(log, indent=2))


def pick_for_band(band: str, tickers: list[str], log: dict) -> str:
    covered = set(log.get(band, {}).get("covered", []))
    remaining = [t for t in tickers if t not in covered]
    if not remaining:
        # full cycle complete -- reset and start a fresh cycle
        remaining = list(tickers)
        covered = set()
    pick = random.choice(remaining)
    covered.add(pick)
    log.setdefault(band, {})["covered"] = sorted(covered)
    log[band].setdefault("history", []).append(
        {"ticker": pick, "date": date.today().isoformat()}
    )
    return pick


def main():
    random.seed()  # system entropy, not a fixed seed -- genuinely different each run
    log = load_log()
    picks = {}
    for band, tickers in UNIVERSES.items():
        picks[band] = pick_for_band(band, tickers, log)
    log["_last_run_utc"] = datetime.now(timezone.utc).isoformat()
    save_log(log)

    for band, ticker in picks.items():
        print(f"{band}: {ticker}")


if __name__ == "__main__":
    main()
