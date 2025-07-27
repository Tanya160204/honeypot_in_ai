import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "intrusion_log_cleaned.csv")
MODEL_PATH = os.path.join(BASE_DIR, "attack_classifier.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# Load dataset
df = pd.read_csv(CSV_PATH, parse_dates=["Timestamp"])

# Feature engineering
df["hour"] = df["Timestamp"].dt.hour
df["dayofweek"] = df["Timestamp"].dt.dayofweek

# Encode IP address
le = LabelEncoder()
df["ip_encoded"] = le.fit_transform(df["IP Address"])

# Features and labels (label is dummy since original data lacks ground truth)
df["label"] = (df["Port"] < 1024).astype(int)  # Example: system ports are "malicious"

X = df[["ip_encoded", "Port", "hour", "dayofweek"]]
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and encoder
joblib.dump(model, MODEL_PATH)
joblib.dump(le, ENCODER_PATH)