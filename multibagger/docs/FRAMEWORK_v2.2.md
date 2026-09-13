# STOCK RESEARCH Unified Framework — v2.2 addendum

**APPLIED-AND-VERIFIED RELEASE.** This document does not replace the source
v2.1 PDF (`STOCK_RESEARCH_Unified_Framework_v2_1.pdf`) — it is a set of
findings and binding corrections discovered by actually *implementing* v2.1
as executable code (`multibagger/`) and running it against six real,
cross-sector, hindsight-confirmed multibaggers. Per **M1 Base-Rate
Discipline**, every finding below states its denominator; per **M2
Complexity Budget**, each fix is a correction to an existing rule, not a
new one, so it does not draw against the complexity budget the way Part 7
did in v2.1.

Read this alongside `multibagger/reports/BACKTEST_REPORT.md`, which is the
evidence base for every finding here.

---

## What v2.2 is, and isn't

v2.1 is a *methodology* — a document a human analyst reads and applies by
hand. v2.2's contribution is turning every rule v2.1 states as a formula or
numeric threshold into executable code (`multibagger/engine.py`,
`gates.py`, `moat.py`, `mqf.py`, `composite.py`), covered by 19 unit tests
including an exact reproduction of the PDF's own worked example (5x/5yr,
38.0% required return, 68% earnings share — see `tests/test_engine.py`).

Rules the PDF explicitly leaves to analyst judgement (moat-source ratings,
MQF pillar scores, industry-phase classification) are **not** automated —
they remain typed inputs a human must supply with Tier 1-3 evidence, exactly
as M6 requires. The engine only mechanizes what the PDF itself mechanizes.

**Data honesty note (read before trusting any number in the backtest
report):** live financial-data tooling was unavailable in the build
environment — the connected market-data API was gated to symbol search
only, and aggregator sites (Screener, Moneycontrol, Tijori, Macrotrends,
WSJ) were unreachable. The six backtest dossiers mix a handful of verified,
cited anchor facts with Tier-5 (general-knowledge) reconstruction of
everything else — explicitly *not* the Tier 1/2 evidence M6 requires for a
real gate-clearing verdict. Every finding below that depends on the
backtest's *numbers* is flagged as data-uncertain; findings that depend only
on the framework's *internal logic* (the gaps in sections 1-3 below) hold
regardless of data quality, because they were caught by reading the code's
own behaviour against the PDF's text, not by trusting the numbers it output.

---

## 1. Gap: G1 has no BFSI/utility carve-out (found applying it to Bajaj Finance)

**The rule as written (v2.1 PDF, Part 2):** "G1 Leverage — D/E above 2.0x
AND interest coverage below 1.5x simultaneously → DISCARD." G2's text
explicitly exempts "regulated utilities, BFSI, turnarounds." G1's does not.

**What happened when applied literally:** Bajaj Finance — one of the best-
documented compounders on the NSE, a lend-to-earn NBFC — structurally runs
D/E of 4-8x because borrowing at a spread *is* the business model. Applied
literally, G1 auto-discards every healthy NBFC before Stage 2 even runs,
which is absurd on its face: leverage is the fuel of a lender's ROE, not a
distress signal, provided the *spread* and *asset quality* are sound.

**Fix (binding, entering at PILOT per M1 — denominator: n=1, this case):**
`gates.py::g1_leverage` now exempts `is_regulated_utility_or_bfsi` names from
the D/E test entirely, returning a TEAL informational finding rather than a
pass or fail, with an explicit note that a sector-appropriate leverage test
(e.g. capital adequacy ratio, gross/net NPA trend, cost-of-funds trend) is
needed in its place and is not yet implemented — flagged, not quietly
scored as clean.

**Also found, same root cause:** Section 5e's ROIIC/RR formula defines
"invested capital" as net fixed assets + CWIP + net working capital — a
manufacturing/services balance-sheet model. For a lender, the capital that
compounds is the loan book funded by borrowings; net fixed assets are
almost irrelevant. Section 6B's profit-pool/runway gate has the same
problem in reverse — there is no product-market TAM for a loan book.
`composite.py::evaluate` now emits an explicit warning note on any BFSI name
that Section 5e's engine-growth figure should not be trusted, and skips the
6B gate's `addressable_profit_pool_cr` requirement (left `None`) rather than
scoring a meaningless number. **Recommended for v2.3, not yet built:** a
parallel BFSI engine test — incremental spread income ÷ incremental AUM in
place of ROIIC, book-value-per-share CAGR in place of RR, credit-cost-
adjusted ROE as the floor test in place of the ROIIC-vs-cost-of-capital gate.

---

## 2. Gap: Section 5e silently double-counts against Section 6A's own margin-delta term

**The rule as written:** Section 5e Gate 1 requires "g (ROIIC×RR) ≥ the
required net-profit CAGR from the Part 7 N1 return bridge." Separately,
Section 6A's operating-leverage-inflection test says: "the first two years
of a multibagger are usually margin, not volume... an unevidenced margin
delta is set to zero in the bridge and the bridge re-run" — implying the N1
bridge's required-EPS-CAGR figure is meant to be splittable into a
revenue-driven term and a margin-delta term, with the latter separately
evidenced and gated by 6A.

**The gap:** as specified, Section 5e's Gate 1 never performs that split —
it compares g (which is, by definition, a *volume/reinvestment-driven*
growth concept: more capital invested at a given return) against the
**full** required net-profit CAGR, which legitimately also contains the
margin-delta term. That silently demands reinvestment alone deliver 100% of
required earnings growth, including the margin contribution 6A already
claims to evidence and gate separately. Applied to all six backtest names,
this is the single most common blocker (see report) — worth checking
whether it is real strictness or a specification gap before trusting the
"AVOID" it produces at face value. It is the latter: comparing a pure-
volume growth figure against a blended volume+margin target isn't a
stricter test, it's an internally inconsistent one.

**Fix (PILOT, denominator n=6 — this backtest; needs independent
confirmation before PROVISIONAL):** `engine.py::compute_return_bridge` now
decomposes the bridge: `required_revenue_cagr = (1+required_eps_cagr) /
(1+margin_delta_used) - 1`, where `margin_delta_used` is the analyst's
`assumed_margin_delta_cagr` **only if** `margin_delta_evidenced=True` **and**
a `margin_delta_mechanism_note` is actually filled in — otherwise it is
zero, per 6A's own rule. Section 5e's Gate 1 (`composite.py::build_gate_table`)
now compares g against `required_revenue_cagr`, not the blended figure.

---

## 3. Gap: "price vs. the bridge" and "engine strength" were accidentally the same axis

**The rule as written (Part 6, the Engine×Price matrix):** the matrix is
explicitly **two independent axes** — "the primary axis is now the
compounding engine (the Part 7 gate); the secondary axis is price versus the
return the engine can deliver." The matrix keeps a real cell open for
"ENGINE WEAK, price BELOW bridge → value candidate only... never above 3%"
— i.e. even a business whose forward engine can't clear an ambitious target
can still be a modest position if today's price is undemanding.

**The gap (introduced by this implementation, not the PDF — flagged
honestly rather than presented as a PDF-derived rule):** the first version
of `composite.py::price_vs_bridge` reused the *same* engine-growth-vs-N1-
target ratio for both axes. That makes them perfectly correlated by
construction — a name failing the engine axis by a wide margin will,
tautologically, also show "price ABOVE bridge," which deletes the
BELOW-bridge value-candidate cell entirely. Running the backtest with this
version, every WEAK-engine name landed at IGNORE/AVOID with no
differentiation — a red flag that the two axes weren't actually independent.

**Fix:** `price_vs_bridge` now scores the price axis against what the
business has **already demonstrated** — a Peter Lynch PEG≈1 heuristic (fair
P/E ≈ trailing 3-year revenue CAGR in percentage points, bounded to
[8, 60]) — rather than against the aspirational N1 target. Re-running the
backtest after this fix immediately produced a differentiated result: Bajaj
Finance moved from a blanket AVOID to "SPECULATIVE / VALUE PATH ONLY —
WATCH," because its entry multiple was undemanding relative to its own
historical growth even though its engine didn't clear the aggressive 10x/10y
target — exactly the cell the PDF's matrix intends to keep open, and exactly
the differentiation a same-axis bug had been silently deleting.

---

## 4. Refinement: Section 5e's engine-growth gate graduated (PILOT)

**Finding:** treating "g < required revenue CAGR" as a single binary
hard-fail is inconsistent with how the rest of the suite grades severity —
G3 has four states, MQF has four bands, moat trajectory has three. A name
missing the requirement by a hair (g at 95% of what's needed) was
previously scored identically to one missing it by 70%.

**Fix:** a near-miss (g at 80-99% of the required revenue-driven CAGR) now
soft-fails — it caps the name at Steady Compounder rather than routing to
WEAK/IGNORE, matching how an ORANGE moat-trajectory miss is already
handled elsewhere in the same table. **Denominator so far: n=0** — none of
the six backtest names actually fell in the 80-99% band (they missed by
30-70%), so this refinement is logically motivated by the inconsistency
above but has not yet been exercised by a real near-miss case. Flagged
PILOT, not claimed as validated.

---

## 5. Practical finding: Section 5e's precise inputs are not sourceable from
   Tier 3 aggregators, let alone Tier 1/2, through automated tooling

Attempting to source real multi-year CWIP, net-working-capital, and
segment-level margin data for six companies via web search and site fetches
failed almost completely — every major Indian equity-data aggregator
(Screener, Moneycontrol, Tijori, Macrotrends) was unreachable from the build
environment, and web search returned only recent-quarter snippets for most
names, not historical annual series. This is not a framework defect, but it
is a real, discovered barrier to running Section 5e or the N8 funnel screen
as a repeatable, automated pipeline: **recommend the framework define an
explicit "screening-grade" approximation** — e.g. invested capital ≈
capital employed (net worth + total debt − cash), the same denominator
already used for ROCE — for use only in the N8 funnel screen and initial
triage, with a hard rule (already implied by M6, now made explicit) that no
BUY/ACCUMULATE verdict may cite this approximation as its Section 5e
evidence; a real verdict re-derives ROIIC from the precise definition using
Tier 1/2 statements.

---

## 6. Headline empirical finding from the backtest (read with the data caveat above)

All six real, hindsight-confirmed multibaggers — Astral (Industrials),
Titan (Consumer), Divi's Labs (Pharma), Persistent Systems (IT), Bajaj
Finance (Financials), Dixon Technologies (Consumer Electronics) — evaluated
as of a snapshot date *before* their known multi-year re-rating, land at
Engine verdict WEAK and fail to reach Multibagger Candidate tier under this
engine, even after the three fixes above. In five of six cases the sole or
dominant blocker is the Section 5e engine-growth gate, missing the required
revenue-driven CAGR by 30-70%, not by a hair.

Two readings are both plausible and neither should be dismissed:

- **(a) Data reading:** the Tier-5 reconstructions likely understate true
  historical ROIIC/reinvestment for all six names, since real balance-sheet
  detail wasn't obtainable. This is the more likely primary explanation and
  is exactly why M6 exists — do not treat any single number here as a
  verdict on these six real companies.
- **(b) Framework reading:** even granting generous, real, hindsight-
  informed assumptions (target multiples and horizons were set to roughly
  match what each stock *actually* delivered, not chosen aggressively), a
  meaningful share of these six real returns came from multiple re-rating
  beyond what a conservative, percentile-capped N1-2 exit-multiple ceiling
  would sanction in advance. That is very likely a real, not an artifactual,
  property of the framework — and it is not obviously a flaw: v2.1's own
  "failure mode" section already names this exact tension in the abstract
  ("a framework this conservative on governance will systematically exclude
  some genuine multibaggers... that exclusion is deliberate and correct").
  This backtest gives that abstract warning a concrete, quantified
  illustration across six sectors rather than a single anecdote.

**Recommendation:** track this at the next M1 review the same way S1/S12
tracks its own false-negative risk — log, for every name that fails only
the Section 5e/N1 gates while clearing everything else (moat, industry
phase, governance, variant perception), what actually happened to it over
the following 3-5 years. If a pattern of missed compounders concentrated on
this specific gate emerges with a real denominator, that is the evidence
needed to revisit the gate's strictness under M1 — not a hunch, a Tier-5
backtest, or this document alone.

---

## M2 accounting for v2.2

Every change above is a **correction to an existing v2.1 rule's
implementation**, not a new rule: G1's carve-out extends G2's existing
carve-out logic to a rule that should have had it from the start; the 5e/6A
split makes two existing sections consistent with each other rather than
adding a new gate; the price-vs-bridge fix repairs an implementation bug
introduced by this codebase, not a PDF rule; the graduated engine-growth
band reuses the multi-state pattern G3 and MQF already established. No new
rule is added, so v2.2 draws nothing against the M2 complexity budget.

## Denominator ledger (M1)

| Finding | Status | Denominator |
|---|---|---|
| G1 BFSI carve-out | PILOT | n=1 (Bajaj Finance) |
| 5e/6A margin-delta split | PILOT | n=6 (this backtest) |
| Price-vs-bridge axis decoupling | PILOT | n=6 (this backtest) |
| Engine-growth graduated band | PILOT | n=0 (not yet exercised by a real near-miss) |
| Screening-grade 5e approximation | Proposed, not implemented | n=0 |
| BFSI-variant engine test | Proposed, not implemented | n=0 |

None of the above may be described as VALIDATED or PROVISIONAL in any report
generated by this engine until a real, out-of-sample denominator exists —
consistent with M1's own text, which already applies this standard to every
Part 7 rule in v2.1.
