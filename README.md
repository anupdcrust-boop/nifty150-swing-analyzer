# nifty150-swing-analyzer

A computable implementation of the **SR STOCK RESEARCH Unified Framework**
for identifying durable, multi-year "multibagger" compounders — built by
implementing the framework's own formulas and gates as tested Python code,
then applying it to six real cross-sector stocks and fixing what broke.

## What's here

- **`multibagger/`** — the engine. Every RULE the framework states as a
  formula or numeric threshold (Stage 1 discard gates, the Section 5e
  compounding-engine test, the N1 return bridge, the N8 funnel screen, MQF
  governance scoring, the consolidated Multibagger Candidate gate) is
  implemented and unit-tested, including an exact reproduction of the
  source PDF's own worked example. Rules the framework leaves to analyst
  judgement (moat evidence, governance pillar scores, industry-phase
  classification) are typed inputs, never invented by the code.
- **`multibagger/docs/FRAMEWORK_v2.2.md`** — every gap found by actually
  running the framework, why it mattered, and the fix, with an M1-style
  denominator ledger. Read this before trusting the backtest's numbers.
- **`multibagger/reports/BACKTEST_REPORT.md`** — the framework applied to
  six real, hindsight-confirmed multibaggers across six sectors (Astral /
  Industrials, Titan / Consumer, Divi's Labs / Pharma, Persistent Systems /
  IT, Bajaj Finance / Financials, Dixon Technologies / Consumer
  Electronics), snapshotted before their known multi-year re-rating.
- **`multibagger/sample_data/`** — the six dossiers behind that report, in
  the JSON schema `main.py` reads. **Data-quality warning:** live financial
  data tooling was unavailable in the build environment, so these are a mix
  of a few verified, cited facts and Tier-5 (general-knowledge)
  reconstruction — explicitly not the Tier 1/2 evidence the framework
  itself requires for a real investment verdict. Treat them as fixtures
  that exercise the engine's logic, not as research on these six companies.
- **`multibagger/tests/`** — 19 unit tests, including the PDF's own N1
  worked example (5x/5yr → 38.0% required return, 68% earnings share) and
  regression tests for every gap found while applying the engine.

## Running it

```
python3 -m pytest multibagger/tests/ -v          # run the test suite
python3 main.py multibagger/sample_data/TITAN.json   # evaluate one dossier
python3 multibagger/scripts/run_backtest.py          # regenerate the backtest report
```

## Using it on a real name

Build a `StockDossier` (see `multibagger/models.py`) either directly in
Python or as JSON matching `multibagger/loader.py`'s schema, using real
Tier 1/2 sourced figures — not aggregator/approximate data — for anything
that will clear a NAVY (binding) gate. `multibagger/scripts/build_backtest_dossiers.py`
is a worked example of how a dossier is assembled.

## What this is not

Not investment advice, not a SEBI research report. A methodology reference
and its computable implementation, for personal research and education
only. See the source PDF's own disclaimer, which this project inherits in
full.
