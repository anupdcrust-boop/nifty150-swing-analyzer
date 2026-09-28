# STOCK RESEARCH — The Unified Framework, Suite v2.2

**Institutional Equity Research | Personal Research Framework**
VERSION 2.2 | APPLIED-AND-VERIFIED RELEASE | SEPTEMBER 2026
Supersedes Unified Framework v2.1 in full.

Component versions under this release: Stage 0 v1.3 (unchanged) · Stage 1 v3.6 (G1 BFSI/utility carve-out) · Stage 2 v7.1 (Section 5e revenue/margin split, graduated engine-growth gate) · MQF v1.1 (unchanged) · Part 7 v1.1 (unchanged text; gate table cross-referenced to the 5e split) · Part 6 v2.2 (implementation notes on the Engine x Price matrix's independence).

>> v2.2 was produced by actually implementing v2.1 as executable code and running it against six real, cross-sector, hindsight-confirmed multibaggers — not by further desk review
>> Found and closed: G1's leverage gate had no BFSI/utility carve-out, unlike G2's explicit one — would have auto-discarded every healthy NBFC
>> Found and closed: Section 5e's engine-growth gate was silently double-counting against Section 6A's own margin-delta term
>> Section 5e's binary engine-growth gate is now graduated (a near-miss soft-fails to Steady Compounder, not to WEAK), matching the multi-state pattern G3 and MQF already use
>> Clarified (implementation guidance, not a rule change): the Engine x Price matrix's two axes must be measured independently — reusing one signal for both silently deletes the "engine weak, price undemanding" cell
>> All three rule amendments enter at PILOT per M1, each with its own denominator, per the ledger in the closing appendix
>> All Part 0 meta-layer rules, all kill-gates, and all other MQF/governance caps carry forward unchanged from v2.1

NOT investment advice — methodology reference for personal research only — consult a SEBI-registered adviser
STOCK RESEARCH · Unified Framework v2.2 · Stage 0 v1.3 · Stage 1 v3.6 · Stage 2 v7.1 · MQF v1.1

---

## Severity Colour Legend (applies to every report produced under this suite)

| Colour | Band | Meaning in a report | Consequence |
|---|---|---|---|
| GREEN | PASS / STRENGTH | Evidenced positive: gate cleared, engine test passed, moat trajectory BUILDING, clean governance finding | None — proceed |
| TEAL | INFORMATION | Neutral structural fact, methodology note, or figure with no directional read | None — context only |
| ORANGE | MEDIUM CONCERN | Irani AMBER, prudential cap, borderline score, PILOT rule invoked, engine test partially met (near-miss) | Cap, monitor, or one-notch conviction reduction |
| RED | SEVERE / DISQUALIFYING | Irani RED, kill-gate fired, G3-A, value-trap disqualifier, MQF AVOID, candidate-gate hard failure | Discard or hard cap — never outvoted by score |
| NAVY | STRUCTURAL RULE | A binding rule, cap or definition quoted from the framework itself | Not relaxable |

Every finding in every report carries exactly one band. A finding with no band is an incomplete finding. Colour is a rule, not decoration.

## What changed in v2.2, in one paragraph

v2.1 was a rigorous methodology that had never been run. Turning it into executable code and testing it against six real, cross-sector, hindsight-confirmed multibaggers (Astral/Industrials, Titan/Consumer, Divi's Labs/Pharma, Persistent Systems/IT, Bajaj Finance/Financials, Dixon Technologies/Electronics) surfaced two genuine textual gaps and one implementation trap. G1's leverage discard test carried no carve-out for BFSI/regulated-utility balance sheets, unlike G2's explicit one — applied literally it would auto-discard every healthy NBFC, Bajaj Finance included, since lending at a spread structurally requires 4-8x D/E. Section 5e's engine-growth gate compared a pure reinvestment-driven growth figure (g = ROIIC x RR) against the N1 bridge's full required earnings growth, which legitimately also contains a margin-delta term Section 6A separately claims to evidence and gate — silently demanding reinvestment alone deliver 100% of required growth, including a component it was never designed to capture. And a first attempt to implement the Engine x Price matrix's two axes reused the same underlying signal for both, collapsing them into one and deleting the "engine weak but price undemanding, value candidate up to 3%" cell the matrix's own text keeps open. v2.2 closes the first two as amendments to the rule text, and documents the third as implementation guidance for anyone coding this framework, since the original text was already correct on the point. It does not loosen a single governance rule, kill-gate, or MQF cap.

## Architecture map

| Layer | Question it answers | Status in v2.2 |
|---|---|---|
| Part 0 — Meta-Layer (M1-M9) | Is the framework itself still trustworthy? | Unchanged from v2.1 — binding on every component below |
| Part 1 — Stage 0 (v1.3) | Is a corporate-action turnaround being staged, and when can evidence exist? | Unchanged from v2.1 |
| Part 2 — Stage 1 (v3.6) | Is it cheap, is it a trap, and at what price? | Amended — G1 gains a BFSI/utility carve-out |
| Part 3 — Stage 2 (v7.1) | Is it durable, of what tier, how large, when to sell? | Amended — Section 5e Gate 1 split into revenue-driven and margin-delta terms |
| Part 4 — MQF (v1.1) | Can the promoter be trusted with the capital? | Unchanged from v2.1 |
| Part 5 — Portfolio & Execution | How does this position fit the book, and when does it leave? | Unchanged from v2.1 |
| Part 7 — Multibagger Engine (v1.1) | Does this business have a mechanism that can multiply capital, and is that mechanism available at this price? | Text unchanged; consolidated gate table's engine-growth row now graduated and cross-referenced to the 5e split |
| Part 6 — Output, Checklist, Integration | How is all of the above assembled and delivered? | Implementation note added on Engine x Price axis independence; no rule text changed |

---

## Part 0 — The Meta-Layer (M1-M9)

Unchanged from v2.1 in every particular. Reproduced here in full because this document supersedes v2.1 in full — nothing is left to a superseded PDF. Binding on all components below; cannot be relaxed by any component rule.

**M1 Base-Rate Discipline** — NAVY
No rule, trigger, band or multiplier may carry status VALIDATED without a stated denominator: N names screened, N that fired the rule, N that subsequently worked, N that failed. Status ladder: PILOT (no denominator) -> PROVISIONAL (denominator stated, n<3 successes or unstable hit-rate) -> VALIDATED (denominator stated, 3+ independent successes, failures disclosed). Every rule new to v2.1 (Part 7, and Stage 2 Sections 5b-T/5e/5f/6A/6B) and every rule amended in v2.2 (G1's carve-out, Section 5e's split, the graduated engine-growth band) enters or re-enters at PILOT.
*Why / how it binds:* Prevents a validation claim from resting on hindsight-selected winners. It is the single rule that keeps this whole suite honest about what it has actually earned.

**M2 Complexity Budget** — NAVY
The suite is capped at its current rule count. A new rule may be added only if (a) an existing rule is retired, or (b) the new rule arrives with an M1-compliant denominator. Annual audit deletes any rule that has not changed a verdict in 24 months. v2.2 adds no new rule — every change is a correction to an existing rule's text or an implementation clarification — so it draws nothing against the budget v2.1 already spent.
*Why / how it binds:* v2.1 added eight new rules with no denominators available and paid for them by retiring three existing rules (see v2.1's own M2 ledger, carried forward unchanged). v2.2 makes no such trade because it adds nothing new.

**M3 Edge Hypothesis (must be stated per position)** — NAVY
Claimed edges, in priority order: (1) time-horizon arbitrage — holding through drawdowns that force institutional selling; (2) coverage neglect — small/microcaps below institutional research thresholds; (3) behavioural discipline — pre-committed exits and pre-mortems reducing unforced errors. Explicitly NOT claimed: superior data, modelling, speed, or information advantage.
*Why / how it binds:* Every BUY must name which edge it relies on. A name relying on none is capped at WATCH — you have no reason to expect to be right.

**M4 Framework Kill-Switch (two-sided)** — NAVY
Downside: at the 24-month check, if BUY-verdict names underperform the relevant index on a cost- and tax-adjusted basis across a majority of closed positions, MANDATORY REVIEW fires — new positions paused. Upside/inaction: rejection rate above 95%, or zero BUY verdicts across four consecutive quarters, fires the same review.
*Why / how it binds:* Answers both failure modes — a process that loses money, and a process tightened until it can never act.

**M5 Adversarial Protocol (replaces solo self-assessment)** — NAVY
Before any first purchase: (a) steelman the short — the strongest bear case, in the bear's own framing; (b) disconfirming-evidence search, logged, including one hostile source; (c) 48-hour cooling period before first purchase, no new buying arguments admitted; (d) the Section 9A pre-mortem, written before the verdict.
*Why / how it binds:* A solo pre-mortem written after the work is confirmatory by default. This protocol also protects the Part 7 N1 return bridge from becoming arithmetic-shaped advocacy.

**M6 Source-Tier Hierarchy** — NAVY
Tier 1 audited statements, regulatory orders, court judgments. Tier 2 exchange filings, shareholding patterns, CARO/MR-3. Tier 3 aggregators (Screener, Trendlyne, Tickertape) — must be cross-checked against Tier 1/2 for any gate-driving figure. Tier 4 management narrative (concalls, investor decks, MD&A). Tier 5 media, brokerage notes, short-seller reports — leads only.
*Why / how it binds:* No gate clears on Tier 3 alone. No Section 5d test rates GREEN on Tier 4 alone. Every figure in a report carries its tier.

**M7 Benchmark Hurdle (opportunity cost)** — NAVY
Every BUY/ACCUMULATE must state: the relevant index benchmark (Nifty 50 / Midcap 150 / Smallcap 250 by cap band), the required annualised return over the stated horizon, and the specific driver expected to deliver it. Suggested floor: index return plus a risk premium sized to the MoS tier.
*Why / how it binds:* A name can clear every gate and still be a worse use of capital than an index fund at near-zero effort.

**M8 Funnel Discipline** — NAVY
Record the candidate source for every name entering the funnel: systematic screen / Stage 0 trigger / news or media / peer mention / existing holding review / other. Annual audit computes hit-rate and verdict distribution by source. Default minimum 50% of the annual funnel from systematic screens.
*Why / how it binds:* Coverage is the binding constraint — a full report is hours of work — so which names enter the funnel matters more than how they are scored.

**M9 Two-Pass Sequencing** — NAVY
Stage 1 Pass 1 runs with MATM fixed at 1.00x and produces a provisional Layer A and composite. Stage 2 then runs in full. Once Section 5b classifies the moat and Section 5b-T classifies its trajectory, Stage 1 Layer A is re-scored once with the correct MATM anchor. Both composites are logged; Pass-2 governs.
*Why / how it binds:* Resolves the circular dependency between Stage 1's MATM and Stage 2's moat classification.

---

## Part 1 — Stage 0: Special Situations & Turnaround, v1.3

Unchanged from v2.1. Question: is a corporate-action turnaround being STAGED, and when can the evidence exist? Stage 0 never produces a buy verdict, a position size, or a gate exemption — the single narrow exception is the v1.3 tracking-position carve-out at S1, capped at 0.5% and hedged by an automatic sunset.

### Triggers T1-T11

| ID | Trigger | Fire condition | Class | Status (M1) |
|---|---|---|---|---|
| T1 | Scheme of arrangement | NCLT scheme approved or merger/demerger effective date announced | A | PILOT |
| T2 | Name / identity change | Company name change, especially shell-to-brand | A | PILOT |
| T3 | Promoter stake rising | Promoter holding up >=5pp across <=2 quarters | A | PILOT |
| T4 | Preferential issue to promoters | Warrants/equity subscribed by promoter group | A | PILOT — co-validated with T5 |
| T5 | Founder / credible promoter return | Founder returns to board/MD, or credible new promoter | A | PILOT — co-validated with T4 |
| T6 | Demerger / subsidiary event | Record date set; subsidiary listed/delisted; carve-in/out | A | PILOT |
| T7 | First profit after loss streak | First profitable quarter after >=3 consecutive loss years | B | PROVISIONAL — 3 successes, denominator not yet counted |
| T8 | Restatement-driven revenue jump | Revenue >100% YoY with restatement/merger-accounting note | B | PILOT |
| T9 | Deleveraging complete | Net debt to net cash within 4 quarters, or >50% debt reduction | B | PROVISIONAL — 2 successes only |
| T10 | Re-rating in a small cap | Price >50% above 52-week low while mcap <Rs10,000 Cr | C | PILOT |
| T11 | First institutional entry | Bulk/block deal or new FII/DII holder, no prior history | C | PILOT |

Class A = corporate-event, Class B = financial-inflection, Class C = microstructure. At least one clustered trigger must be Class A or B. Two Class C triggers never qualify — that is momentum-chasing, not situation detection.

### Clustering, exclusions, re-screen condition

| Triggers in rolling 6 months | Result | Action |
|---|---|---|
| 1 | NOISE | No action, log nothing |
| 2, with >=1 Class A/B | STAGE 0 CANDIDATE | Open Turnaround Journal entry; dated re-screen condition; log cluster validation composition (S11) |
| 3+, with >=1 Class A | STAGE 0 PRIORITY | As above, plus pull scheme docs/AR immediately; pre-draft the Stage 1 data file |
| Spread >6 months apart | RESET | Window is rolling; stale triggers age out |

| Exclusion | Test | Band |
|---|---|---|
| X1 — Fraud-state promoter | Siphoning, funds to promoter entities, CBI/ED arrest — at ANY group entity | RED |
| X2 — Active PFUTP | Active SEBI PFUTP on sitting MD/CMD/CFO/WTD, not stayed or disposed | RED |
| X3 — SME / illiquid shell | 30-day ADTV persistently below Rs25 lakh AND mcap below Rs250 Cr | RED |
| X4 — Serial restructurer | Third or later scheme/name change/reorganisation at the same entity within 5 years | RED |

Re-screen condition, required at entry, no exceptions: earnings evidence (2 consecutive clean standalone profitable quarters post-event, 3 if merger accounting); governance evidence (all open prudential flags resolved per Stage 1 Layer D); structural evidence (corporate action complete); liquidity evidence (30-day ADTV clearing the Part 5 E-2 sized-position floor); a calendared date. Anti-FOMO (S5): a price rally is never a re-screen trigger — evidence dates only.

### Rules S1-S12

| # | Rule |
|---|---|
| S1 (v1.3 amended) | Stage 0 never produces a buy verdict, position size, or attractive-below price, with one narrow exception: a 0.5% tracking position is permitted at a qualifying cluster if >=1 Class A trigger has fired, X1-X4 are all clear, G3 state is D, and G0/E-2 liquidity floors are met at that size. The dated re-screen condition is still logged unchanged and full sizing still waits for the evidence date. Never a gate exemption, a verdict, or grounds to add. |
| S2 | 2+ triggers in a rolling 6-month window, at least one Class A/B. Two Class C never qualify. |
| S3 | X1 and X2 exclude absolutely — do not watch, do not journal beyond the exclusion note. |
| S4 | Every entry gets a dated re-screen condition AT ENTRY. No condition, no entry. |
| S5 | Price action is never a re-screen trigger. Evidence dates only. |
| S6 | Consolidated-only profit never satisfies the earnings evidence requirement. |
| S7 | Never re-screen mid-corporate-event. |
| S8 | Maximum 3 re-screen cycles per entry, then archive with reason. The archive retires the ENTRY, not the NAME — a completed corporate action re-admits the name as a fresh Stage 1 candidate. |
| S9 | Stage 0 membership confers NO exemption from any Stage 1/2 gate — front-door re-entry always. |
| S10 | Trigger status follows PILOT/PROVISIONAL/VALIDATED (M1) and requires a denominator for any validation claim. No trigger in the suite currently holds VALIDATED status. |
| S11 | Every journal entry records the validation composition of its cluster, e.g. 'T4 [PILOT] + T3 [PILOT]', for later false-negative review weighted by evidence strength. |
| S12 (v1.3) | Every S1 tracking position is tagged PILOT under M1 with its own denominator track: N opened, N reaching the evidence date intact, N exited at a loss first. Reviewed at the annual audit; a negative 24-month record reverts S1 to its pre-v1.3 absolute text automatically. |

Flagged for attention (unchanged from v2.1): S1/S12 is the single most dangerous rule change of the v2.0-to-v2.1 transition — it puts a hole in a rule that worked precisely because it was absolute. The 0.5% cap, the Class-A requirement and the self-reverting sunset exist to bound the damage.

---

## Part 2 — Stage 1: Undervalued Stock Identification, v3.6

Question: is it genuinely cheap, is it a trap, and at what price? Runs Pass 1 at MATM 1.00x, then re-scores once after Stage 2 classifies the moat and its trajectory (M9).

### Gates G0-G5

| Gate | Test | Consequence | Band |
|---|---|---|---|
| G0 Liquidity | 30-day ADTV below Rs1 Cr; also tests the Part 5 E-2 sized-position floor | DISCARD | RED |
| G1 Leverage (v2.2 amended) | D/E above 2.0x AND interest coverage below 1.5x simultaneously -> DISCARD. **New in v2.2: does not apply to a BFSI or regulated-utility balance sheet.** A lender's structural 4-8x D/E is the business model, not a distress signal; applying this test literally would auto-discard every healthy NBFC. For a BFSI/utility name, this gate is scored TEAL (informational, not pass/fail) and a sector-appropriate leverage test — capital adequacy ratio, gross/net NPA trend, cost-of-funds trend — must be evidenced separately before sizing. That replacement test is not yet specified by this suite; treat its absence as an open item, not a clean pass. | DISCARD (non-BFSI) / TEAL — informational only (BFSI/utility) | RED / TEAL |
| G2 Earnings | Negative PAT for 3 consecutive years (excl. regulated utilities, BFSI, turnarounds) | DISCARD unless turnaround | RED |
| G3 Promoter integrity | Four-state A/B/C/D taxonomy | State-dependent cap | RED/ORANGE |
| G4 Objectivity | Enforced by the M5 adversarial protocol, not self-assessment | Protocol incomplete = cannot lock | ORANGE |
| G5 Valuation sanity | P/E >3x sector median -> REVIEW. Eliminates only if all four G5 conditions hold | INVESTIGATE | ORANGE |

| G3 state | Definition | Cap | Band |
|---|---|---|---|
| G3-A | Siphoning; funds to promoter entities; CBI/ED arrest | 0% — full discard | RED |
| G3-B | Pledge 10-25%; promoter holding <15%; settled enforcement | Max 1.5% | ORANGE |
| G3-C | Active SEBI PFUTP on sitting MD/CMD/CFO/WTD | Max 1% | RED |
| G3-D | Pledge <10%; no investigation; holding >25%; clean | Standard | GREEN |

### Irani governance flags

| Flag | Trigger | Position impact | Band |
|---|---|---|---|
| Accounting Gap | PAT>OCF 3+yrs; receivables outrunning revenue; exceptionals >50% PAT | Layer C EQ zeroed; value-trap flag | RED |
| SEBI PFUTP | Active, not stayed/disposed | G3-C; position max 1% | RED |
| Leverage Trap | D/E>1.5x rising AND interest coverage<2.0x | G1 logic; value-trap flag (non-BFSI names only — see G1 amendment above) | RED |
| Founder Large OFS IPO | OFS>60% AND fresh issue<40%; founder seller | Layer D -2; cap 3% | ORANGE |
| Value Extraction | Foreign PE promoter + payout>100% for 2+yrs + rev CAGR<10% | Layer D capped 8/15 | ORANGE |
| Di-worse-ification | Frequent unrelated acquisitions; capital destroyed in non-core | Layer C -3; Layer D -2 | ORANGE |
| Commodity Dependence | Revenue 1:1 with commodity; COGS>70%, GM<15% | Passthrough discount | ORANGE |
| ROCE Decay | ROCE down >3pts/2yrs, no capex explanation | Mandatory review | ORANGE |
| Correlation Concentration | Single macro factor >30% of portfolio | Enforced at Part 5 P-3 | ORANGE |
| Auditor/CFO Resignation | Outside routine rotation, or CFO/COO departs w/o succession, within 18mo | Layer D -2; explanation required before BUY | ORANGE — prudential |

### Section 4A — Rule #25

Step 1 — basis. FORWARD EPS at 75% utilisation only if BOTH hold, evidenced separately: (a) the G5 trough/capex/turnaround definition; AND (b) a completed, dated Section 4B bridge. Absent (b), TTM EPS applies even where (a) holds. Steady-state names are always TTM.

| Outcome | Test | Consequence |
|---|---|---|
| PASS | Earnings yield (correct basis) >= live 10-yr G-Sec, sourced and dated | Full scoring; M7 hurdle still applies separately |
| REVIEW BAND | Fails on yield alone, but (earnings yield + sustainable dividend yield) >= G-Sec AND fwd P/E <1.2x sector median | Scoring proceeds, capped at ACCUMULATE/STEADY COMPOUNDER — definitional, not relaxable |
| FAIL | Earnings yield fails and the total-yield test also fails | WATCH only |

Mandatory caveat, printed verbatim on every REVIEW-BAND invocation: "[PILOT — n=1] The Total-Yield Tolerance Band rests on a single validation case (ITC), used as both calibration and live invocation. UNVALIDATED, not confirmed. Conviction reduced one notch." Nominated for deletion at the next annual audit unless a third, genuinely independent case is logged first.

### Layer A — relative valuation (30 pts)

| Metric | How tested | Attractive when |
|---|---|---|
| P/E — TTM / 1yr fwd / 2yr fwd | Forward EPS anchored to capacity/guidance, never hope | Below own 5-yr and sector median on TTM, or compelling forward |
| PEG | 3-yr forward EPS CAGR, not historical | Below 1 attractive; ~1 fair; above 1.5 rich |
| P/B (sector-adjusted) | Sector thresholds table | Below sector deep-value band |
| EV/EBITDA — TTM + fwd | Forward at 75% utilisation; mandatory for capex-phase | Below peers, debt-neutral |
| FCF yield | Operating FCF; capex-phase years documented and excluded | Above 5-7% |
| Earnings yield vs G-Sec (#25) | Section 4A basis logic + tolerance band | Comfortably above G-Sec on the correct basis |
| MATM (bounded, trajectory-conditioned) | Exactly one of 1.00x(none)/1.10x(NARROW)/1.25x(MODERATE)/1.50x(WIDE), read off Section 5b. The 1.10/1.25/1.50 anchors apply only where Section 5b-T rates trajectory BUILDING or HOLDING. ERODING caps MATM at 1.00x regardless of moat class. Pass 1 always uses 1.00x. | Current multiple below the conditioned MATM fair multiple |
| Dividend yield — retired for Part 7 engine-assessed names | Payout sustainability; feeds the tolerance band. Kept in full for the non-engine value path. | Above own history and G-Sec — value path only |
| M7 Benchmark hurdle | Required annualised return vs the relevant index, driver named | Expected return clears index plus tier-appropriate risk premium |

### Section 4C — intrinsic value, EFV, bear-case gate

Two-phase DCF mandatory for ramp/capex-phase businesses (Phase 1 ramp CAGR, Phase 2 steady-state — never a single blended CAGR). Probabilities default 25/50/25, pre-registered with a timestamp before bear/base/bull values are computed; deviation requires a specific dated external fact. EFV = (P_bear x Bear)+(P_base x Base)+(P_bull x Bull), reported alongside the base case, never replacing it. Quantitative bear-case gate: probability-weighted downside must not exceed the Required MoS for the tier. UNDERVALUED additionally requires bear-case forward P/E <=2x sector median.

| Business quality tier | ROCE / character | Required MoS | Band |
|---|---|---|---|
| Exceptional compounder | Above 25%, wide moat, clean governance | 15-20% | GREEN |
| Good quality | 15-25%, moderate moat | 25-30% | GREEN |
| Average / improving | 10-15%, improving trend | 35-40% | TEAL |
| Cyclical / commodity | Highly variable, commodity-linked | 40-50% | ORANGE |
| Turnaround / distressed | Negative to low, recovery thesis | 50%+ — size very small | ORANGE |
| Capex-phase ramp | Below target, ROCE recovery documented | 25-35% on forward intrinsic | TEAL |
| Engine compounder | ROIIC>20%, RR>50%, trajectory BUILDING, all Part 7 gates passed, MQF HIGH-TRUST (85+) — all five required, none waivable | 10-15% on the N1 bridge, taken in duration: bridge must still clear M7 if high-return duration is cut to 60% of assumed period | GREEN |

Abuse guard on the Engine compounder row: gated on MQF HIGH-TRUST — the strictest governance band in the suite — precisely because a compounder-grade MoS on an ungoverned business is how value frameworks blow up. Any MQF band below 85 routes the name back to the tiers above.

### Composite, verdict bands, sizing

Layers: A relative valuation /30 · B intrinsic & MoS /30 · C business quality /25 · D governance & safety /15. Round to nearest 5; within +-3 of a boundary is BORDERLINE, resolved by a Layer C+D tie-break, never by the decimal.

| Composite | Verdict | Band |
|---|---|---|
| 80-100 | STRONGLY UNDERVALUED — high-conviction buy at the appropriate MoS | GREEN |
| 65-79 | UNDERVALUED — accumulate on dips; confirm catalyst | GREEN |
| 65-79 + fwd PE compelling | STEADY COMPOUNDER — route to Stage 2, accumulate slowly | GREEN |
| 50-64 | FAIRLY VALUED — watchlist; re-screen quarterly | ORANGE |
| 35-49 | SLIGHTLY OVERVALUED — no action / trim | ORANGE |
| Below 35 | OVERVALUED — avoid / exit on strength | RED |
| Any disqualifier | VALUE TRAP FLAG — reject regardless of score | RED |

| Condition | Tier | Size |
|---|---|---|
| Score 80-100, Layer D clean, 2+ catalysts | HIGH CONVICTION BUY | 5-7% |
| Score 65-79, Layer D clean, 1+ catalyst | BUY / ACCUMULATE | 3-5% |
| Score 65-79 + fwd PE compelling, 1+ catalyst | STEADY COMPOUNDER | 2-4% |
| Rule #25 REVIEW-BAND pass, any composite | Capped — not relaxable | Max applicable tier; never 5-7% |
| Score 65-79, 0 catalysts | WATCH — no catalyst | 0-1% |
| M3 edge not nameable / M7 hurdle not cleared | Capped at WATCH | 0-1% |
| G3-C / G3-B / G3-A governance caps | Binding governance caps | 1% / 1.5% / 0% |
| 4+ conditional flags | Exception-stack cap (prudential) | Max 1% |

Cap Reconciliation: GOVERNANCE caps (G3-A/B/C, PFUTP, siphoning, Founder-OFS, Value Extraction, MQF cap) are binding, never relaxed. PRUDENTIAL caps (exception stack, catalyst tier, volatility) manage timing/uncertainty and may not alone force an intact high-conviction thesis below its documented floor. DEFINITIONAL caps (Rule #25 REVIEW band, M3, M7) are part of the rule that creates them and never relaxable.

---

## Part 3 — Stage 2: The Multibagger Deep-Dive, v7.1

Question: is this a durable compounder, of what tier, how large, and when to sell?

### Section 1A — Full-Coverage Rule (closes D-8)

Full Stage 2 runs on every name Stage 1 scores FAIRLY VALUED or better, and on every name Stage 1 rejects on price alone with Layers C+D otherwise clean (the multibagger-relevant rejection class, preserved deliberately). Every other rejection — governance-driven, quality-driven, or trap-flagged — receives a 10-line qualitative note plus the mandatory M5 pre-mortem, no Module numbers. Sole carve-out unchanged: G3-A discards get the qualitative note only, no scoring at all. Sizing independence is unchanged — a high Module score on a Stage-1-rejected name is calibration only, never a route back to BUY.

### Section 5 — moat analysis (Module A foundation)

| Moat source | Evidence required | Rating logic |
|---|---|---|
| 1. Pricing power | 5-yr gross margin trend; price-hike history vs volume | GREEN: GM stable/rising through downturns. RED: no pricing power, GM<20% |
| 2. Switching costs | Integration depth; churn; contract length | GREEN: multi-year plus integration. RED: commodity, easy switch |
| 3. Network effects | User CAGR vs revenue CAGR; platform metrics | GREEN: demonstrated with data. RED: none |
| 4. Cost advantage | EBITDA margin vs peers; named process/technology | GREEN: >300bps AND innovation-driven. Scale-only capped AMBER |
| 5. Intangible assets | Documented price premium; patent/licence uniqueness | GREEN: documented premium or unique licence |
| 6. Efficient scale | Market size; entrant ROCE vs incumbent | GREEN: duopoly/oligopoly, entrant ROCE below cost of capital |

| Class | Sources | GREEN ROCE band | Module A range | MATM anchor |
|---|---|---|---|---|
| NONE | 0-1 | Below 12% | 0-20 | 1.00x |
| NARROW | 1-2 | 12-18% | 20-45 | 1.10x |
| MODERATE | 2-3 | 15-25% | 45-65 | 1.25x |
| WIDE | 3+ | Above 25% | 65-100 | 1.50x |

A moat premium is earned by evidence, never assertion. Under M6 the evidence must be Tier 1-3; Tier 4 narrative alone cannot make a source GREEN.

**Section 5b-T Moat Trajectory (closes diagnosis D-5)** — NAVY
Every Section 5 moat source rated GREEN or AMBER is additionally classified BUILDING / HOLDING / ERODING over 3-5 years, on evidence: market-share trend; gross-margin trend versus the sector's; price realisation versus input costs; customer count and retention; the company's share of the industry's incremental capacity additions; brand/R&D/distribution spend and its measurable output.
Rule (binding, feeds Stage 1 Layer A MATM): the MATM anchors 1.10/1.25/1.50 apply only where trajectory is BUILDING or HOLDING. ERODING caps MATM at 1.00x regardless of moat class. Multibagger Candidate tier requires BUILDING on at least one source, with Tier 1-3 evidence. HOLDING throughout caps at Steady Compounder. Re-rated annually alongside Rule #27; a BUILDING->HOLDING transition is a logged conviction event, not a silent one.
*Why / how it binds:* v2.0 grades the moat a company has; the return comes from the moat it is acquiring. A priced-in moat is what the market is best at valuing and therefore the worst place to look for a mispricing.

### Section 5c — Rule #27 moat decay scorecard (mandatory annual)

| Erosion signal | Trigger | Impact | Band |
|---|---|---|---|
| Pricing power loss | GM down >200bps YoY for 2 years | Moat -2 | ORANGE |
| Market share erosion | Revenue CAGR below sector for 3 years | Moat -2 | ORANGE |
| Technology disruption | >20% of TAM threatened by new technology | Moat -3 | RED |
| Customer concentration | Top-3 customers >50% AND one exits | Moat -2 | ORANGE |
| Regulatory moat removed | Licence/patent/regulatory barrier lapsed | Moat -4; full re-score | RED |
| ROCE decay | Down >3pts/2yrs, no capex explanation | Links to Section 8 | ORANGE |

Any RED = mandatory thesis review. Two or more AMBER = reduce conviction tier one step.

### Section 5d — Innovation and Learning Culture (mandatory)

| Test | Question | Evidence floor (M6) |
|---|---|---|
| I-1 Value chain innovation | Structural manufacturing/logistics/procurement improvement in 3-5 yrs? | GREEN requires Tier 1-3 corroboration; concall claims alone cap AMBER |
| I-2 Digital/technology adoption | Creating differentiation, or merely meeting compliance? | Same floor — measurable output, not a stated initiative |
| I-3 Regulatory adaptability | Speed/effectiveness in adapting to regulatory change historically | Tier 1-2 available by nature — no excuse for Tier 4 here |
| I-4 Workforce & succession depth | Institutional knowledge beyond founder/current MD? Real second line? | Named executives with tenure/disclosed responsibility, not org-chart assertion |

Scoring: 3+ GREEN = STRONG. 2 GREEN+1-2 AMBER = ADEQUATE. 2+ RED = WEAK (Module A -3, Module B runway capped). A STRONG/ADEQUATE rating against 2+ Rule #27 AMBER signals, or against declining forward ROCE with no capex explanation, is downgraded one tier and the conflict named in the Section 9A pre-mortem.

**Section 5e The Compounding Engine — reinvestment rate x incremental ROIC (v2.2 amended, binding gate)** — NAVY

Compute and report three figures: ROIIC = Delta NOPAT (3-yr) / Delta invested capital (3-yr), where invested capital = net fixed assets + CWIP + net working capital; Reinvestment rate (RR) = (capex + Delta WC - depreciation) / NOPAT; Engine growth g = ROIIC x RR.

**Gate 1 (tier gate, v2.2 amended).** Multibagger Candidate tier requires g >= the required REVENUE-DRIVEN CAGR from the Part 7 N1 return bridge, computed on ROIIC, not headline ROCE — **not the bridge's full required net-profit CAGR.** The v2.1 text compared g against the bridge's full required growth figure, which can legitimately include a margin-delta (operating-leverage) contribution that Section 6A separately evidences and gates. Comparing a pure reinvestment/volume growth concept (g) against a blended volume-plus-margin target double-counts the bar. v2.2 splits the bridge's required EPS CAGR into its revenue-driven and margin-delta components: `required_revenue_CAGR = (1 + required_EPS_CAGR) / (1 + margin_delta_CAGR) - 1`, where margin_delta_CAGR is zero unless Section 6A's mechanism is explicitly named and evidenced (per 6A's own pre-existing rule: "an unevidenced margin delta is set to zero in the bridge and the bridge re-run"). Gate 1 now tests g against this revenue-driven figure only.

**Gate 1a (graduated, v2.2 new).** A near-miss — g at 80-99% of the required revenue-driven CAGR — soft-fails: it caps the name at Steady Compounder rather than routing to a hard WEAK/AVOID, matching the multi-state pattern G3 and MQF already use elsewhere in this suite, rather than treating a narrow miss identically to a business with no engine at all.

**Gate 2 (floor).** ROIIC below cost of capital for two consecutive years is RED — value is being destroyed at the margin while headline ROCE lags on legacy assets.

**Gate 3 (payout conflict).** 3-yr average payout above 40% forecloses Multibagger Candidate tier outright; route to Steady Compounder. High payout and high compounding are arithmetically incompatible.

**Gate 4.** Layer A's dividend-yield metric is retired for names assessed under this section.

*Why / how it binds:* ROCE tells you what the past capital earned; ROIIC tells you what the next rupee will earn; the reinvestment rate tells you how many rupees there will be. A multibagger is a high ROIIC compounded at a high reinvestment rate for longer than the market assumed. The v2.2 split additionally ensures this gate measures only what it was designed to measure, leaving the margin-expansion story — often the actual first-two-years driver of a real multibagger — to Section 6A, where it is separately evidenced rather than silently assumed away or double-charged against reinvestment math.

**Section 5f Promoter Alignment (forward-looking, distinct from MQF)** — NAVY

MQF answers whether the promoter is honest. This section answers whether the promoter is building. Report: promoter holding level and 3-year direction; open-market promoter purchases (Reg 29/31, M6 Tier 2); pledge trend; the 5-year record of capital deployed and the ROIIC it earned (links to Section 5e); ESOP structure and whether vesting is performance-linked; related-party trend (inherits MQF Section 7). Gate 1. Promoter holding falling three consecutive years with no documented, non-monetising reason is ORANGE, one-notch conviction cap. Gate 2. Promoter holding below 25% in a sub-Rs10,000 Cr name with no institutional anchor is ORANGE. Gate 3. Documented open-market promoter buying near CMP is a GREEN corroborating signal — never sufficient alone, never a substitute for Section 5e or 5b-T.

### Section 6 — capex, business model, ROCE decay

Capex-phase names: quantum vs balance sheet; moat-reinforcing vs commodity-capacity test; ROCE recovery timeline; utilisation milestone triggers; capex discipline history; dilution/completion risk. Capex Phase Modifier: board-approved capex, ROCE declining, utilisation <60% -> forward ROCE at 75% utilisation, suspend the ROCE-decay signal while documented and moat-reinforcing. Utilisation >70% and ROCE still not recovering -> exception expired, activate moat-decay check.

**Section 6A Industry Phase & Operating-Leverage Inflection (entry timing)** — NAVY

Industry phase. Classify EMERGENT / INFLECTION / MATURE / DECLINING with evidence. Multibagger Candidate tier requires EMERGENT or INFLECTION, or a documented share-gainer in a MATURE industry (3 consecutive years of revenue CAGR above sector). MATURE + share-flat caps at Steady Compounder. DECLINING caps at WATCH irrespective of valuation. Operating-leverage inflection. Where the Part 7 N1 bridge relies on a margin delta, name the mechanism and evidence it: capacity utilisation trajectory, gross-block-to-sales turn, fixed-cost absorption, falling interest cost post-deleveraging, or mix shift with segment data. An unevidenced margin delta is set to zero in the bridge and the bridge re-run — **this is the same rule Section 5e's v2.2 amendment now cross-references directly, closing the loop between the two sections.**

**Section 6B Module B sub-test — Runway & Profit Pool** — NAVY

State: current market cap; the addressable profit pool (industry revenue x a defensible normalised industry margin); the company's current share of it; and the share implied at the Part 7 N1 target market cap, holding the exit multiple fixed. Gate. If the target requires capturing more than 25% of the addressable profit pool, and the company is not already the leader of a consolidating duopoly, this is RED and the target multiple must be reduced until the implied share is defensible. Size band. Record the market-cap band at entry (micro <Rs1,000 Cr / small Rs1,000-10,000 Cr / mid Rs10,000-50,000 Cr / large >Rs50,000 Cr). Multibagger Candidate tier above Rs50,000 Cr requires an explicit, logged reason the size objection does not apply.

*Note (v2.2 implementation guidance, not a rule change):* this section's "addressable profit pool" concept does not translate to a lender or other balance-sheet-driven financial business — there is no product-market TAM for a loan book. For a BFSI name, leave this gate unscored (not scored RED for absence of data) and note the limitation, pending a BFSI-specific variant.

### Section 7 — four-question classifier

(Q1) same moat sources as the core? (Q2) management track record in this area? (Q3) capital deployed above cost of capital? (Q4) domain competence AND succession depth beyond the founding team? Four YES = Accretive Adjacency. Two or more NO = Pivot Risk. Capital below cost of capital for 2+ years = Di-worse-ification. Q4 capability-YES-but-succession-NO = AMBER, linked to 5d I-4.

| ROCE trend | Read | Action | Band |
|---|---|---|---|
| -1 to -3pts/1yr | Normal operating variance | Note; watch | TEAL |
| -3pts/2yrs (not capex) | Early decay signal | Mandatory review; re-run Section 5 | ORANGE |
| -5pts/2yrs | Structural concern | Reduce to 50%; reassess moat | ORANGE |
| -8pts/2yrs, or ROCE<10% | Thesis likely broken | Exit unless documented capex-phase | RED |
| ROCE turns negative | Thesis broken | Immediate exit unless a G2 turnaround was set at entry | RED |

### Section 9A — the pre-mortem (inside the M5 adversarial protocol)

Mandatory before any verdict is locked, including every rejection. Step 1 steelman the short — strongest bear case as if arguing for payment. Step 2 disconfirming-evidence search, logged, one hostile source minimum. Step 3 pre-mortem paragraph, 4-5 sentences, written before the verdict — it is three years later and this call was wrong; what proved it wrong, which metric moved first. Logged verbatim, re-read first at every forward check. Step 4 48-hour cooling period before first purchase. A report without Steps 1-3 is incomplete regardless of composite; a purchase without Step 4 is a logged process breach.

### Modules A/B/C, tiers and sizing

Module A economic moat and quality (inclusive of 5b-T trajectory and 5f alignment) · Module B growth and scalability (inclusive of the 6B runway/profit-pool sub-test) · Module C capital efficiency and valuation, cross-checked against the Stage 1 EFV. Each scores to 100. Module C below 65 gates to WATCH regardless of composite.

| Condition | Tier | Size | Band |
|---|---|---|---|
| Composite 80+, A 80+, C 80+, all Part 7 gates clear | MULTIBAGGER CANDIDATE — triple conviction | 6-8% | GREEN |
| Composite 76+, A 75+, C 75+, all Part 7 gates clear | MULTIBAGGER CANDIDATE — quality + future | 5-6% | GREEN |
| Composite 70+, A 75+ | STEADY COMPOUNDER | 4-5% | GREEN |
| Composite 65-74, C 65+ | SPECULATIVE ACCUMULATION | 2% | ORANGE |
| Composite 60-74, C below 65 | WATCHLIST | 0-1% | ORANGE |
| Below 60, or G5 review fails, or Stage 1 verdict AVOID/WATCH | SKIP / CAP | 0-1.5% | RED |
| MQF ELEVATED GOVERNANCE RISK or AVOID | GOVERNANCE-CAPPED — binding | 0-1% | RED |
| G3-A | INSTANT SKIP | 0% | RED |

Multibagger Candidate tier is not available on composite score alone — it additionally requires every Part 7 gate to clear (see the consolidated gate table in Part 7). A name that scores 80+ but fails, say, the runway gate or the engine-growth gate is capped at Steady Compounder. Rule #26 (simplified): VIX-based de-sizing is not used and the four-band table is retired. Tranche for timing only; pause new entries briefly only if liquidity itself is seizing.

---

## Part 4 — Management Quality & Forensic Governance, MQF v1.1

Unchanged from v2.1. Governance is assessed before valuation and can veto Stage 2 sizing outright. A cheap — or fast-compounding — stock with a compromised promoter is not a value pick or a multibagger; it is a slow-motion capital-loss event.

### Kill-gates — automatic disqualification regardless of composite

- Auditor resignation citing inability to access information or non-cooperation, unresolved
- SEBI debarment of a promoter or director from the securities markets, currently in force
- Promoter or group entity classified as a wilful defaulter, currently in force
- Forensic audit ordered by a regulator or lenders, in progress or with adverse findings
- Conviction — not merely charge-sheet — of a promoter in a fraud-related criminal case
- Verified diversion of company funds to promoter entities, by regulatory or judicial finding

| Pillar | Weight | Source |
|---|---|---|
| Related-party transaction conduct | 25% | Section 7 (5-yr lookback, minority-disadvantage test) |
| Board and audit independence | 20% | Sections 9, 10 |
| Ownership and group structure transparency | 15% | Sections 2, 4, 6 |
| Capital allocation discipline | 10% | Section 8 |
| Management stability and remuneration fairness | 10% | Sections 11, 12 |
| Leverage, pledge and regulatory-legal cleanliness | 10% | Sections 13, 14, 15 |
| Earnings quality (forensic checklist) | 10% | Section 17 |

Each pillar scores 0-10. Composite = Sum(pillar x weight) x 10, out of 100. Section 20A Pattern Escalation: 3+ DISCLOSED/UNRESOLVED or ALLEGATION/MEDIA-CLAIM items clustering within a rolling 18 months and spanning >=2 of Sections 7/9/10/15/16 caps the assessment at ELEVATED GOVERNANCE RISK regardless of composite. Single-pillar floor: any one pillar <=3/10 caps the verdict at ACCEPTABLE WITH MONITORING even where the weighted composite would reach HIGH-TRUST. Both caps may apply; the lower governs.

| Score | Verdict | Portfolio implication | Band |
|---|---|---|---|
| 85-100 | HIGH-TRUST MANAGEMENT | No governance-based size constraint | GREEN |
| 65-84 | ACCEPTABLE WITH MONITORING | Position size capped; re-run RPT/pledge/litigation every 2Q | ORANGE |
| 45-64 | ELEVATED GOVERNANCE RISK | Stage 2 sizing capped at WATCHLIST. Tracking position at most | RED |
| Below 45, or any kill-gate | AVOID | Not investable irrespective of valuation, growth or engine score | RED |

Section 19 tags: VERIFIED FACT (Tier 1-2, cite document and date) / DISCLOSED-UNRESOLVED (state current stage) / ALLEGATION-MEDIA CLAIM (Tier 5, name source, never present with the confidence of a verified fact).

---

## Part 5 — Portfolio & Execution Layer, v2.1 (unchanged in v2.2)

Nothing here overrides a governance cap; everything here can reduce a position below what Stage 2 would otherwise allow.

| Rule | Content | Band |
|---|---|---|
| P-1 | 10-15 positions. Max 8% at cost — unchanged, never relaxed. Cap at market raised to 25% for a position whose moat trajectory (5b-T) is BUILDING or HOLDING and whose ROIIC (5e) remains above cost of capital. Above 25% at market: trim review, not automatic trim. Adding above the 8% cost cap remains prohibited in all cases. Minimum meaningful position 2%. | NAVY |
| P-2 | Max 25% of equity capital in any one sector; max 35% in any one macro theme, declared at entry. | TEAL |
| P-3 | Correlation clustering: name the dominant macro factor before entry; if it already exceeds 30% of the book, halve or defer the new position. | TEAL |
| P-4 | Cash is a residual, not a market call. Cash below 5% while 3+ names sit in the entry queue signals sizing is too aggressive. | TEAL |
| P-5 | Queue rank order: Part 7 N1 bridge expected return net of E-3 -> Section 5e engine growth -> Stage 2 composite -> MoS margin. Unfunded names logged DEFERRED with a re-check date, never quietly dropped. | NAVY |
| P-6 (two-sided) | Position down >30% from cost: mandatory thesis re-read (pre-mortem first, per M5), written hold/add/exit. Position up >100% also triggers a mandatory written re-read — hold/trim/add — because selling a working thesis for the wrong reason is the commonest multibagger failure mode and deserves the same documentation as a loss. | NAVY |
| P-7 (Compounder Hold Rule, governs for engine-qualified names) | Trim or exit only on (a) thesis-break per the journal entry; (b) ROIIC below cost of capital for two consecutive years (5e Gate 2); (c) moat trajectory turning ERODING (5b-T); (d) price exceeding 2x the N1 exit-multiple assumption on delivered earnings; (e) a P-2/P-3 concentration limit binding. Base-case fair value is a reference, not a trigger. The pre-v2.1 P-7 ladder stands unchanged for non-engine names. | NAVY |

### Execution rules E-1 to E-4

| Rule | Content |
|---|---|
| E-1 Entry | Rule #26 tranching for timing only. Limit orders in names below Rs5 Cr ADTV. No entry on result/corporate-action day. |
| E-2 Liquidity floors | Days-to-exit = position value / (25% of 30-day ADTV), must be <=5 trading days. Cut size until it is, or do not enter. |
| E-3 Cost drag | Estimate round-trip cost (brokerage + STT + realistic slippage for the ADTV band) and subtract from the M7 expected excess return before finalising the verdict. |
| E-4 Tax | State returns net of LTCG/STCG by expected holding period. |

Review cadence: Quarterly — P-2/P-3 exposure, DEFERRED queue, any P-6 30%-down write-up. Semi-annual — MQF Sections 7/13/14/15/16 on every holding. Annual — Rule #27 scorecard, Section 5d re-score, M1 denominators, M2 audit, M4 kill-switch test, M8 funnel hit-rate.

---

## Part 7 — The Multibagger Engine, v1.1 (rule text unchanged; consolidated gate table amended)

Part 7 is the orchestration layer. Sections 5b-T, 5e, 5f, 6A and 6B (Part 3) supply the evidence; Part 7 turns that evidence into three cross-cutting tests — the return bridge, the variant-perception claim, and the funnel screen that feeds all of it — and then a single consolidated gate. A name that fails the gate cannot hold Multibagger Candidate tier at any composite score. A name that passes is not thereby a BUY: every Stage 1 trap test, every Irani flag, the MQF verdict and every Part 5 limit still apply in full.

**N1 The Multibagger Return Bridge (mandatory, binding)** — NAVY

State the target multiple and horizon, convert to a required annualised return, decompose into four named, separately evidenced terms: (a) revenue CAGR (anchored to capacity, order book or industry volume); (b) margin delta (mechanism named per Section 6A); (c) share-count change (fully diluted — warrants, ESOP pool, announced QIP); (d) exit multiple — the re-rating term. Total return ~= (1+EPS CAGR)x(1+re-rating CAGR)-1.

N1-1 Earnings dominance. At least 60% of the required log-return must come from earnings, not re-rating; a bridge relying mostly on the multiple is a re-rating trade and cannot hold Multibagger Candidate tier. N1-2 Exit-multiple ceiling. The assumed exit multiple may not exceed the lower of the name's own and the sector's 10-year 75th-percentile multiple; no exit multiple above entry where Section 5b-T trajectory is ERODING. N1-3 Dilution honesty. Computed on fully diluted share count; a bridge closing only undiluted is ORANGE and caps at ACCUMULATE.

| Target | 3 years | 5 years | 7 years | 10 years |
|---|---|---|---|---|
| 3x | 44.2% | 24.6% | 17.0% | 11.6% |
| 5x | 71.0% | 38.0% | 25.8% | 17.5% |
| 10x | 115.4% | 58.5% | 39.0% | 25.9% |

Worked example — 5x in 5 years (38.0% required). Entry P/E 15, exit P/E 25 -> re-rating = (25/15)^(1/5)-1 = 10.8% p.a. Required EPS CAGR = 1.380/1.108-1 = 24.6% p.a. Earnings share of log-return = ln(1.246)/ln(1.380) = 68% -> clears N1-1. At 4% p.a. dilution, required net-profit CAGR rises to ~29.6% — the figure Section 6A's revenue CAGR x margin delta must actually deliver, split (v2.2) between Section 5e's revenue-driven g and Section 6A's separately-evidenced margin-delta term.

**N7 Variant Perception & Implied Expectations (closes diagnosis D-10)** — NAVY

Answer four questions in writing, before the verdict: (1) what does the market currently believe? — evidenced with a reverse DCF, solving for the growth and duration the current price embeds; (2) what specifically is wrong with that belief, with Tier 1-3 evidence; (3) why does the mispricing persist? — name the mechanism, which must be one of the three M3 edges: coverage neglect / time-horizon mismatch / structural non-participation (size, liquidity, mandate) / optical ugliness (trough earnings, capex drag, ex-parent complexity); (4) what closes the gap, and by when — a dated, observable event or metric, not "rerating". A name that cannot answer all four is capped at WATCH, per M3.

**N8 The Multibagger Funnel Screen (closes M8's unspecified systematic screen)** — NAVY

Run monthly on the full listed universe, logged with date. Filters: market cap Rs300 Cr-Rs15,000 Cr; revenue CAGR (3-yr) >=15% or a documented inflection from a loss/low base; ROCE >=15% and rising, or crossing 10%->15% for the first time; ROIIC (3-yr) >=18% (the Section 5e pre-filter); 3-yr average payout <=40%; D/E<1.0 and interest coverage>3.0x (non-BFSI names — see the Part 2 G1 amendment for the BFSI carve-out this filter also needs, not yet specified); promoter holding >=40% and not falling; institutional holding <15% (screening deliberately for coverage neglect); OCF/EBITDA 3-yr average >0.60; 30-day ADTV >=Rs1 Cr (G0). Ranked by ROIIC x (1-payout); top 20 enter the funnel with candidate source recorded per M8. This is a funnel, never a verdict — every name still runs the full suite.

*Practical note added in v2.2:* attempting to source the granular multi-year CWIP/net-working-capital detail this screen and Section 5e require, via automated tooling rather than a direct data-vendor subscription, was a real and significant bottleneck when this suite was first implemented as code. Recommend, for screening/triage purposes only, an explicit lighter-weight approximation — invested capital ~= capital employed (net worth + total debt - cash), the same denominator already used for ROCE — with a hard rule that no BUY/ACCUMULATE verdict may cite this approximation as its Section 5e evidence.

### The Multibagger Candidate Gate — consolidated (v2.2 amended rows marked)

Multibagger Candidate tier requires every gate below to clear. A single hard failure caps the name at Speculative Accumulation/WATCH (RED row) — a soft failure caps at Steady Compounder (ORANGE row) — never a route back to full tier by strength elsewhere.

| Gate | Source | Pass condition | Band on failure |
|---|---|---|---|
| Engine growth clears requirement (v2.2 amended) | Section 5e | g (ROIIC x RR) >= the N1 bridge's required REVENUE-DRIVEN CAGR (margin-delta term handled separately by 6A — see the Section 5e amendment above). A near-miss (g at 80-99% of the requirement) soft-fails to a Steady Compounder cap rather than a hard fail. | ORANGE (80-99% of requirement) — Steady Compounder cap / RED (below 80%) — hard fail |
| ROIIC floor | Section 5e | ROIIC above cost of capital, 2 consecutive years | RED — hard fail, Speculative/WATCH |
| Payout ceiling | Section 5e | 3-yr average payout <=40% | RED — hard fail, routes to Steady Compounder |
| Moat trajectory | Section 5b-T | BUILDING on >=1 moat source, Tier 1-3 evidence | ORANGE — Steady Compounder cap |
| Runway / profit pool | Section 6B | Implied share at target <=25% of addressable pool, or documented consolidating-duopoly leader (not scored for BFSI names — see the 6B note above) | RED — hard fail, reduce target |
| Industry phase | Section 6A | EMERGENT/INFLECTION, or documented share-gainer in MATURE | RED (DECLINING) — WATCH regardless of valuation |
| Promoter alignment | Section 5f | No open Gate 1/2 flag, or flag explained and logged | ORANGE — one-notch conviction cap |
| Return bridge closes | Part 7 N1 | Earnings share of log-return >=60%; fully diluted; exit multiple within N1-2 ceiling | RED — hard fail, re-run at reduced target |
| Variant perception complete | Part 7 N7 | All four questions answered, reverse DCF run, mechanism is a named M3 edge | RED — hard fail, caps at WATCH per M3 |
| MQF governance | Part 4 | HIGH-TRUST (85+) for the Engine Compounder MoS tier; ACCEPTABLE (65+) minimum for any Multibagger sizing | RED — binding governance cap, never outvoted |

M1 status: the engine-growth row's graduated band and the 5e/6A split are new to v2.2 and enter at PILOT; the other nine rows are unchanged from v2.1 and remain PILOT as originally logged. No report may describe a gate as VALIDATED or PROVISIONAL. Conviction is reduced one notch per Standing Rule 3 for any BUY carrying a PILOT gate — currently every Multibagger Candidate BUY.

---

## Part 6 — Output Format, Checklist and Integration

Rule text and structure unchanged from v2.1. One implementation note added in v2.2.

### The integration matrix — Engine x Price

The primary axis is the compounding engine (the Part 7 gate); the secondary axis is price versus the return the engine can deliver — the N1 bridge, net of E-3 costs and the M7 hurdle. "Cheap" as a standalone concept no longer gates anything on its own.

| | Price BELOW bridge (room to spare) | Price AT bridge (clears, no cushion) | Price ABOVE bridge (does not clear) |
|---|---|---|---|
| ENGINE STRONG, all gates pass | BUY — Multibagger Candidate tier, size per matrix and Cap Reconciliation | BUY at one tier lower — accumulate on weakness, staged per Rule #26 | WATCH — named, dated price condition; re-check quarterly |
| ENGINE PARTIAL, one soft gate unmet | ACCUMULATE — capped at Steady Compounder until the gate is met | WATCH — named, dated evidence condition on the failing gate | WATCH / IGNORE per Stage 1 composite |
| ENGINE WEAK, any hard gate fails | Value candidate only — runs the Stage 1 value path, never Multibagger tier, never above 3% | AVOID | IGNORE |

Conservative-governs applies only to governance RED flags and the MQF cap. PARTIALLY on either axis still defaults to WATCH; an upgrade requires a named, dated condition that would move that axis to YES.

**Implementation note (v2.2, non-binding on the methodology, binding on anyone coding it):** these are two independent axes by design. A first implementation of this suite scored the price axis using the same engine-growth-vs-N1-target ratio as the engine axis — which makes the two perfectly correlated by construction and silently deletes the "ENGINE WEAK, price BELOW bridge" cell above. Score the price axis against what the business has *already demonstrated* (e.g. a PEG~1 style comparison of current multiple to trailing growth), not against the aspirational N1 target, so a name can register as reasonably priced independent of whether its forward engine clears an ambitious bridge.

### Report structure — mandatory order (unchanged)

Block 0 Colour legend · 1 Stock snapshot · 2 Part 1 Stage 0 · 3 Part 2 Stage 1 · 4 Part 3 Stage 2 · 4A Part 7 Multibagger Engine · 5 Part 4 MQF · 6 Part 5 Portfolio · 7 Combined final recommendation · 8 Sources · 9 Condensed summary, then Stage 0 findings.

### Final call block

```
FINAL CALL: BUY / ACCUMULATE / WATCH / AVOID
Conviction: HIGH / MEDIUM / LOW (-1 notch per PILOT rule invoked)
Engine verdict: STRONG / PARTIAL / WEAK — consolidated gates passed [x of 10]
Return bridge (N1): [target]x / [n]yrs = [r]% p.a. -> EPS CAGR [e]% x re-rating [m]% | earnings share [p]%
Engine growth (5e): ROIIC [i]% x RR [rr]% = [g]% vs [rev]% required revenue-driven CAGR (margin-delta [md]% handled by 6A) — CLEARS / NEAR-MISS / FAILS
Moat trajectory (5b-T): BUILDING / HOLDING / ERODING -> MATM anchor applied [1.00/1.10/1.25/1.50]x
Compounder tier: Multibagger Candidate / Steady Compounder / Speculative Accumulation / Watch
Position: Stage-1 cap [X]% | Stage-2 base [Y]% | MQF cap [G]% | Part 5 limit [P]% | Reconciled [Z]%
Edge relied on (M3): time-horizon / coverage-neglect / behavioural
Why mispriced (N7): [persistence mechanism, one line]
Benchmark hurdle (M7): index, required return, driver — net of E-3
Attractive below: Rs [X]
Hold rule: Compounder Hold Rule (a)-(e) with the trigger number for each, or the pre-v2.1 P-7 ladder if non-engine
Thesis-breaker/exit: [one line]
PILOT rules invoked: [list]
```

### Revised workflow order (unchanged)

STEP 0 Stage 0 -> STEP 0A Part 7 N1/N7/N8 pre-screen (a bridge that cannot close, or a hard gate failure, stops here) -> STEP 1 read this document -> STEP 2 Stage 1 Pass 1 at MATM 1.00x -> STEP 3 Stage 2 per Section 1A scope, including 5b-T/5e/5f/6A/6B -> STEP 3A Stage 1 Pass 2 with trajectory-conditioned MATM -> STEP 3B MQF -> STEP 3C Part 5, including the Compounder Hold Rule where engine-qualified -> STEP 4 deliver in the Part 6 order above.

---

## v2.2 Implementation & Validation Appendix

### What v2.2 found by actually running this framework

Turning this document into executable code and testing it against six real, cross-sector, hindsight-confirmed multibaggers (Astral/Industrials, Titan/Consumer, Divi's Labs/Pharma, Persistent Systems/IT, Bajaj Finance/Financials, Dixon Technologies/Consumer Electronics), snapshotted before their known multi-year re-rating, surfaced the two rule-text gaps and one implementation trap folded into the sections above. It also produced a headline empirical finding worth stating plainly rather than smoothing over: even after both amendments, all six names still failed to reach Multibagger Candidate tier, with the Section 5e engine-growth gate the dominant blocker in five of six cases — missing the required revenue-driven CAGR by 30-70%, not narrowly.

Two readings are both plausible and neither should be dismissed. The data actually used to run this backtest was a mix of a handful of verified anchor facts and Tier-5 (general-knowledge) reconstruction of everything else, since live financial-data tooling was unavailable in the build environment — real Tier 1/2 statements would very plausibly show materially higher historical reinvestment-driven growth than this approximation captured, which is the more likely primary explanation. But it is also true, and not obviously a flaw, that a meaningful share of these six real returns came from multiple re-rating beyond what a conservative, percentile-capped exit-multiple ceiling would sanction in advance — exactly the tension this suite's own honesty note already named in the abstract before v2.2 gave it a concrete illustration across six sectors.

**Recommendation carried forward under M1:** track, at every annual review, what happened over the following 3-5 years to any name that failed only the Section 5e/N1 gates while clearing moat, industry phase, governance and variant perception. If a real, denominator-backed pattern of missed compounders concentrated on this specific gate emerges, that is the evidence needed to revisit its strictness — not a backtest built on approximate data, and not this appendix alone.

### Denominator ledger (M1)

| Finding | Status | Denominator |
|---|---|---|
| G1 BFSI/utility carve-out | PILOT | n=1 (Bajaj Finance) |
| Section 5e revenue/margin-delta split | PILOT | n=6 (this backtest) |
| Engine-growth graduated near-miss band | PILOT | n=0 (not yet exercised by a real near-miss case) |
| Engine x Price axis independence (implementation guidance) | N/A — not a rule | n=6 (confirmed the bug's effect once fixed) |
| BFSI-specific Section 5e/6B variant | Proposed, not yet specified | n=0 |
| Screening-grade Section 5e approximation for N8 | Proposed, not yet specified | n=0 |

None of the above may be described as VALIDATED or PROVISIONAL in any report generated under this suite until a real, out-of-sample denominator exists.

### Revision history

| Version | Date | Summary |
|---|---|---|
| Suite v2.0 | Sep 2026 | Red-team hardening release. Part 0 Meta-Layer (M1-M9), Part 5 Portfolio & Execution Layer, 24-finding register. Trap-avoidance architecture completed. |
| Suite v2.1 | Sep 2026 | Multibagger capability release. New Part 7 — N1 return bridge, N7 variant perception, N8 funnel screen, consolidated candidate gate — orchestrating five new Stage 2 sections. Integration matrix inverted to Engine x Price. Stage 1 adds the MQF-gated Engine Compounder MoS tier. |
| Suite v2.2 | Sep 2026 | Applied-and-verified release. Implemented v2.1 as executable code and tested it against six real cross-sector multibaggers. Amended G1 to carve out BFSI/regulated-utility balance sheets (Part 2). Amended Section 5e to split its engine-growth gate against a revenue-driven CAGR rather than the bridge's full (revenue+margin) required growth, closing a double-count against Section 6A (Part 3, Part 7's consolidated gate table). Graduated the engine-growth gate to a near-miss band rather than a pure binary. Documented, as implementation guidance rather than a rule change, that the Engine x Price matrix's two axes must be scored independently. Added a denominator ledger and a headline validation finding to this appendix. No governance rule, kill-gate, or MQF cap changed. |

---

For personal investment research and education ONLY. Not investment advice, not a SEBI research report, not a recommendation. All equity investment carries market risk including full loss of principal. The framework organises research; it does not guarantee any outcome. Verify all live data independently and consult a SEBI-registered investment adviser before acting. Branding: STOCK RESEARCH only.
