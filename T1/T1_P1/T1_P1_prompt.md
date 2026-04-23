# T1_P1 — Data Loading, Inspection, and dtype Fixing

**Tier:** 1 | **Topic:** Data loading, inspection, dtypes | **Status:** Not Started

---

## Scenario

You've just joined the data team at a fintech startup (think Credit Karma). A colleague dumped a user account table from a legacy CRM into `T1_P1_data.csv` and handed it to you for "a quick cleanup before we load it into the pipeline."

The file has 25 rows and 9 columns. Your job is to load it, understand what's in it, identify all the dtype problems, and fix them — producing a clean DataFrame ready for downstream analysis.

---

## Dataset: `T1_P1_data.csv`

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `signup_date` | Date the user created their account |
| `plan_type` | Subscription tier: free / premium / enterprise |
| `monthly_fee` | Dollar amount charged per month |
| `credit_score` | User's credit score at signup (300–850 range) |
| `is_active` | Whether the account is currently active |
| `transactions_last_30d` | Number of transactions in the past 30 days |
| `referral_source` | How the user found the product |
| `notes` | Freeform notes from the CRM (mostly empty) |

---

## Tasks

Complete all tasks in a single file: `T1_P1.py`

### Part 1 — Load and Inspect
1. Load `T1_P1_data.csv` into a DataFrame.
2. Print: shape, column names, and dtypes.
3. Call `.info()` to display null counts alongside dtypes.
4. Call `.describe(include='all')` — note which columns look off.

### Part 2 — Identify Problems
5. Print a null count per column (`df.isnull().sum()`).
6. In a comment block, list every column that has a dtype problem and describe what's wrong. Example:
   ```
   # monthly_fee: stored as string due to '$' prefix — should be float
   ```

### Part 3 — Fix dtypes
Fix all dtype issues you identified. Requirements:
- `monthly_fee` → `float` (strip the `$` first)
- `signup_date` → `datetime` (handle mixed formats)
- `credit_score` → `float` (coerce invalid strings to NaN)
- `is_active` → `bool` (standardize all variants: True/False/1/0/yes/no)
- `transactions_last_30d` → nullable integer (pandas `Int64`) — preserve NaN-awareness
- `user_id` — do NOT silently convert. Flag rows where `user_id` is not numeric by printing them, then convert the clean ones to `int` where possible.

### Part 4 — Final Summary
7. Print the final dtypes of all columns.
8. Print null counts again (post-fix) — confirm nothing changed unexpectedly.
9. Print any rows where `user_id` could not be converted to a numeric type.

---

## Expected Output (rough shape)

Your script should produce console output covering:
- Pre-fix shape and dtypes
- `.info()` output
- Per-column null counts (before)
- Flagged `user_id` non-numeric rows
- Post-fix dtypes
- Per-column null counts (after)

---

## Grading Reminders
- **Correctness:** All 5 dtype fixes complete; non-numeric user_ids identified, not silently dropped or ignored.
- **Efficiency:** Use vectorized methods — no row-by-row loops for dtype conversion.
- **Code Style:** Clear variable names; brief comments on non-obvious steps; no dead code.

**Submit as:** `T1_P1.py`

---

## Completion Record
**Date:** 2026-04-22 | **Score:** 4.3 / 5 | **Attempts:** 3

**What went well:** Independently identified all dtype issues using `value_counts()` before writing fixes. Correct use of `pd.to_numeric(errors='coerce')` for flagging, `format='mixed'` for datetime, and nullable `Int64`.

**Watch for next time:** When using `.map()` on a column, the dict keys must match the values *after* any transformation. After `.astype(str)`, Python booleans become the strings `'True'`/`'False'` — dict keys must be strings too.
