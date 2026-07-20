# NeoCare — Newborn Risk Monitoring (Multi-page Streamlit App)

A colorful, multi-page Streamlit app around a Random Forest model that
predicts whether a newborn's profile looks **Healthy** or **At Risk** —
plus growth tracking, explainability, a downloadable report, and a
project-grounded chatbot.

## Folder structure

```
newborn_app_v2/
├── Home.py                     ← main entry point (run this)
├── requirements.txt
├── train_model.py              ← regenerates the model files
├── assets/                     ← reserved for logo/images (empty for now)
├── data/
│   └── newborn_health_monitoring_with_risk.csv
├── models/
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   ├── label_encoders.pkl
│   └── feature_columns.pkl
├── pages/
│   ├── 1_Predict_Risk.py       ← the core tool
│   ├── 2_Care_Guide.py         ← warning signs & what to do
│   ├── 3_Ask_NeoCare.py        ← chatbot grounded in this project's data
│   ├── 4_Model_Insights.py     ← dashboard + performance + EDA (tabs)
│   └── 5_About.py
└── utils/
    ├── __init__.py
    ├── charts.py                ← reusable Plotly figure builders
    ├── chatbot.py                ← TF-IDF retrieval chatbot logic
    ├── knowledge_base.py         ← content the chatbot answers from
    ├── prediction.py             ← model/data loading, inference, risk factors, growth tracker
    ├── report.py                  ← PDF health report generator
    └── styles.py                 ← shared CSS theme & UI components
```

## What's on the Predict Risk page now

1. **Prediction** — Healthy / At Risk with a confidence gauge, same as before.
2. **Contributing Factors** — if flagged At Risk, shows which entered values are
   most unusual vs. a typical healthy baby in the dataset, weighted by how much
   the model relies on that feature. It's a transparent heuristic (dataset
   z-score × global feature importance), not a per-instance SHAP explanation —
   clearly labeled as such in the UI.
3. **Growth Tracker** — compares weight/length/head circumference (birth and
   current) against the 10th–90th percentile band of similarly aged babies in
   *this dataset* (not official WHO/CDC charts — the UI says so).
4. **Downloadable PDF report** — one click, includes the result, contributing
   factors, growth readout, and every value submitted, timestamped.

## Ask NeoCare (chatbot)

Runs fully offline by default: `utils/knowledge_base.py` builds a set of text
chunks from the actual trained model (accuracy, feature importance, dataset
stats — computed live, so they stay correct if you retrain) plus curated
newborn-care content. `utils/chatbot.py` retrieves the best-matching chunk
with TF-IDF + cosine similarity (scikit-learn, no API key needed) and returns
it directly — so it can't hallucinate facts outside that knowledge base.

**Optional:** paste your own Anthropic API key in the chatbot page's sidebar
to get more natural, conversational phrasing (retrieval-augmented generation
— it still only uses the same knowledge base as context, just phrases the
answer more fluidly). Entirely optional; the app works fully without it.

## 1. Set up

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 2. Run it

```bash
streamlit run Home.py
```

## 3. Deploy (Streamlit Community Cloud, free)

```bash
git init
git add .
git commit -m "NeoCare app"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then go to https://share.streamlit.io → **New app** → pick the repo/branch
→ set the main file path to `Home.py` → **Deploy**.

> Make sure `data/` and `models/` are committed — the app reads from those
> folders at runtime. Don't regenerate just one `.pkl` file by hand; if you
> retrain, run `train_model.py` so all four stay in sync.

## Notes

- Your original notebook used `imbalanced-learn`'s SMOTE to balance classes;
  `train_model.py` uses simple random oversampling instead since that package
  wasn't available in the build sandbox — test accuracy is essentially
  identical (~99.8%).
- `requirements.txt` uses `>=` rather than pinned `==` versions, since exact
  pins caused a pandas build-from-source failure on some Windows/Python
  combinations.
