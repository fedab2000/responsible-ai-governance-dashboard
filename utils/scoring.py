import pandas as pd

CONTROL_COLUMNS = [
    "bias_testing",
    "explainability",
    "monitoring",
    "human_oversight",
    "documentation",
    "privacy_controls",
]

VALUE_SCORE = {
    "Yes": 100,
    "Medium": 60,
    "No": 0,
    "Not Applicable": 100,
}

SENSITIVITY_SCORE = {"Low": 1, "Medium": 2, "High": 3}
IMPACT_SCORE = {"Low": 1, "Medium": 2, "High": 3}
AUTOMATION_SCORE = {"Low": 1, "Medium": 2, "High": 3}


def score_controls(df: pd.DataFrame) -> pd.DataFrame:
    """Add governance score, inherent risk score, and final risk level."""
    scored = df.copy()

    for col in CONTROL_COLUMNS:
        scored[f"{col}_score"] = scored[col].map(VALUE_SCORE).fillna(0)

    scored["governance_score"] = scored[[f"{c}_score" for c in CONTROL_COLUMNS]].mean(axis=1).round(1)

    scored["inherent_risk_score"] = (
        scored["data_sensitivity"].map(SENSITIVITY_SCORE).fillna(1)
        + scored["decision_impact"].map(IMPACT_SCORE).fillna(1)
        + scored["automation_level"].map(AUTOMATION_SCORE).fillna(1)
    )

    scored["risk_index"] = ((scored["inherent_risk_score"] / 9) * 100 - scored["governance_score"] * 0.35).round(1)
    scored["risk_level"] = scored["risk_index"].apply(classify_risk)
    scored["maturity_level"] = scored["governance_score"].apply(classify_maturity)
    return scored


def classify_risk(risk_index: float) -> str:
    if risk_index >= 50:
        return "High"
    if risk_index >= 30:
        return "Medium"
    return "Low"


def classify_maturity(score: float) -> str:
    if score >= 80:
        return "Advanced"
    if score >= 60:
        return "Managed"
    if score >= 40:
        return "Developing"
    return "Initial"


def generate_gap_analysis(row: pd.Series) -> str:
    gaps = []
    if row["bias_testing"] == "No":
        gaps.append("Add bias and fairness testing")
    if row["monitoring"] == "No":
        gaps.append("Implement ongoing model monitoring")
    if row["explainability"] in ["No", "Medium"]:
        gaps.append("Improve explainability documentation")
    if row["documentation"] in ["No", "Medium"]:
        gaps.append("Strengthen model documentation")
    if row["privacy_controls"] in ["No", "Medium"]:
        gaps.append("Review privacy and data protection controls")
    if row["human_oversight"] in ["No", "Medium"]:
        gaps.append("Define human review and escalation process")

    if not gaps:
        return "No major governance gaps identified"
    return "; ".join(gaps)
