"""
train_model.py
Retrains the Random Forest risk model from the CSV in data/ and writes the
four artifact files into models/. Re-run this only if you change the data
or the preprocessing steps.
"""

from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score,
)
import joblib

np.random.seed(42)

ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "data" / "newborn_health_monitoring_with_risk.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# 1. Load
df = pd.read_csv(DATA_PATH)

# 2. Drop unused columns
df = df.drop(columns=["name", "baby_id", "date", "apgar_score"])

# 3. Fill missing values
numerical_columns = [
    "gestational_age_weeks", "birth_weight_kg", "birth_length_cm",
    "birth_head_circumference_cm", "age_days", "weight_kg", "length_cm",
    "head_circumference_cm", "temperature_c", "heart_rate_bpm", "respiratory_rate_bpm",
    "oxygen_saturation", "feeding_frequency_per_day", "urine_output_count", "stool_count",
    "jaundice_level_mg_dl",
]
for c in numerical_columns:
    df[c] = df[c].fillna(df[c].median())

categorical_columns = ["gender", "feeding_type", "immunizations_done"]
for c in categorical_columns:
    df[c] = df[c].fillna(df[c].mode()[0])

# 4. Outlier treatment (median replace) on a few columns
for column in ["head_circumference_cm", "birth_length_cm", "birth_head_circumference_cm", "length_cm"]:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    median = df[column].median()
    df[column] = df[column].apply(lambda x: median if x < lower or x > upper else x)

# 5. Encode categoricals
cat_cols = ["gender", "feeding_type", "immunizations_done", "reflexes_normal", "risk_level"]
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

print("Label mappings:")
for col, le in label_encoders.items():
    print(" ", col, dict(zip(le.classes_, le.transform(le.classes_))))

# 6. Split
X = df.drop("risk_level", axis=1)
y = df["risk_level"]
feature_columns = list(X.columns)
print("\nFeature columns (order matters):", feature_columns)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 7. Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 8. Balance classes (manual random oversampling of minority class —
#    swap this block for imblearn's SMOTE if you have it installed)
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=feature_columns)
train_bal = X_train_scaled_df.copy()
train_bal["risk_level"] = y_train.values

majority = train_bal[train_bal.risk_level == train_bal.risk_level.value_counts().idxmax()]
minority = train_bal[train_bal.risk_level == train_bal.risk_level.value_counts().idxmin()]
minority_upsampled = minority.sample(n=len(majority), replace=True, random_state=42)
train_bal_full = pd.concat([majority, minority_upsampled]).sample(frac=1, random_state=42)

X_train_resampled = train_bal_full[feature_columns].values
y_train_resampled = train_bal_full["risk_level"].values

print("\nBefore balancing:", y_train.value_counts().to_dict())
print("After balancing:", pd.Series(y_train_resampled).value_counts().to_dict())

# 9. Train tuned Random Forest (best params found via RandomizedSearchCV)
best_rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="log2",
    random_state=42,
)
best_rf.fit(X_train_resampled, y_train_resampled)

y_pred = best_rf.predict(X_test_scaled)
y_prob = best_rf.predict_proba(X_test_scaled)[:, 1]

print("\n--- Test performance ---")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# 10. Save artifacts into models/
joblib.dump(best_rf, MODEL_DIR / "random_forest_model.pkl")
joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
joblib.dump(label_encoders, MODEL_DIR / "label_encoders.pkl")
joblib.dump(feature_columns, MODEL_DIR / "feature_columns.pkl")
print(f"\nSaved artifacts to {MODEL_DIR}/")
