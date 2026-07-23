import streamlit as st

from utils.styles import inject_css, hero, footer
from utils.prediction import load_dataset, load_artifacts

st.set_page_config(
    page_title="NeoCare · Home",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

hero(
    "👶 NeoCare — Newborn Risk Monitoring",
    "An AI-assisted companion for checking, understanding, and tracking newborn health.",
)

# ------------------------------------------------------------------
# Headline stats
# ------------------------------------------------------------------
df = load_dataset()
model, _, _, _ = load_artifacts()

total_babies = df["baby_id"].nunique()
total_records = len(df)
at_risk_pct = (df["risk_level"] == "At Risk").mean() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Babies monitored", f"{total_babies:,}")
c2.metric("Total readings", f"{total_records:,}")
c3.metric("Flagged at-risk", f"{at_risk_pct:.1f}%")
c4.metric("Model", "Random Forest", "99.8% test accuracy")

st.write("")
st.markdown("### Where to go")

# ------------------------------------------------------------------
# Nav cards -> other pages
# ------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="nav-card">
            <h3>🔍 Dashboard</h3>
            <p>Enter a newborn's vitals and growth details for an instant risk read-out —
            with the contributing factors, a growth tracker, and a downloadable report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Dashboard.py", label="Open Dashboard", icon="🔍")

with col2:
    st.markdown(
        """
        <div class="nav-card">
            <h3>🩹 Predict Risk</h3>
            <p>Warning signs, when to call a doctor, and what to do if your baby is
            flagged At Risk.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Predict_Risk.py", label="Predict Risk", icon="🩹")

with col3:
    st.markdown(
        """
        <div class="nav-card">
            <h3> 🩺Newborn Guide</h3>
            <p>A chatbot that answers only from this project's own dataset, model, and
            care guidance — not a generic bot.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Newborn_Guide.py", label="Newborn Guide", icon="🩺")

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(
        """
        <div class="nav-card">
            <h3>🧠 Ask NeoCare</h3>
            <p>For the curious: dataset overview, model accuracy, and how everything was built.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/4_Ask_NeoCare.py", label="Ask NeoCare", icon="🧠")

with col5:
    st.markdown(
        """
        <div class="nav-card">
            <h3> 📊Model Insights</h3>
            <p>What this app does, how it was built, and important disclaimers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/5_Model_Insights.py", label="View Insights", icon="📊")

with col6:
    st.markdown(
        """
        <div class="nav-card">
            <h3>ℹ️ About</h3>
            <p>What this app does, how it was built, and important disclaimers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/6_About.py", label="Read More", icon="ℹ️")

st.write("")
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


