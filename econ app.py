"""
SETP 3113 - Petroleum Economics | Topic 15
Future of Malaysia's Petroleum Industry in a Low-Carbon World
Interactive Dashboard — reads from Malaysia_LowCarbon_Data.xlsx

HOW TO RUN:
1. pip install -r requirements.txt
2. Place Malaysia_LowCarbon_Data.xlsx in the same folder as this script
3. streamlit run app.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# ─── Page config ───
st.set_page_config(
    page_title="Malaysia Low-Carbon Dashboard | SETP 3113",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───
st.markdown("""
<style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
    h1 { color: #0f172a; font-size: 26px !important; }
    h2 { color: #1a365d; font-size: 20px !important; }
    h3 { color: #1a365d; font-size: 16px !important; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: 500; }
    div[data-testid="stExpander"] { border: 1px solid #e2e8f0; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Colors ───
NAVY = "#1a365d"
GREEN = "#16a34a"
EMERALD = "#059669"
TEAL = "#0d9488"
AMBER = "#d97706"
BLUE = "#3b82f6"
SLATE = "#64748b"
COAL = "#334155"
OIL = "#78716c"
RED = "#dc2626"

# ════════════════════════════════════════════════════════════════
# LOAD DATA FROM EXCEL
# ════════════════════════════════════════════════════════════════

XLSX = "Malaysia_LowCarbon_Data.xlsx"

if not os.path.exists(XLSX):
    st.error(f"❌ File '{XLSX}' not found. Place it in the same folder as app.py and reload.")
    st.stop()

@st.cache_data
def load_all_sheets():
    """Load every sheet from the workbook, skipping the title row (row 1)."""
    data = {}

    # --- Primary_Energy_Mix_2023 ---
    df = pd.read_excel(XLSX, sheet_name="Primary_Energy_Mix_2023", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df = df[~df.iloc[:, 0].astype(str).str.startswith(("Total", "Source:"))]
    df.columns = ["Source", "Share", "Category"]
    df["Share"] = pd.to_numeric(df["Share"], errors="coerce")
    df = df.dropna(subset=["Share"])
    df["Share_pct"] = (df["Share"] * 100).round(1)
    data["energy_mix_2023"] = df

    # --- Electricity_Mix_2023 ---
    df = pd.read_excel(XLSX, sheet_name="Electricity_Mix_2023", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df.columns = ["Source", "Share", "Source_Ref"]
    df["Share"] = pd.to_numeric(df["Share"], errors="coerce")
    df = df.dropna(subset=["Share"])
    df["Share_pct"] = (df["Share"] * 100).round(1)
    data["elec_mix_2023"] = df

    # --- RE_Capacity_Targets ---
    df = pd.read_excel(XLSX, sheet_name="RE_Capacity_Targets", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df = df[~df.iloc[:, 0].astype(str).str.startswith("Note")]
    df.columns = ["Milestone", "RE_Share", "Policy_Source"]
    df["RE_Share"] = pd.to_numeric(df["RE_Share"], errors="coerce")
    df = df.dropna(subset=["RE_Share"])
    df["RE_pct"] = (df["RE_Share"] * 100).round(0).astype(int)
    # extract numeric year for chart x-axis
    df["Year"] = df["Milestone"].str.extract(r"(\d{4})").astype(int)
    data["re_targets"] = df

    # --- Generation_Mix_2050 ---
    df = pd.read_excel(XLSX, sheet_name="Generation_Mix_2050", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df = df[~df.iloc[:, 0].astype(str).str.startswith("Total")]
    df.columns = ["Source", "Share", "Type"]
    df["Share"] = pd.to_numeric(df["Share"], errors="coerce")
    df = df.dropna(subset=["Share"])
    df["Share_pct"] = (df["Share"] * 100).round(0).astype(int)
    data["gen_mix_2050"] = df

    # --- Emissions_Targets ---
    df = pd.read_excel(XLSX, sheet_name="Emissions_Targets", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df.columns = ["Target", "Value", "Source"]
    data["emissions"] = df

    # --- CCS_Kasawari ---
    df = pd.read_excel(XLSX, sheet_name="CCS_Kasawari", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df.columns = ["Metric", "Value", "Source"]
    data["kasawari"] = df

    # --- NETR_Investment ---
    df = pd.read_excel(XLSX, sheet_name="NETR_Investment", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df.columns = ["Item", "Value_RM", "Source"]
    data["investment"] = df

    # --- Key_Indicators ---
    df = pd.read_excel(XLSX, sheet_name="Key_Indicators", header=2)
    df = df.dropna(subset=[df.columns[0]])
    df.columns = ["Indicator", "Value", "Source"]
    data["indicators"] = df

    # --- Sources ---
    df = pd.read_excel(XLSX, sheet_name="Sources", header=2)
    df = df.dropna(subset=[df.columns[1]])
    df.columns = ["#", "Source", "URL"]
    data["sources"] = df

    return data

data = load_all_sheets()

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🎓 SETP 3113")
    st.markdown("**Petroleum Economics**")
    st.markdown("---")
    st.markdown("**Topic 15**")
    st.markdown("Future of Malaysia's Petroleum Industry in a Low-Carbon World")
    st.markdown("---")
    st.markdown("**Data file:**")
    st.code(XLSX, language=None)
    st.caption(f"Sheets loaded: {len(data)}")
    st.markdown("---")
    st.markdown("**Data sources:**")
    for _, row in data["sources"].iterrows():
        st.caption(f"[{int(row['#'])}] {row['Source']}")
    st.markdown("---")
    st.caption("Built with Streamlit + Plotly")

# ════════════════════════════════════════════════════════════════
# HEADER + KPIs
# ════════════════════════════════════════════════════════════════

st.markdown("# ⚡ Future of Malaysia's Petroleum Industry in a Low-Carbon World")
st.caption("SETP 3113 — Petroleum Economics | Topic 15 Interactive Dashboard")
st.markdown("---")

# Pull KPI values from the data
kasawari_cap = data["kasawari"].loc[data["kasawari"]["Metric"].str.contains("Annual", case=False), "Value"].values
kasawari_val = kasawari_cap[0] if len(kasawari_cap) > 0 else "3.7 MTPA"

inv_green = data["investment"].loc[data["investment"]["Item"].str.contains("Green investment", case=False), "Value_RM"].values
inv_val = inv_green[0] if len(inv_green) > 0 else "637 billion"

k1, k2, k3, k4 = st.columns(4)
k1.metric("🎯 Net-Zero Target", "2050", help="National GHG commitment under NETR")
k2.metric("⚡ RE Capacity Target", f"{data['re_targets']['RE_pct'].max()}%", help="Installed capacity by 2050 (NETR)")
k3.metric("🏭 Kasawari CCS", str(kasawari_val), help="World's largest offshore CCS project")
k4.metric("💰 Green Investment", f"RM {inv_val}", help="Total needed to reach 70% RE (MIDA)")

st.markdown("")

# ════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🔋 Energy Mix",
    "💰 Investment & Economy",
    "📋 Data Tables",
])

# ──────────── TAB 1: OVERVIEW ────────────
with tab1:
    st.markdown("## Renewable Energy Installed-Capacity Trajectory")
    st.caption("From 25% actual (2023) to 70% by 2050 — NETR / MyRER policy targets")

    re = data["re_targets"]
    fig_re = go.Figure()
    fig_re.add_trace(go.Scatter(
        x=re["Year"], y=re["RE_pct"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in re["RE_pct"]],
        textposition="top center",
        textfont=dict(size=13, color=GREEN, family="Arial Black"),
        line=dict(color=GREEN, width=3),
        marker=dict(size=10, color=GREEN, line=dict(color="white", width=2)),
        fill="tozeroy",
        fillcolor="rgba(22,163,74,0.08)",
        hovertemplate="Year: %{x}<br>RE Share: %{y}%<extra></extra>",
    ))
    fig_re.update_layout(
        yaxis=dict(range=[0, 85], title="RE Share of Installed Capacity (%)", gridcolor="#eee"),
        xaxis=dict(title="Year", dtick=5, gridcolor="#eee"),
        height=380, margin=dict(t=30, b=40, l=60, r=30),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig_re, use_container_width=True)

    # Side-by-side donuts: 2023 vs 2050
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Primary Energy Mix, 2023")
        em = data["energy_mix_2023"]
        fossil_total = em.loc[em["Category"] == "Fossil", "Share_pct"].sum()
        st.caption(f"Fossil fuels dominate at ~{fossil_total:.0f}% of total primary energy supply (WEC 2025)")
        color_map_e = {"Natural Gas": BLUE, "Crude Oil & Petroleum": OIL, "Coal & Coke": COAL, "Renewables": GREEN}
        fig_e = go.Figure(go.Pie(
            labels=em["Source"], values=em["Share_pct"],
            hole=0.5, marker=dict(colors=[color_map_e.get(s, SLATE) for s in em["Source"]]),
            textinfo="label+percent", textposition="outside", textfont=dict(size=12),
            hovertemplate="%{label}: %{value}%<extra></extra>",
        ))
        fig_e.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20),
                            showlegend=False, paper_bgcolor="white")
        st.plotly_chart(fig_e, use_container_width=True)

    with col2:
        st.markdown("### Projected Generation Mix, 2050")
        gm = data["gen_mix_2050"]
        re_total = gm.loc[gm["Type"] == "Renewable", "Share_pct"].sum()
        st.caption(f"RE rises to {re_total}%; gas remains as transition fuel (NETR / ISIS)")
        color_map_g = {"Solar": AMBER, "Natural Gas": SLATE, "Hydropower": BLUE, "Bioenergy": EMERALD}
        fig_g = go.Figure(go.Pie(
            labels=gm["Source"], values=gm["Share_pct"],
            hole=0.5, marker=dict(colors=[color_map_g.get(s, SLATE) for s in gm["Source"]]),
            textinfo="label+percent", textposition="outside", textfont=dict(size=12),
            hovertemplate="%{label}: %{value}%<extra></extra>",
        ))
        fig_g.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20),
                            showlegend=False, paper_bgcolor="white")
        st.plotly_chart(fig_g, use_container_width=True)

    # Decarbonisation targets
    st.markdown("### Decarbonisation Targets")
    st.caption("National and PETRONAS commitments driving the petroleum industry transition")

    em_df = data["emissions"]
    rows_per_col = 4
    d1, d2 = st.columns(2)
    for i, (_, row) in enumerate(em_df.iterrows()):
        target_col = d1 if i < rows_per_col else d2
        target_col.info(f"**{row['Target']}**\n\n### {row['Value']}\n{row['Source']}")


# ──────────── TAB 2: ENERGY MIX ────────────
with tab2:
    st.markdown("## Energy Mix Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Primary Energy Supply, 2023")
        em = data["energy_mix_2023"]
        color_map_bar = {"Natural Gas": BLUE, "Crude Oil & Petroleum": OIL, "Coal & Coke": COAL, "Renewables": GREEN}
        fig_b1 = go.Figure(go.Bar(
            x=em["Source"], y=em["Share_pct"],
            marker_color=[color_map_bar.get(s, SLATE) for s in em["Source"]],
            text=[f"{v}%" for v in em["Share_pct"]], textposition="outside",
            textfont=dict(size=12, family="Arial Black"),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        fig_b1.update_layout(yaxis=dict(range=[0, 58], title="%", gridcolor="#eee"),
                             height=350, margin=dict(t=20, b=40),
                             plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_b1, use_container_width=True)

    with col2:
        st.markdown("### Electricity Generation, 2023")
        el = data["elec_mix_2023"]
        color_map_el = {"Coal": COAL, "Natural Gas": BLUE, "Hydropower": TEAL, "Other / RE": GREEN}
        fig_b2 = go.Figure(go.Bar(
            x=el["Source"], y=el["Share_pct"],
            marker_color=[color_map_el.get(s, SLATE) for s in el["Source"]],
            text=[f"{v}%" for v in el["Share_pct"]], textposition="outside",
            textfont=dict(size=12, family="Arial Black"),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        fig_b2.update_layout(yaxis=dict(range=[0, 55], title="%", gridcolor="#eee"),
                             height=350, margin=dict(t=20, b=40),
                             plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_b2, use_container_width=True)

    # 2023 vs 2050 grouped bar
    st.markdown("### 2023 vs 2050: How the Generation Mix Shifts")
    st.caption("Side-by-side comparison — coal disappears, solar takes over")

    compare = pd.DataFrame({
        "Source": ["Coal", "Natural Gas", "Solar", "Hydropower", "Other RE / Bio"],
        "2023 (%)": [43, 36, 2, 17, 2],
        "2050 (%)": [0, 30, 58, 11, 1],
    })
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name="2023", x=compare["Source"], y=compare["2023 (%)"],
                              marker_color=COAL, text=[f"{v}%" for v in compare["2023 (%)"]],
                              textposition="outside", textfont=dict(size=11)))
    fig_comp.add_trace(go.Bar(name="2050 (projected)", x=compare["Source"], y=compare["2050 (%)"],
                              marker_color=GREEN, text=[f"{v}%" for v in compare["2050 (%)"]],
                              textposition="outside", textfont=dict(size=11)))
    fig_comp.update_layout(barmode="group", height=400,
                           yaxis=dict(range=[0, 70], title="%", gridcolor="#eee"),
                           margin=dict(t=30, b=40), plot_bgcolor="white", paper_bgcolor="white",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_comp, use_container_width=True)

    # Key indicators from sheet
    st.markdown("### Key Energy Indicators")
    ind = data["indicators"]
    cols = st.columns(min(len(ind), 4))
    for i, (_, row) in enumerate(ind.iterrows()):
        if i < len(cols):
            cols[i % len(cols)].metric(row["Indicator"][:35], row["Value"])


# ──────────── TAB 3: INVESTMENT ────────────
with tab3:
    st.markdown("## NETR Investment & Economic Impact")

    # Parse numeric values for chart
    inv = data["investment"].copy()

    def parse_rm(val):
        s = str(val).lower().replace(",", "").replace(">", "").strip()
        if "trillion" in s:
            nums = [float(x) for x in s.replace("trillion", "").replace("–", " ").replace("-", " ").split() if x.replace(".", "").isdigit()]
            return nums[0] * 1000 if nums else None
        elif "billion" in s:
            nums = [float(x) for x in s.replace("billion", "").replace("(private)", "").strip().split() if x.replace(".", "").isdigit()]
            return nums[0] if nums else None
        elif "million" in s:
            nums = [float(x) for x in s.replace("million", "").strip().split() if x.replace(".", "").isdigit()]
            return nums[0] / 1000 if nums else None
        else:
            try:
                return float(s.replace("billion", "").replace("million", "").strip())
            except ValueError:
                return None

    inv["RM_Billion"] = inv["Value_RM"].apply(parse_rm)
    inv_chart = inv.dropna(subset=["RM_Billion"]).sort_values("RM_Billion", ascending=True)

    st.markdown("### Investment Breakdown (RM Billion)")
    st.caption("Key NETR and Budget 2026 allocations — from your Excel data")

    chart_colors = [EMERALD, TEAL, BLUE, AMBER, GREEN, NAVY, RED, SLATE]
    fig_inv = go.Figure(go.Bar(
        y=inv_chart["Item"], x=inv_chart["RM_Billion"],
        orientation="h",
        marker_color=chart_colors[:len(inv_chart)],
        text=[f"RM {v:.1f}B" if v >= 1 else f"RM {v*1000:.0f}M" for v in inv_chart["RM_Billion"]],
        textposition="outside", textfont=dict(size=12, family="Arial Black"),
        hovertemplate="%{y}<br>RM %{x:.1f} billion<extra></extra>",
    ))
    fig_inv.update_layout(
        xaxis=dict(title="RM Billion", gridcolor="#eee"),
        height=max(350, len(inv_chart) * 45 + 80),
        margin=dict(t=20, b=40, l=280, r=80),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig_inv, use_container_width=True)

    # Full investment table
    st.markdown("### All NETR Investment Figures")
    st.dataframe(data["investment"], use_container_width=True, hide_index=True)

    # Transition levers
    st.markdown("### NETR Six Energy Transition Levers")
    st.caption("Structured into 10 flagship catalyst projects (EPU / MIDA)")
    l1, l2, l3 = st.columns(3)
    l1.success("⚡ **Energy Efficiency**\n\nReduce energy intensity across industry and buildings")
    l2.success("☀️ **Renewable Energy**\n\n70% of installed capacity by 2050; solar-led growth")
    l3.success("🔬 **Hydrogen Economy**\n\nGreen hydrogen for industrial decarbonisation")
    l4, l5, l6 = st.columns(3)
    l4.info("🌿 **Bioenergy**\n\nB12 biodiesel blend; biomass and biogas expansion")
    l5.info("🚗 **Green Mobility**\n\nEV adoption; charging infrastructure along highways")
    l6.info("🏭 **CCUS**\n\nKasawari CCS (3.7 MTPA); CCUS Bill 2025")

    # Kasawari from sheet
    st.markdown("### Kasawari CCS Project — Offshore Sarawak")
    st.caption("World's largest offshore carbon capture and storage project")
    kas = data["kasawari"]
    kas_cols = st.columns(min(len(kas), 3))
    for i, (_, row) in enumerate(kas.iterrows()):
        if i < len(kas_cols):
            kas_cols[i % len(kas_cols)].metric(row["Metric"][:30], row["Value"])


# ──────────── TAB 4: DATA TABLES ────────────
with tab4:
    st.markdown("## Raw Data Tables")
    st.caption(f"All data loaded from **{XLSX}** — verify numbers and download as needed")

    sheet_labels = {
        "energy_mix_2023": "📊 Primary Energy Mix 2023",
        "elec_mix_2023": "⚡ Electricity Generation Mix 2023",
        "re_targets": "📈 RE Capacity Targets (NETR / MyRER)",
        "gen_mix_2050": "🔮 Projected Generation Mix 2050",
        "emissions": "🎯 Decarbonisation Targets",
        "kasawari": "🏭 Kasawari CCS Project",
        "investment": "💰 NETR Investment Figures",
        "indicators": "📊 Key Energy Indicators",
    }

    for key, label in sheet_labels.items():
        with st.expander(label, expanded=False):
            st.dataframe(data[key], use_container_width=True, hide_index=True)

    # References
    st.markdown("---")
    st.markdown("### References")
    for _, row in data["sources"].iterrows():
        st.caption(f"[{int(row['#'])}] {row['Source']} — {row['URL']}")


# ─── Footer ───
st.markdown("---")
st.caption("SETP 3113 Petroleum Economics | Topic 15 | Data: Malaysia_LowCarbon_Data.xlsx | Built with Streamlit + Plotly | UTM")
