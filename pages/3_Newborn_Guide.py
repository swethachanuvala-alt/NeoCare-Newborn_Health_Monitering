import streamlit as st

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Newborn Care Guide",
    page_icon="👶",
    layout="wide"
)

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

st.sidebar.markdown("---")

st.sidebar.success("""
### 🏥 Daily Healthy Baby Checklist

✅ Exclusive Breastfeeding

✅ Keep Vaccinations Up-to-date

✅ Maintain Proper Hygiene

✅ Regular Pediatric Checkups

✅ Monitor Weight Gain

✅ Keep Baby Warm
""")

# ---------------- TITLE ---------------- #

st.title("👶 Newborn Care Guide")

st.write(
"""
This guide provides essential recommendations for caring for a newborn.
Follow these best practices to promote healthy growth and recognize warning signs that require immediate medical attention.
"""
)

st.markdown("---")

# ==========================================================
# FEEDING
# ==========================================================

st.header("🍼 Feeding Recommendations")

st.success("""
### Healthy Baby

✔ Exclusive breastfeeding for the first 6 months.

✔ Feed every 2–3 hours (8–12 feeds/day).

✔ Burp the baby after every feeding.

✔ Monitor adequate urine output (6–8 wet diapers/day).

✔ Continue Vitamin D supplementation if advised.
""")

st.warning("""
### If Baby is At Risk

⚠ Feed more frequently if recommended by your pediatrician.

⚠ Monitor feeding difficulties carefully.

⚠ Track baby's weight regularly.

⚠ Watch for dehydration.

⚠ Seek medical attention if baby refuses feeds repeatedly.
""")

# ==========================================================
# SLEEP
# ==========================================================

st.markdown("---")

st.header("😴 Safe Sleep Guidelines")

st.info("""
✔ Place baby on the back while sleeping.

✔ Use a firm mattress.

✔ Avoid pillows and soft toys.

✔ Keep room smoke-free.

✔ Maintain room temperature between 24–26°C.

✔ Babies usually sleep 14–17 hours/day.
""")

# ==========================================================
# HYGIENE
# ==========================================================

st.markdown("---")

st.header("🧼 Hygiene & Infection Prevention")

st.success("""
✔ Wash hands before touching the baby.

✔ Clean feeding bottles properly.

✔ Keep baby's clothes clean and dry.

✔ Change diapers regularly.

✔ Clean umbilical cord as advised.

✔ Avoid contact with sick individuals.
""")

# ==========================================================
# VACCINATION
# ==========================================================

st.markdown("---")

st.header("💉 Vaccination Reminder")

st.info("""
Important newborn vaccines include:

✔ BCG

✔ OPV

✔ Hepatitis B

Follow the National Immunization Schedule recommended by your healthcare provider.
""")

# ==========================================================
# NORMAL VITAL SIGNS
# ==========================================================

st.markdown("---")

st.header("📊 Normal Newborn Vital Signs")

col1, col2 = st.columns(2)

with col1:

    st.success("""
**Temperature**

36.5°C – 37.5°C
""")

    st.success("""
**Heart Rate**

100 – 160 bpm
""")

    st.success("""
**Respiratory Rate**

30 – 60 breaths/min
""")

with col2:

    st.success("""
**Oxygen Saturation**

95% – 100%
""")

    st.success("""
**Birth Weight**

2.5 – 4.0 kg
""")

    st.success("""
**Gestational Age**

37 – 42 weeks
""")

# ==========================================================
# WARNING SIGNS
# ==========================================================

st.markdown("---")

st.header("⚠ Warning Signs Requiring Immediate Medical Attention")

st.error("""
Seek immediate medical care if your newborn has:

🔴 Difficulty breathing

🔴 Fever above 38°C

🔴 Temperature below 36°C

🔴 Bluish lips or skin

🔴 Poor feeding

🔴 Persistent vomiting

🔴 Convulsions

🔴 Yellow discoloration spreading rapidly

🔴 Unusual drowsiness

🔴 Continuous high-pitched crying
""")

# ==========================================================
# IF MODEL PREDICTS HEALTHY
# ==========================================================

st.markdown("---")

st.header("🟢 If the Prediction is HEALTHY")

st.success("""
Recommended Care:

✅ Continue exclusive breastfeeding.

✅ Maintain proper hygiene.

✅ Follow the vaccination schedule.

✅ Monitor baby's weight every week.

✅ Ensure proper sleep.

✅ Attend routine pediatric checkups.

✅ Observe feeding and diaper output daily.

Keep monitoring the baby's health even if the prediction is Healthy.
""")

# ==========================================================
# IF MODEL PREDICTS AT RISK
# ==========================================================

st.markdown("---")

st.header("🔴 If the Prediction is AT RISK")

st.warning("""
Recommended Actions:

⚠ Consult a pediatrician immediately.

⚠ Monitor breathing and temperature every few hours.

⚠ Do not miss scheduled medications.

⚠ Ensure adequate feeding and hydration.

⚠ Watch for worsening jaundice.

⚠ Visit the nearest hospital immediately if symptoms worsen.

⚠ Continue monitoring oxygen saturation if advised.

Early medical intervention greatly improves outcomes.
""")

# ==========================================================
# PARENT CHECKLIST
# ==========================================================

st.markdown("---")

st.header("📋 Daily Parent Checklist")

st.checkbox("Baby fed every 2–3 hours")

st.checkbox("Baby passed urine normally")

st.checkbox("Baby passed stool normally")

st.checkbox("Baby slept well")

st.checkbox("No fever observed")

st.checkbox("No breathing difficulty")

st.checkbox("Vaccinations up-to-date")

st.checkbox("Weight monitored")

# ==========================================================
# QUICK HEALTH TIPS
# ==========================================================

st.markdown("---")

st.header("💡 Quick Health Tips")

tips = [
    "🍼 Breast milk is the best nutrition for newborns.",
    "🌡 Monitor temperature regularly.",
    "🧼 Wash hands before handling the baby.",
    "💤 Ensure safe sleeping position (Back to Sleep).",
    "🚭 Keep baby away from smoke.",
    "💉 Never delay vaccinations.",
    "👨‍⚕ Attend routine pediatric checkups.",
    "❤️ Early detection saves lives."
]

for tip in tips:
    st.info(tip)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption("""
👶 **Newborn Health Monitoring System**

Powered by Machine Learning (Random Forest)

This application is intended for educational and clinical decision-support purposes only and should not be considered a substitute for professional medical advice.
""")