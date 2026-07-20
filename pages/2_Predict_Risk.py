from datetime import datetime

import pandas as pd
import streamlit as st

from utils.styles import inject_css, hero, section_start, section_end, result_banner, footer
from utils.prediction import predict_risk, get_risk_factors, describe_risk_factor
from utils.charts import probability_gauge, risk_factor_bar
from utils.report import generate_report_pdf

st.set_page_config(page_title="NeoCare · Predict Risk", page_icon="🔍", layout="wide")
inject_css()

hero(
    "🔍 Predict Newborn Risk",
    "Enter the baby's vitals and growth details below to get an instant, AI-assisted risk read-out.",
)

st.warning(
    "⚕️ **Not a medical device.** This is a demo/educational tool. "
    "Always consult a pediatrician or neonatal specialist for real clinical decisions."
)

with st.form("risk_form"):

    section_start("🍼 Baby Profile & Birth Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        gestational_age_weeks = st.slider("Gestational age (weeks)", 28.0, 44.0, 38.8, 0.1)
    with c2:
        birth_weight_kg = st.slider("Birth weight (kg)", 0.8, 5.5, 3.2, 0.01)
        birth_length_cm = st.slider("Birth length (cm)", 35.0, 60.0, 49.7, 0.1)
    with c3:
        birth_head_circumference_cm = st.slider("Birth head circumference (cm)", 25.0, 42.0, 34.1, 0.1)
        age_days = st.slider("Current age (days)", 1, 30, 15)
    section_end()

    section_start("📏 Current Growth")
    c1, c2, c3 = st.columns(3)
    with c1:
        weight_kg = st.slider("Current weight (kg)", 0.8, 6.5, 3.67, 0.01)
    with c2:
        length_cm = st.slider("Current length (cm)", 35.0, 62.0, 50.5, 0.1)
    with c3:
        head_circumference_cm = st.slider("Current head circumference (cm)", 25.0, 42.0, 34.4, 0.1)
    section_end()

    section_start("💓 Vitals")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        temperature_c = st.slider("Temperature (°C)", 34.0, 40.0, 37.0, 0.1)
    with c2:
        heart_rate_bpm = st.slider("Heart rate (bpm)", 70, 220, 140)
    with c3:
        respiratory_rate_bpm = st.slider("Respiratory rate (breaths/min)", 15, 70, 39)
    with c4:
        oxygen_saturation = st.slider("Oxygen saturation (%)", 80, 100, 97)
    section_end()

    section_start("🥣 Feeding & Elimination")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        feeding_type = st.selectbox("Feeding type", ["Breastfeeding", "Formula", "Mixed"])
    with c2:
        feeding_frequency_per_day = st.slider("Feedings per day", 3, 16, 9)
    with c3:
        urine_output_count = st.slider("Urine output count", 0, 14, 6)
    with c4:
        stool_count = st.slider("Stool count", 0, 10, 2)
    section_end()

    section_start("🩺 Clinical Signs")
    c1, c2, c3 = st.columns(3)
    with c1:
        jaundice_level_mg_dl = st.slider("Jaundice level (mg/dL)", 0.0, 25.0, 4.0, 0.1)
    with c2:
        immunizations_done = st.selectbox("Immunizations done?", ["Yes", "No"])
    with c3:
        reflexes_normal = st.selectbox("Reflexes normal?", ["Yes", "No"])
    section_end()

    submitted = st.form_submit_button("🔍 Check Risk Level", use_container_width=True)

# ------------------------------------------------------------------
# Run prediction on submit, store in session_state so the download
# button below (which triggers its own page rerun) doesn't wipe the
# result off the screen.
# ------------------------------------------------------------------
if submitted:
    raw_input = {
        "gender": gender,
        "gestational_age_weeks": gestational_age_weeks,
        "birth_weight_kg": birth_weight_kg,
        "birth_length_cm": birth_length_cm,
        "birth_head_circumference_cm": birth_head_circumference_cm,
        "age_days": age_days,
        "weight_kg": weight_kg,
        "length_cm": length_cm,
        "head_circumference_cm": head_circumference_cm,
        "temperature_c": temperature_c,
        "heart_rate_bpm": heart_rate_bpm,
        "respiratory_rate_bpm": respiratory_rate_bpm,
        "oxygen_saturation": oxygen_saturation,
        "feeding_type": feeding_type,
        "feeding_frequency_per_day": feeding_frequency_per_day,
        "urine_output_count": urine_output_count,
        "stool_count": stool_count,
        "jaundice_level_mg_dl": jaundice_level_mg_dl,
        "immunizations_done": immunizations_done,
        "reflexes_normal": reflexes_normal,
    }
    st.session_state.last_input = raw_input
    st.session_state.last_result = predict_risk(raw_input)

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
if "last_result" in st.session_state:
    raw_input = st.session_state.last_input
    result = st.session_state.last_result

    st.markdown("### Result")

    if result["is_healthy"]:
        result_banner(
            True,
            "✅ Healthy",
            f"Confidence: {result['healthy_prob']*100:.1f}% healthy · {result['at_risk_prob']*100:.1f}% at-risk",
        )
        st.balloons()
    else:
        result_banner(
            False,
            "⚠️ At Risk",
            f"Confidence: {result['at_risk_prob']*100:.1f}% at-risk · {result['healthy_prob']*100:.1f}% healthy",
        )
        st.warning("Please consult a pediatrician promptly for a clinical evaluation.")

    st.write("")
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(
            probability_gauge(result["healthy_prob"], "Healthy"), use_container_width=True
        )
    with g2:
        st.plotly_chart(
            probability_gauge(result["at_risk_prob"], "At Risk"), use_container_width=True
        )

    # -------------------- Why is this baby at risk? --------------------
    risk_factors = get_risk_factors(raw_input) if not result["is_healthy"] else []
    if not result["is_healthy"] and risk_factors:
        st.write("")
        section_start("🔎 Contributing Factors — Why This Result?")
        st.caption(
            "These are the entered values most different from a typical healthy newborn "
            "in this dataset, weighted by how much the model relies on each one. This is "
            "a transparency aid, not a clinical diagnosis."
        )
        for f in risk_factors:
            st.markdown(f"- {describe_risk_factor(f)}")
        st.plotly_chart(risk_factor_bar(risk_factors), use_container_width=True)
        section_end()

    # -------------------- Downloadable health report --------------------
    st.write("")
    pdf_bytes = generate_report_pdf(raw_input, result, risk_factors)
    st.download_button(
        "⬇️ Download PDF Health Report",
        data=pdf_bytes,
        file_name=f"neocare_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    with st.expander("See the values that were sent to the model"):
        st.dataframe(pd.DataFrame([raw_input]).T.rename(columns={0: "Value"}))

footer()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("👶 Newborn Health Assistant")

st.sidebar.info("""
## 📞 Emergency Support

🚑 **Emergency Ambulance:** **108**

👩‍⚕ Contact your pediatrician immediately if your baby has:

- Difficulty breathing
- Blue lips or skin
- Fever above **38°C**
- Poor feeding
- Continuous vomiting
- Convulsions or seizures
- Excessive sleepiness
- Persistent crying

⚠ **Medical Disclaimer**

This application is an **AI-powered decision support tool** developed for educational purposes.

It **does NOT replace** professional medical diagnosis, treatment, or consultation.

Always consult a qualified pediatrician for medical advice.
""")