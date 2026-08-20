# DX Executive Dashboard — Streamlit

Streamlit port of `DX_Dashboard_V2.html` (THAI Cargo Terminal Services, Aviation Business Unit).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (via GitHub)
1. Push `app.py`, `requirements.txt` (and this README) to a GitHub repo.
2. Go to https://share.streamlit.io → "New app" → pick the repo/branch → main file path `app.py`.
3. Deploy. No secrets or API keys are required — all data is embedded in `app.py`.

## What's included
- All 9 tabs from the original HTML: Overview, Assumption, Forecast Result, Monthly Trend,
  Revenue Breakdown, Unit Economics, Weight, Operations & HR, Update Guide.
- Same color palette, KPI-card / section-title / data-table look, and chart logic
  (Chart.js was swapped for Plotly, styled to match as closely as Streamlit allows).
- Same forecast engine: growth-assumption-driven Revenue/Expense/Weight projection,
  Capacity Readiness Index (CRI) with Tier-1/Tier-2 Labor & Equipment utilization,
  and the same auto-generated Strategic Insights rules.
- "Export All Data (.xlsx)" button (top-right) and per-table "Export CSV" buttons.
- Assumption inputs and forecast horizon persist for the session via `st.session_state`
  (equivalent of the original's "editing unlocked until Save" behaviour — no browser
  localStorage is used, since Streamlit reruns don't have access to it).

## Known differences from the original HTML (framework limits)
- Streamlit cannot pixel-replicate custom CSS/Chart.js 1:1; layout, colors, fonts and
  chart types are matched as closely as native Streamlit + Plotly allow.
- The dynamic "add/remove weight row" UI is replaced with a single editable table
  (`st.data_editor`) covering the next 12 forecast months — functionally equivalent.
- PDF upload only previews the file (the original HTML itself notes DX's source PDFs
  are flattened chart images that can't be reliably parsed either).
- Assumption values live in `st.session_state` per browser session; there's no
  cross-session persistence (the original used browser `localStorage`, which
  Streamlit's Python runtime has no direct access to).

## Updating the data
Edit the `DATA`, `WEIGHT_BY_TYPE`, `REV_BY_TYPE`, `TOP_AIRLINES`, `STAFF`,
`MARKET_SHARE_TREND`, and `FLIGHTS_BY_TYPE` dictionaries near the top of `app.py` —
same structure/units as the original HTML (see the in-app "Update Guide" tab).
