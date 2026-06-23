"""
SETP 3113 - Petroleum Economics | Topic 15
Future of Malaysia's Petroleum Industry in a Low-Carbon World
Interactive Dashboard built with Streamlit + Plotly

HOW TO RUN:
1. Install requirements:  pip install streamlit plotly pandas
2. Run:                   streamlit run app.py
3. Browser opens at:      http://localhost:8501
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

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

# ─── Color palette ───
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
# DATA
# ════════════════════════════════════════════════════════════════

# 1. Primary energy mix 2023
energy_mix_2023 = pd.DataFrame({
    "Source": ["Natural Gas", "Crude Oil", "Coal & Coke", "Renewables"],
    "Share (%)": [47.0, 25.2, 23.6, 4.2],
    "Type": ["Fossil", "Fossil", "Fossil", "Clean"],
})

# 2. Electricity generation mix 2023
elec_mix_2023 = pd.DataFrame({
    "Source": ["Coal", "Natural Gas", "Hydropower", "Other RE"],
    "Share (%)": [43, 36, 17, 4],
})

# 3. RE capacity targets
re_targets = pd.DataFrame({
    "Year": [2023, 2025, 2030, 2035, 2040, 2045, 2050],
    "RE Share (%)": [25, 31, 35, 40, 50, 60, 70],
    "Status": ["Actual", "Target", "Target", "Target", "Target", "Target", "Target"],
})

# 4. Projected generation mix 2050
gen_mix_2050 = pd.DataFrame({
    "Source": ["Solar", "Natural Gas", "Hydropower", "Bioenergy"],
    "Share (%)": [58, 30, 11, 1],
    "Type": ["Renewable", "Fossil (transition)", "Renewable", "Renewable"],
})

# 5. NETR investment
investment = pd.DataFrame({
    "Item": [
        "Green investment (total to 2050)",
        "NETR flagship (Phase 1)",
        "GLIC/GLC RE (2026)",
        "LSS6 solar (~2 GW)",
        "CRESS programme",
        "Energy Transition Fund (2026)",
    ],
    "RM Billion": [637, 25, 16.5, 6, 3.5, 0.15],
    "Source": ["MIDA", "MIDA", "Budget 2026", "Budget 2026", "Budget 2026", "Budget 2026"],
})

# 6. Economic impact
econ_impact = pd.DataFrame({
    "Metric": [
        "Total investment opportunity by 2050",
        "Additional GDP contribution by 2050",
        "Green jobs by 2050",
        "GHG reduction (flagship projects)",
        "Flagship jobs (Phase 1)",
    ],
    "Value": ["RM 1.2 – 1.85 trillion", "RM 220 billion", "310,000", "10,000 Gg CO₂eq/yr", "23,000"],
    "Source": ["MIDA / NETR", "MIDA", "MIDA", "MIDA", "MIDA"],
})

# 7. Kasawari CCS
kasawari = pd.DataFrame({
    "Metric": [
        "Annual CO₂ capture/injection",
        "Total CO₂ stored (25 years)",
        "Share of global CCS (2021)",
        "First CO₂ injection",
        "Status",
    ],
    "Value": ["3.7 MTPA", "~80 Mt", "~9%", "End 2025 / 2026", "World's largest offshore CCS"],
    "Source": ["IPTC 2023", "IPTC 2023", "IPTC 2023", "PETRONAS", "IPTC 2023"],
})

# 8. Decarbonisation targets
decarb = pd.DataFrame({
    "Target": [
        "National net-zero GHG",
        "Carbon intensity cut (vs 2005 GDP)",
        "Energy-sector GHG reduction by 2050",
        "Coal phase-out",
        "PETRONAS net-zero carbon emissions",
        "PETRONAS operational emissions cap",
        "PETRONAS methane reduction (vs 2019)",
        "Energy sector share of national GHG",
    ],
    "Value": [
        "By 2050", "45% by 2030", "32% vs 2019 (4.3 t CO₂e/capita)",
        "By 2044", "By 2050", "49.5 Mt CO₂e",
        "50% by 2025", "~80%",
    ],
    "Source": [
        "NETR / 12MP", "NDC / NETR", "WEC 2025",
        "Min. NRES (2026)", "PETRONAS NZCE", "PETRONAS",
        "EIA / PETRONAS", "NETR / PwC",
    ],
})

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/UTM_LOGO_FULL.png/220px-UTM_LOGO_FULL.png", width=160)
    st.markdown("### SETP 3113")
    st.markdown("**Petroleum Economics**")
    st.markdown("---")
    st.markdown("**Topic 15**")
    st.markdown("Future of Malaysia's Petroleum Industry in a Low-Carbon World")
    st.markdown("---")
    st.markdown("**Data sources:**")
    st.caption(
        "EPU NETR (2023) · WEC Malaysia Trilemma (2025) · "
        "PETRONAS NZCE Pathway (2023) · MIDA · IPTC 2023 · "
        "Budget 2026 · The Edge / ISIS Malaysia · IRENA"
    )
    st.markdown("---")
    st.caption("Built with Streamlit + Plotly")

# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

st.markdown("# ⚡ Future of Malaysia's Petroleum Industry in a Low-Carbon World")
st.caption("SETP 3113 — Petroleum Economics | Topic 15 Interactive Dashboard")
st.markdown("---")

# ─── KPI Row ───
k1, k2, k3, k4 = st.columns(4)
k1.metric("🎯 Net-Zero Target", "2050", help="National GHG commitment under NETR")
k2.metric("⚡ RE Capacity Target", "70%", help="Installed capacity by 2050 (NETR)")
k3.metric("🏭 Kasawari CCS", "3.7 MT/yr", help="World's largest offshore CCS project")
k4.metric("💰 Green Investment", "RM 637B", help="Total needed to reach 70% RE (MIDA)")

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

    fig_re = go.Figure()
    fig_re.add_trace(go.Scatter(
        x=re_targets["Year"], y=re_targets["RE Share (%)"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in re_targets["RE Share (%)"]],
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
        xaxis=dict(title="Year", gridcolor="#eee"),
        height=380, margin=dict(t=30, b=40, l=60, r=30),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Arial", size=12),
    )
    st.plotly_chart(fig_re, use_container_width=True)

    # Side by side donuts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Primary Energy Mix, 2023")
        st.caption("Fossil fuels dominate at ~96% of total primary energy supply (WEC 2025)")
        fig_e23 = go.Figure(go.Pie(
            labels=energy_mix_2023["Source"], values=energy_mix_2023["Share (%)"],
            hole=0.5, marker=dict(colors=[BLUE, OIL, COAL, GREEN]),
            textinfo="label+percent", textposition="outside",
            textfont=dict(size=12),
            hovertemplate="%{label}: %{value}%<extra></extra>",
        ))
        fig_e23.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20),
                              showlegend=False, paper_bgcolor="white")
        st.plotly_chart(fig_e23, use_container_width=True)

    with col2:
        st.markdown("### Projected Generation Mix, 2050")
        st.caption("RE rises to 70%; gas remains as 30% transition fuel (NETR / ISIS)")
        fig_g50 = go.Figure(go.Pie(
            labels=gen_mix_2050["Source"], values=gen_mix_2050["Share (%)"],
            hole=0.5, marker=dict(colors=[AMBER, SLATE, BLUE, EMERALD]),
            textinfo="label+percent", textposition="outside",
            textfont=dict(size=12),
            hovertemplate="%{label}: %{value}%<extra></extra>",
        ))
        fig_g50.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20),
                              showlegend=False, paper_bgcolor="white")
        st.plotly_chart(fig_g50, use_container_width=True)

    # Decarbonisation targets
    st.markdown("### Decarbonisation Targets")
    st.caption("National and PETRONAS commitments driving the petroleum industry transition")

    d1, d2, d3 = st.columns(3)
    d1.info("**Carbon intensity cut by 2030**\n\n# 45%\nvs 2005 GDP (NDC / NETR)")
    d2.info("**PETRONAS emissions cap**\n\n# 49.5 Mt CO₂e\nOperational cap by 2024")
    d3.info("**Coal phase-out**\n\n# 2044\nMin. NRES announcement (2026)")

    d4, d5, d6 = st.columns(3)
    d4.success("**GHG reduction by 2050**\n\n# 32%\nvs 2019 levels (WEC 2025)")
    d5.success("**Kasawari CCS (25-yr)**\n\n# ~80 Mt CO₂\nWorld's largest offshore (IPTC)")
    d6.success("**PETRONAS methane cut**\n\n# 50%\nvs 2019 by 2025")


# ──────────── TAB 2: ENERGY MIX ────────────
with tab2:
    st.markdown("## Energy Mix Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Primary Energy Supply, 2023")
        fig_bar_e = go.Figure(go.Bar(
            x=energy_mix_2023["Source"], y=energy_mix_2023["Share (%)"],
            marker_color=[BLUE, OIL, COAL, GREEN],
            text=[f"{v}%" for v in energy_mix_2023["Share (%)"]],
            textposition="outside", textfont=dict(size=12, family="Arial Black"),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        fig_bar_e.update_layout(
            yaxis=dict(range=[0, 55], title="%", gridcolor="#eee"),
            height=350, margin=dict(t=20, b=40), plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig_bar_e, use_container_width=True)

    with col2:
        st.markdown("### Electricity Generation, 2023")
        fig_bar_el = go.Figure(go.Bar(
            x=elec_mix_2023["Source"], y=elec_mix_2023["Share (%)"],
            marker_color=[COAL, BLUE, TEAL, GREEN],
            text=[f"{v}%" for v in elec_mix_2023["Share (%)"]],
            textposition="outside", textfont=dict(size=12, family="Arial Black"),
            hovertemplate="%{x}: %{y}%<extra></extra>",
        ))
        fig_bar_el.update_layout(
            yaxis=dict(range=[0, 55], title="%", gridcolor="#eee"),
            height=350, margin=dict(t=20, b=40), plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig_bar_el, use_container_width=True)

    # 2023 vs 2050 comparison
    st.markdown("### 2023 vs 2050: How the Mix Shifts")
    st.caption("Side-by-side comparison of energy generation sources")

    compare_data = pd.DataFrame({
        "Source": ["Coal", "Natural Gas", "Solar", "Hydropower", "Other RE / Bio"],
        "2023 (%)": [43, 36, 2, 17, 2],
        "2050 (%)": [0, 30, 58, 11, 1],
    })

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="2023", x=compare_data["Source"], y=compare_data["2023 (%)"],
        marker_color=COAL, text=[f"{v}%" for v in compare_data["2023 (%)"]],
        textposition="outside", textfont=dict(size=11),
    ))
    fig_comp.add_trace(go.Bar(
        name="2050 (projected)", x=compare_data["Source"], y=compare_data["2050 (%)"],
        marker_color=GREEN, text=[f"{v}%" for v in compare_data["2050 (%)"]],
        textposition="outside", textfont=dict(size=11),
    ))
    fig_comp.update_layout(
        barmode="group", height=380,
        yaxis=dict(range=[0, 70], title="%", gridcolor="#eee"),
        margin=dict(t=30, b=40), plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Key indicators
    st.markdown("### Key Energy Indicators")
    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Fossil share (2023)", "~96%")
    i2.metric("Gas share TPES (2050)", "56%")
    i3.metric("RE share TPES (2050)", "23%")
    i4.metric("RE generation today", "~5-6%")


# ──────────── TAB 3: INVESTMENT ────────────
with tab3:
    st.markdown("## NETR Investment & Economic Impact")

    # Investment bar chart
    st.markdown("### Energy Transition Investment Breakdown (RM Billion)")
    st.caption("Key NETR and Budget 2026 allocations")

    inv_sorted = investment.sort_values("RM Billion", ascending=True)
    fig_inv = go.Figure(go.Bar(
        y=inv_sorted["Item"], x=inv_sorted["RM Billion"],
        orientation="h",
        marker_color=[EMERALD, TEAL, BLUE, AMBER, GREEN, NAVY],
        text=[f"RM {v}B" for v in inv_sorted["RM Billion"]],
        textposition="outside", textfont=dict(size=12, family="Arial Black"),
        hovertemplate="%{y}<br>RM %{x} billion<extra></extra>",
    ))
    fig_inv.update_layout(
        xaxis=dict(title="RM Billion", gridcolor="#eee"),
        height=350, margin=dict(t=20, b=40, l=200, r=80),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig_inv, use_container_width=True)

    # Economic impact
    st.markdown("### Economic Impact by 2050")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Investment opportunity", "RM 1.2-1.85T")
    e2.metric("GDP contribution", "RM 220B")
    e3.metric("Green jobs", "310,000")
    e4.metric("GHG cut (flagships)", "10,000 Gg/yr")

    # Transition levers
    st.markdown("### NETR Six Energy Transition Levers")
    st.caption("Structured into 10 flagship catalyst projects (EPU / MIDA)")
    l1, l2, l3 = st.columns(3)
    l1.success("⚡ **Energy Efficiency (EE)**\n\nReduce energy intensity across industry and buildings")
    l2.success("☀️ **Renewable Energy (RE)**\n\n70% of installed capacity by 2050; solar-led growth")
    l3.success("🔬 **Hydrogen Economy**\n\nGreen hydrogen for industrial decarbonisation")
    l4, l5, l6 = st.columns(3)
    l4.info("🌿 **Bioenergy**\n\nB12 biodiesel blend; biomass and biogas expansion")
    l5.info("🚗 **Green Mobility**\n\nEV adoption; charging infrastructure along highways")
    l6.info("🏭 **CCUS**\n\nKasawari CCS (3.7 MTPA); CCUS Bill 2025")

    # Kasawari CCS detail
    st.markdown("### Kasawari CCS Project — Offshore Sarawak")
    st.caption("World's largest offshore carbon capture and storage project (IPTC 2023)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Annual CO₂ injection", "3.7 MTPA")
    c2.metric("Total stored (25 yrs)", "~80 Mt")
    c3.metric("Global CCS share", "~9%")


# ──────────── TAB 4: DATA TABLES ────────────
with tab4:
    st.markdown("## Raw Data Tables")
    st.caption("All data used in this dashboard — downloadable for your report")

    with st.expander("📊 Primary Energy Mix 2023", expanded=False):
        st.dataframe(energy_mix_2023, use_container_width=True, hide_index=True)

    with st.expander("⚡ Electricity Generation Mix 2023", expanded=False):
        st.dataframe(elec_mix_2023, use_container_width=True, hide_index=True)

    with st.expander("📈 RE Capacity Targets (NETR / MyRER)", expanded=False):
        st.dataframe(re_targets, use_container_width=True, hide_index=True)

    with st.expander("🔮 Projected Generation Mix 2050", expanded=False):
        st.dataframe(gen_mix_2050, use_container_width=True, hide_index=True)

    with st.expander("🏭 Kasawari CCS Project", expanded=False):
        st.dataframe(kasawari, use_container_width=True, hide_index=True)

    with st.expander("🎯 Decarbonisation Targets", expanded=False):
        st.dataframe(decarb, use_container_width=True, hide_index=True)

    with st.expander("💰 NETR Investment Figures", expanded=False):
        st.dataframe(investment, use_container_width=True, hide_index=True)

    with st.expander("📊 Economic Impact", expanded=False):
        st.dataframe(econ_impact, use_container_width=True, hide_index=True)

    # References
    st.markdown("---")
    st.markdown("### References")
    refs = [
        "EPU (2023). National Energy Transition Roadmap (NETR). Ministry of Economy, Malaysia.",
        "World Energy Council (2025). World Energy Trilemma — Malaysia Profile.",
        "MIDA (2024). NETR: Charting a Path to a Sustainable Energy Landscape.",
        "PETRONAS (2023). Pathway to Net Zero Carbon Emissions 2050 (3rd ed.).",
        "IPTC (2023). Kasawari CCS: Unfolding the Largest Offshore CCS Project.",
        "Chan, H.-Y. & Sopian, K. (2022). Phil. Trans. R. Soc. A. DOI: 10.1098/rsta.2021.0132",
        "Heliyon (2024). Economic & environmental analysis of Malaysia 2025 RE targets.",
        "Frontiers in Energy Research (2024). Carbon neutrality in Malaysia and KL.",
        "IRENA (2023). Malaysia Energy Transition Outlook.",
        "U.S. EIA (2024). Malaysia Country Analysis Brief.",
        "The Edge Malaysia / ISIS Malaysia (2025). 2050 generation mix breakdown.",
        "The Malaysian Reserve (2025). Budget 2026 energy-transition allocations.",
    ]
    for i, r in enumerate(refs, 1):
        st.caption(f"[{i}] {r}")

# ─── Footer ───
st.markdown("---")
st.caption("SETP 3113 Petroleum Economics | Topic 15 | Built with Streamlit + Plotly | Universiti Teknologi Malaysia")
