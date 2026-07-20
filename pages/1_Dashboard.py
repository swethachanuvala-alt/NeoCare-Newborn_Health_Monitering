import streamlit as st

from utils.styles import inject_css, hero, section_start, section_end, footer
from utils.prediction import load_dataset
from utils.charts import risk_distribution_pie, category_by_risk_bar, numeric_distribution_hist
from utils.styles import inject_css, hero, section_start, section_end, footer
from utils.prediction import load_dataset, FEATURE_LABELS
from utils.charts import numeric_distribution_hist, category_by_risk_bar, correlation_heatmap

st.set_page_config(page_title="NeoCare · Dashboard", page_icon="📊", layout="wide")
inject_css()

hero("📊 Dashboard", "A high-level view of every newborn currently being monitored.")

df = load_dataset()

# ------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Filters")
    gender_filter = st.multiselect(
        "Gender", options=sorted(df["gender"].dropna().unique()), default=None
    )
    feeding_filter = st.multiselect(
        "Feeding type", options=sorted(df["feeding_type"].dropna().unique()), default=None
    )

filtered = df.copy()
if gender_filter:
    filtered = filtered[filtered["gender"].isin(gender_filter)]
if feeding_filter:
    filtered = filtered[filtered["feeding_type"].isin(feeding_filter)]

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Records shown", f"{len(filtered):,}")
c2.metric("At-risk share", f"{(filtered['risk_level'] == 'At Risk').mean()*100:.1f}%")
c3.metric("Avg. gestational age", f"{filtered['gestational_age_weeks'].mean():.1f} wks")
c4.metric("Avg. oxygen saturation", f"{filtered['oxygen_saturation'].mean():.1f}%")

st.write("")

numeric_options = {
    "gestational_age_weeks": "Gestational Age (weeks)",
    "birth_weight_kg": "Birth Weight (kg)",
    "weight_kg": "Current Weight (kg)",
    "temperature_c": "Temperature (°C)",
    "heart_rate_bpm": "Heart Rate (bpm)",
    "respiratory_rate_bpm": "Respiratory Rate (breaths/min)",
    "oxygen_saturation": "Oxygen Saturation (%)",
    "jaundice_level_mg_dl": "Jaundice Level (mg/dL)",
    "feeding_frequency_per_day": "Feedings per Day",
    "urine_output_count": "Urine Output Count",
    "stool_count": "Stool Count",
}

# ------------------------------------------------------------------
# Charts
# ------------------------------------------------------------------
col1, col2 = st.columns([1, 1.4])
with col1:
    section_start("🩺 Risk Distribution")
    st.plotly_chart(risk_distribution_pie(filtered), use_container_width=True)
    key="risk_pie"

    section_end()

with col2:
    section_start("👶 Risk by Gender")
    st.plotly_chart(category_by_risk_bar(filtered, "gender", "Gender"), use_container_width=True)
    key="gender_bar"
    section_end()

section_start("🟡 Jaundice Level Distribution by Risk")
st.plotly_chart(
    numeric_distribution_hist(filtered, "jaundice_level_mg_dl", "Jaundice Level (mg/dL)"),
    use_container_width=True,
    key="jaundice_hist"
)
section_end()

section_start("🍼 Risk by Feeding Type")
st.plotly_chart(category_by_risk_bar(filtered, "feeding_type", "Feeding Type"), use_container_width=True)
key="feeding_bar"
section_end()


footer()

section_start("🔬 Explore a Feature's Distribution by Risk")
choice = st.selectbox("Pick a feature", options=list(numeric_options.keys()), format_func=lambda c: numeric_options[c])
st.plotly_chart(numeric_distribution_hist(df, choice, numeric_options[choice]), use_container_width=True)
key="distribution_chart"
section_end()


footer()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("👶 Newborn Health Assistant")

st.sidebar.info("""
## 📞 Emergency Support

🚑 **Emergency Ambulance:** **108**

👩‍⚕ Contact your pediatrician immediately if your baby has:

• Difficulty breathing
• Blue lips or skin
• Fever above **38°C**
• Poor feeding
• Continuous vomiting
• Convulsions or seizures
• Excessive sleepiness
• Persistent crying

⚠ **Medical Disclaimer**

This application is an **AI-powered decision support tool** developed for educational purposes.

It **does NOT replace** professional medical diagnosis, treatment, or consultation.

Always consult a qualified pediatrician for medical advice.
""")

