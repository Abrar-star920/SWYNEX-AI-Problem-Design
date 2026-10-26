# SWYNEX Final Data Analytics Project: Retail Orders Case Study

An end-to-end analytics project: from a messy raw orders file to a cleaned dataset, SQL and Python analysis, an interactive Power BI dashboard, and business recommendations.

**Tools:** SQL (SQLite), Python (pandas, matplotlib), Power BI (DAX, Power Query)

---

## 1. Problem statement
A retail business sells four product categories across four Indian cities. Its order data comes from several sources and is inconsistent. Leadership wants to know:

1. How is revenue performing, and how does it change over time?
2. Which categories and cities drive the most revenue?
3. How concentrated is revenue among customers?
4. What should the business do next?

## 2. Dataset
| Item | Detail |
|---|---|
| File | `data/raw_orders.csv` (raw), `data/cleaned_orders.csv` (cleaned) |
| Size | 192 raw rows, 179 cleaned rows |
| Columns | `OrderID`, `CustomerName`, `City`, `Category`, `Quantity`, `Price`, `OrderDate` |
| Period | 1 Jan 2025 to 26 Oct 2025 (October is a partial month) |
| Source | Synthetic dataset generated for this exercise, built with realistic data-quality problems |

**Revenue = Quantity × Price.** Price is treated as the unit price.

## 3. Data cleaning
Profiled with `sql/01_profile.sql`, cleaned with `sql/02_clean.sql`, and run end to end by `python/clean_data.py`.

| Issue found | Count | Fix |
|---|---|---|
| Missing `Quantity` | 40 | Filled with the median |
| Missing `CustomerName` | 2 | Set to `Unknown` |
| Missing `OrderDate` | 1 | Row removed |
| Exact duplicate rows | 8 | Kept first occurrence per `OrderID` |
| `Price` stored as text with a `$` prefix | 78 | Prefix stripped, cast to numeric |
| 16 spellings of 4 cities (`delhi`, `Bombay`, `Bengaluru`, `New Delhi`) | all | Standardized |
| 10 spellings of 4 categories (case and whitespace) | all | Standardized |
| 4 date formats in one column | all | Converted to ISO `YYYY-MM-DD` |
| Negative `Quantity` | 4 | Rows removed |

**Result:** 192 rows reduced to 179, with no nulls, no duplicate `OrderID`s, numeric prices and ISO dates. `clean_data.py` ends with assertions that check these.

## 4. Analysis
Run `python/analysis.py` to reproduce every number and chart below.

### KPIs
| Metric | Value |
|---|---|
| Total revenue | ₹13.93 lakh (1,392,909) |
| Orders | 179 |
| Average order value | ₹7,782 |
| Units sold | 532 |
| Named customers | 85 |

### Revenue by category
| Category | Revenue | Orders | Avg order | Share |
|---|---|---|---|---|
| Electronics | 437,037 | 53 | 8,246 | 31.4% |
| Groceries | 387,858 | 50 | 7,757 | 27.8% |
| Furniture | 292,714 | 38 | 7,703 | 21.0% |
| Clothing | 275,301 | 38 | 7,245 | 19.8% |

### Revenue by city
| City | Revenue | Orders | Avg order | Share |
|---|---|---|---|---|
| Chennai | 423,238 | 49 | 8,638 | 30.4% |
| Bangalore | 382,968 | 51 | 7,509 | 27.5% |
| Mumbai | 316,902 | 41 | 7,729 | 22.8% |
| Delhi | 269,801 | 38 | 7,100 | 19.4% |

### Monthly trend
Revenue peaked in **April (₹2.28 lakh)** and was lowest in **March (₹0.85 lakh)**. The full monthly table is in `data/summary_by_month.csv`.

![Monthly revenue](images/monthly_revenue.png)
![Revenue by category](images/revenue_by_category.png)
![Revenue by city](images/revenue_by_city.png)

## 5. Dashboard
Built in Power BI: `dashboard/SWYNEX-Retail-Dashboard.pbix`, with a PDF export in `dashboard/dashboard.pdf`.

It includes 6 KPI cards, a monthly trend, category, city and top-customer charts, a top-10 orders table, and slicers for city, category and date.

![Dashboard](images/dashboard.png)

A standalone web version (HTML + Chart.js) is in `dashboard/web_dashboard.html`.

## 6. Key business insights
1. **Electronics and Groceries make up 59% of revenue.** Electronics also has the highest average order value (₹8,246) and the most orders (53).
2. **Chennai is the strongest city** at 30% of revenue with the highest average order value (₹8,638). Delhi is the weakest at 19%, with the lowest average order value (₹7,100).
3. **Revenue is volatile by month.** April earned 2.7× March. April's average order value (₹11,381) was well above the ₹7,782 average, which points to a few large orders rather than more orders.
4. **Revenue is spread across many customers.** The top 10 named customers account for 28.6% of revenue, so there is no single-customer dependency.

## 7. Recommendations
- **Invest in Electronics:** bundle accessories, run promotions, and keep stock available, since it leads on both volume and order value.
- **Grow Delhi:** it has the lowest revenue and average order value. Test city-specific offers and track the effect on order value.
- **Investigate April:** find out which orders drove the spike (a campaign, bulk purchases, or a seasonal event) and repeat what is repeatable.
- **Protect the top customers:** a loyalty or early-access programme for the top 10, since they generate over a quarter of revenue.
- **Improve data capture:** enforce dropdowns for city and category, a single date format and numeric price fields. This would have prevented most of the cleaning issues in section 3.

## 8. Limitations
- The data is synthetic, so the findings illustrate the method and are not real business results.
- 40 missing quantities (about a fifth of the raw rows) were filled with the median, so revenue is partly estimated.
- Ten months of data is too short to confirm seasonality.
- The raw `Price` field carried a `$` symbol while the cities are in India. Revenue is shown in ₹ throughout, so confirm the currency before relying on absolute values.

## 9. Repository structure
```
├── README.md
├── data/
│   ├── raw_orders.csv
│   ├── cleaned_orders.csv
│   └── summary_by_*.csv
├── sql/
│   ├── 01_profile.sql
│   └── 02_clean.sql
├── python/
│   ├── clean_data.py
│   └── analysis.py
├── dashboard/
│   ├── SWYNEX-Retail-Dashboard.pbix
│   ├── dashboard.pdf
│   └── web_dashboard.html
└── images/
```

## 10. How to run
```bash
pip install pandas matplotlib
python python/clean_data.py     # profiles and cleans raw data, writes data/cleaned_orders.csv
python python/analysis.py       # prints KPIs and writes charts to images/
```
Open the `.pbix` in Power BI Desktop to explore the dashboard.
