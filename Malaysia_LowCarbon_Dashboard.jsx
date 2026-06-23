import { useState } from "react";
import {
  PieChart, Pie, Cell, LineChart, Line, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  Legend, Area, AreaChart
} from "recharts";

const COLORS = {
  navy: "#1a365d",
  green: "#16a34a",
  emerald: "#059669",
  teal: "#0d9488",
  amber: "#d97706",
  slate: "#64748b",
  coal: "#334155",
  oil: "#78716c",
  red: "#dc2626",
  lightGreen: "#bbf7d0",
  lightBlue: "#dbeafe",
  bg: "#f8fafc",
  cardBg: "#ffffff",
  border: "#e2e8f0",
  textPrimary: "#0f172a",
  textSecondary: "#64748b",
  textMuted: "#94a3b8",
};

const energyMix2023 = [
  { name: "Natural gas", value: 47.0, color: "#3b82f6" },
  { name: "Crude oil", value: 25.2, color: COLORS.oil },
  { name: "Coal", value: 23.6, color: COLORS.coal },
  { name: "Renewables", value: 4.2, color: COLORS.green },
];

const genMix2050 = [
  { name: "Solar", value: 58, color: COLORS.amber },
  { name: "Natural gas", value: 30, color: COLORS.slate },
  { name: "Hydropower", value: 11, color: "#3b82f6" },
  { name: "Bioenergy", value: 1, color: COLORS.emerald },
];

const reTrajectory = [
  { year: "2023", re: 25, label: "25% (actual)" },
  { year: "2025", re: 31, label: "31%" },
  { year: "2030", re: 35, label: "35%" },
  { year: "2035", re: 40, label: "40%" },
  { year: "2040", re: 50, label: "50%" },
  { year: "2050", re: 70, label: "70%" },
];

const investmentData = [
  { name: "Green investment\n(total to 2050)", value: 637, unit: "B" },
  { name: "NETR flagship\n(Phase 1)", value: 25, unit: "B" },
  { name: "GLIC/GLC RE\n(2026)", value: 16.5, unit: "B" },
  { name: "LSS6 solar\n(~2 GW)", value: 6, unit: "B" },
  { name: "Energy transition\nfund (2026)", value: 0.15, unit: "B" },
];

const elecMix2023 = [
  { name: "Coal", value: 43, color: COLORS.coal },
  { name: "Natural gas", value: 36, color: "#3b82f6" },
  { name: "Hydropower", value: 17, color: COLORS.teal },
  { name: "Other RE", value: 4, color: COLORS.green },
];

const CustomTooltip = ({ active, payload, suffix = "%" }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 8, padding: "8px 12px", fontSize: 13, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
      <p style={{ margin: 0, fontWeight: 500 }}>{payload[0].name || payload[0].payload?.name || payload[0].payload?.year}</p>
      <p style={{ margin: "2px 0 0", color: COLORS.textSecondary }}>{payload[0].value}{suffix}</p>
    </div>
  );
};

const PieLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
  const RADIAN = Math.PI / 180;
  const radius = outerRadius + 20;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  if (percent < 0.03) return null;
  return (
    <text x={x} y={y} fill={COLORS.textPrimary} textAnchor={x > cx ? "start" : "end"} dominantBaseline="central" fontSize={11} fontWeight={500}>
      {name} {(percent * 100).toFixed(1)}%
    </text>
  );
};

const KpiCard = ({ icon, label, value, sub, accent = COLORS.navy }) => (
  <div style={{ background: COLORS.cardBg, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: "18px 20px", borderTop: `3px solid ${accent}` }}>
    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
      <span style={{ fontSize: 18 }}>{icon}</span>
      <span style={{ fontSize: 11, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.6px", fontWeight: 600 }}>{label}</span>
    </div>
    <div style={{ fontSize: 28, fontWeight: 700, color: accent, lineHeight: 1.1 }}>{value}</div>
    <div style={{ fontSize: 11, color: COLORS.textSecondary, marginTop: 4 }}>{sub}</div>
  </div>
);

const SectionTitle = ({ children, sub }) => (
  <div style={{ marginBottom: 12 }}>
    <h3 style={{ fontSize: 15, fontWeight: 600, color: COLORS.textPrimary, margin: 0 }}>{children}</h3>
    {sub && <p style={{ fontSize: 11, color: COLORS.textSecondary, margin: "2px 0 0" }}>{sub}</p>}
  </div>
);

const ChartCard = ({ children, style = {} }) => (
  <div style={{ background: COLORS.cardBg, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20, ...style }}>
    {children}
  </div>
);

const TargetRow = ({ label, value, color = COLORS.navy }) => (
  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 14px", background: COLORS.bg, borderRadius: 8, borderLeft: `3px solid ${color}` }}>
    <span style={{ fontSize: 13, color: COLORS.textSecondary }}>{label}</span>
    <span style={{ fontSize: 17, fontWeight: 700, color }}>{value}</span>
  </div>
);

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif", background: COLORS.bg, minHeight: "100vh", padding: "0" }}>
      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #164e3e 100%)", padding: "28px 32px 20px", color: "#fff" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLORS.green }} />
          <span style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "1.5px", opacity: 0.7, fontWeight: 600 }}>SETP 3113 — Petroleum economics</span>
        </div>
        <h1 style={{ fontSize: 22, fontWeight: 700, margin: "4px 0 2px", letterSpacing: "-0.3px" }}>
          Future of Malaysia's petroleum industry in a low-carbon world
        </h1>
        <p style={{ fontSize: 13, opacity: 0.6, margin: 0 }}>Topic 15 — Data sources: NETR (EPU), WEC, PETRONAS, IRENA, MIDA, Budget 2026</p>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 0, borderBottom: `1px solid ${COLORS.border}`, background: COLORS.cardBg, padding: "0 32px" }}>
        {["overview", "energy mix", "investments"].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            style={{ padding: "12px 20px", fontSize: 13, fontWeight: activeTab === tab ? 600 : 400, color: activeTab === tab ? COLORS.navy : COLORS.textSecondary, background: "none", border: "none", borderBottom: activeTab === tab ? `2px solid ${COLORS.navy}` : "2px solid transparent", cursor: "pointer", textTransform: "capitalize", transition: "all 0.2s" }}>
            {tab}
          </button>
        ))}
      </div>

      <div style={{ padding: "20px 32px 32px" }}>
        {/* KPI Row — always visible */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 20 }}>
          <KpiCard icon="🎯" label="Net-zero target" value="2050" sub="National GHG commitment" accent={COLORS.navy} />
          <KpiCard icon="⚡" label="RE capacity target" value="70%" sub="Installed capacity by 2050" accent={COLORS.green} />
          <KpiCard icon="🏭" label="Kasawari CCS" value="3.7 MT/yr" sub="World's largest offshore CCS" accent={COLORS.teal} />
          <KpiCard icon="💰" label="Green investment" value="RM637B" sub="Needed to reach 70% RE" accent={COLORS.amber} />
        </div>

        {/* OVERVIEW TAB */}
        {activeTab === "overview" && (
          <>
            {/* RE Trajectory — hero chart */}
            <ChartCard style={{ marginBottom: 16 }}>
              <SectionTitle sub="From 25% actual (2023) to 70% by 2050 under NETR / MyRER policy targets">
                Renewable energy installed-capacity trajectory
              </SectionTitle>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={reTrajectory} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <defs>
                    <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={COLORS.green} stopOpacity={0.2} />
                      <stop offset="95%" stopColor={COLORS.green} stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="year" tick={{ fontSize: 12, fill: COLORS.textSecondary }} />
                  <YAxis tick={{ fontSize: 12, fill: COLORS.textSecondary }} domain={[0, 80]} tickFormatter={v => v + "%"} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="re" stroke={COLORS.green} strokeWidth={3} fill="url(#gGreen)" dot={{ r: 5, fill: COLORS.green, stroke: "#fff", strokeWidth: 2 }}
                    label={({ x, y, value }) => <text x={x} y={y - 14} textAnchor="middle" fill={COLORS.green} fontSize={12} fontWeight={600}>{value}%</text>} />
                </AreaChart>
              </ResponsiveContainer>
            </ChartCard>

            {/* Side by side: 2023 mix vs targets */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
              <ChartCard>
                <SectionTitle sub="Fossil fuels dominate at ~96% of total primary energy supply">
                  Primary energy mix, 2023
                </SectionTitle>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie data={energyMix2023} dataKey="value" cx="50%" cy="50%" innerRadius={50} outerRadius={85} paddingAngle={2} labelLine={false} label={PieLabel}>
                      {energyMix2023.map((e, i) => <Cell key={i} fill={e.color} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard>
                <SectionTitle sub="RE rises to 70% of installed capacity; gas remains as transition fuel at 30%">
                  Projected generation mix, 2050
                </SectionTitle>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie data={genMix2050} dataKey="value" cx="50%" cy="50%" innerRadius={50} outerRadius={85} paddingAngle={2} labelLine={false} label={PieLabel}>
                      {genMix2050.map((e, i) => <Cell key={i} fill={e.color} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>

            {/* Decarbonisation targets */}
            <ChartCard>
              <SectionTitle sub="National and PETRONAS commitments driving the petroleum industry transition">
                Decarbonisation targets
              </SectionTitle>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                <TargetRow label="Carbon intensity cut by 2030" value="45%" color={COLORS.red} />
                <TargetRow label="PETRONAS emissions cap" value="49.5 Mt CO₂e" color={COLORS.navy} />
                <TargetRow label="Coal phase-out by" value="2044" color={COLORS.coal} />
                <TargetRow label="GHG reduction by 2050 (vs 2019)" value="32%" color={COLORS.emerald} />
                <TargetRow label="Kasawari CCS (25-yr total)" value="~80 Mt CO₂" color={COLORS.teal} />
                <TargetRow label="PETRONAS methane cut (vs 2019)" value="50%" color={COLORS.amber} />
              </div>
            </ChartCard>
          </>
        )}

        {/* ENERGY MIX TAB */}
        {activeTab === "energy mix" && (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
              <ChartCard>
                <SectionTitle sub="Total primary energy supply by source (WEC 2025)">
                  Primary energy mix, 2023
                </SectionTitle>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie data={energyMix2023} dataKey="value" cx="50%" cy="50%" innerRadius={55} outerRadius={95} paddingAngle={2} labelLine={false} label={PieLabel}>
                      {energyMix2023.map((e, i) => <Cell key={i} fill={e.color} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard>
                <SectionTitle sub="Electricity generation by source (WEC 2025)">
                  Electricity generation mix, 2023
                </SectionTitle>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie data={elecMix2023} dataKey="value" cx="50%" cy="50%" innerRadius={55} outerRadius={95} paddingAngle={2} labelLine={false} label={PieLabel}>
                      {elecMix2023.map((e, i) => <Cell key={i} fill={e.color} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>

            <ChartCard style={{ marginBottom: 16 }}>
              <SectionTitle sub="NETR / ISIS Malaysia breakdown — solar dominates at 58%">
                Projected electricity generation mix, 2050
              </SectionTitle>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={genMix2050} margin={{ top: 20, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: COLORS.textSecondary }} />
                  <YAxis tick={{ fontSize: 12, fill: COLORS.textSecondary }} tickFormatter={v => v + "%"} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]}
                    label={{ position: "top", fontSize: 12, fontWeight: 600, formatter: v => v + "%" }}>
                    {genMix2050.map((e, i) => <Cell key={i} fill={e.color} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard>
              <SectionTitle sub="Gas share of total primary energy supply projected to rise to 56% by 2050">
                Key energy indicators
              </SectionTitle>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
                <div style={{ background: COLORS.bg, borderRadius: 8, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 4 }}>Fossil share of TPES (2023)</div>
                  <div style={{ fontSize: 24, fontWeight: 700, color: COLORS.red }}>~96%</div>
                </div>
                <div style={{ background: COLORS.bg, borderRadius: 8, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 4 }}>Gas share by 2050</div>
                  <div style={{ fontSize: 24, fontWeight: 700, color: "#3b82f6" }}>56%</div>
                </div>
                <div style={{ background: COLORS.bg, borderRadius: 8, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 4 }}>RE share of TPES by 2050</div>
                  <div style={{ fontSize: 24, fontWeight: 700, color: COLORS.green }}>23%</div>
                </div>
              </div>
            </ChartCard>
          </>
        )}

        {/* INVESTMENTS TAB */}
        {activeTab === "investments" && (
          <>
            <ChartCard style={{ marginBottom: 16 }}>
              <SectionTitle sub="Key NETR and Budget 2026 investment allocations (RM billion)">
                Energy transition investment breakdown
              </SectionTitle>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={investmentData} layout="vertical" margin={{ top: 5, right: 60, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
                  <XAxis type="number" tick={{ fontSize: 11, fill: COLORS.textSecondary }} tickFormatter={v => `RM${v}B`} />
                  <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 11, fill: COLORS.textSecondary, style: { whiteSpace: "pre-line" } }} />
                  <Tooltip content={({ active, payload }) => active && payload?.length ? (
                    <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 8, padding: "8px 12px", fontSize: 13, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
                      <p style={{ margin: 0, fontWeight: 500 }}>{payload[0].payload.name?.replace("\n", " ")}</p>
                      <p style={{ margin: "2px 0 0", color: COLORS.textSecondary }}>RM {payload[0].value} billion</p>
                    </div>
                  ) : null} />
                  <Bar dataKey="value" fill={COLORS.emerald} radius={[0, 6, 6, 0]} barSize={28}
                    label={{ position: "right", fontSize: 12, fontWeight: 600, fill: COLORS.textPrimary, formatter: v => `RM${v}B` }} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <ChartCard>
                <SectionTitle sub="NETR economic projections by 2050">
                  Economic impact
                </SectionTitle>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  <TargetRow label="Total investment opportunity" value="RM1.2–1.85T" color={COLORS.navy} />
                  <TargetRow label="Additional GDP contribution" value="RM220B" color={COLORS.emerald} />
                  <TargetRow label="Green jobs created" value="310,000" color={COLORS.green} />
                  <TargetRow label="GHG reduction (flagship projects)" value="10,000 Gg/yr" color={COLORS.teal} />
                </div>
              </ChartCard>

              <ChartCard>
                <SectionTitle sub="NETR six energy transition levers">
                  Transition levers
                </SectionTitle>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {[
                    { label: "Energy efficiency (EE)", icon: "⚡" },
                    { label: "Renewable energy (RE)", icon: "☀️" },
                    { label: "Hydrogen economy", icon: "🔬" },
                    { label: "Bioenergy", icon: "🌿" },
                    { label: "Green mobility", icon: "🚗" },
                    { label: "Carbon capture (CCUS)", icon: "🏭" },
                  ].map((item, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", background: COLORS.bg, borderRadius: 8 }}>
                      <span style={{ fontSize: 18 }}>{item.icon}</span>
                      <span style={{ fontSize: 13, color: COLORS.textPrimary, fontWeight: 500 }}>{item.label}</span>
                    </div>
                  ))}
                </div>
              </ChartCard>
            </div>
          </>
        )}

        {/* Footer */}
        <div style={{ marginTop: 24, padding: "16px 0", borderTop: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 10, color: COLORS.textMuted }}>
            Sources: EPU NETR (2023) · WEC Malaysia Trilemma (2025) · PETRONAS NZCE Pathway (2023) · MIDA · IPTC 2023 · Budget 2026 · The Edge / ISIS Malaysia · IRENA
          </span>
          <span style={{ fontSize: 10, color: COLORS.textMuted }}>SETP 3113 Group Project — Topic 15</span>
        </div>
      </div>
    </div>
  );
}
