import pandas as pd
import joblib
import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "attack_classifier.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# Load model and encoder
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# Predict function
def predict(ip, port, timestamp_str):
    timestamp = pd.to_datetime(timestamp_str)
    hour = timestamp.hour
    dayofweek = timestamp.dayofweek
    ip_encoded = label_encoder.transform([ip])[0]

    features = pd.DataFrame([{
        "ip_encoded": ip_encoded,
        "Port": int(port),
        "hour": hour,
        "dayofweek": dayofweek
    }])

    prediction = model.predict(features)[0]
    return "Malicious" if prediction == 1 else "Benign"

# Example usage
if __name__ == "__main__":
    test_result = predict("10.5.66.187", 22, "2025-04-08 14:35:47")
    print("Prediction:", test_result)