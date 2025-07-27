Honeypot_in_AI – Flask Server (app.py)
This is the backend server of the Honeypot_in_AI project, responsible for serving a web interface and exposing an API to detect and report the latest intrusion attempts from a live log.

🔧 Features
📥 Reads intrusion data from a cleaned CSV file

📊 Uses a trained ML model to classify attack types

🧠 Integrates with a label encoder to map predictions

🌐 Provides an API endpoint /api/latest-attack to fetch new threats in real-time

🧾 Displays attack information like timestamp, IP address, and port

📂 File Paths
attack_classifier.pkl – Trained scikit-learn model for classifying attacks

label_encoder.pkl – Label encoder to map numeric predictions to labels

intrusion_log_cleaned.csv – Cleaned log data with timestamps and metadata

🛠️ Dependencies
bash
Copy
Edit
pip install flask pandas joblib
▶️ How to Run
bash
Copy
Edit
python app.py
Then open your browser to:
http://127.0.0.1:5000/

📡 API Endpoint
/api/latest-attack
Returns:

new_attack → When a new entry appears in the log

no_update → No new entries since last check

no_data → If log file is missing or empty

error → If the CSV can't be read

Example response:

json
Copy
Edit
{
  "status": "new_attack",
  "timestamp": "2025-07-27T18:45:00",
  "ip": "192.168.1.10",
  "port": 8080
}
📌 Notes
The script keeps track of the last seen timestamp to only return new attacks

The data is expected to have a Timestamp, IP Address, and Port column

Ensure the model and encoder files exist in the project directory
