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

## Function Reference

---

### `pd.read_csv()`

**Full signature (key parameters):**
`pd.read_csv(filepath_or_buffer, sep=',', header='infer', names=None, index_col=None, usecols=None, dtype=None, na_values=None, keep_default_na=True, parse_dates=False, nrows=None)`

- **filepath_or_buffer** (str or path): Path to the CSV file.
- **sep** (str, default `','`): The delimiter character. Use `'\t'` for tab-separated files.
- **header** (int or list, default `'infer'`): Row number to use as column names. `0` means the first row. `None` means the file has no header row.
- **names** (list, optional): Provide your own column names. Used when `header=None`.
- **index_col** (int or str, optional): Column to use as the row index. If not set, pandas creates a default integer index.
- **usecols** (list, optional): Load only a subset of columns by name or position.
- **dtype** (dict, optional): Force specific dtypes on load (e.g. `{'id': str}`) instead of letting pandas infer.
- **na_values** (list or dict, optional): Additional strings to recognize as NaN beyond pandas' defaults (e.g. `['N/A', 'missing']`).
- **keep_default_na** (bool, default `True`): If False, pandas won't treat its built-in NA strings (like `''`, `'NULL'`) as NaN.
- **parse_dates** (bool or list, default `False`): If True, attempts to parse the index as dates. Pass a list of column names to parse specific columns.
- **nrows** (int, optional): Only read the first N rows — useful for previewing large files.

**Example:**
```python
df = pd.read_csv('data.csv')
# Loads the entire file with default settings. Pandas infers every column's dtype.
# A column of mostly integers with one 'N/A' string will load as object, not int.

df = pd.read_csv('data.csv', usecols=['name', 'score'], nrows=100)
# Loads only two columns and stops after 100 rows — useful for a quick preview.

df = pd.read_csv('data.csv', dtype={'id': str}, na_values=['missing', 'n/a'])
# Forces 'id' to load as string instead of int, and treats 'missing' and 'n/a' as NaN.
```

---

### `DataFrame.info()`

**Full signature:**
`DataFrame.info(verbose=None, buf=None, max_cols=None, memory_usage=True, show_counts=None)`

- **verbose** (bool, optional): If True, prints every column. If False, abbreviates for wide DataFrames.
- **buf** (writable buffer, optional): Where to write the output. Defaults to stdout (your console).
- **max_cols** (int, optional): The threshold for switching from verbose to abbreviated output.
- **memory_usage** (bool or `'deep'`, default `True`): Whether to display memory usage. `'deep'` introspects object columns for a more accurate number.
- **show_counts** (bool, optional): Whether to show non-null counts. Defaults to True when the DataFrame is small enough.

**Example:**
```python
df.info()
# Prints something like:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 25 entries, 0 to 24
# Data columns (total 4 columns):
#  #   Column   Non-Null Count  Dtype
# ---  ------   --------------  -----
#  0   name     25 non-null     object
#  1   score    23 non-null     float64   ← 2 nulls visible here
#  2   date     25 non-null     object    ← still object, not datetime
#  3   active   25 non-null     bool
# This is the fastest way to see dtypes and null counts together in one view.
```

---

### `DataFrame.describe()`

**Full signature:**
`DataFrame.describe(percentiles=None, include=None, exclude=None)`

- **percentiles** (list of floats, optional): Which percentiles to include in the output. Default is `[0.25, 0.5, 0.75]`.
- **include** (list of dtypes or `'all'`, optional): Which column dtypes to summarize. Default is numeric only. Pass `'all'` to include object and bool columns too.
- **exclude** (list of dtypes, optional): Column dtypes to exclude from the summary.

**Example:**
```python
df.describe()
# Shows count, mean, std, min, 25%, 50%, 75%, max for numeric columns only.
# If a column that should be numeric shows up missing here, it probably loaded as object.

df.describe(include='all')
# Extends the summary to string and bool columns.
# String columns will show count, unique, top (most frequent value), and freq.
# Useful for spotting unexpected variety — e.g. a 'yes'/'no'/'True' mix in one column.
```

---

### `Series.isnull()` / `Series.isna()`

**Full signature:**
`Series.isnull()` (no parameters — `isna()` is an identical alias)

Returns a boolean Series of the same shape — `True` wherever the value is `NaN` or `None`. Chaining `.sum()` onto the result gives a count of missing values per column.

**Example:**
```python
df.isnull().sum()
# Returns a count of NaN values per column, e.g.:
# name      0
# score     2
# notes    18
# dtype: int64

df[df['score'].isnull()]
# Returns only the rows where 'score' is NaN — useful for inspecting which records are missing data.
```

---

### `Series.value_counts()`

**Full signature:**
`Series.value_counts(normalize=False, sort=True, ascending=False, bins=None, dropna=True)`

- **normalize** (bool, default `False`): If True, returns relative frequencies (proportions) instead of counts.
- **sort** (bool, default `True`): If True, sorts by frequency. If False, sorts by value.
- **ascending** (bool, default `False`): If True, shows least frequent first instead of most frequent.
- **bins** (int, optional): For numeric columns, groups values into N equal-width bins instead of counting unique values.
- **dropna** (bool, default `True`): If False, includes NaN as a counted category.

**Example:**
```python
df['status'].value_counts()
# active      18
# inactive     5
# pending      2
# Shows every unique value and how many times it appears. Useful for spotting
# unexpected variants like 'Active', 'ACTIVE', 'yes' mixed in with 'active'.

df['status'].value_counts(dropna=False)
# active      18
# inactive     5
# pending      2
# NaN          1   ← now you can see there's also a null hiding in there
```

---

### `pd.to_datetime()`

**Full signature:**
`pd.to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=False, format=None, unit=None, origin='unix', cache=True)`

- **arg**: The column (or value) to convert. Usually `df['col']`.
- **errors** (default `'raise'`): What to do when a value can't be parsed. `'raise'` throws an error. `'coerce'` replaces bad values with `NaT` (Not a Time). `'ignore'` returns the input unchanged.
- **dayfirst** (bool, default `False`): If True, interprets ambiguous dates like `01/02/03` as DD/MM/YY instead of MM/DD/YY.
- **yearfirst** (bool, default `False`): If True, interprets the first component as the year.
- **format** (str, optional): The strftime pattern to parse against (e.g. `'%Y-%m-%d'`). Pass `'mixed'` to detect each row's format individually when formats vary across rows.
- **utc** (bool, default `False`): If True, returns UTC-localized timestamps.
- **unit** (str, optional): The unit of a numeric argument (e.g. `'s'` for seconds since epoch, `'ms'` for milliseconds).
- **cache** (bool, default `True`): Cache unique parsed values for speed when the column has many repeated dates.

**Example:**
```python
df['date'] = pd.to_datetime(df['date'])
# Works when all dates follow the same format. Pandas guesses the pattern.
# The column dtype changes from object → datetime64[ns].

df['date'] = pd.to_datetime(df['date'], format='mixed')
# Use this when dates in the same column follow different formats,
# e.g. some rows are '2023-01-15' and others are '01/15/2023'.
# Pandas detects the format of each row individually instead of expecting one pattern.

df['date'] = pd.to_datetime(df['date'], errors='coerce')
# Any value that can't be parsed (like 'not a date' or 'TBD') becomes NaT instead
# of crashing the whole operation. Lets you inspect the failures afterward.
```

---

### `pd.to_numeric()`

**Full signature:**
`pd.to_numeric(arg, errors='raise', downcast=None)`

- **arg**: The column (or value) to convert. Usually `df['col']`.
- **errors** (default `'raise'`): What to do when a value can't be parsed. `'raise'` throws an error. `'coerce'` replaces bad values with `NaN`. `'ignore'` returns the input unchanged.
- **downcast** (str, optional): If set, attempts to cast to a smaller numeric dtype. Options: `'integer'`, `'signed'`, `'unsigned'`, `'float'`. Rarely needed.

**Example:**
```python
df['score'] = pd.to_numeric(df['score'])
# Converts the column to a number. Throws an error immediately if any value can't convert.
# Use this when you're confident the data is clean.

df['score'] = pd.to_numeric(df['score'], errors='coerce')
# Converts what it can; turns unparseable values (like 'N/A' or 'missing') into NaN.
# Use this when the column is dirty — you want to fix the good values and inspect the bad ones.

# Common pattern: identify which rows failed before committing the conversion
bad_rows = df[pd.to_numeric(df['score'], errors='coerce').isna()]
print(bad_rows)  # inspect the problem rows
df['score'] = pd.to_numeric(df['score'], errors='coerce')  # then apply
```

---

### `Series.str.replace()`

**Full signature:**
`Series.str.replace(pat, repl, n=-1, case=None, flags=0, regex=False)`

- **pat** (str or compiled regex): The pattern to search for.
- **repl** (str or callable): The replacement string, or a function that takes a match object and returns a string.
- **n** (int, default `-1`): Maximum number of replacements per string. `-1` means replace all occurrences.
- **case** (bool, optional): Whether the match is case-sensitive. Only applies when `regex=False`. If None, defaults to case-sensitive.
- **flags** (int, default `0`): Regex flags from the `re` module. Only applies when `regex=True`.
- **regex** (bool, default `False`): If True, `pat` is treated as a regular expression. If False, it is treated as a plain literal string.

**Example:**
```python
df['price'] = df['price'].str.replace('$', '', regex=False)
# Removes the '$' character from every value in the column.
# regex=False is important here — '$' has special meaning in regex (end of string),
# so treating it as a literal prevents unexpected behavior.
# After this, the column is still object dtype — you still need .astype(float) to convert.

df['label'] = df['label'].str.replace(' ', '_', regex=False)
# Replaces spaces with underscores across all rows — common for cleaning column-like values.
```

---

### `Series.astype()`

**Full signature:**
`Series.astype(dtype, copy=True, errors='raise')`

- **dtype** (dtype or str): The target type to cast to. Common values: `'float64'`, `'int64'`, `'Int64'` (nullable int), `'str'`, `'bool'`, `'datetime64[ns]'`.
- **copy** (bool, default `True`): If False, modifies the data in place when possible. Leaving this as True is safer.
- **errors** (default `'raise'`): If `'raise'`, throws an error when a value can't be cast. If `'ignore'`, returns the original input unchanged on failure.

**Example:**
```python
df['price'] = df['price'].astype(float)
# Casts the column to float. Will throw an error if any value can't convert (e.g. 'N/A').
# Always clean the column first (strip characters, coerce nulls) before calling astype.

df['id'] = df['id'].astype(str)
# Casts to string. Note: True becomes 'True', 1 becomes '1', False becomes 'False'.
# If you plan to use .map() after this, your dictionary keys must be strings too.

df['count'] = df['count'].astype('Int64')
# Capital-I Int64: the nullable integer dtype. Unlike int64, it can hold NaN values.
# Use this when a column should be integer but has missing entries.
```

---

### `Series.map()`

**Full signature:**
`Series.map(arg, na_action=None)`

- **arg** (dict, Series, or callable): The mapping to apply. When passed a dictionary, each value in the Series is looked up as a key — matched values are replaced, unmatched values become `NaN`. When passed a function, it is applied element-wise.
- **na_action** (default `None`): If `'ignore'`, leaves `NaN` values unchanged rather than passing them through the mapping.

**Example:**
```python
df['status'] = df['status'].map({'yes': True, 'no': False, '1': True, '0': False})
# Replaces each value using the dictionary. Keys must exactly match the values in the column.
# Any value not in the dictionary becomes NaN — so if 'maybe' appears in the column,
# that row will become NaN after the map.

# If you did .astype(str) before this, your keys must be strings:
df['flag'] = df['flag'].astype(str).map({'True': True, 'False': False, '1': True, '0': False})
# 'True' (string), not True (bool) — because astype(str) converted the original booleans.
```

---

### `'Int64'` — Nullable Integer dtype

Not a function, but a dtype string you pass to `.astype()`. The standard `'int64'` dtype cannot hold `NaN` — if a null exists in the column, the cast will fail. `'Int64'` (capital I) is pandas' nullable integer type that preserves `NaN` while still treating the column as integer.

**Example:**
```python
df['count'] = df['count'].astype('Int64')
# The column can now hold both integers and NaN at the same time.
# If you used lowercase 'int64' and NaN was present, pandas would throw a ValueError.

# You can verify it worked:
print(df['count'].dtype)   # Int64
print(df['count'].isna().sum())  # confirms NaN values are preserved, not dropped
```

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
