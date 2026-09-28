# Data Cleaning & Preparation — Task 1

## Dataset

A retail orders dataset (`raw_orders.csv`, 192 rows) containing customer orders
with columns: `OrderID`, `CustomerName`, `City`, `Category`, `Quantity`,
`Price`, `OrderDate`. The raw export is representative of a typical messy
business dataset, containing:

- Missing values (customer names, quantities, order dates)
- Duplicate records (exact duplicate rows and repeated order IDs)
- Incorrect data types (price stored as text, sometimes with a `$` prefix)
- Inconsistent categorical values (e.g. `Delhi`, `delhi`, `New Delhi`,
  `DELHI ` all referring to the same city; `Bombay` as an alias for `Mumbai`)
- Inconsistent date formats (`YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`,
  `DD-Mon-YYYY` all present in the same column)
- Invalid values (negative order quantities)

## Tools used

Python (pandas, numpy)

## Cleaning steps

| # | Issue | Fix |
|---|-------|-----|
| 1 | Leading/trailing whitespace in text fields | Stripped whitespace from `CustomerName`, `City`, `Category` |
| 2 | Inconsistent city spelling/casing | Mapped all variants (case, spacing, aliases like `Bombay`→`Mumbai`, `Bengaluru`→`Bangalore`) to one canonical name |
| 3 | Inconsistent category casing | Normalized to title case (`electronics`/`ELECTRONICS` → `Electronics`) |
| 4 | Mixed date formats | Parsed all 4 formats found in the column and standardized to ISO `YYYY-MM-DD` |
| 5 | Price stored as text with `$` symbol | Stripped currency symbol, cast to numeric (float) |
| 6 | Missing `Quantity` values (40 rows) | Filled with the column median |
| 7 | Negative `Quantity` values (4 rows) | Removed — physically invalid |
| 8 | Missing `CustomerName` (2 rows) | Filled with `"Unknown"` |
| 9 | Missing/unparseable `OrderDate` (1 row) | Row dropped — unusable for time-based analysis |
| 10 | Duplicate rows / repeated `OrderID`s (8 rows) | Removed, keeping the first occurrence |

## Result

- **Rows before cleaning:** 192
- **Rows after cleaning:** 179
- Output file: `cleaned_orders.csv`

## Files in this repository

- `raw_orders.csv` — original raw dataset
- `clean_data.py` — Python script that performs the cleaning (pandas)
- `cleaned_orders.csv` — cleaned dataset, ready for analysis
- `README.md` — this file

## How to reproduce

```bash
pip install pandas numpy
python clean_data.py
```
