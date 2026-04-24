# T1_P2 — Filtering, Boolean Indexing, and `.query()`

**Tier:** 1 | **Topic:** Filtering, boolean indexing, `.query()` | **Status:** Not Started

---

## Scenario

The fraud ops team at your fintech company flagged a batch of transactions for review and handed you the raw export: `T1_P2_data.csv`, 30 rows of user transactions spanning January–April 2024. Before they can triage, they need you to slice the data several different ways — by status, amount thresholds, region, category, and merchant name. Your job is to produce the filtered views they asked for, using both boolean indexing and `.query()`.

---

## Dataset: `T1_P2_data.csv`

| Column | Description |
|---|---|
| `txn_id` | Unique transaction identifier (string) |
| `user_id` | User who made the transaction (int) |
| `txn_date` | Date the transaction occurred (YYYY-MM-DD, all clean) |
| `amount` | Dollar amount of the transaction (float) |
| `category` | Transaction category: `food`, `shopping`, `transport`, `transfer` |
| `merchant` | Merchant name — **some rows are null** (merchant data missing from source) |
| `channel` | How the transaction was made: `app`, `web`, `card` |
| `region` | Geographic region: `West`, `East`, `South`, `North` |
| `is_flagged` | Whether fraud ops flagged this transaction (bool) |
| `status` | Transaction status: `completed`, `pending`, `failed` |

> **Dtype note:** `txn_date` will load as object — convert it to datetime in Part 1. All other columns load with correct types.

---

## Function Reference

---

### Boolean Indexing

Not a function — a pandas pattern. Passing a condition inside `df[...]` returns only the rows where that condition is True.

```python
df[df['col'] == 'some_value']
df[df['col'] > 100]
```

Combine conditions with `&` (AND) or `|` (OR). **Each condition must be wrapped in its own parentheses** — Python's `and` / `or` keywords do not work here.

```python
df[(df['col_a'] == 'x') & (df['col_b'] > 10)]
df[(df['col_a'] == 'x') | (df['col_a'] == 'y')]
```

Negate a condition with `~`:

```python
df[~(df['col'] == 'x')]
```

**Example:**
```python
# Start with a DataFrame of orders:
# status     amount   region
# complete   250      West
# pending     80      East
# complete   410      West
# failed      30      East

high_value_complete = df[(df['status'] == 'complete') & (df['amount'] > 100)]
# Returns only the rows where BOTH conditions are true — here, the two 'complete' rows over 100.

west_or_east = df[(df['region'] == 'West') | (df['region'] == 'East')]
# Returns all rows — both regions are present, so everything qualifies.

not_failed = df[~(df['status'] == 'failed')]
# Returns every row except the one with status 'failed'.
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
# Converts a string column like '2024-01-15' to datetime64[ns] dtype.
# Once converted, you can compare dates directly with >= or <= operators.

print(df['date'].dtype)   # before:  object
df['date'] = pd.to_datetime(df['date'])
print(df['date'].dtype)   # after:   datetime64[ns]

# After conversion, date comparisons work naturally:
recent = df[df['date'] >= '2024-03-01']
# Pandas parses the string on the right-hand side automatically.
```

---

### `DataFrame.query()`

**Full signature:**
`DataFrame.query(expr, inplace=False, **kwargs)`

- **expr** (str): The filter expression as a string. Column names are referenced directly. Use `and`, `or`, `not` for logic (not `&`, `|`, `~`). String values need inner quotes: `"col == 'value'"`.
- **inplace** (bool, default `False`): If True, modifies the DataFrame in place rather than returning a new one.
- **kwargs**: Additional keyword arguments passed to `eval()`. Rarely needed.

**Example:**
```python
result = df.query("amount > 100 and status == 'complete'")
# Equivalent to: df[(df['amount'] > 100) & (df['status'] == 'complete')]
# The string expression is often easier to read for complex conditions.

result = df.query("region == 'West' or region == 'East'")
# Equivalent to: df[(df['region'] == 'West') | (df['region'] == 'East')]

result = df.query("is_active == True and amount < 50")
# For boolean columns, use == True or == False explicitly inside the string.
# Using bare 'is_active' or 'not is_active' can behave unexpectedly.
```

---

### `Series.isin()`

**Full signature:**
`Series.isin(values)`

- **values** (set or list-like): The collection of values to test membership against. Returns a boolean Series — True where the element is found in `values`, False otherwise.

**Example:**
```python
target_ids = [101, 205, 310]
result = df[df['user_id'].isin(target_ids)]
# Returns all rows where user_id is 101, 205, or 310.
# Much cleaner than: df[(df['user_id'] == 101) | (df['user_id'] == 205) | (df['user_id'] == 310)]

# Works with strings too:
result = df[df['category'].isin(['food', 'transport'])]
# Returns rows where category is either 'food' or 'transport'.
```

---

### `Series.str.contains()`

**Full signature:**
`Series.str.contains(pat, case=True, flags=0, na=None, regex=True)`

- **pat** (str): The character sequence or regular expression pattern to search for.
- **case** (bool, default `True`): If True, the match is case-sensitive. If False, it is case-insensitive.
- **flags** (int, default `0`): Regex flags from the `re` module (e.g. `re.IGNORECASE`). Only applies when `regex=True`.
- **na** (scalar, default `None`): How to handle missing values. By default returns `NaN` for null entries, which causes errors when used as a boolean mask. Setting `na=False` treats nulls as non-matches and returns `False` instead.
- **regex** (bool, default `True`): If True, `pat` is treated as a regular expression. If False, it is treated as a plain literal string (faster, and avoids unintended regex behavior with special characters).

**Example:**
```python
result = df[df['name'].str.contains('corp')]
# Returns rows where 'name' contains 'corp' — case-sensitive, so 'Corp' would NOT match.

result = df[df['name'].str.contains('corp', case=False)]
# Now matches 'corp', 'Corp', 'CORP', etc.

result = df[df['name'].str.contains('corp', case=False, na=False)]
# Also handles null values safely — rows where 'name' is NaN return False instead of NaN.
# Without na=False, a null in the column causes a ValueError when used as a filter mask.

# The difference na=None vs na=False produces:
# na=None  → [True, NaN, False]  ← NaN rows cause errors in df[...]
# na=False → [True, False, False] ← safe to use directly as a filter
```

---

### `DataFrame.sort_values()`

**Full signature:**
`DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)`

- **by** (str or list of str): Column name(s) to sort by. Pass a list to sort by multiple columns in order of priority.
- **axis** (default `0`): `0` sorts rows (the usual case). `1` sorts columns.
- **ascending** (bool or list of bool, default `True`): If True, sorts smallest to largest (A→Z). If False, reverses. Pass a list to set direction per column when sorting by multiple columns.
- **inplace** (bool, default `False`): If True, sorts the DataFrame in place rather than returning a new one.
- **kind** (default `'quicksort'`): The sort algorithm. `'mergesort'` and `'stable'` preserve original order of equal values. Rarely needs changing.
- **na_position** (default `'last'`): Where to place NaN values — `'last'` or `'first'`.
- **ignore_index** (bool, default `False`): If True, resets the index on the result so it runs 0, 1, 2… instead of keeping original row numbers.
- **key** (callable, optional): A function applied to column values before sorting (similar to Python's built-in `sorted(key=...)`).

**Example:**
```python
df.sort_values('amount')
# Returns a new DataFrame sorted by amount, smallest to largest.
# The original df is unchanged — assign to a variable to keep the result.

df.sort_values('amount', ascending=False)
# Largest to smallest.

df.sort_values(['region', 'amount'], ascending=[True, False])
# Sorts by region A→Z first, then within each region sorts amount largest to smallest.
# Pass a list to 'by' and a matching list to 'ascending'.

df.sort_values('score', na_position='first')
# Rows with NaN in 'score' float to the top instead of the bottom.
```

---

## Tasks

Complete all tasks in a single file: `T1_P2.py`

### Part 1 — Load and Setup

1. Load `T1_P2_data.csv` into a DataFrame.
2. Print shape, dtypes, and null counts per column.
3. Convert `txn_date` to datetime (all dates are clean — one line is enough).

### Part 2 — Boolean Indexing

4. Filter for all `completed` transactions with `amount > 100`. Print the count and the first 5 rows.
5. Filter for transactions in the `West` or `East` region where `is_flagged` is `True`. Print the full result.
6. Filter for `food` or `transport` transactions with `amount < 20`. Print the count and the full result.
7. Filter for rows where `merchant` is null. Print those rows.

### Part 3 — `.query()` Equivalents

8. Repeat task 4 using `.query()`. Verify the row count matches your boolean index result (print both counts).
9. Use `.query()` to find non-flagged, non-pending transactions in the `South` region with `amount > 50`. Print the result.

> **Note on `.query()` and booleans:** Use `is_flagged == True` / `is_flagged == False` inside `.query()` strings — do not use bare `is_flagged` or Python `not`.

### Part 4 — Advanced Filtering

10. Use `.isin()` to get all transactions from `user_id` values `[1001, 1003, 1005]`. Print the count and the result.
11. Use `.str.contains()` (case-insensitive, null-safe) to find all rows where `merchant` contains the word `"pay"`. Print the result.
    > Watch out: `.str.contains()` returns `NaN` for null merchant values by default — use `na=False` to treat nulls as non-matches.
12. Filter for Q1 2024 transactions only (January 1 through March 31, 2024). Print the count and the result.
13. Chain all four conditions into one filter:
    - `status == 'completed'`
    - `is_flagged == False`
    - Q1 2024 (`txn_date` between Jan 1 and Mar 31, 2024)
    - `amount` between $50 and $500 (inclusive)

    Sort the result by `amount` descending and print it.

---

## Expected Output (rough shape)

Your script should produce labeled console output covering:
- Shape, dtypes, null counts
- Results for tasks 4–13, each labeled with a short header comment so output is readable
- Count verification for task 8 (two prints confirming the counts match)

---

## Grading Reminders

- **Correctness:** All filter conditions produce the right rows — double-check compound conditions, null handling in task 11, and date bounds in tasks 12–13.
- **Efficiency:** Use vectorized pandas operations throughout — no Python loops over rows. `.isin()` over multiple `==` conditions chained with `|`. Date filtering via datetime comparison, not string slicing.
- **Code Style:** Label each output block with a short `print()` header. Use intermediate variables for complex multi-condition filters rather than one unreadable chained expression.

**Submit as:** `T1_P2.py`
