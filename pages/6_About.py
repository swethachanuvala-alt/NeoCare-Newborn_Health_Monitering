import streamlit as st

from utils.styles import inject_css, hero, section_start, section_end, footer

st.set_page_config(page_title="NeoCare · About", page_icon="ℹ️", layout="wide")
inject_css()

hero("ℹ️ About NeoCare", "What this app does, how it was built, and what it isn't.")

section_start("🎯 What this app does")
st.write(
    """
NeoCare is a demo application that predicts whether a newborn's current
vitals, growth measurements, and clinical signs look **Healthy** or
**At Risk**, based on patterns learned from a monitoring dataset of 3,000
newborn health records. Beyond the prediction itself, it explains *why*
a result came out the way it did, tracks growth against dataset norms,
generates a downloadable report, and includes a chatbot that only draws
on this project's own data and model — not generic internet knowledge.
"""
)
section_end()

section_start("🛠️ How it was built")
st.markdown(
    """
- **Data cleaning:** missing numeric values filled with the median, missing
  categorical values filled with the mode, and outliers in a few growth
  columns capped using the IQR method.
- **Encoding:** categorical fields (gender, feeding type, immunizations,
  reflexes, risk level) label-encoded.
- **Scaling:** all features standardized with `StandardScaler`.
- **Class balancing:** the training set was rebalanced so the minority
  ("At Risk") class isn't drowned out by "Healthy" cases.
- **Modeling:** six algorithms were trained and compared — Logistic
  Regression, Decision Tree, Random Forest, XGBoost, KNN, and SVM.
- **Tuning:** the top models were hyperparameter-tuned with grid/randomized
  search and validated with 5-fold cross-validation.
- **Final model:** a tuned **Random Forest** was selected for its strong
  accuracy and generalization, reaching ~99.8% accuracy on a held-out test set.
"""
)
section_end()

section_start("🧭 How to use it")
st.markdown(
    """
1. Go to **Predict Risk**, fill in a newborn's details, and submit for an
   instant Healthy / At Risk read-out with a confidence score.
2. If flagged **At Risk**, the page shows the specific **Contributing
   Factors** behind that result, plus a **Growth Tracker** comparing the
   baby's measurements to typical ranges for their age.
3. Download a **PDF health report** to keep or bring to a doctor.
4. Visit the **Care Guide** for warning signs, general newborn care tips,
   and what to do with an At Risk result.
5. Ask the **Ask NeoCare** chatbot any question — it answers only from
   this project's own dataset, model, and care content.
6. Check **Model Insights** if you're curious how the model was built,
   how it performs, and what patterns are in the training data.
"""
)
section_end()

section_start("⚕️ Disclaimer")
st.warning(
    """
This app is an **educational / portfolio demo** and is **not a certified
medical device**. Its predictions, growth comparisons, PDF reports, and
chatbot answers should never be used to make real clinical decisions.
Always consult a qualified pediatrician or neonatal specialist for any
concerns about a newborn's health.
"""
)
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



