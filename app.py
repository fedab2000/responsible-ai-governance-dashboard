import pandas as pd
import plotly.express as px
import streamlit as st

from utils.scoring import CONTROL_COLUMNS, generate_gap_analysis, score_controls

st.set_page_config(
    page_title="Responsible AI Governance Dashboard",
    page_icon="🤖",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/ai_system_inventory.csv")
    return score_controls(df)


df = load_data()

st.title("Responsible AI Governance Dashboard")
st.caption("Portfolio-level dashboard for monitoring AI ethics, governance maturity, and risk across deployed AI/ML systems.")

with st.sidebar:
    st.header("Filters")
    domains = st.multiselect("Domain", sorted(df["domain"].unique()), default=sorted(df["domain"].unique()))
    risk_levels = st.multiselect("Risk Level", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])

filtered = df[df["domain"].isin(domains) & df["risk_level"].isin(risk_levels)]

st.subheader("Executive Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("AI Systems", len(filtered))
col2.metric("Average Governance Score", f"{filtered['governance_score'].mean():.1f}/100")
col3.metric("High-Risk Systems", int((filtered["risk_level"] == "High").sum()))
col4.metric("Advanced Maturity Systems", int((filtered["maturity_level"] == "Advanced").sum()))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Governance Score by AI System")
    fig = px.bar(
        filtered.sort_values("governance_score", ascending=True),
        x="governance_score",
        y="system_name",
        orientation="h",
        text="governance_score",
        labels={"governance_score": "Governance Score", "system_name": "AI System"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Risk Level Distribution")
    risk_counts = filtered["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]
    fig = px.pie(risk_counts, names="risk_level", values="count", hole=0.45)
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("AI System Inventory")
st.dataframe(
    filtered[[
        "system_name", "domain", "department", "model_type", "data_sensitivity",
        "decision_impact", "automation_level", "governance_score", "maturity_level", "risk_level"
    ]],
    use_container_width=True,
)

st.subheader("Risk Heatmap")
heatmap_data = filtered.set_index("system_name")[[f"{c}_score" for c in CONTROL_COLUMNS]]
heatmap_data.columns = [c.replace("_", " ").title() for c in CONTROL_COLUMNS]
fig = px.imshow(
    heatmap_data,
    aspect="auto",
    labels=dict(x="Governance Control", y="AI System", color="Control Score"),
    text_auto=True,
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Gap Analysis and Recommended Actions")
gap_df = filtered.copy()
gap_df["recommended_actions"] = gap_df.apply(generate_gap_analysis, axis=1)
st.dataframe(
    gap_df[["system_name", "risk_level", "maturity_level", "governance_score", "recommended_actions"]],
    use_container_width=True,
)

st.subheader("Framework Alignment")
st.write(
    "This first version uses a practical governance score aligned with common Responsible AI themes: "
    "fairness, transparency, accountability, privacy, documentation, monitoring, and human oversight. "
    "Future versions can map each control directly to NIST AI RMF, OECD AI Principles, EU Trustworthy AI, and Canadian AIA-style criteria."
)
