"""
prediction.py
Everything to do with loading trained artifacts, loading the raw dataset,
and turning a form's raw inputs into a risk prediction.
"""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"
DATA_DIR = ROOT_DIR / "data"
DATA_PATH = DATA_DIR / "newborn_health_monitoring_with_risk.csv"

# Friendly display names for feature columns (used across pages/charts)
FEATURE_LABELS = {
    "gender": "Gender",
    "gestational_age_weeks": "Gestational Age (weeks)",
    "birth_weight_kg": "Birth Weight (kg)",
    "birth_length_cm": "Birth Length (cm)",
    "birth_head_circumference_cm": "Birth Head Circumference (cm)",
    "age_days": "Age (days)",
    "weight_kg": "Current Weight (kg)",
    "length_cm": "Current Length (cm)",
    "head_circumference_cm": "Current Head Circumference (cm)",
    "temperature_c": "Temperature (°C)",
    "heart_rate_bpm": "Heart Rate (bpm)",
    "respiratory_rate_bpm": "Respiratory Rate (breaths/min)",
    "oxygen_saturation": "Oxygen Saturation (%)",
    "feeding_type": "Feeding Type",
    "feeding_frequency_per_day": "Feedings per Day",
    "urine_output_count": "Urine Output Count",
    "stool_count": "Stool Count",
    "jaundice_level_mg_dl": "Jaundice Level (mg/dL)",
    "immunizations_done": "Immunizations Done",
    "reflexes_normal": "Reflexes Normal",
}


@st.cache_resource(show_spinner="Loading model...")
def load_artifacts():
    """Load the trained model, scaler, label encoders, and feature order."""
    model = joblib.load(MODEL_DIR / "random_forest_model.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    encoders = joblib.load(MODEL_DIR / "label_encoders.pkl")
    feature_columns = joblib.load(MODEL_DIR / "feature_columns.pkl")
    return model, scaler, encoders, feature_columns


@st.cache_data(show_spinner="Loading dataset...")
def load_dataset() -> pd.DataFrame:
    """Load the raw newborn monitoring CSV (used by Dashboard/Insights pages)."""
    return pd.read_csv(DATA_PATH)


def get_healthy_index(risk_encoder):
    return list(risk_encoder.classes_).index("Healthy")


def predict_risk(raw_input: dict) -> dict:
    """
    Take a dict of raw (human-readable) feature values, run it through the
    same encode -> scale -> predict pipeline used at training time, and
    return a small result dict.
    """
    model, scaler, encoders, feature_columns = load_artifacts()
    risk_encoder = encoders["risk_level"]
    healthy_idx = get_healthy_index(risk_encoder)

    row = {}
    for col in feature_columns:
        val = raw_input[col]
        if col in encoders:
            val = encoders[col].transform([val])[0]
        row[col] = val

    input_df = pd.DataFrame([row])[feature_columns]
    input_scaled = scaler.transform(input_df)

    pred_class = model.predict(input_scaled)[0]
    pred_proba = model.predict_proba(input_scaled)[0]

    label = risk_encoder.inverse_transform([pred_class])[0]
    healthy_prob = float(pred_proba[healthy_idx])
    at_risk_prob = 1 - healthy_prob

    return {
        "label": label,
        "is_healthy": label == "Healthy",
        "healthy_prob": healthy_prob,
        "at_risk_prob": at_risk_prob,
    }


def get_feature_importance() -> pd.DataFrame:
    """Return a DataFrame of feature importances sorted descending, with friendly labels."""
    model, _, _, feature_columns = load_artifacts()
    df = pd.DataFrame(
        {
            "feature": feature_columns,
            "label": [FEATURE_LABELS.get(c, c) for c in feature_columns],
            "importance": model.feature_importances_,
        }
    )
    return df.sort_values("importance", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------
# "Why is this baby at risk?" — contributing factor explanation
# ------------------------------------------------------------------
NUMERIC_RISK_FEATURES = [
    "gestational_age_weeks", "birth_weight_kg", "birth_length_cm",
    "birth_head_circumference_cm", "age_days", "weight_kg", "length_cm",
    "head_circumference_cm", "temperature_c", "heart_rate_bpm", "respiratory_rate_bpm",
    "oxygen_saturation", "feeding_frequency_per_day", "urine_output_count",
    "stool_count", "jaundice_level_mg_dl",
]


@st.cache_data(show_spinner=False)
def _group_stats():
    """Per-feature mean/std for Healthy vs At Risk groups, and which
    direction (higher/lower) is associated with risk in this dataset."""
    df = load_dataset()
    healthy = df[df["risk_level"] == "Healthy"]
    at_risk = df[df["risk_level"] == "At Risk"]
    stats = {}
    for col in NUMERIC_RISK_FEATURES:
        h_mean, h_std = healthy[col].mean(), healthy[col].std()
        a_mean = at_risk[col].mean()
        stats[col] = {
            "healthy_mean": h_mean,
            "healthy_std": h_std if h_std and h_std > 1e-6 else 1.0,
            "at_risk_mean": a_mean,
            "direction": 1 if a_mean > h_mean else -1,  # 1 = higher is riskier
        }
    return stats


def get_risk_factors(raw_input: dict, top_n: int = 5) -> list:
    """
    Rank which of the entered values are (a) furthest from the typical
    'Healthy' baby in this dataset and (b) weighted by how much the model
    relies on that feature overall. This is a transparent heuristic
    (dataset z-score x global feature importance), not a per-instance
    SHAP explanation — it's meant to give an honest, directionally
    correct sense of what's driving a given prediction.
    """
    importance_df = get_feature_importance()
    importances = dict(zip(importance_df["feature"], importance_df["importance"]))
    stats = _group_stats()

    scored = []
    for col in NUMERIC_RISK_FEATURES:
        s = stats[col]
        z = (raw_input[col] - s["healthy_mean"]) / s["healthy_std"]
        signed = s["direction"] * z  # positive => pushing toward "at risk"
        if signed > 0.35:
            scored.append({
                "feature": col,
                "label": FEATURE_LABELS.get(col, col),
                "value": raw_input[col],
                "healthy_typical": round(s["healthy_mean"], 1),
                "direction": "high" if s["direction"] == 1 else "low",
                "score": importances.get(col, 0) * signed,
            })

    # simple categorical flags
    if raw_input.get("reflexes_normal") == "No":
        scored.append({
            "feature": "reflexes_normal", "label": "Reflexes Normal",
            "value": "No", "healthy_typical": "Yes", "direction": "abnormal",
            "score": importances.get("reflexes_normal", 0) * 1.5,
        })
    if raw_input.get("immunizations_done") == "No":
        scored.append({
            "feature": "immunizations_done", "label": "Immunizations Done",
            "value": "No", "healthy_typical": "Yes", "direction": "abnormal",
            "score": importances.get("immunizations_done", 0) * 1.5,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def describe_risk_factor(f: dict) -> str:
    if f["direction"] == "high":
        return (f"**{f['label']}** is elevated at **{f['value']}** "
                f"(typical for a healthy newborn: ~{f['healthy_typical']})")
    if f["direction"] == "low":
        return (f"**{f['label']}** is lower than typical at **{f['value']}** "
                f"(typical for a healthy newborn: ~{f['healthy_typical']})")
    return (f"**{f['label']}** is **{f['value']}**, which differs from the "
            f"typical healthy pattern ({f['healthy_typical']})")


# ------------------------------------------------------------------
# Growth tracker — compare entered measurements to dataset norms
# ------------------------------------------------------------------
GROWTH_METRICS = {
    "weight_kg": {"label": "Current Weight", "unit": "kg", "age_col": "age_days", "window": 3},
    "length_cm": {"label": "Current Length", "unit": "cm", "age_col": "age_days", "window": 3},
    "head_circumference_cm": {"label": "Current Head Circumference", "unit": "cm", "age_col": "age_days", "window": 3},
    "birth_weight_kg": {"label": "Birth Weight", "unit": "kg", "age_col": "gestational_age_weeks", "window": 1},
    "birth_length_cm": {"label": "Birth Length", "unit": "cm", "age_col": "gestational_age_weeks", "window": 1},
    "birth_head_circumference_cm": {"label": "Birth Head Circumference", "unit": "cm", "age_col": "gestational_age_weeks", "window": 1},
}


def get_growth_reference(raw_input: dict) -> list:
    """
    For each growth measurement, compare it to the 10th-90th percentile
    band of babies in this dataset at a similar age (or gestational age,
    for birth measurements). Returns per-metric percentile + status.

    Note: this reference band comes from this project's own dataset, not
    official WHO/CDC growth charts — it's useful for a relative sense of
    where a baby sits, not a clinical growth-chart replacement.
    """
    df = load_dataset()
    results = []
    for col, meta in GROWTH_METRICS.items():
        age_col = meta["age_col"]
        window = meta["window"]
        center = raw_input[age_col]
        subset = df[(df[age_col] >= center - window) & (df[age_col] <= center + window)]
        if len(subset) < 20:
            subset = df

        p10, p50, p90 = subset[col].quantile([0.10, 0.50, 0.90])
        value = raw_input[col]
        percentile_rank = float((subset[col] < value).mean() * 100)
        status = "low" if value < p10 else ("high" if value > p90 else "normal")

        results.append({
            "feature": col, "label": meta["label"], "unit": meta["unit"],
            "value": value, "p10": float(p10), "p50": float(p50), "p90": float(p90),
            "percentile_rank": percentile_rank, "status": status,
        })
    return results
