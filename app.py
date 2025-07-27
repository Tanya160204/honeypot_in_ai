# app.py (Flask Server - backend)
from flask import Flask, render_template, jsonify
import pandas as pd
import joblib
import os
from datetime import datetime

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'attack_classifier.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')
CSV_PATH = os.path.join(BASE_DIR, 'intrusion_log_cleaned.csv')

# Load model and encoder
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# Cache last seen timestamp
last_seen_timestamp = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/latest-attack')
def latest_attack():
    global last_seen_timestamp

    if not os.path.exists(CSV_PATH):
        return jsonify({'status': 'no_data'})

    try:
        df = pd.read_csv(CSV_PATH, parse_dates=['Timestamp'])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    if df.empty or 'Timestamp' not in df.columns:
        return jsonify({'status': 'no_data'})

    df.sort_values('Timestamp', inplace=True)
    latest_entry = df.iloc[-1]
    timestamp = latest_entry['Timestamp']

    if last_seen_timestamp is None or timestamp > last_seen_timestamp:
        last_seen_timestamp = timestamp
        return jsonify({
            'status': 'new_attack',
            'timestamp': timestamp.isoformat(),
            'ip': latest_entry['IP Address'],
            'port': int(latest_entry['Port'])
        })

    return jsonify({'status': 'no_update'})

if __name__ == "__main__":
    app.run(debug=True)
