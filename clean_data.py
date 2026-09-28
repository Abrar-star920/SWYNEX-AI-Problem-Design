"""
Cleans raw_orders.csv and writes cleaned_orders.csv.

Steps:
1. Load data, standardize column dtypes.
2. Fix inconsistent text values (city names, category names) via mapping/casing.
3. Parse mixed date formats into a single ISO format.
4. Strip currency symbols from Price and cast to float.
5. Handle missing values (CustomerName, OrderDate, Quantity).
6. Remove exact duplicate rows.
7. Remove/flag invalid values (negative quantity).
8. Save cleaned CSV + print a summary of what changed.
"""
import pandas as pd
import numpy as np

df = pd.read_csv("raw_orders.csv")
n_start = len(df)
summary = {}

# --- 1. Strip whitespace from all string columns ---
str_cols = ["CustomerName", "City", "Category"]
for col in str_cols:
    df[col] = df[col].astype(str).str.strip()
    df.loc[df[col].isin(["nan", "None", ""]), col] = np.nan

# --- 2. Standardize City names ---
city_map = {
    "delhi": "Delhi", "new delhi": "Delhi",
    "mumbai": "Mumbai", "bombay": "Mumbai",
    "bangalore": "Bangalore", "bengaluru": "Bangalore",
    "chennai": "Chennai",
}
df["City"] = df["City"].str.lower().map(city_map).fillna(df["City"])
summary["city_values_standardized"] = "Delhi/Mumbai/Bangalore/Chennai variants (case, spacing, aliases like 'Bombay'->'Mumbai', 'Bengaluru'->'Bangalore') unified to one canonical spelling"

# --- 3. Standardize Category names ---
df["Category"] = df["Category"].str.strip().str.title()
summary["category_values_standardized"] = "Category casing/whitespace unified (e.g. 'electronics ', 'ELECTRONICS' -> 'Electronics')"

# --- 4. Parse mixed date formats ---
def parse_date(val):
    if pd.isna(val) or str(val).strip() == "":
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d-%b-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.to_datetime(val, errors="coerce")

df["OrderDate"] = df["OrderDate"].apply(parse_date)
n_missing_dates = df["OrderDate"].isna().sum()
summary["dates_parsed"] = f"4 mixed date formats normalized to ISO (YYYY-MM-DD); {n_missing_dates} unparseable/missing dates flagged as NaT"

# --- 5. Clean Price: strip $ signs, cast to float ---
df["Price"] = (
    df["Price"].astype(str).str.replace("$", "", regex=False).str.strip()
)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
summary["price_cleaned"] = "Removed '$' currency symbols and cast Price to numeric (float)"

# --- 6. Quantity: cast to nullable integer, flag missing ---
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype("Int64")
n_missing_qty = df["Quantity"].isna().sum()
summary["missing_quantity"] = f"{n_missing_qty} missing Quantity values found; filled with the column median"
median_qty = int(df["Quantity"].median(skipna=True))
df["Quantity"] = df["Quantity"].fillna(median_qty)

# --- 7. Remove invalid values (negative quantity = data entry error) ---
n_invalid_qty = (df["Quantity"] < 0).sum()
df = df[df["Quantity"] >= 0]
summary["invalid_quantity_removed"] = f"{n_invalid_qty} rows with negative Quantity (impossible value) removed"

# --- 8. Missing CustomerName ---
n_missing_name = df["CustomerName"].isna().sum()
df["CustomerName"] = df["CustomerName"].fillna("Unknown")
summary["missing_customer_name"] = f"{n_missing_name} missing CustomerName values filled with 'Unknown'"

# --- 9. Missing OrderDate: drop, since it's a key analysis field ---
n_before_date_drop = len(df)
df = df.dropna(subset=["OrderDate"])
n_dropped_for_date = n_before_date_drop - len(df)
summary["rows_dropped_missing_date"] = f"{n_dropped_for_date} rows dropped due to missing/unparseable OrderDate (unusable for time-based analysis)"

# --- 10. Remove exact duplicate rows ---
n_before_dupes = len(df)
df = df.drop_duplicates(subset=["OrderID", "CustomerName", "City", "Category", "Quantity", "Price", "OrderDate"])
# Also drop duplicate OrderIDs (same order recorded twice, keep first)
df = df.drop_duplicates(subset=["OrderID"], keep="first")
n_dupes_removed = n_before_dupes - len(df)
summary["duplicates_removed"] = f"{n_dupes_removed} duplicate rows removed (exact duplicates and repeated OrderIDs)"

# --- 11. Correct data types recap ---
df["OrderDate"] = df["OrderDate"].dt.strftime("%Y-%m-%d")
df["Price"] = df["Price"].round(2)

df = df.sort_values("OrderID").reset_index(drop=True)
df.to_csv("cleaned_orders.csv", index=False)

n_end = len(df)
print(f"Rows before cleaning: {n_start}")
print(f"Rows after cleaning:  {n_end}")
print()
for k, v in summary.items():
    print(f"- {k}: {v}")
