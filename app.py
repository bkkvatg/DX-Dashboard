# -*- coding: utf-8 -*-
"""
DX Executive Dashboard — Streamlit port of DX_Dashboard_V2.html
BKKDX : THAI Cargo Terminal Services — Board-Level Executive Report (Aviation Business Unit)

Run with:  streamlit run app.py
"""

import io
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="DX Executive Dashboard | THAI Cargo Terminal Services",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# COLOR TOKENS  (mirrors :root{} in the original HTML)
# ============================================================
PURPLE = "#370E62"
PURPLE_LIGHT = "#8A5FC2"
GOLD = "#F5C300"
PINK = "#B6007D"
PINK_LIGHT = "#E58FC4"
BG = "#F4F2F8"
CARD = "#FFFFFF"
TEXT = "#26203A"
TEXT_SUB = "#6B6480"
BORDER = "#E5E0EE"
GOOD = "#1E8E5A"
BAD = "#C0392B"
GREY = "#B9B3C7"

COLORS = {
    "purple": PURPLE, "purpleLight": PURPLE_LIGHT, "gold": GOLD, "pink": PINK,
    "pinkLight": PINK_LIGHT, "good": GOOD, "bad": BAD, "grey": GREY,
}

# ============================================================
# GLOBAL CSS  (recreates header / tabs / kpi-card / chart-card / table look)
# ============================================================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: "Segoe UI", Tahoma, "Sarabun", Arial, sans-serif;
}}
.stApp {{ background:{BG}; }}
#MainMenu, footer, header {{visibility:hidden;}}
.block-container {{ padding-top:0.5rem; padding-bottom:3rem; max-width:1320px; }}

/* ---------- header ---------- */
.app-header{{
  background:linear-gradient(120deg,{PURPLE} 0%,{PURPLE_LIGHT} 100%);
  color:#fff; padding:22px 28px; display:flex; justify-content:space-between;
  align-items:center; flex-wrap:wrap; gap:12px; border-radius:0 0 14px 14px; margin-bottom:6px;
}}
.app-header h1{{margin:0;font-size:22px;font-weight:700;}}
.app-header p{{margin:4px 0 0;font-size:13px;color:#E5D9F5;}}
.app-header .badge{{
  background:{GOLD}; color:{PURPLE}; font-weight:700; font-size:12px;
  padding:6px 14px; border-radius:20px; display:inline-block;
}}

/* ---------- kpi cards ---------- */
.kpi-row{{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; margin-bottom:18px;}}
.kpi-card{{
  background:{CARD}; border-radius:12px; padding:16px 18px;
  box-shadow:0 2px 8px rgba(55,14,98,0.08); border-top:4px solid {PINK};
}}
.kpi-card.gold{{border-top-color:{GOLD};}}
.kpi-card.purple{{border-top-color:{PURPLE};}}
.kpi-label{{font-size:12px; color:{TEXT_SUB}; text-transform:uppercase; letter-spacing:.5px; font-weight:600;}}
.kpi-value{{font-size:23px; font-weight:800; color:{PURPLE}; margin:6px 0 2px;}}
.kpi-sub{{font-size:12px; color:{TEXT_SUB};}}
.kpi-change{{font-size:12px; font-weight:700; margin-top:2px;}}
.kpi-change.positive{{color:{GOOD};}}
.kpi-change.negative{{color:{BAD};}}

/* ---------- section title ---------- */
.section-title{{font-size:15px; font-weight:700; color:{PURPLE}; margin:22px 0 10px; display:flex; align-items:center; gap:8px;}}
.section-title:before{{content:""; width:5px; height:16px; background:{GOLD}; border-radius:3px; display:inline-block;}}

/* ---------- chart card ---------- */
.chart-card-title{{font-size:14px; font-weight:700; color:{TEXT}; margin:0 0 6px;}}
.note{{font-size:12px; color:{TEXT_SUB}; margin-top:2px; margin-bottom:10px; line-height:1.5;}}
.info-box{{
  background:#FFF7DF; border:1px solid #F0DC9A; border-radius:12px; padding:16px 20px; font-size:13px; line-height:1.7; margin-bottom:18px;
}}
.info-box b{{color:{PURPLE};}}
.stat-mini{{display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed {BORDER}; font-size:13px;}}
.stat-mini b{{color:{PURPLE};}}

/* ---------- data table ---------- */
table.data-table{{width:100%; border-collapse:collapse; font-size:13px; background:#fff;}}
.data-table thead th{{
  text-align:right; padding:9px 10px; background:{PURPLE}; color:#fff; font-weight:600; font-size:12px;
}}
.data-table thead th:first-child{{text-align:left; border-radius:8px 0 0 0;}}
.data-table thead th:last-child{{border-radius:0 8px 0 0;}}
.data-table tbody td{{padding:8px 10px; text-align:right; border-bottom:1px solid {BORDER}; color:{TEXT};}}
.data-table tbody td:first-child{{text-align:left; font-weight:600;}}
.data-table tbody tr:nth-child(even){{background:#FAF8FD;}}
.table-wrap{{overflow-x:auto; background:{CARD}; border-radius:12px; padding:16px 18px; box-shadow:0 2px 8px rgba(55,14,98,0.08); margin-bottom:14px; max-height:520px; overflow-y:auto;}}

/* ---------- insight boxes ---------- */
.insight{{padding:11px 15px; border-radius:8px; margin-bottom:9px; font-size:13px; line-height:1.65;}}
.insight.warning{{background:#FDEDEC; border-left:4px solid {BAD}; color:#7A2318;}}
.insight.good{{background:#EAF7F0; border-left:4px solid {GOOD}; color:#134E31;}}
.insight.info{{background:#F0EAF9; border-left:4px solid {PURPLE}; color:#2E1049;}}

/* ---------- pretty-up native streamlit widgets to match theme ---------- */
.stTabs [data-baseweb="tab-list"]{{gap:4px; background:#fff; border-bottom:2px solid {BORDER}; padding:0 4px;}}
.stTabs [data-baseweb="tab"]{{height:44px; font-weight:600; color:{TEXT_SUB};}}
.stTabs [aria-selected="true"]{{color:{PURPLE} !important; border-bottom:3px solid {PINK} !important;}}
div[data-testid="stMetric"]{{background:{CARD}; border-radius:12px; padding:10px 14px; box-shadow:0 2px 8px rgba(55,14,98,0.08); border-top:4px solid {PINK};}}
.stButton>button{{border-radius:20px; font-weight:700;}}
div[data-testid="stVerticalBlockBorderWrapper"]{{
  background:{CARD}; border-radius:12px !important; box-shadow:0 2px 8px rgba(55,14,98,0.08);
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA  (verbatim port of the DATA / ANNUAL / ... objects in the HTML file)
# ============================================================
MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

DATA = {
    "y2023": {
        "revenue": [237755, 243040, 251297, 232125, 254039, 227952, 224125, 235001, 227860, 256953, 266196, 268809],
        "expense": [128724, 117806, 120858, 129974, 138175, 121801, 133673, 133975, 125527, 138991, 131600, 171255],
        "profit": [109031, 125233, 130439, 102151, 115864, 106150, 90452, 101027, 102333, 117962, 134596, 97554],
        "margin": [45.9, 51.5, 51.9, 44.0, 45.6, 46.6, 40.4, 43.0, 44.9, 45.9, 50.6, 36.3],
        "weight": [54417710, 56464740, 65911514, 59861163, 60192591, 60201778, 56937005, 57959044, 66482236, 66128818, 68737412, 68238644],
        "costPerKg": [2.37, 2.22, 1.93, 2.17, 2.30, 2.02, 2.39, 2.31, 1.93, 2.13, 1.91, 2.51],
        "revPerKg": [4.37, 4.30, 3.81, 3.88, 4.22, 3.79, 3.94, 4.05, 3.43, 3.89, 3.87, 3.94],
        "capacity": [73, 75, 87, 79, 84, 81, 85, 87, 88, 91, 90, 85],
    },
    "y2024": {
        "revenue": [273964, 277192, 290971, 355742, 303725, 290334, 312430, 320572, 304762, 321533, 340146, 333294],
        "expense": [130297, 128447, 141478, 134427, 138126, 127247, 135133, 148132, 140306, 146710, 167578, 159406],
        "profit": [143667, 148745, 149494, 221315, 165598, 163087, 177297, 172440, 164456, 174823, 172568, 173887],
        "margin": [52.4, 53.7, 51.4, 62.2, 54.5, 56.2, 56.7, 53.8, 54.0, 54.4, 50.7, 52.2],
        "weight": [66970890, 67202754, 79397191, 72015486, 76959731, 73917941, 78219338, 79341327, 80170924, 82871328, 83017604, 77871831],
        "costPerKg": [1.95, 1.91, 1.78, 1.87, 1.79, 1.72, 1.73, 1.87, 1.84, 1.81, 2.03, 2.05],
        "revPerKg": [4.07, 4.14, 3.79, 4.03, 3.95, 3.93, 3.99, 4.04, 3.79, 3.88, 4.10, 4.28],
        "capacity": [73, 75, 87, 79, 84, 81, 85, 87, 88, 91, 90, 85],
    },
    "y2025": {
        "revenue": [319307, 295668, 348245, 353025, 353045, 366580, 350955, 336420, 339155, 344985, 362260, 374991],
        "expense": [141941, 137242, 142201, 148582, 149404, 176059, 132404, 136378, 142696, 159643, 140069, 308667],
        "profit": [177367, 158426, 206044, 204443, 203641, 190521, 218552, 200042, 196459, 185342, 222191, 66324],
        "margin": [55.5, 53.6, 59.2, 57.9, 57.7, 52.0, 62.3, 59.5, 57.9, 53.7, 61.3, 17.7],
        "weight": [74361329, 71196236, 88747577, 85445544, 89318237, 84737255, 85967431, 84138800, 86691501, 83897840, 88477495, 82245579],
        "costPerKg": [1.86, 1.93, 1.62, 1.74, 1.69, 2.08, 1.56, 1.62, 1.65, 1.90, 1.71, 3.75],
        "revPerKg": [4.29, 4.15, 3.92, 4.13, 3.94, 4.33, 4.08, 4.00, 3.91, 4.11, 4.09, 4.56],
        "capacity": [81, 78, 97, 93, 98, 93, 94, 92, 95, 92, 97, 90],
    },
    "y2026": {
        "revenue": [367402, 352990, 409954, 412282, 416608, 414456, None, None, None, None, None, None],
        "expense": [176975, 110488, 151525, 165172, 155093, 149021, None, None, None, None, None, None],
        "profit": [190427, 242502, 258429, 247109, 261515, 265436, None, None, None, None, None, None],
        "margin": [51.8, 68.7, 63.0, 59.9, 62.8, 64.0, None, None, None, None, None, None],
        "weight": [78761376, 78184971, 91377891, 83607316, 87430543, 85249268, None, None, None, None, None, None],
        "costPerKg": [2.25, 1.41, 1.84, 1.98, 1.77, 1.75, None, None, None, None, None, None],
        "revPerKg": [4.66, 4.51, 4.48, 4.93, 4.75, 4.86, None, None, None, None, None, None],
        "capacity": [86, 86, 100, 92, 96, 94, None, None, None, None, None, None],
        "laborUtilPct": [78, 76, 88, 84, 90, 87, None, None, None, None, None, None],
        "equipmentUtilPct": [70, 68, 82, 79, 85, 83, None, None, None, None, None, None],
        "spaceUtilPct": [65, 64, 79, 74, 80, 77, None, None, None, None, None, None],
    },
}

ANNUAL = {
    "labels": ['2023', '2024', '2025'],
    "revenue": [2925152, 3724665, 4144636],
    "expense": [1592359, 1697289, 1915287],
    "profit": [1332792, 2027376, 2229350],
    "margin": [45.6, 52.2, 53.8],
    "tonnage": [741533, 917956, 1005225],
    "marketShare": [59, 61, 61],
}

WEIGHT_BY_TYPE = {
    "y2023": {
        "import": [18702989, 19233173, 19336091, 16078770, 16817491, 16267221, 16501973, 16832664, 16742420, 18889672, 20573536, 19456244],
        "export": [19859812, 20768308, 24000775, 23788914, 25252874, 23155065, 19043987, 19349224, 21414497, 23152041, 23870606, 23716034],
        "transit": [15799242, 16409033, 22510991, 19932775, 18062839, 20779493, 21391045, 21777156, 27641726, 24087105, 24293270, 25066366],
    },
    "y2024": {
        "import": [19270995, 19558440, 22264866, 18999316, 19594758, 20162367, 22486371, 21571604, 21430234, 22458609, 23295542, 21755396],
        "export": [23684275, 25792780, 31509971, 29856161, 32413422, 28468888, 29155052, 29127288, 30752336, 30715782, 30174662, 27808593],
        "transit": [24015620, 21851534, 25622353, 23160009, 24951551, 25286687, 26577915, 28642435, 27988354, 29696938, 29547400, 28307842],
    },
    "y2025": {
        "import": [20843566, 19002100, 22810786, 21220778, 22640118, 21420394, 23039564, 21560598, 22314359, 23181541, 25307791, 24927179],
        "export": [24219454, 26973286, 32874409, 35697417, 37389412, 34588185, 32236886, 30817495, 32262861, 30899798, 32558212, 32622533],
        "transit": [29298309, 25220850, 33062582, 28527350, 29308707, 28728675, 30690981, 31760707, 32114280, 29816501, 30611492, 24708466],
    },
    "y2026": {
        "import": [22926226, 22232344, 27230880, 23943824, 23962496, 24307385, None, None, None, None, None, None],
        "export": [28963170, 28497580, 35373514, 35870734, 39140467, 36053537, None, None, None, None, None, None],
        "transit": [26871980, 27431544, 28773497, 23792758, 24327580, 24888345, None, None, None, None, None, None],
    },
}

REV_BY_TYPE = {
    "y2023": {"cargoServices": 662315, "deliveryOrder": 203814, "storageFees": 514814, "terminalCharges": 788889, "otherHandling": 202329, "internal": 551457, "totalExternal": 2373694, "total": 2925152},
    "y2024": {"cargoServices": 926913, "deliveryOrder": 239842, "storageFees": 620126, "terminalCharges": 928943, "otherHandling": 212534, "internal": 796308, "totalExternal": 2928358, "total": 3724665},
    "y2025": {"cargoServices": 1031393, "deliveryOrder": 251905, "storageFees": 761205, "terminalCharges": 1054912, "otherHandling": 275480, "internal": 769742, "totalExternal": 3374894, "total": 4144636},
    "y2026": {"cargoServices": 564988, "deliveryOrder": 151073, "storageFees": 550737, "terminalCharges": 572181, "otherHandling": 149600, "internal": 385113, "totalExternal": 1988579, "total": 2373692},
}

TOP_AIRLINES = [
    {"airline": "TG (Thai Airways)", "freq": 5132, "revenue": 55, "weightProp": 44},
    {"airline": "BR (EVA Air)", "freq": 428, "revenue": 7, "weightProp": 6},
    {"airline": "NH (ANA)", "freq": 312, "revenue": 7, "weightProp": 6},
    {"airline": "CI (China Airlines)", "freq": 329, "revenue": 5, "weightProp": 4},
    {"airline": "CX (Cathay Pacific)", "freq": 441, "revenue": 4, "weightProp": 3},
    {"airline": "JL (Japan Airlines)", "freq": 242, "revenue": 4, "weightProp": 4},
    {"airline": "CV (Cargolux)", "freq": 46, "revenue": 3, "weightProp": 3},
    {"airline": "MU (China Eastern)", "freq": 471, "revenue": 3, "weightProp": 2},
    {"airline": "CK (China Cargo Airlines)", "freq": 26, "revenue": 3, "weightProp": 2},
    {"airline": "KE (Korean Air)", "freq": 257, "revenue": 3, "weightProp": 3},
]

STAFF = {"labels": ['2023', '2024', '2025', '2026 (Jun)'], "permanent": [503, 527, 516, 511], "outsource": [1207, 1278, 1439, 1479]}
STAFF_BY_YEAR = {"2023": 503, "2024": 527, "2025": 516, "2026": 511}
MARKET_SHARE_TREND = {"labels": ['2023', '2024', '2025', '2026 (H1)'], "thaiCargo": [59, 61, 61, 60], "bfs": [41, 32, 32, 32], "other": [0, 7, 7, 8]}
MARKET_SHARE_BY_YEAR = {"2023": 59, "2024": 61, "2025": 61, "2026": 60}

FLIGHTS_BY_TYPE = {
    "y2025": {"tg": [7486, 6675, 7303, 7077, 7166, 7073, 7301, 7228, 6928, 7185, 6959, 7380],
              "oal": [13011, 11130, 11853, 11562, 11081, 10932, 11747, 11295, 10402, 11281, 11328, 12643]},
    "y2026": {"tg": [7436, 6780, 7499, 7135, 8295, 6992, None, None, None, None, None, None],
              "oal": [13525, 12976, 13734, 12255, 7975, 9131, None, None, None, None, None, None]},
}

RESOURCE_CAPACITY_DEFAULT = {
    "maxTonnagePerMonth": 90000,
    "laborFTEAvailable": 620,
    "laborTonPerFTEBenchmark": 165,
    "equipmentUnits": {"forklift": 14, "etv": 6, "uldDolly": 20, "highLoader": 4, "tugTractor": 8, "asrsCrane": 4},
    "equipmentHoursPerDayAvailable": 16,
    "spaceASRSSlotsTotal": 12000,
}
EQUIPMENT_DAYS_ASSUMED = 30

EQUIPMENT_TYPES = [
    {"key": "forkliftHrs", "unitKey": "forklift", "label": "Forklift Hrs", "placeholder": "e.g. 3200"},
    {"key": "etvHrs", "unitKey": "etv", "label": "ETV Hrs", "placeholder": "e.g. 1200"},
    {"key": "uldDollyHrs", "unitKey": "uldDolly", "label": "ULD Dolly Hrs", "placeholder": "e.g. 4200"},
    {"key": "highLoaderHrs", "unitKey": "highLoader", "label": "High Loader Hrs", "placeholder": "e.g. 800"},
    {"key": "tugTractorHrs", "unitKey": "tugTractor", "label": "Tug/Tractor Hrs", "placeholder": "e.g. 1600"},
    {"key": "asrsCraneHrs", "unitKey": "asrsCrane", "label": "ASRS Crane Hrs", "placeholder": "e.g. 700"},
]
EQUIPMENT_FLEET_FIELDS = [
    {"unitKey": "forklift", "label": "Forklift (Number)"},
    {"unitKey": "etv", "label": "ETV (Number)"},
    {"unitKey": "uldDolly", "label": "ULD Dolly (Number)"},
    {"unitKey": "highLoader", "label": "High Loader (Number)"},
    {"unitKey": "tugTractor", "label": "Tractor (Number)"},
]
SPECIAL_CARGO_FIELDS = [
    {"key": "perishable", "label": "Perishable"},
    {"key": "dg", "label": "Dangerous Goods"},
    {"key": "coldChain", "label": "Cold Chain"},
    {"key": "live", "label": "Live Animal"},
    {"key": "valuable", "label": "Valuable"},
]
OPS_WEIGHT_BREAKDOWN_FIELDS = [
    ("tgImport", "TG (Import)"), ("tgExport", "TG (Export)"), ("tgTransit", "TG (Transit)"),
    ("oaImport", "OA (Import)"), ("oaExport", "OA (Export)"), ("oaTransit", "OA (Transit)"),
]

OPS_INPUT_DEFAULT = {
    "fteCount": 511, "forkliftHrs": None, "etvHrs": None, "uldDollyHrs": None,
    "highLoaderHrs": None, "tugTractorHrs": None, "asrsCraneHrs": None,
    "shipmentAwb": None, "peakDayTons": None,
    "perishable": None, "dg": None, "coldChain": None, "live": None, "valuable": None,
}

# ============================================================
# FORMAT HELPERS
# ============================================================
def fmt(n):
    if n is None:
        return "-"
    return f"{round(n):,}"

def fmt1(n):
    if n is None:
        return "-"
    return f"{n:.1f}"

def fmt2(n):
    if n is None:
        return "-"
    return f"{n:.2f}"

def avg(arr):
    valid = [v for v in arr if v is not None]
    if not valid:
        return None
    return sum(valid) / len(valid)

def pct_change(cur, prev):
    if not prev:
        return 0
    return (cur - prev) / prev * 100

def null_array(n):
    return [None] * n

# combine every year/month into one flat timeline (mirrors buildAllMonths())
def build_all_months():
    arr = []
    for y in ["2023", "2024", "2025", "2026"]:
        d = DATA["y" + y]
        for m in range(12):
            arr.append({
                "year": y, "m": m, "revenue": d["revenue"][m], "expense": d["expense"][m],
                "profit": d["profit"][m], "margin": d["margin"][m], "weight": d["weight"][m],
                "costPerKg": d["costPerKg"][m], "revPerKg": d["revPerKg"][m],
            })
    return arr

ALL_MONTHS = build_all_months()

def ytd_sum_field(year, max_m, field):
    d = DATA.get("y" + year)
    if not d:
        return None
    s, any_ = 0, False
    for m in range(max_m + 1):
        v = d[field][m]
        if v is not None:
            s += v
            any_ = True
    return s if any_ else None

# ============================================================
# UI HELPERS
# ============================================================
def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def note(text):
    st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)

def kpi_card(label, value, sub=None, change=None, change_label="YoY", cls="pink", invert=False, extra_html=""):
    chg_html = ""
    if change is not None:
        good = (change <= 0) if invert else (change >= 0)
        css_cls = "positive" if good else "negative"
        sign = "+" if change >= 0 else ""
        chg_html = f'<div class="kpi-change {css_cls}">{sign}{change:.1f}% {change_label}</div>'
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi-card {cls}"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>{sub_html}{chg_html}{extra_html}</div>')

def kpi_row(cards_html):
    st.markdown(f'<div class="kpi-row">{"".join(cards_html)}</div>', unsafe_allow_html=True)

def data_table(headers, rows, table_id=""):
    """rows: list of lists of already-formatted strings/HTML. First column left aligned."""
    thead = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>"
    tbody = "<tbody>"
    for r in rows:
        tbody += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    tbody += "</tbody>"
    html = f'<div class="table-wrap"><table class="data-table" id="{table_id}">{thead}{tbody}</table></div>'
    st.markdown(html, unsafe_allow_html=True)

def df_download_button(df, filename, label="⬇ Export CSV", key=None):
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(label, data=csv, file_name=filename, mime="text/csv", key=key)

def chart_card(fig, title=None, height=300):
    with st.container(border=True):
        if title:
            st.markdown(f'<div class="chart-card-title">{title}</div>', unsafe_allow_html=True)
        fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, width='stretch', config={"displaylogo": False})

# ============================================================
# PLOTLY CHART BUILDERS  (mimic Chart.js look: legend bottom, transparent bg)
# ============================================================
BASE_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5, font=dict(size=11)),
    font=dict(color=TEXT, size=12),
    margin=dict(l=10, r=10, t=10, b=10),
)

def line_chart(labels, series, y_suffix="", y_title=None, y_range=None):
    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(
            x=labels, y=s["data"], mode="lines+markers", name=s["label"],
            line=dict(color=s.get("color", PURPLE), width=s.get("width", 2),
                      dash=s.get("dash", None), shape="spline", smoothing=0.5),
            marker=dict(size=s.get("point_radius", 4)),
            connectgaps=False,
        ))
    fig.update_layout(**BASE_LAYOUT)
    fig.update_yaxes(ticksuffix=y_suffix, title=y_title, gridcolor=BORDER, range=y_range)
    fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
    return fig

def bar_chart(labels, series, stacked=False, y_suffix="", y_title=None, horizontal=False):
    fig = go.Figure()
    for s in series:
        if horizontal:
            fig.add_trace(go.Bar(y=labels, x=s["data"], name=s["label"],
                                  marker_color=s.get("color", PURPLE), orientation="h"))
        else:
            fig.add_trace(go.Bar(x=labels, y=s["data"], name=s["label"],
                                  marker_color=s.get("color", PURPLE)))
    fig.update_layout(barmode="stack" if stacked else "group", **BASE_LAYOUT)
    if horizontal:
        fig.update_xaxes(ticksuffix=y_suffix, gridcolor=BORDER, title=y_title)
    else:
        fig.update_yaxes(ticksuffix=y_suffix, gridcolor=BORDER, title=y_title)
        fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
    return fig

def combo_bar_line(labels, bars, lines, y_title=None):
    fig = go.Figure()
    for s in bars:
        fig.add_trace(go.Bar(x=labels, y=s["data"], name=s["label"], marker_color=s.get("color", PURPLE)))
    for s in lines:
        fig.add_trace(go.Scatter(x=labels, y=s["data"], name=s["label"], mode="lines+markers",
                                  line=dict(color=s.get("color", GOLD), width=2)))
    fig.update_layout(**BASE_LAYOUT)
    fig.update_yaxes(gridcolor=BORDER, title=y_title)
    fig.update_xaxes(gridcolor="rgba(0,0,0,0)")
    return fig

def doughnut_chart(labels, values, colors, title=None):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55, marker=dict(colors=colors),
        textinfo="percent", texttemplate="%{percent:.1%}",
        textfont=dict(color="#fff", size=12),
    ))
    layout = dict(BASE_LAYOUT)
    if title:
        layout = {**layout, "title": dict(text=title, x=0.5, font=dict(size=12, color=TEXT_SUB))}
    fig.update_layout(**layout)
    return fig

# ============================================================
# HEADER
# ============================================================
h_left, h_right = st.columns([3, 1])
with h_left:
    st.markdown("""
    <div class="app-header">
      <div>
        <h1>DX Executive Dashboard</h1>
        <p>BKKDX : THAI Cargo Terminal Services — Board-Level Executive Report (Aviation Business Unit)</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# (export button + badge rendered inline just under the header, since Streamlit
#  can't place a native download_button inside the raw HTML gradient banner)
b1, b2, b3 = st.columns([5, 1.4, 1.6])
with b2:
    st.markdown(f'<div style="text-align:right;padding-top:6px;"><span class="badge">Last Updated: June 2026</span></div>', unsafe_allow_html=True)
with b3:
    pass  # export button placed after workbook bytes are built (see bottom of Update Guide section is too late — build now)

# ============================================================
# SESSION STATE — assumptions (Assumption tab inputs), persists for the session
# ============================================================
def init_state():
    ss = st.session_state
    if "assumption_locked" not in ss:
        ss.assumption_locked = False
    if "rev_growth" not in ss or "exp_growth" not in ss or "weight_growth" not in ss:
        def growth_stats(arr):
            vals = [v for v in arr if v is not None]
            rates = []
            for i in range(1, len(vals)):
                if vals[i - 1] != 0:
                    rates.append((vals[i] - vals[i - 1]) / vals[i - 1])
            if not rates:
                return 0.0
            return sum(rates) / len(rates)
        ss.rev_growth = round(growth_stats(DATA["y2026"]["revPerKg"]) * 100, 2)
        ss.exp_growth = round(growth_stats(DATA["y2026"]["costPerKg"]) * 100, 2)
        ss.weight_growth = round(growth_stats(DATA["y2026"]["weight"]) * 100, 2)
    if "ops_input" not in ss:
        ss.ops_input = dict(OPS_INPUT_DEFAULT)
    if "equipment_units" not in ss:
        ss.equipment_units = dict(RESOURCE_CAPACITY_DEFAULT["equipmentUnits"])
    if "ops_weight_tons" not in ss:
        ss.ops_weight_tons = {}          # {global_month_index: tons}
    if "ops_weight_breakdown" not in ss:
        ss.ops_weight_breakdown = {k: {} for k, _ in OPS_WEIGHT_BREAKDOWN_FIELDS}  # {field: {gidx: value}}
    if "horizon" not in ss:
        ss.horizon = 6
    if "overview_year" not in ss:
        ss.overview_year = "2026"
    if "weight_year" not in ss:
        ss.weight_year = "2026"
    if "trend_years" not in ss:
        ss.trend_years = {"2023": True, "2024": True, "2025": True, "2026": True}

init_state()

# ============================================================
# CRI / FORECAST ENGINE  (Python port of the Assumption/Forecast JS logic)
# ============================================================
def find_last_actual_month_index():
    d = DATA["y2026"]
    for m in range(11, -1, -1):
        if d["revenue"][m] is not None:
            return m
    return None

def compute_labor_util_tier2(m):
    weight_ton = st.session_state.ops_weight_tons.get(m)
    fte = st.session_state.ops_input.get("fteCount")
    if weight_ton is None or not fte:
        return None
    ton_per_fte = weight_ton / fte
    return ton_per_fte / RESOURCE_CAPACITY_DEFAULT["laborTonPerFTEBenchmark"] * 100

def get_labor_util_for_month(m):
    t2 = compute_labor_util_tier2(m)
    return t2 if t2 is not None else DATA["y2026"]["laborUtilPct"][m]

def compute_equipment_util_tier2():
    max_util, max_type = None, None
    for t in EQUIPMENT_TYPES:
        hours_used = st.session_state.ops_input.get(t["key"])
        units = st.session_state.equipment_units.get(t["unitKey"])
        if hours_used is None or not units:
            continue
        hours_avail = units * RESOURCE_CAPACITY_DEFAULT["equipmentHoursPerDayAvailable"] * EQUIPMENT_DAYS_ASSUMED
        util = (hours_used / hours_avail * 100) if hours_avail > 0 else None
        if util is not None and (max_util is None or util > max_util):
            max_util, max_type = util, t["label"]
    return {"util": max_util, "type": max_type}

def get_equipment_util_for_month(m):
    last_m = find_last_actual_month_index()
    if m == last_m:
        t2 = compute_equipment_util_tier2()
        if t2["util"] is not None:
            return t2
    return {"util": DATA["y2026"]["equipmentUtilPct"][m], "type": None}

def get_last_actual_2026():
    m = find_last_actual_month_index()
    if m is None:
        return None
    d = DATA["y2026"]
    return {
        "m": m, "year": 2026, "revenue": d["revenue"][m], "expense": d["expense"][m], "weight": d["weight"][m],
        "laborUtilPct": get_labor_util_for_month(m), "equipmentUtilPct": get_equipment_util_for_month(m)["util"],
        "spaceUtilPct": d["spaceUtilPct"][m], "capacity": d["capacity"][m],
    }

def cri_color(pct):
    if pct is None:
        return {"hex": GREY, "label": "No data"}
    if pct >= 90:
        return {"hex": BAD, "label": "Red — Constrained"}
    if pct >= 70:
        return {"hex": GOLD, "label": "Yellow — Plan Ahead"}
    return {"hex": GOOD, "label": "Green — Healthy"}

def resource_items(row):
    return [
        ("Labor", row.get("laborUtilPct")),
        ("Equipment", row.get("equipmentUtilPct")),
        ("Space (ASRS)", row.get("spaceUtilPct")),
        ("Tonnage/Warehouse", row.get("capacity")),
    ]

def compute_cri(row):
    items = resource_items(row)
    valued = [it for it in items if it[1] is not None]
    if not valued:
        return None, items[0][0]
    top = max(valued, key=lambda x: x[1])
    return top[1], top[0]

def compute_forecast_rows(horizon, rev_g_pct, exp_g_pct, w_g_pct):
    base = get_last_actual_2026()
    if not base:
        return None
    rev_g, exp_g, w_g = rev_g_pct / 100.0, exp_g_pct / 100.0, w_g_pct / 100.0
    rev_per_kg = (base["revenue"] * 1000 / base["weight"]) if base["weight"] else 0
    cost_per_kg = (base["expense"] * 1000 / base["weight"]) if base["weight"] else 0

    rows = []
    last_known_weight = base["weight"]
    steps_since_anchor = 0
    for t in range(1, horizon + 1):
        g_idx = base["m"] + t
        manual_tons = st.session_state.ops_weight_tons.get(g_idx)
        if manual_tons is not None:
            w = manual_tons * 1000
            last_known_weight = w
            steps_since_anchor = 0
            weight_is_manual = True
        else:
            steps_since_anchor += 1
            w = last_known_weight * ((1 + w_g) ** steps_since_anchor)
            weight_is_manual = False

        rev_per_kg = rev_per_kg * (1 + rev_g)
        cost_per_kg = cost_per_kg * (1 + exp_g)
        rev = w * rev_per_kg / 1000
        exp = w * cost_per_kg / 1000
        profit = rev - exp
        margin = (profit / rev * 100) if rev else 0
        capacity_pct = (w / 1000) / RESOURCE_CAPACITY_DEFAULT["maxTonnagePerMonth"] * 100
        growth_factor = (w / base["weight"]) if base["weight"] else 1
        labor = base["laborUtilPct"] * growth_factor if base["laborUtilPct"] is not None else None
        equip = base["equipmentUtilPct"] * growth_factor if base["equipmentUtilPct"] is not None else None
        space = base["spaceUtilPct"] * growth_factor if base["spaceUtilPct"] is not None else None
        m_idx = g_idx % 12
        yr = base["year"] + g_idx // 12
        row = {
            "month": MONTHS_EN[m_idx], "year": yr, "revenue": rev, "expense": exp, "profit": profit,
            "margin": margin, "weight": w, "weightIsManual": weight_is_manual, "costPerKg": cost_per_kg,
            "revPerKg": rev_per_kg, "capacity": capacity_pct, "laborUtilPct": labor,
            "equipmentUtilPct": equip, "spaceUtilPct": space,
        }
        cri, bottleneck = compute_cri(row)
        row["cri"], row["bottleneck"] = cri, bottleneck
        rows.append(row)
    return {"rows": rows, "base": base, "revG": rev_g, "expG": exp_g}

def get_same_period_last_year(rows):
    ref_revenue = ref_expense = ref_weight_kg = 0
    count = 0
    last_month_margin = None
    first_label = last_label = None
    n = len(rows)
    for idx, r in enumerate(rows):
        m_idx = MONTHS_EN.index(r["month"])
        prev_year = r["year"] - 1
        yd = DATA.get("y" + str(prev_year))
        label = f'{r["month"]} {prev_year}'
        if idx == 0:
            first_label = label
        last_label = label
        if yd and yd["revenue"][m_idx] is not None:
            ref_revenue += yd["revenue"][m_idx]
            ref_expense += yd["expense"][m_idx]
            ref_weight_kg += yd["weight"][m_idx]
            count += 1
            if idx == n - 1:
                last_month_margin = (yd["revenue"][m_idx] - yd["expense"][m_idx]) / yd["revenue"][m_idx] * 100
    if count == 0:
        return None
    return {
        "revenue": ref_revenue, "expense": ref_expense, "profit": ref_revenue - ref_expense,
        "weightTon": round(ref_weight_kg / 1000), "lastMonthMargin": last_month_margin,
        "label": first_label if first_label == last_label else f"{first_label} – {last_label}",
        "complete": count == n, "monthsFound": count, "monthsTotal": n,
    }

def gap_vs_last_year_html(current, ref, unit, decimals=0, no_pct=False, invert=False):
    if ref is None or current is None:
        return ""
    f = fmt1 if decimals == 1 else fmt
    diff = current - ref
    pct_txt = ""
    if not no_pct and ref != 0:
        pct = diff / abs(ref) * 100
        pct_txt = f' ({"+" if pct >= 0 else ""}{pct:.1f}%)'
    is_higher = diff >= 0
    is_good = (not is_higher) if invert else is_higher
    cls = "positive" if is_good else "negative"
    if is_higher:
        return f'<div class="kpi-change {cls}">▲ +{f(abs(diff))}{unit}{pct_txt} higher than same period last year</div>'
    return f'<div class="kpi-change {cls}">▼ {f(abs(diff))}{unit}{pct_txt} short of matching same period last year</div>'

def render_forecast_insights(rows, base, rev_g, exp_g):
    last_row = rows[-1]
    base_margin = (base["revenue"] - base["expense"]) / base["revenue"] * 100
    margin_delta = last_row["margin"] - base_margin
    base_rev_per_kg = base["revenue"] * 1000 / base["weight"]
    insights = []

    if margin_delta < -3:
        insights.append(("warning", f'Profit margin is projected to fall by {abs(margin_delta):.1f} points over the next {len(rows)} months (from {fmt1(base_margin)}% to {fmt1(last_row["margin"])}%). Action: review Personnel Expense and Other Expense, DX\'s largest direct cost lines, and consider a cost-efficiency program before this trend compounds.'))
    elif margin_delta > 3:
        insights.append(("good", f'Profit margin is projected to improve by {margin_delta:.1f} points (from {fmt1(base_margin)}% to {fmt1(last_row["margin"])}%). Action: validate that the underlying revenue/cost assumptions are realistic and sustainable before using this scenario to set formal budget targets.'))
    else:
        insights.append(("info", f'Profit margin is projected to stay broadly stable (from {fmt1(base_margin)}% to {fmt1(last_row["margin"])}%) under this scenario. Action: use this as the base-case budget reference and stress-test by editing the Growth Assumption boxes directly (e.g. lower Revenue Growth, higher Expense Growth).'))

    max_capacity, max_cap_month = 0, ""
    min_capacity, min_cap_month = 999, ""
    for r in rows:
        if r["capacity"] > max_capacity:
            max_capacity, max_cap_month = r["capacity"], f'{r["month"]} {r["year"]}'
        if r["capacity"] < min_capacity:
            min_capacity, min_cap_month = r["capacity"], f'{r["month"]} {r["year"]}'
    if max_capacity > 95:
        insights.append(("warning", f'Capacity utilization is projected to reach {fmt1(max_capacity)}% by {max_cap_month}, approaching the 90,000-ton/month ceiling. Action: plan capacity expansion, overflow arrangements, or demand-shaping (e.g. off-peak incentives) ahead of that month to avoid service-level risk.'))
    elif min_capacity < 70:
        insights.append(("info", f'Capacity utilization is projected to stay as low as {fmt1(min_capacity)}% in {min_cap_month}. Action: there may be room to pursue additional volume or new airline/customer partnerships without near-term capacity investment.'))

    if rev_g < 0:
        insights.append(("warning", f'The revenue growth assumption is negative ({rev_g*100:.2f}%/month). Action: review the commercial pipeline and retention risk for top accounts (TG, BR, NH, CI, CX) and identify specific recovery actions before this scenario is used as a target.'))
    elif exp_g > rev_g:
        insights.append(("warning", f'Expense is assumed to grow faster than Revenue ({exp_g*100:.2f}%/month vs {rev_g*100:.2f}%/month). Action: this scenario will compress margin over time even if revenue keeps growing — prioritize cost-control levers (staffing mix, concession/lease renegotiation, utility efficiency).'))
    else:
        insights.append(("good", f'Revenue is assumed to grow at least as fast as Expense ({rev_g*100:.2f}%/month vs {exp_g*100:.2f}%/month), which should support margin if the assumption holds. Action: monitor actuals monthly against this assumption and update the scenario as new data comes in.'))

    if last_row["revPerKg"] < base_rev_per_kg - 0.1:
        insights.append(("warning", f'Revenue per Kg is projected to decline from {fmt2(base_rev_per_kg)} to {fmt2(last_row["revPerKg"])} THB/Kg even as volume grows. Action: review yield/pricing management so that volume growth does not dilute unit margins.'))

    red_month = None
    for r in rows:
        if r["cri"] is not None and r["cri"] >= 90:
            red_month = r
            break
    if red_month:
        insights.append(("warning", f'At this growth assumption, <b>{red_month["bottleneck"]}</b> is projected to become the binding constraint (≥90% utilization) by <b>{red_month["month"]} {red_month["year"]}</b> — before the other three resources. This is the resource to invest in first; the warehouse tonnage ceiling is not necessarily where the real bottleneck sits. Action: review {red_month["bottleneck"].lower()} capacity (headcount/fleet/slots) and start the appropriate lead-time process (hiring, procurement, or expansion) now.'))
    elif last_row["cri"] is not None and last_row["cri"] >= 70:
        insights.append(("info", f'Capacity Readiness Index is projected to reach {fmt1(last_row["cri"])}% (bottleneck: {last_row["bottleneck"]}) by the end of this horizon — still under the 90% action threshold, but worth planning ahead for since it has crossed into the yellow zone.'))
    else:
        insights.append(("good", f'All four resources (Labor, Equipment, Space, Tonnage) are projected to stay under 70% utilization through the end of this horizon (CRI: {fmt1(last_row["cri"])}%, bottleneck: {last_row["bottleneck"]}). There should be room to pursue additional volume without near-term resource investment.'))

    html = ""
    for typ, text in insights:
        icon = "⚠" if typ == "warning" else ("✓" if typ == "good" else "ℹ")
        html += f'<div class="insight {typ}">{icon} {text}</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# EXCEL EXPORT (mirrors exportAllToExcel())
# ============================================================
def build_export_workbook():
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        # Sheet 1: Monthly Data
        rows = []
        for y in ["2023", "2024", "2025", "2026"]:
            d = DATA["y" + y]
            for m in range(12):
                if d["revenue"][m] is None:
                    continue
                rows.append([y, MONTHS_EN[m], d["revenue"][m], d["expense"][m], d["profit"][m], d["margin"][m],
                             d["weight"][m], d["costPerKg"][m], d["revPerKg"][m], d["capacity"][m]])
        pd.DataFrame(rows, columns=["Year", "Month", "Revenue (Thousand Baht)", "Expense (Thousand Baht)",
                                     "Profit (Thousand Baht)", "Margin %", "Weight (Kg)", "Cost per Kg (THB)",
                                     "Revenue per Kg (THB)", "Capacity %"]).to_excel(writer, sheet_name="Monthly Data", index=False)

        # Sheet 2: Annual Summary
        annual_rows = [
            ["Revenue (Thousand Baht)"] + ANNUAL["revenue"],
            ["Expense (Thousand Baht)"] + ANNUAL["expense"],
            ["Profit (Thousand Baht)"] + ANNUAL["profit"],
            ["Profit Margin %"] + ANNUAL["margin"],
            ["Total Weight (Tons)"] + ANNUAL["tonnage"],
            ["Market Share %"] + ANNUAL["marketShare"],
        ]
        pd.DataFrame(annual_rows, columns=["Metric"] + ANNUAL["labels"]).to_excel(writer, sheet_name="Annual Summary", index=False)

        # Sheet 3: Revenue By Type
        rev_items = [["Cargo Terminal Charges", "terminalCharges"], ["Cargo Services", "cargoServices"],
                     ["Cargo Storage Fees", "storageFees"], ["Delivery Order Fees", "deliveryOrder"],
                     ["Other Cargo Handling", "otherHandling"], ["Internal Revenue (TG)", "internal"],
                     ["Total Revenue", "total"]]
        rev_rows = [[label, REV_BY_TYPE["y2023"][key], REV_BY_TYPE["y2024"][key], REV_BY_TYPE["y2025"][key], REV_BY_TYPE["y2026"][key]]
                    for label, key in rev_items]
        pd.DataFrame(rev_rows, columns=["Revenue Type", "2023", "2024", "2025", "2026 (H1)"]).to_excel(writer, sheet_name="Revenue By Type", index=False)

        # Sheet 4: Top Airlines
        pd.DataFrame([[a["airline"], a["freq"], a["revenue"], a["weightProp"]] for a in TOP_AIRLINES],
                     columns=["Airline", "Flights", "Revenue (Million Baht)", "Weight Share %"]).to_excel(writer, sheet_name="Top Airlines", index=False)

        # Sheet 5: Staff & Market Share
        staff_rows = [[STAFF["labels"][i], STAFF["permanent"][i], STAFF["outsource"][i]] for i in range(len(STAFF["labels"]))]
        pd.DataFrame(staff_rows, columns=["Year", "Permanent Staff", "Outsource / Out Job"]).to_excel(writer, sheet_name="Staff & Market Share", index=False, startrow=0)
        ms_rows = [[MARKET_SHARE_TREND["labels"][i], MARKET_SHARE_TREND["thaiCargo"][i], MARKET_SHARE_TREND["bfs"][i], MARKET_SHARE_TREND["other"][i]] for i in range(len(MARKET_SHARE_TREND["labels"]))]
        pd.DataFrame(ms_rows, columns=["Year", "THAI Cargo Share %", "BFS Share %", "Other Share %"]).to_excel(writer, sheet_name="Staff & Market Share", index=False, startrow=len(staff_rows) + 3)

        # Sheet 6: Weight By Type
        wt_rows = []
        for y in ["2023", "2024", "2025", "2026"]:
            d = WEIGHT_BY_TYPE["y" + y]
            for m in range(12):
                if d["import"][m] is None:
                    continue
                total = d["import"][m] + d["export"][m] + d["transit"][m]
                wt_rows.append([y, MONTHS_EN[m], d["import"][m], d["export"][m], d["transit"][m], total])
        pd.DataFrame(wt_rows, columns=["Year", "Month", "Import (Kg)", "Export (Kg)", "Transit (Kg)", "Total (Kg)"]).to_excel(writer, sheet_name="Weight By Type", index=False)

    return buf.getvalue()

with b3:
    st.markdown('<div style="padding-top:2px;"></div>', unsafe_allow_html=True)
    st.download_button("⬇ Export All Data (.xlsx)", data=build_export_workbook(),
                        file_name="DX_Dashboard_Export.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="export_all")

# ============================================================
# TABS
# ============================================================
TAB_NAMES = ["Overview", "Assumption", "Forecast Result", "Monthly Trend", "Revenue Breakdown",
             "Unit Economics", "Weight", "Operations & HR", "Update Guide"]
tabs = st.tabs(TAB_NAMES)

# ------------------------------------------------------------------
# TAB 1 — OVERVIEW
# ------------------------------------------------------------------
with tabs[0]:
    years = ["2023", "2024", "2025", "2026"]
    sel = st.radio("Select Year (KPIs below):", years, index=years.index(st.session_state.overview_year),
                    horizontal=True, key="overview_year_radio")
    st.session_state.overview_year = sel
    year = sel

    year_months = [x for x in ALL_MONTHS if x["year"] == year and x["revenue"] is not None]
    if year_months:
        latest = year_months[-1]
        month_label = f'{MONTHS_EN[latest["m"]]} {year}'
        ytd_rev = sum(x["revenue"] for x in year_months)
        ytd_expense = sum(x["expense"] for x in year_months)
        ytd_profit = sum(x["profit"] for x in year_months)
        ytd_weight_ton = round(sum(x["weight"] for x in year_months) / 1000)
        year_avg_margin = ytd_profit / ytd_rev * 100
        avg_rev_per_kg = avg([x["revPerKg"] for x in year_months])
        avg_cost_per_kg = avg([x["costPerKg"] for x in year_months])

        prev_year = str(int(year) - 1)
        prev_ytd_rev = ytd_sum_field(prev_year, latest["m"], "revenue")
        prev_ytd_exp = ytd_sum_field(prev_year, latest["m"], "expense")
        prev_ytd_profit = ytd_sum_field(prev_year, latest["m"], "profit")
        yoy_rev = pct_change(ytd_rev, prev_ytd_rev) if prev_ytd_rev else None
        yoy_exp = pct_change(ytd_expense, prev_ytd_exp) if prev_ytd_exp else None
        yoy_profit = pct_change(ytd_profit, prev_ytd_profit) if prev_ytd_profit else None

        staff_count = STAFF_BY_YEAR.get(year)
        months_elapsed = len(year_months)
        rev_per_employee = (ytd_rev * 1000 / staff_count / months_elapsed) if staff_count else None
        ton_per_employee = (ytd_weight_ton / staff_count / months_elapsed) if staff_count else None

        fd = FLIGHTS_BY_TYPE.get("y" + year)
        ytd_flights_tg = ytd_flights_oal = None
        if fd:
            ytd_flights_tg, ytd_flights_oal = 0, 0
            for fm in range(latest["m"] + 1):
                if fd["tg"][fm] is not None:
                    ytd_flights_tg += fd["tg"][fm]
                    ytd_flights_oal += fd["oal"][fm]

        cards = [
            kpi_card("Revenue YTD (Thousand Baht)", fmt(ytd_rev), f"YTD to {month_label}", yoy_rev, "YoY", "gold"),
            kpi_card("Expense YTD (Thousand Baht)", fmt(ytd_expense), f"YTD to {month_label}", yoy_exp, "YoY", "pink", invert=True),
            kpi_card("Profit YTD (Thousand Baht)", fmt(ytd_profit), f"YTD to {month_label}", yoy_profit, "YoY", "purple"),
            kpi_card("Profit Margin (Avg YTD)", f"{fmt1(year_avg_margin)}%", f"Average for {year} YTD", cls="gold"),
            kpi_card("Revenue per Kg (Avg YTD)", f"{fmt2(avg_rev_per_kg)} THB/Kg", f"Average for {year} YTD", cls="purple"),
            kpi_card("Cost per Kg (Avg YTD)", f"{fmt2(avg_cost_per_kg)} THB/Kg", f"Average for {year} YTD", cls="pink"),
            kpi_card("Cumulative Weight (Tons)", fmt(ytd_weight_ton), f"YTD to {month_label}", cls="purple"),
            kpi_card(f"Market Share {year}", f'{MARKET_SHARE_BY_YEAR.get(year, "-")}%', "vs BFS and other providers", cls="pink"),
            kpi_card("Revenue / Employee (Monthly Avg)", f'{fmt(rev_per_employee) if rev_per_employee is not None else "-"} THB/mo',
                      f'YTD Revenue ÷ {fmt(staff_count)} permanent staff ÷ {months_elapsed} month(s)', cls="gold"),
            kpi_card("Tonnage / Employee (Monthly Avg)", f'{fmt1(ton_per_employee) if ton_per_employee is not None else "-"} Tons/mo',
                      f'YTD Weight ÷ {fmt(staff_count)} permanent staff ÷ {months_elapsed} month(s)', cls="purple"),
            kpi_card("Number of Flights (YTD)",
                      f'TG {fmt(ytd_flights_tg)} / OAL {fmt(ytd_flights_oal)}' if ytd_flights_tg is not None else "N/A",
                      (f'YTD to {month_label} — Total: {fmt(ytd_flights_tg + ytd_flights_oal)}' if ytd_flights_tg is not None
                       else f'Not available for {year} (source reports don\'t table this split)'), cls="pink"),
        ]
        kpi_row(cards)

    section_title("Annual Performance Comparison (2023–2025, Unit: Thousand Baht)")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = bar_chart(ANNUAL["labels"], [
            {"label": "Revenue", "data": ANNUAL["revenue"], "color": PURPLE},
            {"label": "Expense", "data": ANNUAL["expense"], "color": PINK},
            {"label": "Profit", "data": ANNUAL["profit"], "color": GOLD},
        ])
        chart_card(fig, "Revenue / Expense / Profit by Year (Thousand Baht)")
    with c2:
        fig = go.Figure(go.Scatter(x=ANNUAL["labels"], y=ANNUAL["margin"], mode="lines+markers",
                                    line=dict(color=PINK, width=3, shape="spline"),
                                    fill="tozeroy", fillcolor="rgba(229,143,196,0.3)",
                                    marker=dict(size=8, color=PINK)))
        fig.update_layout(**BASE_LAYOUT, showlegend=False)
        fig.update_yaxes(ticksuffix="%", gridcolor=BORDER)
        chart_card(fig, "Profit Margin % by Year")
        note("Note: 2025's Profit Margin (53.8% cumulative) was affected by a one-time expense item in December 2025, which pulled that month's margin down to 17.7%. This chart shows full years 2023–2025 only; 2026 data (Jan–Jun) is still a partial year — see the H1 comparison table below.")

    section_title("Full-Year Comparison (2023–2025)")
    def row2(label, arr, unit, decimals=0):
        yoy = pct_change(arr[2], arr[1])
        f = fmt1 if decimals == 1 else fmt
        color = GOOD if yoy >= 0 else BAD
        return [label, f(arr[0]) + unit, f(arr[1]) + unit, f(arr[2]) + unit,
                f'<span style="color:{color}">{"+" if yoy>=0 else ""}{yoy:.1f}%</span>']
    rows = [
        row2("Revenue (Thousand Baht)", ANNUAL["revenue"], ""),
        row2("Expense (Thousand Baht)", ANNUAL["expense"], ""),
        row2("Profit (Thousand Baht)", ANNUAL["profit"], ""),
        row2("Profit Margin", ANNUAL["margin"], "%", 1),
        row2("Total Weight (Tons)", ANNUAL["tonnage"], ""),
        row2("Market Share", ANNUAL["marketShare"], "%", 1),
    ]
    data_table(["Metric", "2023", "2024", "2025", "YoY 25/24"], rows, "tblAnnualSummary")
    df_download_button(pd.DataFrame({"Metric": ["Revenue", "Expense", "Profit", "Margin %", "Weight (Tons)", "Market Share %"],
                                      "2023": [ANNUAL["revenue"][0], ANNUAL["expense"][0], ANNUAL["profit"][0], ANNUAL["margin"][0], ANNUAL["tonnage"][0], ANNUAL["marketShare"][0]],
                                      "2024": [ANNUAL["revenue"][1], ANNUAL["expense"][1], ANNUAL["profit"][1], ANNUAL["margin"][1], ANNUAL["tonnage"][1], ANNUAL["marketShare"][1]],
                                      "2025": [ANNUAL["revenue"][2], ANNUAL["expense"][2], ANNUAL["profit"][2], ANNUAL["margin"][2], ANNUAL["tonnage"][2], ANNUAL["marketShare"][2]]}),
                        "Annual_Summary.csv", key="dl_annual")

    section_title("First-Half (H1: Jan–Jun) Comparison: 2025 vs 2026")
    def sum6(arr):
        return sum(arr[:6])
    h1_2025 = {"revenue": sum6(DATA["y2025"]["revenue"]), "expense": sum6(DATA["y2025"]["expense"]),
               "profit": sum6(DATA["y2025"]["profit"]), "weight": sum6(DATA["y2025"]["weight"])}
    h1_2026 = {"revenue": sum6(DATA["y2026"]["revenue"]), "expense": sum6(DATA["y2026"]["expense"]),
               "profit": sum6(DATA["y2026"]["profit"]), "weight": sum6(DATA["y2026"]["weight"])}
    h1_margin_2025 = h1_2025["profit"] / h1_2025["revenue"] * 100
    h1_margin_2026 = h1_2026["profit"] / h1_2026["revenue"] * 100
    def h1row(label, v25, v26, unit, decimals=0):
        yoy = pct_change(v26, v25)
        f = fmt1 if decimals == 1 else fmt
        color = GOOD if yoy >= 0 else BAD
        return [label, f(v25) + unit, f(v26) + unit, f'<span style="color:{color}">{"+" if yoy>=0 else ""}{yoy:.1f}%</span>']
    h1_rows = [
        h1row("Revenue (Thousand Baht)", h1_2025["revenue"], h1_2026["revenue"], ""),
        h1row("Expense (Thousand Baht)", h1_2025["expense"], h1_2026["expense"], ""),
        h1row("Profit (Thousand Baht)", h1_2025["profit"], h1_2026["profit"], ""),
        h1row("Profit Margin", h1_margin_2025, h1_margin_2026, "%", 1),
        h1row("Total Weight (Tons)", round(h1_2025["weight"] / 1000), round(h1_2026["weight"] / 1000), ""),
    ]
    data_table(["Metric (Jan-Jun)", "2025 (H1)", "2026 (H1)", "YoY"], h1_rows, "tblH1Summary")

# ------------------------------------------------------------------
# TAB 2 — ASSUMPTION
# ------------------------------------------------------------------
with tabs[1]:
    locked = st.session_state.assumption_locked
    status_col, btn_col = st.columns([3, 1])
    with status_col:
        status_txt = "🔒 Assumptions locked — click Edit to change them." if locked else "✎ Editing is unlocked — set your growth & operational assumptions below."
        st.markdown(f'<div style="font-size:13px;font-weight:600;color:{"#1E8E5A" if locked else TEXT_SUB};padding-top:8px;">{status_txt}</div>', unsafe_allow_html=True)
    with btn_col:
        if locked:
            if st.button("✎ Edit", key="btn_edit_assumption"):
                st.session_state.assumption_locked = False
                st.rerun()
        else:
            if st.button("💾 Save & Lock", key="btn_save_assumption"):
                st.session_state.assumption_locked = True
                st.rerun()

    disabled = locked

    section_title("Growth Assumptions")
    g1, g2, g3 = st.columns(3)
    with g1:
        st.session_state.rev_growth = st.number_input("Revenue per Kg Growth (%/mo)", value=float(st.session_state.rev_growth), step=0.1, disabled=disabled, key="in_rev_growth")
    with g2:
        st.session_state.exp_growth = st.number_input("Cost per Kg Growth (%/mo)", value=float(st.session_state.exp_growth), step=0.1, disabled=disabled, key="in_exp_growth")
    with g3:
        st.session_state.weight_growth = st.number_input("Weight Growth (%/mo)", value=float(st.session_state.weight_growth), step=0.1, disabled=disabled, key="in_weight_growth")
    note("Default values = the mean month-to-month growth rate calculated from 2026's actual data. Revenue/Expense Growth apply to the <b>per-Kg rate</b> (pricing/cost inflation) — the volume effect already lives in Weight Growth / the Monthly Weight entries below, to avoid double counting.")

    section_title("Operational Data (CRI Inputs)")
    st.caption("Single current-value snapshot — leave a box blank to keep using the Tier-1 (judgment-call) estimate.")
    oc1, oc2, oc3, oc4 = st.columns(4)
    ops_cols = [oc1, oc2, oc3, oc4]
    ops_fields = [{"key": "fteCount", "label": "FTE Count"}] + \
                 [{"key": t["key"], "label": t["label"]} for t in EQUIPMENT_TYPES] + \
                 [{"key": "shipmentAwb", "label": "Shipment/AWB"}, {"key": "peakDayTons", "label": "Peak Day (Tons)"}]
    for i, f in enumerate(ops_fields):
        with ops_cols[i % 4]:
            cur = st.session_state.ops_input.get(f["key"])
            val = st.number_input(f["label"], value=float(cur) if cur is not None else None,
                                   step=1.0, disabled=disabled, key=f"opsinput_{f['key']}",
                                   format="%.0f")
            st.session_state.ops_input[f["key"]] = val

    section_title("Special Cargo % (context only — not yet fed into CRI)")
    sc_cols = st.columns(5)
    for i, f in enumerate(SPECIAL_CARGO_FIELDS):
        with sc_cols[i]:
            cur = st.session_state.ops_input.get(f["key"])
            val = st.number_input(f["label"], value=float(cur) if cur is not None else None,
                                   step=0.1, min_value=0.0, max_value=100.0, disabled=disabled, key=f"cargo_{f['key']}")
            st.session_state.ops_input[f["key"]] = val

    section_title("Equipment Fleet Size (Number of Units)")
    fl_cols = st.columns(5)
    for i, f in enumerate(EQUIPMENT_FLEET_FIELDS):
        with fl_cols[i]:
            cur = st.session_state.equipment_units.get(f["unitKey"])
            val = st.number_input(f["label"], value=float(cur) if cur is not None else 0.0, step=1.0,
                                   min_value=0.0, disabled=disabled, key=f"fleet_{f['unitKey']}")
            st.session_state.equipment_units[f["unitKey"]] = val

    section_title("Monthly Weight (Tons) — Future Months")
    last_m = find_last_actual_month_index()
    horizon_edit = 12
    idx_range = [last_m + off for off in range(1, horizon_edit + 1)]
    month_labels = [f"{MONTHS_EN[i % 12]} {2026 + i // 12}" for i in idx_range]

    editor_rows = []
    for gidx, label in zip(idx_range, month_labels):
        row = {"Month": label, "_gidx": gidx}
        for key, flabel in OPS_WEIGHT_BREAKDOWN_FIELDS:
            row[flabel] = st.session_state.ops_weight_breakdown[key].get(gidx)
        editor_rows.append(row)
    edit_df = pd.DataFrame(editor_rows).set_index("Month")
    display_df = edit_df.drop(columns=["_gidx"])

    edited = st.data_editor(display_df, disabled=disabled, width='stretch', key="weight_editor",
                             column_config={flabel: st.column_config.NumberColumn(flabel, step=1) for _, flabel in OPS_WEIGHT_BREAKDOWN_FIELDS})

    # write back into session state + recompute OPS_WEIGHT_TONS totals
    for gidx, label in zip(idx_range, month_labels):
        total = 0
        any_val = False
        for key, flabel in OPS_WEIGHT_BREAKDOWN_FIELDS:
            v = edited.loc[label, flabel] if label in edited.index else None
            v = None if pd.isna(v) else float(v)
            st.session_state.ops_weight_breakdown[key][gidx] = v
            if v is not None:
                total += v
                any_val = True
        st.session_state.ops_weight_tons[gidx] = total if any_val else None

    note("● Enter TG (Thai Airways) and OA (Other Airlines) weight in Tons, split by Import / Export / Transit, for whichever future months you want to forecast directly. Months left blank are extrapolated using the Weight Growth % assumption above, from the nearest earlier known month. Feeds the Forecast Result tab's 'Monthly Weight by Activity' chart and the Excel export.")

# ------------------------------------------------------------------
# TAB 3 — FORECAST RESULT
# ------------------------------------------------------------------
with tabs[2]:
    hc1, hc2 = st.columns([3, 1])
    with hc2:
        horizon = st.select_slider("Forecast horizon (months)", options=[3, 6, 9, 12], value=st.session_state.horizon, key="horizon_slider")
        st.session_state.horizon = horizon

    computed = compute_forecast_rows(horizon, st.session_state.rev_growth, st.session_state.exp_growth, st.session_state.weight_growth)

    if not computed:
        st.info("No actual 2026 data found to forecast from.")
    else:
        rows, base, rev_g, exp_g = computed["rows"], computed["base"], computed["revG"], computed["expG"]

        section_title("Capacity Readiness Index (CRI) — Which Resource Runs Out First?")
        last_row = rows[-1]
        base_row_cri = {"laborUtilPct": base["laborUtilPct"], "equipmentUtilPct": base["equipmentUtilPct"],
                         "spaceUtilPct": base["spaceUtilPct"], "capacity": base["capacity"]}
        base_cri, base_bottleneck = compute_cri(base_row_cri)

        def cri_card(label, projected, current, extra_sub=None):
            c = cri_color(projected)
            sub = f'Current: {fmt1(current)+"%" if current is not None else "—"} → Projected: {fmt1(projected)+"%" if projected is not None else "—"}'
            if extra_sub:
                sub += f' · {extra_sub}'
            return (f'<div class="kpi-card" style="border-top-color:{c["hex"]};">'
                    f'<div class="kpi-label">{label}</div>'
                    f'<div class="kpi-value" style="color:{c["hex"]};">{fmt1(projected)+"%" if projected is not None else "—"}</div>'
                    f'<div class="kpi-sub">{c["label"]}</div><div class="kpi-sub">{sub}</div></div>')

        cri_cards = [
            cri_card("Capacity Readiness Index (CRI)", last_row["cri"], base_cri, f'Bottleneck: {last_row["bottleneck"]}'),
            cri_card("Labor Utilization", last_row["laborUtilPct"], base["laborUtilPct"]),
            cri_card("Equipment Utilization", last_row["equipmentUtilPct"], base["equipmentUtilPct"]),
            cri_card("Space (ASRS) Utilization", last_row["spaceUtilPct"], base["spaceUtilPct"]),
            cri_card("Tonnage/Warehouse Utilization", last_row["capacity"], base["capacity"]),
        ]
        kpi_row(cri_cards)

        c1, c2 = st.columns(2)
        with c1:
            items = resource_items(base_row_cri)
            fig = bar_chart([it[0] for it in items], [{"label": "Current Utilization %", "data": [it[1] for it in items], "color": PURPLE}], horizontal=True, y_suffix="%")
            fig.update_traces(marker_color=[cri_color(it[1])["hex"] for it in items])
            fig.update_xaxes(range=[0, 120])
            chart_card(fig, "Current Utilization by Resource (Last Actual Month)")
        with c2:
            hist_labels, hist_labor, hist_equip, hist_space, hist_tonnage = [], [], [], [], []
            for m in range(base["m"] + 1):
                hist_labels.append(f'{MONTHS_EN[m]} {base["year"]}')
                hist_labor.append(get_labor_util_for_month(m))
                hist_equip.append(get_equipment_util_for_month(m)["util"])
                hist_space.append(DATA["y2026"]["spaceUtilPct"][m])
                hist_tonnage.append(DATA["y2026"]["capacity"][m])
            fore_labels = [f'{r["month"]} {r["year"]}' for r in rows]
            labels = hist_labels + fore_labels

            def series_pair(hist_arr, fore_arr):
                actual = hist_arr + null_array(len(fore_arr))
                forecast = null_array(len(hist_arr) - 1) + [hist_arr[-1]] + fore_arr
                return actual, forecast

            labor_a, labor_f = series_pair(hist_labor, [r["laborUtilPct"] for r in rows])
            equip_a, equip_f = series_pair(hist_equip, [r["equipmentUtilPct"] for r in rows])
            space_a, space_f = series_pair(hist_space, [r["spaceUtilPct"] for r in rows])
            tonnage_a, tonnage_f = series_pair(hist_tonnage, [r["capacity"] for r in rows])

            fig = line_chart(labels, [
                {"label": "Labor (Actual)", "data": labor_a, "color": PURPLE, "point_radius": 3},
                {"label": "Labor (Forecast)", "data": labor_f, "color": PURPLE, "dash": "dash", "point_radius": 3},
                {"label": "Equipment (Actual)", "data": equip_a, "color": PINK, "point_radius": 3},
                {"label": "Equipment (Forecast)", "data": equip_f, "color": PINK, "dash": "dash", "point_radius": 3},
                {"label": "Space/ASRS (Actual)", "data": space_a, "color": PURPLE_LIGHT, "point_radius": 3},
                {"label": "Space/ASRS (Forecast)", "data": space_f, "color": PURPLE_LIGHT, "dash": "dash", "point_radius": 3},
                {"label": "Tonnage (Actual)", "data": tonnage_a, "color": PINK_LIGHT, "point_radius": 3},
                {"label": "Tonnage (Forecast)", "data": tonnage_f, "color": PINK_LIGHT, "dash": "dash", "point_radius": 3},
                {"label": "70% Threshold", "data": [70] * len(labels), "color": GREY, "dash": "dot", "point_radius": 0, "width": 1},
                {"label": "90% Threshold", "data": [90] * len(labels), "color": BAD, "dash": "dot", "point_radius": 0, "width": 1},
            ], y_suffix="%", y_range=[0, 120])
            chart_card(fig, "Resource Utilization Forecast (%)")
        note("Labor/Equipment/Space utilization are projected forward by scaling with the Weight Growth assumption (set on the Assumption tab) — treat these as directional, not precise. Dashed grey/red lines mark the 70%/90% thresholds.")

        # ---- forecast KPI row ----
        cum_rev = sum(r["revenue"] for r in rows)
        cum_exp = sum(r["expense"] for r in rows)
        cum_profit = cum_rev - cum_exp
        cum_weight_ton = round(sum(r["weight"] for r in rows) / 1000)
        ref = get_same_period_last_year(rows)

        fc_cards = [
            kpi_card(f"Projected Revenue (Next {len(rows)}M)", f"{fmt(cum_rev)} TTHB", cls="gold",
                      extra_html=gap_vs_last_year_html(cum_rev, ref["revenue"] if ref else None, " TTHB")),
            kpi_card(f"Projected Expense (Next {len(rows)}M)", f"{fmt(cum_exp)} TTHB", cls="pink",
                      extra_html=gap_vs_last_year_html(cum_exp, ref["expense"] if ref else None, " TTHB", invert=True)),
            kpi_card(f"Projected Profit (Next {len(rows)}M)", f"{fmt(cum_profit)} TTHB", cls="purple",
                      extra_html=gap_vs_last_year_html(cum_profit, ref["profit"] if ref else None, " TTHB")),
            kpi_card("Projected Margin (End of Period)", f"{fmt1(last_row['margin'])}%", cls="gold",
                      extra_html=gap_vs_last_year_html(last_row["margin"], ref["lastMonthMargin"] if ref else None, " pts", decimals=1, no_pct=True)),
            kpi_card("Projected Cost/Kg (End of Period)", f"{fmt2(last_row['costPerKg'])} THB/Kg", cls="pink"),
            kpi_card("Projected Revenue/Kg (End of Period)", f"{fmt2(last_row['revPerKg'])} THB/Kg", cls="purple"),
            kpi_card(f"Projected Weight (Next {len(rows)}M, Tons)", fmt(cum_weight_ton), cls="purple",
                      extra_html=gap_vs_last_year_html(cum_weight_ton, ref["weightTon"] if ref else None, " Tons")),
            kpi_card("Projected Capacity Util. (End of Period)", f"{fmt1(last_row['capacity'])}%", cls="pink"),
        ]
        kpi_row(fc_cards)

        section_title("Financial Forecast — Revenue / Expense / Profit (Thousand Baht)")
        hist_labels2 = [f'{MONTHS_EN[m]} {base["year"]}' for m in range(base["m"] + 1)]
        hist_rev = DATA["y2026"]["revenue"][:base["m"] + 1]
        hist_exp = DATA["y2026"]["expense"][:base["m"] + 1]
        hist_profit = DATA["y2026"]["profit"][:base["m"] + 1]
        fore_rev = [r["revenue"] for r in rows]
        fore_exp = [r["expense"] for r in rows]
        fore_profit = [r["profit"] for r in rows]
        all_labels_fin = hist_labels2 + fore_labels
        rev_a, rev_f = series_pair(hist_rev, fore_rev)
        exp_a, exp_f = series_pair(hist_exp, fore_exp)
        profit_a, profit_f = series_pair(hist_profit, fore_profit)
        fig = line_chart(all_labels_fin, [
            {"label": "Revenue (Actual)", "data": rev_a, "color": PURPLE, "point_radius": 3},
            {"label": "Revenue (Forecast)", "data": rev_f, "color": PURPLE, "dash": "dash", "point_radius": 3},
            {"label": "Expense (Actual)", "data": exp_a, "color": PINK, "point_radius": 3},
            {"label": "Expense (Forecast)", "data": exp_f, "color": PINK, "dash": "dash", "point_radius": 3},
            {"label": "Profit (Actual)", "data": profit_a, "color": GOLD, "point_radius": 3},
            {"label": "Profit (Forecast)", "data": profit_f, "color": GOLD, "dash": "dash", "point_radius": 3},
        ])
        chart_card(fig, height=340)
        note("Solid lines = actual 2026 data. Dashed lines = forecast, computed as Weight × Revenue/Kg and Weight × Cost/Kg using the assumptions set on the Assumption tab.")

        section_title("Profit Margin Forecast")
        hist_margin = DATA["y2026"]["margin"][:base["m"] + 1]
        fore_margin = [r["margin"] for r in rows]
        margin_a, margin_f = series_pair(hist_margin, fore_margin)
        fig = line_chart(all_labels_fin, [
            {"label": "Margin (Actual)", "data": margin_a, "color": PINK, "point_radius": 3},
            {"label": "Margin (Forecast)", "data": margin_f, "color": PINK, "dash": "dash", "point_radius": 3},
        ], y_suffix="%")
        chart_card(fig)

        section_title("Unit Cost Forecast (THB/Kg)")
        hist_costkg = DATA["y2026"]["costPerKg"][:base["m"] + 1]
        fore_costkg = [r["costPerKg"] for r in rows]
        costkg_a, costkg_f = series_pair(hist_costkg, fore_costkg)
        fig = line_chart(all_labels_fin, [
            {"label": "Cost/Kg (Actual)", "data": costkg_a, "color": PINK, "point_radius": 3},
            {"label": "Cost/Kg (Forecast)", "data": costkg_f, "color": PINK, "dash": "dash", "point_radius": 3},
        ])
        chart_card(fig)

        section_title("Operational Performance Forecast")
        oc1, oc2 = st.columns(2)
        with oc1:
            hist_weight_ton = [w / 1000 if w is not None else None for w in DATA["y2026"]["weight"][:base["m"] + 1]]
            fore_weight_ton = [r["weight"] / 1000 for r in rows]
            wt_a, wt_f = series_pair(hist_weight_ton, fore_weight_ton)
            fig = line_chart(all_labels_fin, [
                {"label": "Weight (Actual)", "data": wt_a, "color": PURPLE, "point_radius": 3},
                {"label": "Weight (Forecast)", "data": wt_f, "color": PURPLE, "dash": "dash", "point_radius": 3},
            ], y_title="Tons")
            chart_card(fig, "Weight (Tons)")
        with oc2:
            hist_cap = DATA["y2026"]["capacity"][:base["m"] + 1]
            fore_cap = [r["capacity"] for r in rows]
            cap_a, cap_f = series_pair(hist_cap, fore_cap)
            fig = line_chart(all_labels_fin, [
                {"label": "Capacity (Actual)", "data": cap_a, "color": PINK, "point_radius": 3},
                {"label": "Capacity (Forecast)", "data": cap_f, "color": PINK, "dash": "dash", "point_radius": 3},
                {"label": "Max Capacity", "data": [100] * len(all_labels_fin), "color": BAD, "dash": "dot", "point_radius": 0},
            ], y_suffix="%")
            chart_card(fig, "Capacity Utilization (%) vs Max Capacity")

        section_title("Monthly Weight by Activity — Import / Export / Transit (Tons)")
        idx_range_cm = list(range(base["m"] + 1, base["m"] + 1 + 12))
        cm_labels, cm_imp, cm_exp, cm_tra = [], [], [], []
        for gidx in idx_range_cm:
            cm_labels.append(f'{MONTHS_EN[gidx % 12]} {2026 + gidx // 12}')
            tg_i = st.session_state.ops_weight_breakdown["tgImport"].get(gidx)
            oa_i = st.session_state.ops_weight_breakdown["oaImport"].get(gidx)
            tg_e = st.session_state.ops_weight_breakdown["tgExport"].get(gidx)
            oa_e = st.session_state.ops_weight_breakdown["oaExport"].get(gidx)
            tg_t = st.session_state.ops_weight_breakdown["tgTransit"].get(gidx)
            oa_t = st.session_state.ops_weight_breakdown["oaTransit"].get(gidx)
            cm_imp.append(None if tg_i is None and oa_i is None else (tg_i or 0) + (oa_i or 0))
            cm_exp.append(None if tg_e is None and oa_e is None else (tg_e or 0) + (oa_e or 0))
            cm_tra.append(None if tg_t is None and oa_t is None else (tg_t or 0) + (oa_t or 0))
        fig = bar_chart(cm_labels, [
            {"label": "Import", "data": cm_imp, "color": PINK},
            {"label": "Export", "data": cm_exp, "color": PURPLE},
            {"label": "Transit", "data": cm_tra, "color": GOLD},
        ], stacked=True, y_title="Tons")
        chart_card(fig)
        note("Built from the TG (Import) / TG (Export) / TG (Transit) / OA (Import) / OA (Export) / OA (Transit) entries made per month on the Assumption tab (TG + OA combined per activity), for whichever future months have been filled in.")

        section_title("Strategic Insights & Action Plan")
        render_forecast_insights(rows, base, rev_g, exp_g)

        section_title("Forecast Detail Table")
        note('<span style="color:#1E8E5A;">●</span> = Weight entered directly on the Assumption tab for that month &nbsp;&nbsp; <span style="color:#6B6480;">○</span> = Weight extrapolated via Weight Growth % from the nearest earlier known month.')
        table_rows = []
        for r in rows:
            marker = '<span style="color:#1E8E5A;">●</span>' if r["weightIsManual"] else '<span style="color:#6B6480;">○</span>'
            month_label = f'{r["month"]} {r["year"]} {marker}'
            table_rows.append([
                month_label, fmt(r["revenue"]), fmt(r["expense"]), fmt(r["profit"]), f'{fmt1(r["margin"])}%',
                fmt(r["weight"] / 1000), fmt2(r["costPerKg"]), fmt2(r["revPerKg"]), f'{fmt1(r["capacity"])}%',
                f'{fmt1(r["laborUtilPct"])}%', f'{fmt1(r["equipmentUtilPct"])}%', f'{fmt1(r["spaceUtilPct"])}%',
                f'<span style="font-weight:800;color:{cri_color(r["cri"])["hex"]};">{fmt1(r["cri"])}%</span>', r["bottleneck"],
            ])
        data_table(["Month", "Revenue", "Expense", "Profit", "Margin%", "Weight (Tons)", "Cost/Kg", "Revenue/Kg",
                    "Capacity%", "Labor%", "Equipment%", "Space%", "CRI%", "Bottleneck"], table_rows, "tblForecast")

# ------------------------------------------------------------------
# TAB 4 — MONTHLY TREND
# ------------------------------------------------------------------
with tabs[3]:
    st.markdown("**Select Years to Display:**")
    yc1, yc2, yc3, yc4 = st.columns(4)
    for col, y in zip([yc1, yc2, yc3, yc4], ["2023", "2024", "2025", "2026"]):
        with col:
            st.session_state.trend_years[y] = st.checkbox(y, value=st.session_state.trend_years[y], key=f"trendyear_{y}")

    section_title("Monthly Revenue Trend (Thousand Baht)")
    series = []
    year_colors = {"2023": GREY, "2024": PURPLE_LIGHT, "2025": PINK_LIGHT, "2026": PINK}
    for y in ["2023", "2024", "2025", "2026"]:
        if st.session_state.trend_years[y]:
            series.append({"label": y, "data": DATA["y" + y]["revenue"], "color": year_colors[y],
                            "width": 3 if y == "2026" else 2})
    fig = line_chart(MONTHS_EN, series)
    chart_card(fig)

    section_title("Revenue vs Expense vs Profit (Latest Year: 2026)")
    fig = combo_bar_line(MONTHS_EN,
                          bars=[{"label": "Revenue", "data": DATA["y2026"]["revenue"], "color": PURPLE},
                                {"label": "Expense", "data": DATA["y2026"]["expense"], "color": PINK}],
                          lines=[{"label": "Profit", "data": DATA["y2026"]["profit"], "color": GOLD}])
    chart_card(fig)

    section_title("Monthly Profit Margin %")
    fig = line_chart(MONTHS_EN, [
        {"label": "2023", "data": DATA["y2023"]["margin"], "color": GREY},
        {"label": "2024", "data": DATA["y2024"]["margin"], "color": PURPLE_LIGHT},
        {"label": "2025", "data": DATA["y2025"]["margin"], "color": PINK_LIGHT},
        {"label": "2026", "data": DATA["y2026"]["margin"], "color": PINK, "width": 3},
    ], y_suffix="%")
    chart_card(fig)

    section_title("Monthly Data Table (Thousand Baht)")
    trend_year = st.selectbox("Year:", ["2026", "2025", "2024", "2023"], key="trend_table_year")
    d = DATA["y" + trend_year]
    rows = []
    for i in range(12):
        if d["revenue"][i] is None:
            rows.append([f"{MONTHS_EN[i]} {trend_year}", '<span style="color:#B9B3C7;" colspan="5">No data yet</span>', "", "", "", ""])
        else:
            rows.append([f"{MONTHS_EN[i]} {trend_year}", fmt(d["revenue"][i]), fmt(d["expense"][i]), fmt(d["profit"][i]),
                         f'{fmt1(d["margin"][i])}%', fmt(d["weight"][i] / 1000)])
    data_table(["Month", "Revenue", "Expense", "Profit", "Margin%", "Weight (Tons)"], rows, "tblMonthly")
    valid_rows = [i for i in range(12) if d["revenue"][i] is not None]
    df_download_button(pd.DataFrame({
        "Month": [f"{MONTHS_EN[i]} {trend_year}" for i in valid_rows],
        "Revenue": [d["revenue"][i] for i in valid_rows], "Expense": [d["expense"][i] for i in valid_rows],
        "Profit": [d["profit"][i] for i in valid_rows], "Margin%": [d["margin"][i] for i in valid_rows],
        "Weight (Tons)": [d["weight"][i] / 1000 for i in valid_rows]}), "Monthly_Data.csv", key="dl_monthly")

# ------------------------------------------------------------------
# TAB 5 — REVENUE BREAKDOWN
# ------------------------------------------------------------------
with tabs[4]:
    rev_year = st.selectbox("Year:", ["2026", "2025", "2024", "2023"], key="rev_year_select",
                             format_func=lambda y: f"{y} (H1, Jan-Jun)" if y == "2026" else y)
    r = REV_BY_TYPE["y" + rev_year]

    type_labels = ["Cargo Terminal Charges", "Cargo Services", "Cargo Storage Fees", "Delivery Order Fees", "Other Cargo Handling"]
    type_data = [r["terminalCharges"], r["cargoServices"], r["storageFees"], r["deliveryOrder"], r["otherHandling"]]
    type_colors = [PURPLE, PINK, GOLD, PURPLE_LIGHT, PINK_LIGHT]

    c1, c2 = st.columns(2)
    with c1:
        fig = doughnut_chart(type_labels, type_data, type_colors)
        chart_card(fig, "Revenue by Type (Cumulative for Selected Year)")
    with c2:
        fig = doughnut_chart(["External Revenue (Other Airlines)", "Internal Revenue (TG)"],
                              [r["totalExternal"], r["internal"]], [PURPLE, GOLD])
        chart_card(fig, "Internal (TG) vs External (Other Airlines) Revenue Share")

    section_title("Revenue by Type — Year-over-Year Trend (Cumulative, Thousand Baht)")
    yoy_labels = ["2023", "2024", "2025", "2026 (H1)"]
    fig = bar_chart(yoy_labels, [
        {"label": "Cargo Terminal Charges", "data": [REV_BY_TYPE["y2023"]["terminalCharges"], REV_BY_TYPE["y2024"]["terminalCharges"], REV_BY_TYPE["y2025"]["terminalCharges"], REV_BY_TYPE["y2026"]["terminalCharges"]], "color": PURPLE},
        {"label": "Cargo Services", "data": [REV_BY_TYPE["y2023"]["cargoServices"], REV_BY_TYPE["y2024"]["cargoServices"], REV_BY_TYPE["y2025"]["cargoServices"], REV_BY_TYPE["y2026"]["cargoServices"]], "color": PINK},
        {"label": "Cargo Storage Fees", "data": [REV_BY_TYPE["y2023"]["storageFees"], REV_BY_TYPE["y2024"]["storageFees"], REV_BY_TYPE["y2025"]["storageFees"], REV_BY_TYPE["y2026"]["storageFees"]], "color": GOLD},
        {"label": "Delivery Order Fees", "data": [REV_BY_TYPE["y2023"]["deliveryOrder"], REV_BY_TYPE["y2024"]["deliveryOrder"], REV_BY_TYPE["y2025"]["deliveryOrder"], REV_BY_TYPE["y2026"]["deliveryOrder"]], "color": PURPLE_LIGHT},
        {"label": "Other Cargo Handling", "data": [REV_BY_TYPE["y2023"]["otherHandling"], REV_BY_TYPE["y2024"]["otherHandling"], REV_BY_TYPE["y2025"]["otherHandling"], REV_BY_TYPE["y2026"]["otherHandling"]], "color": PINK_LIGHT},
    ], stacked=True)
    chart_card(fig)
    note('Note: the "2026 (H1)" bar reflects only the first 6 months (Jan–Jun) of cumulative data, so it is naturally smaller than a full year and should not be compared directly in scale with the other years.')

    section_title("Revenue by Type Table (Thousand Baht)")
    item_defs = [["Cargo Terminal Charges", "terminalCharges"], ["Cargo Services", "cargoServices"],
                 ["Cargo Storage Fees", "storageFees"], ["Delivery Order Fees", "deliveryOrder"],
                 ["Other Cargo Handling", "otherHandling"], ["Internal Revenue (TG)", "internal"]]
    rows = []
    for label, key in item_defs:
        pct = r[key] / r["total"] * 100
        rows.append([label, fmt(REV_BY_TYPE["y2023"][key]), fmt(REV_BY_TYPE["y2024"][key]), fmt(REV_BY_TYPE["y2025"][key]), fmt(REV_BY_TYPE["y2026"][key]), f"{pct:.1f}%"])
    rows.append([f'<b>Total Revenue</b>', f'<b>{fmt(REV_BY_TYPE["y2023"]["total"])}</b>', f'<b>{fmt(REV_BY_TYPE["y2024"]["total"])}</b>',
                 f'<b>{fmt(REV_BY_TYPE["y2025"]["total"])}</b>', f'<b>{fmt(REV_BY_TYPE["y2026"]["total"])}</b>', '<b>100%</b>'])
    data_table(["Revenue Type", "2023", "2024", "2025", "2026 (H1)", "Share of Selected Year"], rows, "tblRevByType")

# ------------------------------------------------------------------
# TAB 6 — UNIT ECONOMICS
# ------------------------------------------------------------------
with tabs[5]:
    latest_rev_kg, latest_cost_kg = DATA["y2026"]["revPerKg"][5], DATA["y2026"]["costPerKg"][5]
    cards = [
        kpi_card("Latest Revenue per Kg (Jun 2026)", f"{fmt2(latest_rev_kg)} THB/Kg", cls="purple"),
        kpi_card("Latest Cost per Kg (Jun 2026)", f"{fmt2(latest_cost_kg)} THB/Kg", cls="pink"),
        kpi_card("Latest Spread per Kg", f"{fmt2(latest_rev_kg - latest_cost_kg)} THB/Kg", cls="gold"),
        kpi_card("Revenue/Kg — 2026 YTD Average (H1)", f'{fmt2(avg(DATA["y2026"]["revPerKg"]))} THB/Kg', cls="purple"),
        kpi_card("Cost/Kg — 2026 YTD Average (Jun)", f'{fmt2(avg(DATA["y2026"]["costPerKg"]))} THB/Kg', cls="pink"),
    ]
    kpi_row(cards)

    section_title("Unit Pricing (THB/Kg) — Revenue vs Cost")
    c1, c2 = st.columns(2)
    with c1:
        fig = line_chart(MONTHS_EN, [
            {"label": "2023", "data": DATA["y2023"]["revPerKg"], "color": GREY},
            {"label": "2024", "data": DATA["y2024"]["revPerKg"], "color": PURPLE_LIGHT},
            {"label": "2025", "data": DATA["y2025"]["revPerKg"], "color": PINK_LIGHT},
            {"label": "2026", "data": DATA["y2026"]["revPerKg"], "color": PURPLE, "width": 3},
        ])
        chart_card(fig, "DX Revenue per Kilo (THB/Kg) — Monthly")
    with c2:
        fig = line_chart(MONTHS_EN, [
            {"label": "2023", "data": DATA["y2023"]["costPerKg"], "color": GREY},
            {"label": "2024", "data": DATA["y2024"]["costPerKg"], "color": PURPLE_LIGHT},
            {"label": "2025", "data": DATA["y2025"]["costPerKg"], "color": PINK_LIGHT},
            {"label": "2026", "data": DATA["y2026"]["costPerKg"], "color": PINK, "width": 3},
        ])
        chart_card(fig, "DX Cost per Kilo (THB/Kg) — Monthly")

    section_title("Unit Price Spread (per Kilogram)")
    spread2026 = [None if v is None else v - DATA["y2026"]["costPerKg"][i] for i, v in enumerate(DATA["y2026"]["revPerKg"])]
    spread2025 = [v - DATA["y2025"]["costPerKg"][i] for i, v in enumerate(DATA["y2025"]["revPerKg"])]
    fig = bar_chart(MONTHS_EN, [
        {"label": "Spread 2025", "data": spread2025, "color": PINK_LIGHT},
        {"label": "Spread 2026", "data": spread2026, "color": GOLD},
    ])
    chart_card(fig)
    note("Spread = Revenue per Kilo − Cost per Kilo (a higher value means better unit-level profitability per kilogram of weight handled). Unit: THB/Kg")

    section_title("Monthly Unit Pricing Table (THB/Kg)")
    rows = []
    for i in range(12):
        rows.append([MONTHS_EN[i], fmt2(DATA["y2025"]["revPerKg"][i]), fmt2(DATA["y2025"]["costPerKg"][i]),
                     fmt2(DATA["y2026"]["revPerKg"][i]), fmt2(DATA["y2026"]["costPerKg"][i])])
    data_table(["Month", "Revenue/Kg 2025", "Cost/Kg 2025", "Revenue/Kg 2026", "Cost/Kg 2026"], rows, "tblUnitEcon")

# ------------------------------------------------------------------
# TAB 7 — WEIGHT
# ------------------------------------------------------------------
with tabs[6]:
    def find_last_actual_index(arr):
        last = -1
        for i, v in enumerate(arr):
            if v is not None:
                last = i
        return last

    def latest_weight_type_month():
        for y in ["2026", "2025", "2024", "2023"]:
            d = WEIGHT_BY_TYPE["y" + y]
            last_m = find_last_actual_index(d["import"])
            if last_m >= 0:
                return y, last_m
        return "2023", 0

    ly, lm = latest_weight_type_month()
    ld = WEIGHT_BY_TYPE["y" + ly]
    l_imp, l_exp, l_tra = ld["import"][lm], ld["export"][lm], ld["transit"][lm]
    l_total = l_imp + l_exp + l_tra
    l_total_official = DATA["y" + ly]["weight"][lm]

    cards = [
        kpi_card("Latest Month", f"{MONTHS_EN[lm]} {ly}", cls="purple"),
        kpi_card("Export Weight (Kg)", fmt(l_exp), cls="pink"),
        kpi_card("Import Weight (Kg)", fmt(l_imp), cls="gold"),
        kpi_card("Transit Weight (Kg)", fmt(l_tra), cls="purple"),
        kpi_card("Total Weight (Kg)", fmt(l_total_official if l_total_official is not None else l_total), cls="pink"),
    ]
    kpi_row(cards)

    section_title("Total Cargo Weight (Kgs) — Monthly")
    fig = line_chart(MONTHS_EN, [
        {"label": "2023", "data": [v / 1_000_000 for v in DATA["y2023"]["weight"]], "color": GREY},
        {"label": "2024", "data": [v / 1_000_000 for v in DATA["y2024"]["weight"]], "color": PURPLE_LIGHT},
        {"label": "2025", "data": [v / 1_000_000 for v in DATA["y2025"]["weight"]], "color": PINK_LIGHT},
        {"label": "2026", "data": [None if v is None else v / 1_000_000 for v in DATA["y2026"]["weight"]], "color": PURPLE, "width": 3},
    ], y_title="Million Kg")
    chart_card(fig, height=340)

    section_title("Cargo Weight by Activity — Import / Export / Transit (Kgs)")
    weight_year = st.radio("Year:", ["2023", "2024", "2025", "2026"], index=["2023", "2024", "2025", "2026"].index(st.session_state.weight_year), horizontal=True, key="weight_year_radio")
    st.session_state.weight_year = weight_year
    wd = WEIGHT_BY_TYPE["y" + weight_year]

    c1, c2 = st.columns(2)
    with c1:
        fig = bar_chart(MONTHS_EN, [
            {"label": "Import", "data": wd["import"], "color": PINK},
            {"label": "Export", "data": wd["export"], "color": PURPLE},
            {"label": "Transit", "data": wd["transit"], "color": GOLD},
        ], stacked=True)
        chart_card(fig, "Monthly Split — Import / Export / Transit (Selected Year)")
    with c2:
        fig = doughnut_chart(["Import", "Export", "Transit"], [l_imp, l_exp, l_tra], [PINK, PURPLE, GOLD],
                              title=f"{MONTHS_EN[lm]} {ly}")
        chart_card(fig, "Composition — Latest Reported Month")
    note('Import / Export / Transit weight is taken directly from the "Weight : Kilo" breakdown on each month\'s Handling Productivity and Revenue Report. Export here is the full outbound total (scheduled Passenger + Freighter service plus Charter combined) — the source reports do not separately meter Charter vs scheduled flights.')

    section_title("Import / Export / Transit — Monthly Detail (All Years)")
    rows = []
    for y in ["2023", "2024", "2025", "2026"]:
        d = WEIGHT_BY_TYPE["y" + y]
        rows.append([f'<b>{y}</b>', "", "", "", ""])
        for m in range(12):
            if d["import"][m] is None:
                continue
            total = d["import"][m] + d["export"][m] + d["transit"][m]
            rows.append([f"{MONTHS_EN[m]} {y}", fmt(d["import"][m]), fmt(d["export"][m]), fmt(d["transit"][m]), fmt(total)])
    data_table(["Month", "Import (Kg)", "Export (Kg)", "Transit (Kg)", "Total (Kg)"], rows, "tblWeightByType")

    st.markdown("""
    <div class="info-box">
      <b>Want Export split further into Passenger+Freighter vs Charter flights?</b> That level of detail (flight-type share of export weight) isn't published in the source monthly PDF reports and isn't captured by this dashboard's manual-entry tools either — the <b>Assumption</b> tab's <i>"Monthly Weight (Tons)"</i> section only splits by carrier group (TG / Other Airlines) and activity (Import / Export / Transit), not by flight type within Export.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# TAB 8 — OPERATIONS & HR
# ------------------------------------------------------------------
with tabs[7]:
    c1, c2 = st.columns(2)
    with c1:
        fig = line_chart(MONTHS_EN, [
            {"label": "2024", "data": DATA["y2024"]["capacity"], "color": PURPLE_LIGHT},
            {"label": "2025", "data": DATA["y2025"]["capacity"], "color": PINK_LIGHT},
            {"label": "2026", "data": DATA["y2026"]["capacity"], "color": PINK, "width": 3},
            {"label": "Max Capacity", "data": [100] * 12, "color": BAD, "dash": "dash", "point_radius": 0},
        ], y_suffix="%", y_range=[0, 110])
        chart_card(fig, "Capacity Utilization (%) vs Max Capacity 90,000 Tons/Month")
    with c2:
        fig = bar_chart(MARKET_SHARE_TREND["labels"], [
            {"label": "THAI Cargo (DX)", "data": MARKET_SHARE_TREND["thaiCargo"], "color": PURPLE},
            {"label": "BFS", "data": MARKET_SHARE_TREND["bfs"], "color": PINK},
            {"label": "Other", "data": MARKET_SHARE_TREND["other"], "color": GREY},
        ], stacked=True, y_suffix="%")
        chart_card(fig, "Market Share (Weight, %) — DX vs BFS vs AOT Total")

    section_title("Top 10 Airlines by Revenue (Latest: June 2026)")
    rows = [[a["airline"], fmt(a["freq"]), fmt(a["revenue"]), f'{a["weightProp"]}%'] for a in TOP_AIRLINES]
    data_table(["Airline", "Flights", "Revenue (Million Baht)", "Weight Share"], rows, "tblTopAirlines")

    section_title("Human Resources")
    c1, c2 = st.columns(2)
    with c1:
        fig = bar_chart(STAFF["labels"], [
            {"label": "Permanent Staff", "data": STAFF["permanent"], "color": PURPLE},
            {"label": "Outsource / Out Job", "data": STAFF["outsource"], "color": GOLD},
        ])
        chart_card(fig, "Permanent Staff vs Outsource/Out Job")
    with c2:
        with st.container(border=True):
            st.markdown('<div class="chart-card-title">Latest Summary (June 2026)</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="stat-mini"><span>Permanent Staff</span><b>511</b></div>
            <div class="stat-mini"><span>Outsource / Out Job</span><b>1,479</b></div>
            <div class="stat-mini"><span>Average Age</span><b>49.3 years</b></div>
            <div class="stat-mini"><span>Gender Ratio, Male : Female (Jun 2026)</span><b>80% : 20%</b></div>
            <div class="stat-mini"><span>Largest Job Levels</span><b>L06 (256 staff), L07 (203 staff)</b></div>
            """, unsafe_allow_html=True)
            note("Sourced from the monthly Human Resource report — useful for tracking succession planning and retirement rates.")

# ------------------------------------------------------------------
# TAB 9 — UPDATE GUIDE
# ------------------------------------------------------------------
with tabs[8]:
    section_title("Quick Update: Upload a File")
    c1, c2 = st.columns(2)
    with c1:
        up = st.file_uploader("Upload Excel (.xlsx) or CSV — updates Monthly Data on next reload", type=["xlsx", "xls", "csv"], key="upload_excel")
        if up is not None:
            try:
                if up.name.lower().endswith(".csv"):
                    df_up = pd.read_csv(up)
                else:
                    df_up = pd.read_excel(up, sheet_name=0)
                st.success(f"Read {len(df_up)} rows from **{up.name}**. Preview below — wire this into `DATA` to make it live (see note).")
                st.dataframe(df_up.head(20), width='stretch')
            except Exception as e:
                st.error(f"Could not read file: {e}")
    with c2:
        st.file_uploader("Upload PDF Report (best-effort text scan)", type=["pdf"], key="upload_pdf")
        st.caption("DX's monthly reports export key numbers as flattened chart images, not selectable text, so automatic extraction from these PDFs is not reliable — use the Excel/CSV route for dependable updates.")

    st.markdown("""
    <div class="note">
      <b>Excel/CSV:</b> use the same layout as "Export All Data (.xlsx)" in the header — sheet names <code>Monthly Data</code>, <code>Top Airlines</code>, <code>Staff &amp; Market Share</code>, <code>Weight By Type</code> are recognized. Leave Profit/Margin/Cost per Kg/Revenue per Kg blank and they're calculated automatically from Revenue, Expense, and Weight.<br><br>
      <b>PDF:</b> uploading a PDF here only lets you preview it — automatic number extraction from DX's source PDFs is not reliable (see note above); please use the Excel/CSV route for dependable updates.
    </div>
    <div class="info-box">
      <b>Key point:</b> the source PDF reports are <b>month-end closing</b> data from SAP (issued in early days of the following month), and are denominated in <b>Thousand Baht (TTHB)</b>. This dashboard is therefore most accurate when updated <b>monthly</b>.
    </div>
    """, unsafe_allow_html=True)

    section_title("Approach 1: Monthly Update (matches the current source data)")
    st.markdown("""
1. When a new *Handling Productivity and Revenue Report* and *Profit and Loss* report is issued, open `app.py` in a code editor (VS Code).
2. Find the `DATA["y2026"]` dictionary (or the matching year) near the top of the file.
3. Replace the value for that month (by array index, 0 = Jan ... 11 = Dec) with the actual figure from the report (unit = Thousand Baht, matching the P&L Report).
4. Do the same for `expense`, `profit`, `margin`, `weight`, `costPerKg`, `revPerKg`, `capacity`, `laborUtilPct`, `equipmentUtilPct`, and `spaceUtilPct` — plus, if available, the Tier-2 operational inputs on the Assumption tab.
5. Save the file, redeploy (or rerun `streamlit run app.py`) — the charts, KPIs, and Forecast Result tab will all update automatically since the forecast always starts from the latest actual month in this data.
    """)

    section_title("Using the Assumption / Forecast Result Tabs")
    st.markdown("""
The **Assumption** tab holds every input (Growth Assumptions, Operational Data / CRI Inputs, Special Cargo %, Monthly Weight by Activity). The **Forecast Result** tab holds every output (KPIs, charts, CRI, insights, forecast table) computed from those inputs. The forecast always projects forward from whatever the latest non-empty month is in `DATA["y2026"]`. Values entered on the Assumption tab persist for the session (via `st.session_state`) until changed again — switching tabs never resets them. The default Growth Assumption values shown are the mean month-to-month growth rate calculated from 2026's actual data.
    """)

    section_title("Capacity Readiness Index (CRI) — Data Maturity Levels")
    st.markdown("""
The `laborUtilPct`, `equipmentUtilPct`, and `spaceUtilPct` arrays in `DATA["y2026"]` hold **Tier-1 estimates** (an Ops/Warehouse/HR lead's monthly % judgment call). Labor and Equipment automatically upgrade to **Tier-2** whenever real inputs exist in the **"Operational Data (CRI Inputs)"** boxes on the Assumption tab:

- **Labor (Tier-2):** computed as (Weight ÷ FTE Count) ÷ the tons-per-FTE benchmark.
- **Equipment (Tier-2):** computed as MAX across all six machine types of (Hours Used ÷ Hours Available).
- **Space/ASRS (still Tier-1):** no ASRS slot-occupancy field exists yet.

A blank box means "not yet supplied" — the dashboard falls back to the Tier-1 estimate rather than showing a fabricated number.
    """)

    section_title("Exporting Data")
    st.markdown('Use the **"Export All Data (.xlsx)"** button in the top-right header to download the entire dataset as a multi-sheet Excel workbook. Each table also has its own **"Export CSV"** link.')

    section_title("Example Data Structure (for those who want to edit it directly)")
    st.code("""
DATA["y2026"] = {
  "revenue":   [367402,352990,409954,412282,416608,414456,None,None,None,None,None,None],
  "expense":   [176975,110488,151525,165172,155093,149021,None,None,None,None,None,None],
  "profit":    [190427,242502,258429,247109,261515,265436,None,None,None,None,None,None],
  "margin":    [51.8,68.7,63.0,59.9,62.8,64.0,None,None,None,None,None,None],
  "weight":    [78761376,78184971,91377891,83607316,87430543,85249268,None,None,None,None,None,None],
  "costPerKg": [2.25,1.41,1.84,1.98,1.77,1.75,None,None,None,None,None,None],
  "revPerKg":  [4.66,4.51,4.48,4.93,4.75,4.86,None,None,None,None,None,None],
  "capacity":  [86,86,100,92,96,94,None,None,None,None,None,None],
}
""", language="python")
    note("Array index 0–11 = Jan–Dec, in order (monetary unit = Thousand Baht / unit price = THB/Kg). Use <code>None</code> for months without data yet — the charts will automatically leave a gap for that point.")
