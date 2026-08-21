# DX Executive Dashboard — Streamlit (v2)

Streamlit port of `DX_Dashboard_V2.html` (THAI Cargo Terminal Services, Aviation Business Unit),
now with **automatic monthly PDF import**.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (via GitHub)
1. Push `app.py`, `requirements.txt`, and this README to a GitHub repo.
2. Go to https://share.streamlit.io → "New app" → pick the repo/branch → main file path `app.py`.
3. Deploy. No secrets or API keys are required — all data ships embedded in `app.py`, and any
   PDF-uploaded updates are saved to `dx_live_data.json` in the app's working directory.

## What's new in v2

### 1. Upload the monthly factsheet PDF and everything updates
Go to the **Assumption** tab (or **Update Guide**) and upload that month's
`DX Factsheet_YYYYMM.pdf`. The app reads the PDF's "Profit and Loss" table (this is real,
selectable text in DX's factsheets — not a chart image) and automatically fills in, for every
month found in the report:
- Revenue, Expense, Profit, Margin %, Weight (Kg), Cost per Kg, Revenue per Kg
- Revenue-by-type breakdown (Cargo Services, Delivery Order Fees, Storage Fees, Terminal
  Charges, Other Handling, Internal vs External)
- Staff snapshot (Total permanent staff, Outsource/Out Job, Average age, Job-level counts)

Every tab and KPI card (Overview, Monthly Trend, Revenue Breakdown, Unit Economics, Weight,
Operations & HR, Forecast Result) reads from this same data, so uploading one PDF refreshes
the whole dashboard at once.

**Saved automatically** — the merged result is written to `dx_live_data.json` next to `app.py`,
so it's still there the next time you run `streamlit run app.py`. Upload a new month's PDF each
month to keep the dashboard current; re-uploading an earlier month never overwrites a later
month you've already loaded.

**Not auto-extracted** (published only as chart/table images inside the PDF, not selectable
text): Import/Export/Transit weight split, Number of Flights, Top 10 Airlines, Market Share.
Update these manually (Weight Projection table on the Assumption tab, or by editing the data
dictionaries in `app.py`) if they change.

### 2. Assumption tab redesigned
- **Removed:** Revenue per Kg Growth / Cost per Kg Growth / Weight Growth (%/mo) inputs.
- **Added — Revenue Projection:** pick a month (up to 6 months ahead of the latest actual
  month) and enter the target Revenue directly in Baht (e.g. Aug 2026 → 307,000,000). Click
  "➕ Add month" for more rows. Months without an entry simply carry the last known revenue
  forward flat.
- **Renamed — Weight Projection** (previously "Monthly Weight (Tons) — Future Months"),
  capped at 6 months ahead, same TG/OA × Import/Export/Transit entry table as before.
- Expense is always forecast as projected Weight × the latest actual Cost per Kg (no separate
  expense-growth input needed).

### 3. Forecast Result tab
- KPI cards no longer show the "higher / short of matching same period last year" line —
  just the plain projected value.
- Insights, CRI, and charts all reflect the new manual-projection-driven forecast engine.

### 4. Chart styling
- All line charts are thicker (default width 3.5, 4.5 for the current year) with larger
  markers, so trends read clearly at a glance.
- All bar charts have rounded corners (`marker.cornerradius`).
- Chart margins/legend position were tuned (`automargin`, more bottom padding, horizontal
  legend further below the plot) so axis labels and legend text never overlap.

## Known limitations
- Streamlit cannot pixel-replicate custom CSS/Chart.js 1:1; layout, colors and chart types are
  matched as closely as native Streamlit + Plotly allow.
- The PDF parser is tuned to the specific layout of DX's monthly factsheet (a "Profit and Loss"
  page with a Jan→current-month table). If DX changes that report's template, the parser may
  need adjusting.
- `dx_live_data.json` persistence works reliably when you run the app locally / on your own
  server. On some hosted platforms (e.g. Streamlit Community Cloud) the filesystem can reset
  on redeploy, so re-upload the latest PDF after a redeploy if that happens.
- Assumption inputs that aren't PDF-derived (Revenue/Weight Projection, Operational Data,
  Equipment Fleet) live in `st.session_state` per browser session only — they are not written
  to `dx_live_data.json`.

## Updating data manually (fallback)
Edit the `DATA`, `WEIGHT_BY_TYPE`, `REV_BY_TYPE`, `TOP_AIRLINES`, `STAFF`, `MARKET_SHARE_TREND`,
and `FLIGHTS_BY_TYPE` dictionaries near the top of `app.py` — same structure/units as before
(see the in-app "Update Guide" tab).
