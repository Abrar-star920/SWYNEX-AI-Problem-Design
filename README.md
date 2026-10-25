# SWYNEX Interactive Dashboard (Task 3)

Interactive sales dashboard built on the cleaned retail orders dataset from Task 1 (179 orders, Jan-Oct 2025, 4 cities, 4 categories).

**Live demo:** _add your GitHub Pages link here_ (Settings > Pages > Deploy from branch `main` / root)

## Features
- **KPIs:** total revenue, orders, average order value, units sold, unique customers, top category
- **Charts:** monthly revenue trend, revenue by category, revenue by city, top 8 customers
- **Filters:** city, category, date range (all KPIs, charts, findings and table update together)
- **Key findings** that recalculate for the current filter selection
- **Top 10 orders** table

## Screenshot
_Add `screenshots/dashboard.png` here._

## Notes
- Revenue = `Quantity x Price` (Price treated as unit price).
- 40 missing quantities were filled with the median in Task 1, so revenue figures are partly estimated.
- Data is synthetic (generated for the exercise).

## Tools
HTML, JavaScript, Chart.js. Data: `data/cleaned_orders.csv` (embedded in `index.html`, so it works offline apart from the Chart.js CDN).

## Run
Open `index.html` in a browser.
