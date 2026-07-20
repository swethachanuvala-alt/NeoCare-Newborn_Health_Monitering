import pandas as pd
import streamlit as st

from utils.styles import inject_css, hero, section_start, section_end, footer
from utils.prediction import get_feature_importance
from utils.charts import feature_importance_bar, confusion_matrix_heatmap, model_comparison_bar

st.set_page_config(page_title="NeoCare · Model Performance", page_icon="🧠", layout="wide")
inject_css()

hero("🧠 Model Performance", "How the final Random Forest model was chosen, tuned, and evaluated.")

# ------------------------------------------------------------------
# Headline metrics (final tuned Random Forest, held-out test set)
# ------------------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accuracy", "99.8%")
c2.metric("Precision", "100%")
c3.metric("Recall", "99.8%")
c4.metric("F1 Score", "99.9%")
c5.metric("ROC-AUC", "1.00")

st.write("")

col1, col2 = st.columns([1, 1])
with col1:
    section_start("🧮 Confusion Matrix (test set, n=600)")
    cm = [[80, 0], [1, 519]]
    st.plotly_chart(confusion_matrix_heatmap(cm), use_container_width=True)
    st.caption("Rows = actual, columns = predicted. 1 'At Risk' newborn was missed; 0 'Healthy' newborns were misclassified.")
    section_end()

with col2:
    section_start("⭐ Feature Importance")
    importance_df = get_feature_importance()
    st.plotly_chart(feature_importance_bar(importance_df), use_container_width=True)
    section_end()

# ------------------------------------------------------------------
# Model comparison (from the original notebook's experiments)
# ------------------------------------------------------------------
section_start("🏆 Model Comparison")
st.write("Six algorithms were trained and compared before Random Forest was selected as the final model.")

comparison_df = pd.DataFrame(
    [
        {"Model": "Random Forest", "Accuracy": 0.9983, "Precision": 1.0000, "Recall": 0.9981, "F1 Score": 0.9990, "ROC-AUC": 1.0000},
        {"Model": "XGBoost", "Accuracy": 0.9967, "Precision": 1.0000, "Recall": 0.9962, "F1 Score": 0.9981, "ROC-AUC": 1.0000},
        {"Model": "Decision Tree", "Accuracy": 0.9900, "Precision": 1.0000, "Recall": 0.9885, "F1 Score": 0.9942, "ROC-AUC": 0.9952},
        {"Model": "SVM", "Accuracy": 0.9617, "Precision": 0.9807, "Recall": 0.9750, "F1 Score": 0.9778, "ROC-AUC": 0.9852},
        {"Model": "Logistic Regression", "Accuracy": 0.8967, "Precision": 0.9731, "Recall": 0.9058, "F1 Score": 0.9382, "ROC-AUC": 0.9563},
        {"Model": "KNN", "Accuracy": 0.8667, "Precision": 0.9762, "Recall": 0.8673, "F1 Score": 0.9185, "ROC-AUC": 0.9295},
    ]
)
# ------------------------------------------------------------------
# Why Random Forest? (Advantages & Strengths)
# ------------------------------------------------------------------

section_start("🎯 Why Random Forest Was Selected")

st.success("""
After evaluating multiple machine learning algorithms, **Random Forest** was selected as the final model because it consistently achieved the best balance of performance, reliability, and generalization.

### Key Advantages

✅ Highest Test Accuracy (99.8%)

✅ Excellent Precision, Recall, and F1 Score

✅ Perfect ROC-AUC (1.00)

✅ Stable Performance During Cross Validation

✅ Less Prone to Overfitting than a Single Decision Tree

✅ Handles Complex Non-Linear Relationships Effectively

✅ Robust to Noise and Outliers in Healthcare Data

✅ Works Well with Imbalanced Data after Applying SMOTE

✅ Provides Feature Importance for Better Clinical Interpretation

✅ Fast Prediction Time Suitable for Real-Time Decision Support

✅ Reliable and Consistent Performance on Unseen Data

These strengths make Random Forest an excellent choice for newborn health risk prediction, enabling accurate and dependable clinical decision support.
""")

section_end()
st.plotly_chart(model_comparison_bar(comparison_df), use_container_width=True)
st.dataframe(
    comparison_df.style.format({c: "{:.2%}" for c in ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]}),
    use_container_width=True,
    hide_index=True,
)
section_end()



section_start("🔁 Cross-Validation (5-fold, tuned models)")
cv_df = pd.DataFrame(
    [
        {"Model": "Decision Tree", "CV Accuracy": 0.9988, "Std Dev": 0.0017},
        {"Model": "Random Forest", "CV Accuracy": 0.9971, "Std Dev": 0.0028},
        {"Model": "XGBoost", "CV Accuracy": 0.9971, "Std Dev": 0.0028},
    ]
)
st.dataframe(
    cv_df.style.format({"CV Accuracy": "{:.2%}", "Std Dev": "{:.4f}"}),
    use_container_width=True,
    hide_index=True,
)
st.caption(
    "Random Forest was selected over Decision Tree despite a near-identical CV score because it "
    "generalizes better and is less prone to overfitting on unseen data."
)
section_end()
# ------------------------------------------------------------------
# Final Conclusion
# ------------------------------------------------------------------

section_start("✅ Conclusion")

st.success("""
The Random Forest model demonstrated outstanding predictive performance for newborn
health risk assessment, achieving high accuracy, precision, recall, and ROC-AUC.

Combined with proper clinical evaluation, this AI-powered decision support system
can assist healthcare professionals in identifying newborns who may require
additional monitoring and timely medical intervention.

**Note:** This application is intended to support—not replace—professional medical judgement.
""")

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


