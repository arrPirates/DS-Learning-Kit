# DS Python Interview Prep — Master Syllabus
**Maintained by Claude | Updated each session**

---

## HOW TO USE THIS DOCUMENT
This file is the persistent brain of the prep program. At the start of every session, import this file plus the zip of completed work. Claude will:
1. Read this file to understand current position, rules, and history
2. Scan the zip for any new submissions since last session
3. Update `## Session Log` and problem statuses before doing anything else
4. Proceed with next problem, repeat, or new tier as appropriate

**File naming convention for submissions:** `T{tier}_{problem_number}.py`
- Example: `T1_P3.py` = Tier 1, Problem 3
- SQL submissions (where applicable): `T{tier}_{problem_number}_sql.py`
- If a problem is repeated due to low score: `T1_P3b.py`, `T1_P3c.py`, etc.

---

## GRADING RULES
Each submission is scored **1–5** across three dimensions:

| Dimension | What it measures |
|---|---|
| **Correctness** | Does the output match expected results? Edge cases handled? |
| **Efficiency** | Is the approach appropriately vectorized? Avoids unnecessary loops? |
| **Code Style** | Readable variable names, comments where helpful, no redundant code |

**Overall Score** = average of three dimensions, rounded to one decimal.

**Repeat rule:** If overall score < 3.5 OR any single dimension scores a 2 or below → problem is flagged for repeat with a fresh dataset/scenario before advancing. Repeated problems are labeled `b`, `c`, etc.

**Advancement rule:** Must achieve ≥ 3.5 overall on final attempt of every problem in a tier before unlocking the next tier.

---

## CONTEXT
- **Learner background:** ~6 years DS experience, strong SQL, Looker, business analytics. Python used but not at interview depth.
- **Domain focus:** Problems are framed in growth marketing / fintech / user behavior contexts where possible (mirrors Credit Karma experience and target company domains).
- **Target companies:** DoorDash, Robinhood, Google, Reddit, OpenAI, Anthropic
- **Python environment:** VSCode on PC, standard data science libraries (pandas, numpy, sqlite3 built-in)
- **SQL approach:** `sqlite3` only — no external DB setup required. Included as a light parallel track from Tier 2 onward.
- **Session cadence:** 3–4x per week, ~45–60 min per session

---

## TIER OVERVIEW

| Tier | Name | Focus | Est. Duration | Problems |
|---|---|---|---|---|
| 1 | Foundations | Core pandas operations | 3–4 weeks | 10 |
| 2 | Applied Analytics | DS-specific patterns + intro SQL | 3–4 weeks | 10 |
| 3 | Interview Simulation | Timed, edge-case-heavy problems | 3–4 weeks | 10 |
| 4 | Take-Home Projects | Mini-project format, open-ended | 4–6 weeks | 5 |

---

## TIER 1 — FOUNDATIONS
**Goal:** Build fluency in core pandas operations under realistic data conditions (nulls, duplicates, type issues, messy strings). No SQL in this tier.

**Unlock condition:** ≥ 3.5 overall on all 10 problems (repeats counted on final attempt only).

### Problem List

| ID | Topic | Status | Score | Notes |
|---|---|---|---|---|
| T1_P1 | Data loading, inspection, dtypes | ✅ Complete | 4.3 | 3 attempts. Bool map string key issue resolved by attempt 3. |
| T1_P2 | Filtering, boolean indexing, `.query()` | ⬜ Not Started | — | — |
| T1_P3 | GroupBy + aggregation (single level) | ⬜ Not Started | — | — |
| T1_P4 | GroupBy + aggregation (multi-level) | ⬜ Not Started | — | — |
| T1_P5 | Merges and joins (inner, left, anti-join) | ⬜ Not Started | — | — |
| T1_P6 | Reshaping — pivot tables and melt | ⬜ Not Started | — | — |
| T1_P7 | Null handling — detect, fill, drop strategies | ⬜ Not Started | — | — |
| T1_P8 | String operations and regex on text columns | ⬜ Not Started | — | — |
| T1_P9 | Window functions — rolling, shift, pct_change | ⬜ Not Started | — | — |
| T1_P10 | Apply and lambda — row/column-wise transforms | ⬜ Not Started | — | — |

### Tier 1 Notes
- **T1_P1:** Strong instinct to use `value_counts()` before fixing — good diagnostic habit to keep. Watch: `.map()` dict keys must match post-transform string representations. When `.astype(str)` is applied first, all keys must be strings (`'True'` not `True`).

---

## TIER 2 — APPLIED ANALYTICS
**Goal:** Translate pandas skills into DS-relevant analytical tasks. Introduction of `sqlite3` SQL problems as a parallel track (~30% of problems). Problems mirror what a DS hire would produce in their first 30 days.

**Unlock condition:** Tier 1 complete. ≥ 3.5 overall on all 10 problems.

### Problem List

| ID | Topic | SQL Parallel? | Status | Score | Notes |
|---|---|---|---|---|---|
| T2_P1 | User funnel analysis — drop-off rates by step | No | ⬜ Not Started | — | — |
| T2_P2 | Cohort retention table (weekly) | No | ⬜ Not Started | — | — |
| T2_P3 | Revenue aggregation + period-over-period change | Yes | ⬜ Not Started | — | — |
| T2_P4 | Deduplication and session stitching | No | ⬜ Not Started | — | — |
| T2_P5 | A/B test summary — means, std, sample sizes | No | ⬜ Not Started | — | — |
| T2_P6 | Feature engineering for a model input table | No | ⬜ Not Started | — | — |
| T2_P7 | Time series resampling + forward fill | Yes | ⬜ Not Started | — | — |
| T2_P8 | Ranking and percentile bucketing | Yes | ⬜ Not Started | — | — |
| T2_P9 | Multi-source data pipeline (3-table merge) | No | ⬜ Not Started | — | — |
| T2_P10 | Anomaly flagging — outlier detection heuristics | No | ⬜ Not Started | — | — |

### Tier 2 Notes
*(Claude appends here)*

---

## TIER 3 — INTERVIEW SIMULATION
**Goal:** Timed, interview-style problems with edge cases intentionally embedded. Problems are delivered without hints. Grading mirrors what a DS interviewer would expect. SQL problems included where relevant.

**Format change:** Problems in this tier come with a **suggested time limit** (30–45 min). Submissions should note actual time taken.

**Unlock condition:** Tier 2 complete. ≥ 3.5 overall on all 10 problems.

### Problem List

| ID | Topic | Time Limit | SQL? | Status | Score | Notes |
|---|---|---|---|---|---|---|
| T3_P1 | Funnel + cohort combined, with data quality issues | 40 min | No | ⬜ Not Started | — | — |
| T3_P2 | Rolling 7-day metrics with business logic edge cases | 35 min | No | ⬜ Not Started | — | — |
| T3_P3 | Ranking + tie-breaking logic | 30 min | Yes | ⬜ Not Started | — | — |
| T3_P4 | Session-level aggregation from raw event logs | 40 min | No | ⬜ Not Started | — | — |
| T3_P5 | Attribution modeling (first-touch / last-touch) | 45 min | No | ⬜ Not Started | — | — |
| T3_P6 | Statistical significance from raw test data | 35 min | No | ⬜ Not Started | — | — |
| T3_P7 | Multi-step data cleaning pipeline, full output | 40 min | No | ⬜ Not Started | — | — |
| T3_P8 | Churn flagging with configurable lookback window | 35 min | Yes | ⬜ Not Started | — | — |
| T3_P9 | LTV estimation from transaction history | 45 min | No | ⬜ Not Started | — | — |
| T3_P10 | End-to-end: raw CSV → cleaned → analyzed → output | 45 min | No | ⬜ Not Started | — | — |

### Tier 3 Notes
*(Claude appends here)*

---

## TIER 4 — TAKE-HOME PROJECTS
**Goal:** Open-ended mini-projects that mirror real DS take-home interviews. Each project spans 1–2 sessions and produces a deliverable (script + written summary of findings). Grading adds a fourth dimension: **Communication** (clarity of findings, not just code).

**Unlock condition:** Tier 3 complete. No strict score gate — these are evaluated holistically.

### Project List

| ID | Project | Status | Score | Notes |
|---|---|---|---|---|
| T4_P1 | Growth diagnostics — why did DAU drop last month? | ⬜ Not Started | — | — |
| T4_P2 | A/B test analysis — full write-up from raw data | ⬜ Not Started | — | — |
| T4_P3 | User segmentation — define and profile 4 segments | ⬜ Not Started | — | — |
| T4_P4 | Funnel optimization proposal — data-backed recs | ⬜ Not Started | — | — |
| T4_P5 | Open project — learner proposes, Claude scopes | ⬜ Not Started | — | — |

### Tier 4 Notes
*(Claude appends here)*

---

## SESSION LOG
*(Claude updates this section at the start of every session after reading zip contents)*

| Session # | Date | Problems Worked | Outcomes | Next Up |
|---|---|---|---|---|
| 1 | 2026-04-22 | T1_P1 | 4.3/5 ✅ — Passed on attempt 3. All dtype fixes correct, fully vectorized. Bool map string key issue was the sticking point. | T1_P2 |

---

## AUGMENTATION LOG
*(Claude logs any structural changes to the syllabus here — added problems, reordered topics, tier rule changes, etc.)*

| Date | Change | Reason |
|---|---|---|
| 2026-04-16 | Initial syllabus created | Program kickoff |

---

## PROBLEM BANK — COMPLETED PROBLEMS

### T1_P1 — Data Loading, Inspection, dtypes
- **Score:** 4.3 / 5 (Correctness 4, Efficiency 5, Style 4) | **Attempts:** 3
- **Core skills tested:** `pd.read_csv`, `.info()`, `.describe()`, `pd.to_datetime(format='mixed')`, `pd.to_numeric(errors='coerce')`, `.str.replace()`, `.astype()`, `.map()`, nullable `Int64`
- **Key lesson:** `.astype(str)` before `.map()` means dict keys must be strings. `True` → `'True'`, `1` → `'1'`
- **Data file:** 25-row user account table with mixed date formats, `$`-prefixed fees, `USR`-prefixed IDs, mixed bool representations
