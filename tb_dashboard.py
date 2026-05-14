
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
 
st.set_page_config(
    page_title="TB Dashboard - First Health Cluster",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ── Palette ────────────────────────────────────────────────────────────────────
NAVY       = "#0D2B5E"
NAVY_MED   = "#1B4F9B"
BLUE_MED   = "#2563EB"
BLUE_LT    = "#3B82F6"
BLUE_PALE  = "#EFF6FF"
BLUE_PALE2 = "#DBEAFE"
TEAL       = "#0891B2"
AMBER      = "#D97706"
RED        = "#DC2626"
GREEN      = "#16A34A"
GRAY_DARK  = "#1E293B"
GRAY_MED   = "#64748B"
GRAY_LT    = "#94A3B8"
GRAY_BG    = "#F1F5F9"
BORDER     = "#E2E8F0"
WHITE      = "#FFFFFF"
SIDEBAR_BG = "#0D2B5E"
SIDEBAR_ACTIVE = "#1B4F9B"
 
BLUE_SCALE = [[0.0, BLUE_PALE2], [0.5, BLUE_LT], [1.0, NAVY]]
PALETTE    = [BLUE_MED, TEAL, "#8B5CF6", "#F59E0B", "#10B981",
              "#EF4444", "#6366F1", "#14B8A6", NAVY, GRAY_MED]
 
# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, * {{ font-family: 'Inter', sans-serif !important; }}
 
  .main .block-container {{
      background-color:{GRAY_BG};
      padding:24px 28px 28px 28px !important;
      max-width:100% !important;
  }}
  .stApp {{ background-color:{GRAY_BG}; }}
 
  /* ── Sidebar (dark navy) ── */
  [data-testid="stSidebar"] {{
      background-color:{SIDEBAR_BG} !important;
      border-right:none !important;
      min-width:220px !important;
      max-width:220px !important;
  }}
  [data-testid="stSidebar"] > div {{
      padding:0 !important;
  }}
  /* sidebar radio buttons → nav items */
  [data-testid="stSidebar"] .stRadio > label {{
      display:none;
  }}
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
      display:flex;
      flex-direction:column;
      gap:2px;
  }}
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
      display:flex !important;
      align-items:center;
      padding:10px 20px;
      border-radius:8px;
      margin:0 10px;
      cursor:pointer;
      font-size:0.82rem;
      font-weight:500;
      color:rgba(255,255,255,0.65) !important;
      transition:background 0.15s, color 0.15s;
  }}
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
      background:rgba(255,255,255,0.08) !important;
      color:{WHITE} !important;
  }}
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [aria-checked="true"] + div {{
      background:{SIDEBAR_ACTIVE} !important;
      color:{WHITE} !important;
  }}
  /* hide radio circle */
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > span:first-child {{
      display:none !important;
  }}
  /* thin divider after each nav item */
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
      border-bottom:1px solid rgba(255,255,255,0.06);
  }}
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:last-child {{
      border-bottom:none;
  }}
  /* sidebar file uploader */
  [data-testid="stSidebar"] .stFileUploader {{
      padding:0 12px;
  }}
  [data-testid="stSidebar"] .stFileUploader > label {{
      color:rgba(255,255,255,0.6) !important;
      font-size:0.70rem !important;
  }}
  [data-testid="stSidebar"] .stFileUploader section {{
      border:1px dashed rgba(255,255,255,0.2) !important;
      background:rgba(255,255,255,0.05) !important;
      border-radius:8px !important;
  }}
  [data-testid="stSidebar"] .stFileUploader section span,
  [data-testid="stSidebar"] .stFileUploader section p {{
      color:rgba(255,255,255,0.55) !important;
      font-size:0.72rem !important;
  }}
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span {{
      color:rgba(255,255,255,0.55) !important;
  }}
  [data-testid="stSidebar"] .sidebar-divider {{
      border-top:1px solid rgba(255,255,255,0.10);
      margin:10px 16px;
  }}
 
  /* ── Top header ── */
  .top-header {{
      background:linear-gradient(120deg,{NAVY} 0%,{NAVY_MED} 55%,{BLUE_MED} 100%);
      padding:16px 24px;
      border-radius:12px;
      margin-bottom:16px;
      display:flex;
      align-items:center;
      justify-content:space-between;
  }}
  .top-header h1 {{
      margin:0; font-size:1.1rem; font-weight:700; color:{WHITE};
  }}
  .top-header p {{
      margin:3px 0 0 0; font-size:0.74rem; color:rgba(255,255,255,0.62);
  }}
  .header-badge {{
      background:rgba(255,255,255,0.14);
      border:1px solid rgba(255,255,255,0.22);
      border-radius:20px; padding:4px 14px;
      font-size:0.70rem; color:{WHITE}; font-weight:500;
  }}
 
  /* ── Filter card (inside header area) ── */
  .filter-card {{
      background:{WHITE};
      border:1px solid {BORDER};
      border-radius:12px;
      padding:14px 20px 10px 20px;
      margin-bottom:16px;
      box-shadow:0 1px 3px rgba(0,0,0,0.05);
  }}
  .filter-card-title {{
      font-size:0.60rem;
      font-weight:700;
      color:{GRAY_MED};
      text-transform:uppercase;
      letter-spacing:0.8px;
      margin-bottom:10px;
  }}
 
  /* Selectbox / multiselect — light style */
  .stSelectbox > div > div,
  .stMultiSelect > div > div {{
      background:{WHITE} !important;
      border:1.5px solid {BORDER} !important;
      border-radius:8px !important;
      font-size:0.78rem !important;
      min-height:34px !important;
      color:{GRAY_DARK} !important;
      box-shadow:none !important;
  }}
  .stSelectbox > div > div:focus-within,
  .stMultiSelect > div > div:focus-within {{
      border-color:{BLUE_LT} !important;
      box-shadow:0 0 0 2px rgba(59,130,246,0.15) !important;
  }}
  /* multiselect tags */
  [data-baseweb="tag"] {{
      background:{BLUE_PALE2} !important;
      color:{NAVY} !important;
      border-radius:6px !important;
      font-size:0.72rem !important;
  }}
  [data-baseweb="tag"] span {{ color:{NAVY} !important; }}
  div[data-baseweb="select"] span {{ font-size:0.78rem !important; }}
  .stSelectbox label, .stMultiSelect label {{
      font-size:0.68rem !important;
      font-weight:600 !important;
      color:{GRAY_DARK} !important;
      margin-bottom:3px !important;
  }}
 
  /* ── KPI cards — strict uniform size ── */
  .kpi-card {{
      background:{WHITE};
      border:1px solid {BORDER};
      border-radius:12px;
      text-align:center;
      box-shadow:0 1px 3px rgba(0,0,0,0.04);
      height:100px;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      padding:0 12px;
      transition:box-shadow 0.15s, border-color 0.15s;
  }}
  .kpi-card:hover {{
      box-shadow:0 4px 14px rgba(37,99,235,0.10);
      border-color:{BLUE_LT};
  }}
  .kpi-value {{
      font-size:1.65rem;
      font-weight:700;
      color:{NAVY};
      line-height:1;
      white-space:nowrap;
  }}
  .kpi-label {{
      font-size:0.60rem;
      color:{GRAY_DARK};
      margin-top:5px;
      font-weight:600;
      text-transform:uppercase;
      letter-spacing:0.5px;
  }}
  .kpi-sub {{
      font-size:0.58rem;
      color:{GRAY_LT};
      margin-top:3px;
  }}
  .kpi-group-label {{
      font-size:0.60rem;
      font-weight:700;
      color:{GRAY_MED};
      text-transform:uppercase;
      letter-spacing:0.8px;
      margin:14px 0 8px 0;
  }}
 
  /* ── Chart card ── */
  .chart-card {{
      background:{WHITE};
      border:1px solid {BORDER};
      border-radius:12px;
      padding:18px 20px 14px 20px;
      box-shadow:0 1px 3px rgba(0,0,0,0.04);
      margin-bottom:16px;
  }}
  .card-title {{
      font-size:0.68rem;
      font-weight:700;
      color:{GRAY_DARK};
      border-left:3px solid {BLUE_MED};
      padding-left:8px;
      margin:0 0 12px 0;
      text-transform:uppercase;
      letter-spacing:0.4px;
  }}
  .section-title {{
      font-size:0.68rem;
      font-weight:700;
      color:{GRAY_DARK};
      border-left:3px solid {BLUE_MED};
      padding-left:8px;
      margin:18px 0 10px 0;
      text-transform:uppercase;
      letter-spacing:0.4px;
  }}
 
  /* ── Contact profile ── */
  .contact-profile {{
      background:{BLUE_PALE};
      border:1px solid {BLUE_PALE2};
      border-radius:12px;
      padding:18px 22px;
      margin-bottom:14px;
  }}
  .contact-profile h3 {{
      color:{NAVY}; font-size:1rem; font-weight:700; margin:0 0 12px 0;
  }}
  .info-row {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .info-item {{
      background:{WHITE}; border:1px solid {BORDER};
      border-radius:8px; padding:7px 14px; min-width:100px;
  }}
  .info-item .label {{
      font-size:0.56rem; color:{GRAY_LT};
      text-transform:uppercase; letter-spacing:0.5px; font-weight:600;
  }}
  .info-item .value {{
      font-size:0.88rem; color:{NAVY}; font-weight:700; margin-top:1px;
  }}
  .info-item .value.amber {{ color:{AMBER}; }}
  .info-item .value.blue  {{ color:{BLUE_MED}; }}
  .info-item .value.red   {{ color:{RED}; }}
 
  /* ── Page title ── */
  .page-title {{
      font-size:1rem; font-weight:700; color:{NAVY};
      margin:0 0 16px 0; padding-bottom:10px;
      border-bottom:2px solid {BLUE_PALE2};
  }}
 
  hr {{ border-color:{BORDER}; margin:14px 0; }}
  .modebar {{ display:none !important; }}
  .stDataFrame {{ border-radius:10px; overflow:hidden; }}
</style>
""", unsafe_allow_html=True)
 
# ── Column lists ───────────────────────────────────────────────────────────────
A_TO_F = ['INV ID', 'Date of entry in HESN', 'Recieved Date', 'Epi year', 'Epi week', 'Name']
HIGHLIGHTED_COLS = [
    'Gender', 'Age in years', 'Nationality', 'Saudi', 'Address', 'Occupation',
    'Region', 'Primary Dis', 'Final Dis', 'TB code', 'Code Status',
    'Team Type', 'Treatment Hospital', 'Medication Type', 'Admission', 'Pt type',
    'Patient Have Contacts', 'Number of contacts', 'Contact Screened',
    'Diabetes', 'Lung diseases', 'Chronic renal failure', 'Aids',
    'Immunosuppressive drugs', 'Cancer', 'Smoking',
    'Cough', 'Fever', 'Night Sweating', 'Loss Of Weight',
    'Sputumsmearmicroscopy', 'Xpert Mtb', 'Culture', 'HIV result ',
    'Outcome', 'Closing date',
]
TARGET_COLS = A_TO_F + HIGHLIGHTED_COLS
 
# ── Chart helper ───────────────────────────────────────────────────────────────
def base_layout(fig, height=320, margin=None, legend=False):
    m = margin or dict(t=10, b=40, l=6, r=6)
    fig.update_layout(
        paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(size=11, color=GRAY_DARK),
        height=height, margin=m, showlegend=legend,
        xaxis=dict(gridcolor="#F1F5F9", linecolor=BORDER, tickfont=dict(size=10, color=GRAY_MED)),
        yaxis=dict(gridcolor="#F1F5F9", linecolor=BORDER, tickfont=dict(size=10, color=GRAY_MED)),
    )
    return fig
 
# ── Data loaders ───────────────────────────────────────────────────────────────
@st.cache_data
def load_df(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    cols = [c for c in TARGET_COLS if c in df.columns]
    df = df[cols].copy()
    for col in ['Age in years', 'Number of contacts', 'Epi week']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'Saudi' in df.columns and 'Nationality' in df.columns:
        def fix_nat(row):
            s = str(row.get('Saudi', '')).strip()
            n = str(row.get('Nationality', '')).strip()
            if s in ('Yes', 'Yes ') or n in ('Saudi Arabia', 'Saudi'):
                return 'Saudi'
            return n if n not in ('No', 'nan', '') else 'Non-Saudi'
        df['Nationality_Clean'] = df.apply(fix_nat, axis=1)
    if 'Age in years' in df.columns:
        df['Age Group'] = pd.cut(
            df['Age in years'],
            bins=[0, 14, 24, 44, 64, 200],
            labels=['0-14', '15-24', '25-44', '45-64', '65+'], right=True
        )
    return df
 
@st.cache_data
def load_contacts(file_bytes):
    raw = pd.read_excel(io.BytesIO(file_bytes), sheet_name='Contact 2026', header=0)
    new_cols = raw.iloc[0].tolist()
    raw = raw.iloc[1:].copy()
    raw.columns = [str(c).strip() for c in new_cols]
    raw['TB_Code'] = raw['TB_Code'].ffill()
    raw['Age'] = pd.to_numeric(raw['Age'], errors='coerce')
    return raw
 
@st.cache_data
def load_verify_sheet(file_bytes):
    """Load مؤشر المخالطين sheet.
    col 'code'      = all pulmonary cases with contacts
    col 'تم الفحص'  = نعم / لا — whether contacts were screened
    """
    raw = pd.read_excel(io.BytesIO(file_bytes),
                        sheet_name='مؤشر المخالطين', header=0)
    raw.columns = [str(c).strip() for c in raw.columns]
    # Keep only rows with a valid code
    raw = raw[raw['code'].notna()].copy()
    raw['code'] = raw['code'].astype(str).str.strip()
    raw = raw[raw['code'].str.strip() != '']
    registered = raw['code'].tolist()
    # Use column index 3 to avoid encoding issues with Arabic column name
    fahss_col = raw.columns[3]
    screened   = raw[raw[fahss_col].astype(str).str.strip() == 'نعم']['code'].tolist()
    return registered, screened
 
# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Navigation + Upload + Filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / title
    st.markdown(f"""
    <div style="padding:20px 20px 16px 20px;background:rgba(0,0,0,0.15);
                border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:6px;">
      <div style="font-size:1rem;font-weight:700;color:{WHITE};">TB Dashboard</div>
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);margin-top:3px;">
        First Health Cluster · 2026
      </div>
    </div>""", unsafe_allow_html=True)
 
    # Navigation
    st.markdown(f"""
    <div style="padding:10px 20px 4px 20px;font-size:0.58rem;font-weight:700;
                color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:1px;">
      Navigation
    </div>""", unsafe_allow_html=True)
 
    NAV_ITEMS = [
        "Epidemic Curve",
        "Demographics",
        "Disease & Treatment",
        "Comorbidities",
        "Contacts",
        "Raw Data",
    ]
    page = st.radio("", NAV_ITEMS, label_visibility="collapsed")
 
    st.markdown(f"""<div style="border-top:1px solid rgba(255,255,255,0.10);
                margin:10px 16px 14px 16px;"></div>""", unsafe_allow_html=True)
 
    # Upload
    st.markdown(f"""
    <div style="padding:0 20px 6px 20px;font-size:0.58rem;font-weight:700;
                color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:1px;">
      Data File
    </div>""", unsafe_allow_html=True)
 
    uploaded_file = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")
 
    st.markdown(f"""<div style="border-top:1px solid rgba(255,255,255,0.10);
                margin:14px 16px 12px 16px;"></div>""", unsafe_allow_html=True)
 
    df = None
    contacts_df = None
    sel_weeks = sel_gender = sel_status = sel_hospital = None
 
    if uploaded_file:
        file_bytes = uploaded_file.read()
        df = load_df(file_bytes)
        contacts_df = load_contacts(file_bytes)
        registered_codes, screened_codes = load_verify_sheet(file_bytes)
 
        # Filters inside sidebar
        st.markdown(f"""
        <div style="padding:0 20px 6px 20px;font-size:0.58rem;font-weight:700;
                    color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:1px;">
          Filters
        </div>""", unsafe_allow_html=True)
 
        with st.container():
            if 'Epi week' in df.columns:
                weeks = sorted(df['Epi week'].dropna().unique().astype(int).tolist())
                # Slider range instead of multiselect
                min_w, max_w = int(min(weeks)), int(max(weeks))
                if min_w < max_w:
                    sel_range = st.slider("Epi Week Range", min_w, max_w, (min_w, max_w))
                    sel_weeks = list(range(sel_range[0], sel_range[1] + 1))
                else:
                    sel_weeks = weeks
 
            if 'Gender' in df.columns:
                genders = ['All'] + df['Gender'].dropna().unique().tolist()
                gv = st.selectbox("Gender", genders)
                sel_gender = None if gv == 'All' else [gv]
 
            if 'Code Status' in df.columns:
                statuses = ['All'] + df['Code Status'].dropna().unique().tolist()
                sv = st.selectbox("Case Status", statuses)
                sel_status = None if sv == 'All' else [sv]
 
            if 'Treatment Hospital' in df.columns:
                hospitals = ['All'] + sorted(df['Treatment Hospital'].dropna().unique().tolist())
                hv = st.selectbox("Treatment Hospital", hospitals)
                sel_hospital = None if hv == 'All' else [hv]
 
        st.markdown(f"""<div style="border-top:1px solid rgba(255,255,255,0.10);
                    margin:14px 16px 8px 16px;"></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding:0 20px;font-size:0.70rem;color:rgba(255,255,255,0.40);">
          Total records: <span style="color:{WHITE};font-weight:600;">{len(df):,}</span>
        </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
if df is None:
    st.markdown(f"""
    <div class="top-header">
      <div>
        <h1>TB Cases Dashboard — First Health Cluster</h1>
        <p>Epidemiological Surveillance · 2026</p>
      </div>
      <div class="header-badge">Jeddah Health Cluster</div>
    </div>""", unsafe_allow_html=True)
    st.info("Upload an Excel file from the sidebar to load the dashboard.")
    st.stop()
registered_codes = registered_codes if 'registered_codes' in dir() else []
screened_codes   = screened_codes   if 'screened_codes'   in dir() else []
 
# ── Password ──────────────────────────────────────────────────────────────────
password = st.text_input("Password", type="password",
                          placeholder="Enter password to continue",
                          label_visibility="collapsed")
if password != "JEH2026":
    if password != "":
        st.error("Incorrect password. Please try again.")
    st.stop()
 
# ── Apply filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_weeks    and 'Epi week'           in fdf.columns: fdf = fdf[fdf['Epi week'].isin(sel_weeks)]
if sel_gender   and 'Gender'             in fdf.columns: fdf = fdf[fdf['Gender'].isin(sel_gender)]
if sel_status   and 'Code Status'        in fdf.columns: fdf = fdf[fdf['Code Status'].isin(sel_status)]
if sel_hospital and 'Treatment Hospital' in fdf.columns: fdf = fdf[fdf['Treatment Hospital'].isin(sel_hospital)]
 
if fdf.empty:
    st.warning("No records match the selected filters.")
    st.stop()
 
total = len(fdf)
contacts_total = len(contacts_df) if contacts_df is not None else 0
 
# ── Shared KPI values ─────────────────────────────────────────────────────────
active_week = int(fdf['Epi week'].max()) if 'Epi week' in fdf.columns else '-'
males   = int((fdf['Gender'] == 'Male').sum())           if 'Gender'      in fdf.columns else 0
females = int((fdf['Gender'] == 'Female').sum())         if 'Gender'      in fdf.columns else 0
pulm    = int((fdf['Final Dis'] == 'Pulmonary').sum())   if 'Final Dis'   in fdf.columns else 0
extra_p = total - pulm
regular = int((fdf['Code Status'] == 'Regular').sum())   if 'Code Status' in fdf.columns else 0
temp_c  = int((fdf['Code Status'] == 'Temporary').sum()) if 'Code Status' in fdf.columns else 0
avg_age = fdf['Age in years'].mean()                     if 'Age in years' in fdf.columns else 0
died    = int((fdf['Outcome'] == 'Died').sum())          if 'Outcome'     in fdf.columns else 0
in_prog = int((fdf['Outcome'].astype(str).str.strip() == 'In progress').sum()) if 'Outcome' in fdf.columns else 0
 
# ── Top header (always visible) ───────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
  <div>
    <h1>TB Cases Dashboard — First Health Cluster</h1>
    <p>Epidemiological Year 2026 &nbsp;·&nbsp; Latest Epi Week: {active_week} &nbsp;·&nbsp; Filtered Cases: {total:,}</p>
  </div>
  <div class="header-badge">Jeddah First Health Cluster</div>
</div>""", unsafe_allow_html=True)
 
# ── Filter summary bar (above KPIs) ──────────────────────────────────────────
st.markdown(f"""
<div style="background:{WHITE};border:1px solid {BORDER};border-radius:10px;
            padding:10px 18px;margin-bottom:14px;display:flex;align-items:center;
            gap:24px;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
  <span style="font-size:0.60rem;font-weight:700;color:{GRAY_MED};
               text-transform:uppercase;letter-spacing:0.8px;">Active Filters</span>
  <span style="font-size:0.74rem;color:{GRAY_DARK};">
    Epi Weeks: <b style="color:{NAVY};">{min(sel_weeks) if sel_weeks else '–'} – {max(sel_weeks) if sel_weeks else '–'}</b>
  </span>
  <span style="font-size:0.74rem;color:{GRAY_DARK};">
    Gender: <b style="color:{NAVY};">{sel_gender[0] if sel_gender else 'All'}</b>
  </span>
  <span style="font-size:0.74rem;color:{GRAY_DARK};">
    Case Status: <b style="color:{NAVY};">{sel_status[0] if sel_status else 'All'}</b>
  </span>
  <span style="font-size:0.74rem;color:{GRAY_DARK};">
    Hospital: <b style="color:{NAVY};">{sel_hospital[0] if sel_hospital else 'All'}</b>
  </span>
  <span style="margin-left:auto;font-size:0.70rem;color:{GRAY_MED};">
    Showing <b style="color:{NAVY};">{total:,}</b> of <b>{len(df):,}</b> records
  </span>
</div>""", unsafe_allow_html=True)
 
# ── KPIs (always visible under header) ───────────────────────────────────────
st.markdown(f'<div class="kpi-group-label">Case Indicators</div>', unsafe_allow_html=True)
r1 = st.columns(5, gap="small")
for col, (label, val, sub) in zip(r1, [
    ("Total Cases",     f"{total:,}",           ""),
    ("Male / Female",   f"{males} / {females}", "gender split"),
    ("Pulmonary",       f"{pulm:,}",            f"{pulm/total*100:.0f}% of total"),
    ("Extra-Pulmonary", f"{extra_p:,}",         f"{extra_p/total*100:.0f}% of total"),
    ("Avg. Age",        f"{avg_age:.1f} yrs",   ""),
]):
    with col:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-value">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-sub">{sub if sub else "&nbsp;"}</div>
        </div>""", unsafe_allow_html=True)
 
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="kpi-group-label">Follow-up & Contact Indicators</div>', unsafe_allow_html=True)
r2 = st.columns(5, gap="small")
for col, (label, val, sub) in zip(r2, [
    ("Total Contacts",  f"{contacts_total:,}", ""),
    ("Regular",         f"{regular:,}",         f"{regular/total*100:.0f}% of cases"),
    ("Temporary",       f"{temp_c:,}",           f"{temp_c/total*100:.0f}% of cases"),
    ("In Treatment",    f"{in_prog:,}",          f"{in_prog/total*100:.0f}% of cases"),
    ("Deaths",          f"{died:,}",             f"{died/total*100:.1f}% of cases"),
]):
    with col:
        st.markdown(f"""<div class="kpi-card">
          <div class="kpi-value">{val}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-sub">{sub if sub else "&nbsp;"}</div>
        </div>""", unsafe_allow_html=True)
 
st.markdown(f"<hr style='border-color:{BORDER};margin:18px 0 14px 0;'>", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTING via sidebar radio
# ══════════════════════════════════════════════════════════════════════════════
clean_page = page.strip()
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Epidemic Curve
# ════════════════════════════════════════════════════════════════════════════════
if clean_page == "Epidemic Curve":
    st.markdown('<div class="page-title">Epidemic Curve</div>', unsafe_allow_html=True)
 
    if 'Epi week' not in fdf.columns:
        st.info("No Epi week column found.")
    else:
        epi_df = fdf.groupby('Epi week').size().reset_index(name='Cases')
        epi_df = epi_df.sort_values('Epi week')
        epi_df['Epi week'] = epi_df['Epi week'].astype(int)
        wk_labels = ['Wk ' + str(w) for w in epi_df['Epi week']]
 
        peak_wk    = int(epi_df.loc[epi_df['Cases'].idxmax(), 'Epi week'])
        peak_cnt   = int(epi_df['Cases'].max())
        avg_wk     = epi_df['Cases'].mean()
        latest_cnt = int(epi_df.iloc[-1]['Cases']) if len(epi_df) else 0
 
        # Row 1: big epidemic curve + weekly summary side by side
        col_chart, col_summary = st.columns([3, 1], gap="large")
 
        with col_chart:
            st.markdown('<div class="chart-card"><div class="card-title">Cases by Epidemiological Week</div>',
                        unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=wk_labels, y=epi_df['Cases'],
                marker=dict(color=epi_df['Cases'], colorscale=BLUE_SCALE,
                            line=dict(color='rgba(0,0,0,0)', width=0)),
                name='Cases',
                hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>',
            ))
            fig.add_trace(go.Scatter(
                x=wk_labels, y=epi_df['Cases'],
                mode='lines+markers',
                line=dict(color=AMBER, width=2.5),
                marker=dict(size=7, color=AMBER, line=dict(color=WHITE, width=2)),
                name='Trend',
            ))
            fig = base_layout(fig, height=340, legend=True, margin=dict(t=8, b=50, l=6, r=6))
            fig.update_layout(
                bargap=0.32,
                legend=dict(orientation='h', y=1.06, x=0),
                xaxis=dict(title='Epi Week', title_font=dict(size=11)),
                yaxis=dict(title='Cases', title_font=dict(size=11)),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with col_summary:
            st.markdown('<div class="chart-card"><div class="card-title">Weekly Summary</div>',
                        unsafe_allow_html=True)
            for lbl, val in [
                ("Peak Week",      f"Wk {peak_wk} ({peak_cnt} cases)"),
                ("Avg / Week",     f"{avg_wk:.1f} cases"),
                ("Latest Week",    f"Wk {int(epi_df.iloc[-1]['Epi week'])} · {latest_cnt} cases"),
                ("Weeks Reported", f"{len(epi_df)} weeks"),
                ("Total (filtered)", f"{total:,} cases"),
            ]:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:8px 0;border-bottom:1px solid {BORDER};">
                  <span style="font-size:0.70rem;color:{GRAY_MED};">{lbl}</span>
                  <span style="font-size:0.75rem;font-weight:600;color:{NAVY};">{val}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        # Row 2: Gender split by week — full width
        if 'Gender' in fdf.columns:
            st.markdown('<div class="chart-card"><div class="card-title">Gender Split by Week</div>',
                        unsafe_allow_html=True)
            epi_g = fdf.groupby(['Epi week', 'Gender']).size().reset_index(name='Cases')
            epi_g['Epi week'] = epi_g['Epi week'].astype(int)
            epi_g['Wk'] = 'Wk ' + epi_g['Epi week'].astype(str)
            fig3 = px.bar(epi_g, x='Wk', y='Cases', color='Gender', barmode='group',
                          color_discrete_map={'Male': BLUE_MED, 'Female': TEAL})
            fig3 = base_layout(fig3, height=280, legend=True, margin=dict(t=8, b=50, l=6, r=6))
            fig3.update_layout(bargap=0.28, bargroupgap=0.08,
                               legend=dict(orientation='h', y=1.06, x=0),
                               xaxis=dict(title='Epi Week'), yaxis=dict(title='Cases'))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
            # Row 3: Gender pie — full width but shorter
            st.markdown('<div class="chart-card"><div class="card-title">Gender Distribution</div>',
                        unsafe_allow_html=True)
            col_pie, col_stats = st.columns([1, 2], gap="large")
            with col_pie:
                gdf = fdf['Gender'].value_counts().reset_index()
                gdf.columns = ['Gender', 'Count']
                fig_pie = px.pie(gdf, names='Gender', values='Count',
                                 color_discrete_map={'Male': BLUE_MED, 'Female': TEAL}, hole=0.52)
                fig_pie.update_traces(textfont_size=12)
                fig_pie.update_layout(paper_bgcolor=WHITE, height=220,
                                      margin=dict(t=6, b=6, l=6, r=6),
                                      legend=dict(font=dict(size=10)))
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_stats:
                st.markdown(f"""
                <div style="display:flex;gap:16px;align-items:center;height:100%;padding-top:20px;">
                  <div style="text-align:center;flex:1;padding:16px;background:{BLUE_PALE};
                              border-radius:10px;border:1px solid {BLUE_PALE2};">
                    <div style="font-size:2rem;font-weight:700;color:{BLUE_MED};">{males}</div>
                    <div style="font-size:0.65rem;font-weight:600;color:{GRAY_MED};
                                text-transform:uppercase;letter-spacing:0.5px;margin-top:4px;">Male</div>
                    <div style="font-size:0.75rem;color:{GRAY_LT};margin-top:2px;">
                      {males/total*100:.1f}%</div>
                  </div>
                  <div style="text-align:center;flex:1;padding:16px;
                              background:#ECFEFF;border-radius:10px;border:1px solid #A5F3FC;">
                    <div style="font-size:2rem;font-weight:700;color:{TEAL};">{females}</div>
                    <div style="font-size:0.65rem;font-weight:600;color:{GRAY_MED};
                                text-transform:uppercase;letter-spacing:0.5px;margin-top:4px;">Female</div>
                    <div style="font-size:0.75rem;color:{GRAY_LT};margin-top:2px;">
                      {females/total*100:.1f}%</div>
                  </div>
                  <div style="text-align:center;flex:1;padding:16px;background:#F0FDF4;
                              border-radius:10px;border:1px solid #BBF7D0;">
                    <div style="font-size:2rem;font-weight:700;color:{GREEN};">
                      {males/females:.1f}x</div>
                    <div style="font-size:0.65rem;font-weight:600;color:{GRAY_MED};
                                text-transform:uppercase;letter-spacing:0.5px;margin-top:4px;">M:F Ratio</div>
                    <div style="font-size:0.75rem;color:{GRAY_LT};margin-top:2px;">male predominance</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Demographics
# ════════════════════════════════════════════════════════════════════════════════
elif clean_page == "Demographics":
    st.markdown('<div class="page-title">Demographics</div>', unsafe_allow_html=True)
 
    # Neighbourhood distribution (full width first)
    if 'Address' in fdf.columns:
        st.markdown('<div class="chart-card"><div class="card-title">Cases by Neighbourhood (Top 20)</div>',
                    unsafe_allow_html=True)
        nbhd_df = fdf['Address'].dropna().value_counts().head(20).reset_index()
        nbhd_df.columns = ['Neighbourhood', 'Count']
        fig_nbhd = px.bar(nbhd_df, x='Count', y='Neighbourhood', orientation='h',
                          color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
        fig_nbhd.update_traces(textposition='outside', textfont_size=10)
        h_nbhd = max(320, len(nbhd_df) * 28)
        fig_nbhd = base_layout(fig_nbhd, height=h_nbhd, margin=dict(t=6, b=16, l=6, r=55))
        fig_nbhd.update_layout(bargap=0.22, coloraxis_showscale=False,
                                yaxis=dict(autorange='reversed', title=''),
                                xaxis=dict(title='Cases'))
        st.plotly_chart(fig_nbhd, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    col_a, col_b = st.columns(2, gap="large")
 
    with col_a:
        st.markdown('<div class="chart-card"><div class="card-title">Nationality (Top 12)</div>',
                    unsafe_allow_html=True)
        if 'Nationality_Clean' in fdf.columns:
            nat_df = fdf['Nationality_Clean'].value_counts().head(12).reset_index()
            nat_df.columns = ['Nationality', 'Count']
            fig = px.bar(nat_df, x='Count', y='Nationality', orientation='h',
                         color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
            fig.update_traces(textposition='outside', textfont_size=10)
            fig = base_layout(fig, height=430, margin=dict(t=6, b=16, l=6, r=55))
            fig.update_layout(bargap=0.25, coloraxis_showscale=False,
                              yaxis=dict(autorange='reversed', title=''),
                              xaxis=dict(title='Cases'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with col_b:
        st.markdown('<div class="chart-card"><div class="card-title">Age Groups by Gender</div>',
                    unsafe_allow_html=True)
        if 'Age Group' in fdf.columns:
            if 'Gender' in fdf.columns:
                age_df = fdf.groupby(['Age Group', 'Gender']).size().reset_index(name='Cases')
                fig = px.bar(age_df, x='Age Group', y='Cases', color='Gender', barmode='group',
                             color_discrete_map={'Male': BLUE_MED, 'Female': TEAL}, text='Cases')
            else:
                age_df = fdf['Age Group'].value_counts().reset_index()
                age_df.columns = ['Age Group', 'Cases']
                fig = px.bar(age_df, x='Age Group', y='Cases',
                             color_discrete_sequence=[BLUE_MED], text='Cases')
            fig.update_traces(textposition='outside', textfont_size=10)
            fig = base_layout(fig, height=430, legend=True, margin=dict(t=6, b=35, l=6, r=6))
            fig.update_layout(bargap=0.28, bargroupgap=0.10,
                              legend=dict(orientation='h', y=1.06, x=0),
                              xaxis=dict(title='Age Group'), yaxis=dict(title='Cases'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Disease & Treatment
# ════════════════════════════════════════════════════════════════════════════════
elif clean_page == "Disease & Treatment":
    st.markdown('<div class="page-title">Disease & Treatment</div>', unsafe_allow_html=True)
 
    c1, c2, c3 = st.columns(3, gap="large")
    for col, title, col_name, pal in [
        (c1, "Disease Type", 'Final Dis',   PALETTE),
        (c2, "Case Status",  'Code Status', [BLUE_MED, TEAL, "#8B5CF6"]),
        (c3, "Team Type",    'Team Type',   [BLUE_MED, TEAL]),
    ]:
        with col:
            st.markdown(f'<div class="chart-card"><div class="card-title">{title}</div>',
                        unsafe_allow_html=True)
            if col_name in fdf.columns:
                d = fdf[col_name].value_counts().reset_index()
                d.columns = ['x', 'Count']
                fig = px.pie(d, names='x', values='Count',
                             color_discrete_sequence=pal, hole=0.48)
                fig.update_traces(textfont_size=11)
                fig.update_layout(paper_bgcolor=WHITE, height=270,
                                  margin=dict(t=8, b=8, l=6, r=6),
                                  legend=dict(font=dict(size=9)))
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
    c4, c5 = st.columns(2, gap="large")
    with c4:
        st.markdown('<div class="chart-card"><div class="card-title">Medication Type</div>',
                    unsafe_allow_html=True)
        if 'Medication Type' in fdf.columns:
            med_df = fdf['Medication Type'].value_counts().reset_index()
            med_df.columns = ['Type', 'Count']
            fig = px.bar(med_df, x='Type', y='Count',
                         color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
            fig.update_traces(textposition='outside', textfont_size=11)
            fig = base_layout(fig, height=270, margin=dict(t=6, b=45, l=6, r=6))
            fig.update_layout(bargap=0.40, coloraxis_showscale=False,
                              xaxis=dict(title=''), yaxis=dict(title='Cases'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with c5:
        st.markdown('<div class="chart-card"><div class="card-title">Treatment Outcome</div>',
                    unsafe_allow_html=True)
        if 'Outcome' in fdf.columns:
            out_df = fdf['Outcome'].value_counts().reset_index()
            out_df.columns = ['Outcome', 'Count']
            color_map = {'In progress': BLUE_LT, 'Died': RED, 'Deported': GRAY_MED, 'Completed': GREEN}
            fig = px.bar(out_df, x='Outcome', y='Count', color='Outcome',
                         color_discrete_map={k: color_map.get(k, BLUE_MED) for k in out_df['Outcome']},
                         text='Count')
            fig.update_traces(textposition='outside', textfont_size=11)
            fig = base_layout(fig, height=270, margin=dict(t=6, b=45, l=6, r=6))
            fig.update_layout(bargap=0.40, showlegend=False,
                              xaxis=dict(title=''), yaxis=dict(title='Cases'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    st.markdown('<div class="chart-card"><div class="card-title">Cases by Treatment Hospital</div>',
                unsafe_allow_html=True)
    if 'Treatment Hospital' in fdf.columns:
        hosp_df = fdf['Treatment Hospital'].value_counts().head(15).reset_index()
        hosp_df.columns = ['Hospital', 'Count']
        fig = px.bar(hosp_df, x='Count', y='Hospital', orientation='h',
                     color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
        fig.update_traces(textposition='outside', textfont_size=10)
        h = max(300, len(hosp_df) * 34)
        fig = base_layout(fig, height=h, margin=dict(t=6, b=16, l=6, r=55))
        fig.update_layout(bargap=0.24, coloraxis_showscale=False,
                          yaxis=dict(autorange='reversed', title=''),
                          xaxis=dict(title='Cases'))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Comorbidities
# ════════════════════════════════════════════════════════════════════════════════
elif clean_page == "Comorbidities":
    st.markdown('<div class="page-title">Comorbidities</div>', unsafe_allow_html=True)
 
    comorbidities = [c for c in
        ['Diabetes', 'Lung diseases', 'Chronic renal failure',
         'Aids', 'Immunosuppressive drugs', 'Cancer', 'Smoking']
        if c in fdf.columns]
 
    if comorbidities:
        yes_counts = {c: int((fdf[c].astype(str).str.strip().str.lower() == 'yes').sum())
                      for c in comorbidities}
        co_df = pd.DataFrame({'Condition': list(yes_counts.keys()),
                              'Count': list(yes_counts.values())})
        co_df['%'] = (co_df['Count'] / total * 100).round(1)
        co_df = co_df.sort_values('Count', ascending=False)
 
        c1, c2 = st.columns([3, 1], gap="large")
        with c1:
            st.markdown('<div class="chart-card"><div class="card-title">Comorbidity Prevalence</div>',
                        unsafe_allow_html=True)
            fig = px.bar(co_df, x='Condition', y='%',
                         color='%', color_continuous_scale=BLUE_SCALE, text='%')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont_size=11)
            fig = base_layout(fig, height=340, margin=dict(t=6, b=55, l=6, r=6))
            fig.update_layout(bargap=0.36, coloraxis_showscale=False,
                              xaxis=dict(title=''), yaxis=dict(title='% of cases'))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with c2:
            st.markdown('<div class="chart-card"><div class="card-title">Summary</div>',
                        unsafe_allow_html=True)
            st.dataframe(co_df[['Condition', 'Count', '%']],
                         use_container_width=True, hide_index=True, height=300)
            st.markdown('</div>', unsafe_allow_html=True)
 
    symptoms = [s for s in ['Cough', 'Fever', 'Night Sweating', 'Loss Of Weight'] if s in fdf.columns]
    if symptoms:
        st.markdown('<div class="section-title">Clinical Symptoms</div>', unsafe_allow_html=True)
        scols = st.columns(len(symptoms), gap="small")
        for col, s in zip(scols, symptoms):
            cnt = int((fdf[s].astype(str).str.strip().str.lower() == 'yes').sum())
            with col:
                st.markdown(f"""<div class="kpi-card">
                  <div class="kpi-value">{cnt:,}</div>
                  <div class="kpi-label">{s}</div>
                  <div class="kpi-sub">{cnt/total*100:.1f}% of cases</div>
                </div>""", unsafe_allow_html=True)
 
    # ── Deaths ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Deaths</div>', unsafe_allow_html=True)
    if 'Outcome' in fdf.columns:
        died_df = fdf[fdf['Outcome'] == 'Died'].copy()
        n_died = len(died_df)
 
        if n_died == 0:
            st.info("No deaths recorded in the current filter.")
        else:
            # KPIs
            d_male   = int((died_df['Gender'] == 'Male').sum())   if 'Gender' in died_df.columns else 0
            d_female = int((died_df['Gender'] == 'Female').sum()) if 'Gender' in died_df.columns else 0
 
            def is_saudi(row):
                s = str(row.get('Saudi', '')).strip()
                n = str(row.get('Nationality', '')).strip()
                return s in ('Yes', 'Yes ') or n in ('Saudi Arabia', 'Saudi')
            d_saudi     = int(died_df.apply(is_saudi, axis=1).sum())
            d_nonsaudi  = n_died - d_saudi
            d_hiv       = int((died_df['HIV result '].astype(str).str.strip().str.lower() == 'positive').sum()) if 'HIV result ' in died_df.columns else 0
 
            dk = st.columns(5, gap="small")
            for col, (label, val, sub) in zip(dk, [
                ("Total Deaths",   f"{n_died}",      f"{n_died/total*100:.1f}% of cases"),
                ("Male",           f"{d_male}",      f"{d_male/n_died*100:.0f}%"),
                ("Female",         f"{d_female}",    f"{d_female/n_died*100:.0f}%"),
                ("Non-Saudi",      f"{d_nonsaudi}",  f"{d_nonsaudi/n_died*100:.0f}%"),
                ("HIV Positive",   f"{d_hiv}",       "among deaths"),
            ]):
                with col:
                    st.markdown(f"""<div class="kpi-card">
                      <div class="kpi-value" style="color:{RED if label=='Total Deaths' else NAVY_MED}">{val}</div>
                      <div class="kpi-label">{label}</div>
                      <div class="kpi-sub">{sub}</div>
                    </div>""", unsafe_allow_html=True)
 
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
 
            # Nationality breakdown of deaths
            d1, d2 = st.columns(2, gap="large")
            with d1:
                st.markdown('<div class="chart-card"><div class="card-title">Deaths by Nationality</div>', unsafe_allow_html=True)
                if 'Nationality' in died_df.columns:
                    nat_d = died_df.copy()
                    nat_d['Nat'] = nat_d.apply(lambda r: 'Saudi' if is_saudi(r) else str(r.get('Nationality','')).strip(), axis=1)
                    nat_d = nat_d['Nat'].value_counts().reset_index()
                    nat_d.columns = ['Nationality', 'Count']
                    fig = px.bar(nat_d, x='Nationality', y='Count',
                                 color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
                    fig.update_traces(textposition='outside', textfont_size=11)
                    fig = base_layout(fig, height=260, margin=dict(t=6, b=40, l=6, r=6))
                    fig.update_layout(bargap=0.40, coloraxis_showscale=False,
                                      xaxis=dict(title=''), yaxis=dict(title=''))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
 
            with d2:
                st.markdown('<div class="chart-card"><div class="card-title">Deaths by Disease Type</div>', unsafe_allow_html=True)
                if 'Final Dis' in died_df.columns:
                    dis_d = died_df['Final Dis'].value_counts().reset_index()
                    dis_d.columns = ['Disease', 'Count']
                    fig = px.pie(dis_d, names='Disease', values='Count',
                                 color_discrete_sequence=[BLUE_MED, TEAL, GRAY_MED], hole=0.48)
                    fig.update_traces(textfont_size=10)
                    fig.update_layout(paper_bgcolor=WHITE, height=260,
                                      margin=dict(t=6, b=6, l=6, r=6),
                                      legend=dict(font=dict(size=10)))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
 
    # ── HIV ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">HIV Co-infection</div>', unsafe_allow_html=True)
    if 'HIV result ' in fdf.columns:
        hiv_pos_df  = fdf[fdf['HIV result '].astype(str).str.strip().str.lower() == 'positive'].copy()
        hiv_pend_df = fdf[fdf['HIV result '].astype(str).str.strip().str.lower() == 'pending'].copy()
        n_hiv_pos   = len(hiv_pos_df)
        n_hiv_pend  = len(hiv_pend_df)
        n_hiv_neg   = int((fdf['HIV result '].astype(str).str.strip().str.lower() == 'negative').sum())
        n_hiv_nd    = int((fdf['HIV result '].astype(str).str.strip().str.lower() == 'not done').sum())
 
        hk = st.columns(4, gap="small")
        for col, (label, val, sub) in zip(hk, [
            ("HIV Positive",  f"{n_hiv_pos}",  f"{n_hiv_pos/total*100:.1f}% of cases"),
            ("HIV Negative",  f"{n_hiv_neg}",  f"{n_hiv_neg/total*100:.1f}% of cases"),
            ("Pending",       f"{n_hiv_pend}", f"{n_hiv_pend/total*100:.1f}% of cases"),
            ("Not Done",      f"{n_hiv_nd}",   f"{n_hiv_nd/total*100:.1f}% of cases"),
        ]):
            with col:
                st.markdown(f"""<div class="kpi-card">
                  <div class="kpi-value" style="color:{RED if label=='HIV Positive' else NAVY_MED}">{val}</div>
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)
 
        if n_hiv_pos > 0:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            h1, h2, h3 = st.columns(3, gap="large")
 
            with h1:
                st.markdown('<div class="chart-card"><div class="card-title">HIV Positive — Gender</div>', unsafe_allow_html=True)
                if 'Gender' in hiv_pos_df.columns:
                    gd = hiv_pos_df['Gender'].value_counts().reset_index()
                    gd.columns = ['Gender', 'Count']
                    fig = px.pie(gd, names='Gender', values='Count',
                                 color_discrete_map={'Male': BLUE_MED, 'Female': TEAL}, hole=0.48)
                    fig.update_traces(textfont_size=11)
                    fig.update_layout(paper_bgcolor=WHITE, height=220,
                                      margin=dict(t=6, b=6, l=6, r=6),
                                      legend=dict(font=dict(size=10)))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
 
            with h2:
                st.markdown('<div class="chart-card"><div class="card-title">HIV Positive — Nationality</div>', unsafe_allow_html=True)
                if 'Nationality' in hiv_pos_df.columns:
                    def is_saudi(row):
                        s = str(row.get('Saudi', '')).strip()
                        n = str(row.get('Nationality', '')).strip()
                        return s in ('Yes', 'Yes ') or n in ('Saudi Arabia', 'Saudi')
                    hiv_pos_df['Nat'] = hiv_pos_df.apply(lambda r: 'Saudi' if is_saudi(r) else str(r.get('Nationality','')).strip(), axis=1)
                    nat_h = hiv_pos_df['Nat'].value_counts().reset_index()
                    nat_h.columns = ['Nationality', 'Count']
                    fig = px.bar(nat_h, x='Nationality', y='Count',
                                 color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
                    fig.update_traces(textposition='outside', textfont_size=11)
                    fig = base_layout(fig, height=220, margin=dict(t=6, b=40, l=6, r=6))
                    fig.update_layout(bargap=0.40, coloraxis_showscale=False,
                                      xaxis=dict(title=''), yaxis=dict(title=''))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
 
            with h3:
                st.markdown('<div class="chart-card"><div class="card-title">HIV Positive — Outcome</div>', unsafe_allow_html=True)
                if 'Outcome' in hiv_pos_df.columns:
                    out_h = hiv_pos_df['Outcome'].fillna('Unknown').value_counts().reset_index()
                    out_h.columns = ['Outcome', 'Count']
                    color_map = {'In progress': BLUE_MED, 'Died': RED, 'Completed': GREEN, 'Unknown': GRAY_MED}
                    fig = px.pie(out_h, names='Outcome', values='Count', color='Outcome',
                                 color_discrete_map={k: color_map.get(k, NAVY_MED) for k in out_h['Outcome']},
                                 hole=0.48)
                    fig.update_traces(textfont_size=11)
                    fig.update_layout(paper_bgcolor=WHITE, height=220,
                                      margin=dict(t=6, b=6, l=6, r=6),
                                      legend=dict(font=dict(size=10)))
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
 
 
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 5 — Contacts
# ════════════════════════════════════════════════════════════════════════════════
elif clean_page == "Contacts":
    st.markdown('<div class="page-title">Contacts</div>', unsafe_allow_html=True)
 
    if contacts_df is None or contacts_df.empty:
        st.info("No contact data found.")
    else:
        # Filter contacts to only cases present in the filtered main dataset
        filtered_codes = set(fdf['TB code'].dropna().astype(str).str.strip()) if 'TB code' in fdf.columns else set()
        cdf = contacts_df[contacts_df['TB_Code'].astype(str).str.strip().isin(filtered_codes)].copy() if filtered_codes else contacts_df.copy()
        TST_COL = 'Result tuberculin skin test (TST)  #1 MM'
 
        total_contacts = len(cdf)
        unique_cases   = cdf['TB_Code'].nunique()
        tst_pos   = int((cdf[TST_COL].astype(str).str.strip().str.lower() == 'positive').sum()) if TST_COL in cdf.columns else 0
        on_inh    = int((cdf['Intervention'].astype(str).str.strip().str.upper() == 'INH').sum()) if 'Intervention' in cdf.columns else 0
        is_case   = int((cdf['Is he/she a Case?'].astype(str).str.strip().str.lower() == 'yes').sum()) if 'Is he/she a Case?' in cdf.columns else 0
 
        # ── حساب أرقام الرئوي والمخالطين ──────────────────────────────────
        pulm_all       = fdf[fdf['Final Dis'] == 'Pulmonary'] if 'Final Dis' in fdf.columns else fdf
        n_pulm_all     = len(pulm_all)
        n_have_contacts = int((pulm_all['Patient Have Contacts'] == 'Yes').sum()) if 'Patient Have Contacts' in pulm_all.columns else 0
        n_no_contacts   = int((pulm_all['Patient Have Contacts'] == 'No').sum())  if 'Patient Have Contacts' in pulm_all.columns else 0
        screened_n      = len(screened_codes)
        n_not_yet_scr   = n_have_contacts - screened_n if n_have_contacts >= screened_n else 0
 
        pct_have  = n_have_contacts / n_pulm_all * 100 if n_pulm_all else 0
        pct_no    = n_no_contacts   / n_pulm_all * 100 if n_pulm_all else 0
        pct_scr   = screened_n      / n_have_contacts * 100 if n_have_contacts else 0
        pct_notsc = n_not_yet_scr   / n_have_contacts * 100 if n_have_contacts else 0
 
        # ── PULMONARY CASES — CONTACT SCREENING STATUS ─────────────────────
        st.markdown(f"""
        <div style="font-size:0.60rem;font-weight:700;color:{GRAY_MED};
                    text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;">
          Pulmonary Cases — Contact Screening Status
        </div>""", unsafe_allow_html=True)
 
        pulm_cols = st.columns(5, gap="small")
        for col, (label, val, sub) in zip(pulm_cols, [
            ("Pulmonary Cases",   f"{n_pulm_all}",    "total pulmonary"),
            ("Have Contacts",     f"{n_have_contacts}", f"{pct_have:.0f}% of pulmonary"),
            ("No Contacts",       f"{n_no_contacts}",  f"{pct_no:.0f}% of pulmonary"),
            ("Screened",          f"{screened_n}",     f"{pct_scr:.0f}% of have-contacts"),
            ("Not Yet Screened",  f"{n_not_yet_scr}",  f"{pct_notsc:.0f}% pending"),
        ]):
            with col:
                st.markdown(f"""<div class="kpi-card">
                  <div class="kpi-value">{val}</div>
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)
 
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
 
        # ── مؤشر فحص المخالطين العام ──────────────────────────────────────
        scr_rate    = screened_n / n_pulm_all * 100 if n_pulm_all else 0
 
        if scr_rate >= 80:
            ind_color, ind_bg, ind_label = GREEN,   "#E8F8EF", "Good"
        elif scr_rate >= 60:
            ind_color, ind_bg, ind_label = AMBER,   "#FEF3E2", "Needs Improvement"
        else:
            ind_color, ind_bg, ind_label = RED,     "#FDECEA", "Critical"
 
        st.markdown(f"""
        <div style="background:{ind_bg};border:2px solid {ind_color};border-radius:14px;
                    padding:22px 32px;margin-bottom:20px;
                    display:flex;align-items:center;justify-content:space-between;
                    box-shadow:none;border:none;">
          <div>
            <div style="font-size:0.68rem;font-weight:700;color:{GRAY_MED};
                        text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">
              General Contact Screening Indicator
            </div>
            <div style="font-size:0.80rem;color:{GRAY_DARK};">
              <b style="color:{NAVY_MED}">{screened_n}</b> screened out of
              <b style="color:{NAVY_MED}">{n_pulm_all}</b> registered pulmonary cases
            </div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:3.2rem;font-weight:800;color:{ind_color};line-height:1;">
              {scr_rate:.1f}%
            </div>
            <div style="font-size:0.72rem;font-weight:700;color:{ind_color};
                        background:white;border-radius:6px;padding:3px 12px;
                        display:inline-block;margin-top:4px;border:1.5px solid {ind_color};">
              {ind_label}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
 
        st.markdown(f"""
        <div style="font-size:0.60rem;font-weight:700;color:{GRAY_MED};
                    text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;">
          Contact Overview
        </div>""", unsafe_allow_html=True)
        krow = st.columns(4, gap="small")
        for col, (label, val, sub) in zip(krow, [
            ("Total Contacts",    f"{total_contacts:,}", f"from {unique_cases} cases"),
            ("TST Positive",      f"{tst_pos:,}",        f"{tst_pos/total_contacts*100:.0f}% of contacts"),
            ("On INH Therapy",    f"{on_inh:,}",         f"{on_inh/total_contacts*100:.0f}% of contacts"),
            ("Converted to Case", f"{is_case:,}",        ""),
        ]):
            with col:
                st.markdown(f"""<div class="kpi-card">
                  <div class="kpi-value">{val}</div>
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-sub">{sub if sub else "&nbsp;"}</div>
                </div>""", unsafe_allow_html=True)
 
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
 
        ch1, ch2, ch3 = st.columns(3, gap="large")
        with ch1:
            st.markdown('<div class="chart-card"><div class="card-title">Contact Type</div>',
                        unsafe_allow_html=True)
            ct_df = cdf['Contact Type'].value_counts().reset_index()
            ct_df.columns = ['Type', 'Count']
            fig = px.pie(ct_df, names='Type', values='Count',
                         color_discrete_sequence=[BLUE_MED, TEAL, "#8B5CF6", GRAY_MED], hole=0.48)
            fig.update_traces(textfont_size=10)
            fig.update_layout(paper_bgcolor=WHITE, height=255,
                              margin=dict(t=6, b=6, l=6, r=6),
                              legend=dict(font=dict(size=9)))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with ch2:
            st.markdown('<div class="chart-card"><div class="card-title">TST Result</div>',
                        unsafe_allow_html=True)
            if TST_COL in cdf.columns:
                tst_df = cdf[TST_COL].value_counts().reset_index()
                tst_df.columns = ['Result', 'Count']
                tst_colors = {'Positive': AMBER, 'Negative': GREEN, 'Not_Done': GRAY_MED}
                fig = px.pie(tst_df, names='Result', values='Count', color='Result',
                             color_discrete_map={k: tst_colors.get(k, BLUE_MED) for k in tst_df['Result']},
                             hole=0.48)
                fig.update_traces(textfont_size=10)
                fig.update_layout(paper_bgcolor=WHITE, height=255,
                                  margin=dict(t=6, b=6, l=6, r=6),
                                  legend=dict(font=dict(size=9)))
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with ch3:
            st.markdown('<div class="chart-card"><div class="card-title">Contacts per Case (Top 15)</div>',
                        unsafe_allow_html=True)
            cc = cdf.groupby('TB_Code').size().reset_index(name='N')
            cc = cc.sort_values('N', ascending=False).head(15)
            fig = px.bar(cc, x='N', y='TB_Code', orientation='h',
                         color='N', color_continuous_scale=BLUE_SCALE, text='N')
            fig.update_traces(textposition='outside', textfont_size=9)
            fig = base_layout(fig, height=330, margin=dict(t=6, b=16, l=6, r=40))
            fig.update_layout(bargap=0.22, coloraxis_showscale=False,
                              yaxis=dict(autorange='reversed', title=''),
                              xaxis=dict(title='Contacts'))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        # Sector chart
        if 'sector' in cdf.columns:
            st.markdown('<div class="chart-card"><div class="card-title">Contacts by Sector</div>',
                        unsafe_allow_html=True)
            sec_df = cdf['sector'].dropna().value_counts().reset_index()
            sec_df.columns = ['Sector', 'Count']
            fig_sec = px.bar(sec_df, x='Sector', y='Count',
                             color='Count', color_continuous_scale=BLUE_SCALE, text='Count')
            fig_sec.update_traces(textposition='outside', textfont_size=11)
            fig_sec = base_layout(fig_sec, height=280, margin=dict(t=6, b=45, l=6, r=6))
            fig_sec.update_layout(bargap=0.38, coloraxis_showscale=False,
                                  xaxis=dict(title='Sector'), yaxis=dict(title='Contacts'))
            st.plotly_chart(fig_sec, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        # Screened contacts KPI (from verification sheet)
        n_registered  = len(registered_codes)
        n_screened    = len([c for c in screened_codes if c in set(cdf['TB_Code'].astype(str).str.strip())])
        n_not_screened = n_registered - len(screened_codes)
 
        st.markdown('<div class="section-title">Contact Screening Status</div>', unsafe_allow_html=True)
        scr_cols = st.columns(3, gap="small")
        for col, (label, val, sub) in zip(scr_cols, [
            ("Registered Cases",  f"{n_registered:,}",   "cases with contacts recorded"),
            ("Screened",          f"{len(screened_codes):,}", f"{len(screened_codes)/n_registered*100:.0f}% of registered" if n_registered else ""),
            ("Not Yet Screened",  f"{n_not_screened:,}", f"{n_not_screened/n_registered*100:.0f}% pending" if n_registered else ""),
        ]):
            with col:
                st.markdown(f"""<div class="kpi-card">
                  <div class="kpi-value">{val}</div>
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-sub">{sub if sub else "&nbsp;"}</div>
                </div>""", unsafe_allow_html=True)
 
        # ── Cases Not Yet Screened ─────────────────────────────────────────
        st.markdown('<div class="section-title">Cases Not Yet Screened</div>', unsafe_allow_html=True)
        if 'Final Dis' in fdf.columns and 'Patient Have Contacts' in fdf.columns:
            screened_set = set(str(c).strip() for c in screened_codes)
            pulm_have_contacts = fdf[
                (fdf['Final Dis'] == 'Pulmonary') &
                (fdf['Patient Have Contacts'] == 'Yes')
            ].copy()
            not_yet = pulm_have_contacts[
                ~pulm_have_contacts['TB code'].astype(str).str.strip().isin(screened_set)
            ].copy()
            n_not_yet = len(not_yet)
            st.markdown(
                f"<p style='font-size:0.78rem;color:{GRAY_MED};margin-bottom:10px;'>"
                f"<b style='color:{RED};'>{n_not_yet}</b> pulmonary cases with contacts not yet screened</p>",
                unsafe_allow_html=True
            )
            if n_not_yet > 0:
                show_cols = [c for c in ['TB code', 'Name', 'Treatment Hospital', 'Code Status', 'Patient Have Contacts'] if c in not_yet.columns]
                st.dataframe(not_yet[show_cols].reset_index(drop=True),
                             use_container_width=True,
                             height=min(520, 56 + n_not_yet * 38),
                             hide_index=True)
                st.download_button(
                    "Download — Cases Not Yet Screened",
                    data=not_yet[show_cols].to_csv(index=False, encoding='utf-8-sig'),
                    file_name="cases_not_yet_screened.csv",
                    mime="text/csv"
                )
            else:
                st.success("All pulmonary cases with contacts have been screened.")
 
        # Case Lookup
        st.markdown('<div class="section-title">Case Lookup</div>', unsafe_allow_html=True)
        all_codes = sorted(cdf['TB_Code'].dropna().unique().tolist())
        search_code = st.text_input("", placeholder="Type a TB code to search…",
                                     label_visibility="collapsed")
        matched = [c for c in all_codes if search_code.strip().lower() in str(c).lower()] \
                  if search_code.strip() else all_codes
 
        if not matched:
            st.warning(f"No case found matching '{search_code}'")
        else:
            sel_code = st.selectbox(
                f"{len(matched)} matching code(s)" if search_code.strip() else "Select Case Code",
                matched, label_visibility="collapsed"
            )
            case_contacts = cdf[cdf['TB_Code'] == sel_code].copy().reset_index(drop=True)
            n_case = len(case_contacts)
 
            tst_pos_c = int((case_contacts[TST_COL].astype(str).str.strip().str.lower() == 'positive').sum()) if TST_COL in case_contacts.columns else 0
            inh_c     = int((case_contacts['Intervention'].astype(str).str.strip().str.upper() == 'INH').sum()) if 'Intervention' in case_contacts.columns else 0
            symp_c    = int((case_contacts['Is he/she complaining of TB symptoms?'].astype(str).str.strip().str.lower() == 'yes').sum()) if 'Is he/she complaining of TB symptoms?' in case_contacts.columns else 0
            hh_c      = int((case_contacts['Contact Type'].astype(str).str.strip().str.lower() == 'household contact').sum()) if 'Contact Type' in case_contacts.columns else 0
            work_c    = int((case_contacts['Contact Type'].astype(str).str.strip().str.lower() == 'work contacts').sum()) if 'Contact Type' in case_contacts.columns else 0
 
            st.markdown(f"""
            <div class="contact-profile">
              <h3>Case Code: {sel_code}</h3>
              <div class="info-row">
                <div class="info-item"><div class="label">Total Contacts</div>
                  <div class="value">{n_case}</div></div>
                <div class="info-item"><div class="label">Household</div>
                  <div class="value">{hh_c}</div></div>
                <div class="info-item"><div class="label">Work</div>
                  <div class="value">{work_c}</div></div>
                <div class="info-item"><div class="label">TST Positive</div>
                  <div class="value amber">{tst_pos_c}</div></div>
                <div class="info-item"><div class="label">On INH</div>
                  <div class="value blue">{inh_c}</div></div>
                <div class="info-item"><div class="label">Symptomatic</div>
                  <div class="value red">{symp_c}</div></div>
              </div>
            </div>""", unsafe_allow_html=True)
 
            display_cols = ['Name', 'Age', 'Gender', 'Contact Type',
                            'Is he/she complaining of TB symptoms?',
                            TST_COL, 'Is he/she a Case?', 'Intervention',
                            'Completed Prevention Therapy?',
                            'Health Eduucation for contact', 'Remarks']
            display_cols = [c for c in display_cols if c in case_contacts.columns]
 
            st.markdown(f"<p style='font-size:0.73rem;color:{GRAY_MED};margin-bottom:8px;'>"
                        f"Showing <b>{n_case}</b> contact(s) for case <b>{sel_code}</b></p>",
                        unsafe_allow_html=True)
            st.dataframe(case_contacts[display_cols], use_container_width=True,
                         height=min(420, 56 + n_case * 38), hide_index=True)
            st.download_button(f"Download contacts for {sel_code}",
                               data=case_contacts.to_csv(index=False, encoding='utf-8-sig'),
                               file_name=f"contacts_{sel_code}.csv", mime="text/csv")
 
# ════════════════════════════════════════════════════════════════════════════════
# PAGE 6 — Raw Data
# ════════════════════════════════════════════════════════════════════════════════
elif clean_page == "Raw Data":
    st.markdown('<div class="page-title">Raw Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="card-title">All Records</div>',
                unsafe_allow_html=True)
    search = st.text_input("", placeholder="Search records by name, code, hospital…",
                            label_visibility="collapsed")
    disp = fdf.copy()
    if search:
        mask = disp.astype(str).apply(lambda c: c.str.contains(search, case=False, na=False)).any(axis=1)
        disp = disp[mask]
    st.markdown(f"<p style='font-size:0.73rem;color:{GRAY_MED};'>Showing <b>{len(disp):,}</b> records</p>",
                unsafe_allow_html=True)
    st.dataframe(disp, use_container_width=True, height=500)
    st.download_button("Download CSV", data=disp.to_csv(index=False, encoding='utf-8-sig'),
                       file_name="tb_cases_filtered.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:14px 0 4px 0;border-top:1px solid {BORDER};margin-top:20px;">
  <span style="font-size:0.66rem;color:{GRAY_LT};">
    TB Cases Dashboard · First Health Cluster · 2026
  </span>
</div>""", unsafe_allow_html=True)