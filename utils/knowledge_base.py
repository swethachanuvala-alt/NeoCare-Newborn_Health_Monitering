"""
knowledge_base.py
Builds the set of text chunks the chatbot retrieves answers from. Some
chunks are static (curated newborn-care facts, mirrored from the Care
Guide page); others are generated live from the actual trained model and
dataset, so the bot's answers about "this app" stay accurate even if the
model is retrained.

Each chunk carries a few example question phrasings ("questions") used
ONLY to improve retrieval matching (TF-IDF has no stemming, so "accurate"
vs "accuracy" are unrelated tokens without this) — they are never shown
to the user, only `content` is.
"""

import streamlit as st

from utils.prediction import load_dataset, get_feature_importance


@st.cache_data(show_spinner=False)
def build_knowledge_base() -> list:
    chunks = []

    def add(topic, content, questions=""):
        chunks.append({"topic": topic, "content": content, "questions": questions})

    # ---------------- Dynamic: dataset & model facts ----------------
    df = load_dataset()
    total = len(df)
    at_risk_pct = (df["risk_level"] == "At Risk").mean() * 100
    importance_df = get_feature_importance()
    top5 = importance_df.head(5)
    top5_text = ", ".join(
        f"{row['label']} ({row['importance']*100:.0f}%)" for _, row in top5.iterrows()
    )

    add(
        "what is neocare",
        "NeoCare is an AI-assisted app that predicts whether a newborn's current vitals, "
        "growth measurements, and clinical signs look Healthy or At Risk, using a Random "
        "Forest model trained on newborn monitoring data.",
        "what is this app what does neocare do what is neocare",
    )
    add(
        "dataset size",
        f"The model was trained on {total:,} newborn monitoring records, of which "
        f"about {at_risk_pct:.1f}% were labeled At Risk and the rest Healthy.",
        "how much data how many records was the model trained on dataset size how big is the dataset",
    )
    add(
        "model accuracy",
        "The final model is a tuned Random Forest classifier that reaches about 99.8% "
        "accuracy, 100% precision, and 99.8% recall on a held-out test set, with an "
        "ROC-AUC near 1.00. It was chosen after comparing Logistic Regression, Decision "
        "Tree, Random Forest, XGBoost, KNN, and SVM.",
        "how accurate is the model what is the accuracy how good is the prediction how reliable is neocare model performance precision recall",
    )
    add(
        "important features",
        f"The features the model relies on most are: {top5_text}. Jaundice level, "
        "heart rate, age in days, and oxygen saturation together account for the large "
        "majority of the model's decision — other inputs like feeding type or birth "
        "weight matter much less.",
        "what features matter most which inputs matter most important factors what does the model look at feature importance",
    )
    add(
        "how prediction works",
        "When you fill in the Predict Risk form, the app encodes and scales your inputs "
        "exactly as done during training, then runs them through the trained Random "
        "Forest model, which outputs a Healthy/At Risk label with a confidence percentage.",
        "how does the prediction work how does neocare predict risk how is risk calculated",
    )
    add(
        "why at risk contributing factors",
        "On the Predict Risk page, if a baby is flagged At Risk, the app shows "
        "'Contributing Factors' — the specific entered values that are most unusual "
        "compared to healthy babies in the dataset, weighted by how important the model "
        "considers that feature. It's a transparency heuristic, not a medical diagnosis.",
        "why is my baby at risk what should i do if flagged at risk why did i get this result contributing factors explanation",
    )
    add(
        "growth tracker explanation",
        "The Growth Tracker on the Predict Risk page compares a baby's weight, length, "
        "and head circumference (both at birth and currently) against the 10th-90th "
        "percentile range of similarly aged babies in this project's dataset. It flags "
        "'low' or 'high' if a measurement falls outside that typical band. This is a "
        "dataset-based reference, not an official WHO/CDC growth chart.",
        "how does the growth tracker work what is the growth chart percentile weight length head circumference tracking",
    )
    add(
        "download report",
        "You can download a PDF health report from the Predict Risk page after running a "
        "prediction — it includes the result, contributing factors, growth tracker "
        "readout, and every value you entered, timestamped.",
        "how do i download a report can i save the results pdf report export",
    )

    # ---------------- Static: newborn care & safety ----------------
    add(
        "jaundice info",
        "Jaundice causes a yellowish tint to a newborn's skin and eyes and is common in "
        "the first week of life as their liver clears bilirubin. Mild jaundice often "
        "resolves on its own, but rapidly worsening jaundice, jaundice spreading to the "
        "arms/legs, or jaundice with a very sleepy or hard-to-wake baby needs prompt "
        "pediatrician evaluation, since untreated severe jaundice can be serious.",
        "what is jaundice when should i worry about jaundice yellow skin bilirubin",
    )
    add(
        "oxygen saturation info",
        "Healthy newborns typically maintain oxygen saturation around 95-100%. Readings "
        "consistently below 95%, especially alongside fast or labored breathing, "
        "grunting, or bluish lips/skin, warrant urgent medical attention.",
        "what is normal oxygen saturation spo2 oxygen levels for a newborn",
    )
    add(
        "heart rate info",
        "A newborn's normal resting heart rate is roughly 100-160 beats per minute (it "
        "can go higher briefly with crying or activity). A heart rate that's persistently "
        "very high, very low, or irregular should be checked by a doctor.",
        "what is a normal heart rate pulse bpm for a newborn baby",
    )
    add(
        "temperature info",
        "Normal newborn body temperature is about 36.5-37.5°C (97.7-99.5°F). A "
        "temperature at or above 38°C (100.4°F) in a baby under 3 months is considered a "
        "medical emergency and needs immediate care; a low temperature (below 36.5°C) "
        "also needs attention, especially with lethargy or poor feeding.",
        "what is a normal temperature for a newborn body temperature range",
    )
    add(
        "fever in newborn",
        "A fever in a newborn is a temperature of 38°C (100.4°F) or higher. In babies "
        "under 3 months old, any fever is considered a medical emergency and needs "
        "immediate attention — do not wait it out at home, contact your pediatrician or "
        "emergency services right away, especially if the fever comes with poor feeding, "
        "unusual sleepiness, or difficulty breathing.",
        "what counts as a fever what should i do if my baby has a fever high temperature",
    )
    add(
        "feeding guidance",
        "Newborns typically feed 8-12 times a day in the first weeks, whether "
        "breastfed, formula-fed, or mixed. Watch for at least 6 wet diapers and regular "
        "stools per day as signs of adequate feeding; a baby who consistently refuses "
        "feeds or feeds very infrequently should be seen by a pediatrician.",
        "how often should a newborn eat feed feeding frequency breastfeeding formula",
    )
    add(
        "emergency warning signs",
        "Seek emergency care immediately if a newborn has: bluish lips, tongue, or skin; "
        "difficulty breathing, grunting, or flaring nostrils; a temperature of 38°C "
        "(100.4°F) or higher; is very hard to wake or unusually limp; refuses feeds "
        "repeatedly; has a seizure; or has a sunken soft spot with very few wet diapers "
        "(signs of dehydration).",
        "what are emergency warning signs when should i go to the er urgent symptoms",
    )
    add(
        "when to call pediatrician",
        "Call your pediatrician (same day, not necessarily an emergency) for: jaundice "
        "that's spreading or worsening, mild fever, unusual fussiness or crying that "
        "won't settle, mild feeding difficulties, umbilical cord redness or discharge, or "
        "any change in the baby's usual behavior that concerns you.",
        "when should i call the doctor pediatrician non emergency concerns",
    )
    add(
        "reflexes and immunizations",
        "Normal newborn reflexes (like the startle/Moro reflex, grasp reflex, and "
        "rooting reflex) are an early sign of healthy neurological development — absent "
        "or very weak reflexes should be flagged to a doctor. Staying current on the "
        "recommended immunization schedule is one of the most effective ways to protect "
        "a newborn from serious preventable illness.",
        "what are normal reflexes moro reflex vaccines immunization schedule",
    )
    add(
        "sleep safety",
        "Newborns typically sleep 14-17 hours a day in short stretches, which is normal "
        "and not something to worry about on its own. For safe sleep: always place a "
        "baby on their back to sleep, on a firm flat surface, with no loose blankets, "
        "pillows, or soft toys in the crib — this reduces the risk of SIDS (Sudden "
        "Infant Death Syndrome). A baby who is unusually difficult to wake, or sleeping "
        "far more than usual while also feeding poorly, should be checked by a doctor.",
        "how much should a newborn sleep is it normal to sleep a lot safe sleep sids crib",
    )
    add(
        "bathing and hygiene",
        "Until the umbilical cord stump falls off (usually 1-3 weeks), sponge baths are "
        "recommended instead of full immersion. Use lukewarm water and mild, "
        "fragrance-free baby soap, 2-3 times a week is usually enough — newborn skin "
        "doesn't need daily bathing. Always support the head and neck during bath time.",
        "how do i bathe a newborn how often should i bathe my baby bath time hygiene",
    )
    add(
        "umbilical cord care",
        "Keep the umbilical cord stump clean and dry, and fold diapers below it to avoid "
        "irritation. It's normal for the area to look slightly dry or darken before "
        "falling off. Contact a pediatrician if you see redness, swelling, pus, a bad "
        "smell, or bleeding around the cord — those can be signs of infection.",
        "how do i care for the umbilical cord belly button stump falls off",
    )
    add(
        "hydration and water",
        "Newborns get all the hydration they need from breast milk or formula — plain "
        "water is not recommended in the first 6 months, as it can interfere with "
        "nutrient absorption and, in excess, is dangerous for a newborn's kidneys and "
        "sodium balance. Wet diapers (at least 6/day after the first week) are the best "
        "sign a baby is getting enough fluid.",
        "can i give my baby water hydration dehydration drinking",
    )
    add(
        "birth weight meaning",
        "Average birth weight for a full-term newborn is roughly 2.5-4.0 kg (5.5-8.8 "
        "lbs). A birth weight below 2.5 kg is generally classified as low birth weight, "
        "and can be linked to prematurity or growth restriction — babies with low birth "
        "weight are often monitored more closely for feeding, temperature regulation, "
        "and weight gain in the early weeks.",
        "what does low birth weight mean average birth weight is my baby's birth weight normal",
    )
    add(
        "gestational age meaning",
        "Gestational age is how many weeks pregnant the mother was at birth, counted "
        "from the first day of her last menstrual period. A full-term birth is 37-42 "
        "weeks. Babies born before 37 weeks are considered preterm (premature) and "
        "often need closer monitoring for breathing, temperature regulation, and "
        "feeding; babies born after 42 weeks are considered post-term. It's one of the "
        "inputs on the Predict Risk form because it affects what's 'typical' for a "
        "baby's other measurements.",
        "what is gestational age what does gestational age mean preterm premature full term weeks pregnant",
    )
    add(
        "diaper output guidance",
        "By day 5-7 onward, expect roughly 6 or more wet diapers and 3-4 or more soiled "
        "diapers a day as a sign of adequate feeding and hydration. Noticeably fewer wet "
        "diapers than that, dark yellow urine, or a spell without a wet diaper for many "
        "hours can be an early sign of dehydration and is worth mentioning to a doctor.",
        "how many diapers per day wet diapers urine output stool count normal",
    )
    add(
        "disclaimer",
        "NeoCare is an educational/portfolio demo, not a certified medical device. Its "
        "predictions and this chatbot's answers should never replace professional "
        "medical advice — always consult a qualified pediatrician or neonatal specialist "
        "for real concerns about a newborn's health.",
        "is this a real medical device can i trust this diagnosis disclaimer",
    )

    return chunks