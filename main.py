from flask import Flask, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from firebase import firebase
import threading
import time

app = Flask(__name__)

# Firebase configuration
config = {}
firebase_app = firebase.FirebaseApplication(config['databaseURL'], None)

# Load CSV data
csv_data = pd.read_csv('D:\moh\Jops\mostaqel\Moaaz\AI Codes\sugar_level.csv')
sugar_levels = csv_data['Sugar level']  # Column name in your CSV file
current_csv_index = 0  # To keep track of the current position in the CSV file

# Load models
Seizure_Detection_model = joblib.load(r'D:\moh\Jops\mostaqel\Moaaz\AI Codes\seizure_detection.pkl')
Fall_Detection_model = joblib.load(r'D:\moh\Jops\mostaqel\Moaaz\AI Codes\Fall_Detection.pkl')

# Function to get the next sugar level
def get_next_sugar_level():
    global current_csv_index
    if current_csv_index >= len(sugar_levels):
        return sugar_levels.iloc[-1]  # Return the last value if index exceeds length
    value = sugar_levels.iloc[current_csv_index]  # Get the current sugar level
    current_csv_index += 1
    return value

# Function to update sensor data from Firebase
def fetch_sensor_data():
    global heart_rate, spo2, Temperature, Distance, sugar_level, GSR, seizure_prediction, fall_prediction
    while True:
        try:
            # Fetch data from Firebase
            data = firebase_app.get('/sensors', None)
            if data:
                # Assign values to required variables
                heart_rate = data.get('MAX30102', 88)  # Default value if missing
                spo2 = data.get('MAX30102', 88)       # SpO2 same as MAX30102 here
                Temperature = data.get('MAX30205', 35)  # Default value if missing
                Distance = data.get('VL53L0X', 16)     # Default value if missing
                sugar_level = get_next_sugar_level()   # Get the next sugar level from CSV
                GSR = data.get('GSR', 0)              # Default value if missing

                # Seizure Detection Prediction
                X_test_seizure = np.array([heart_rate, Temperature, spo2]).reshape(1, -1)
                seizure_result = Seizure_Detection_model.predict(X_test_seizure)[0]
                seizure_prediction = "لا يوجد" if seizure_result == 0 else "يوجد"

                # Fall Detection Prediction
                X_test_fall = np.array([Distance, heart_rate, sugar_level, spo2]).reshape(1, -1)
                fall_result = Fall_Detection_model.predict(X_test_fall)[0]
                if fall_result == 0:
                    fall_prediction = "طبيعي"
                elif fall_result == 1:
                    fall_prediction = "احتمال للسقوط"
                else:
                    fall_prediction = "سقوط"

        except Exception as e:
            print(f"Error fetching sensor data: {e}")
        time.sleep(15)

# API endpoint to get real-time data
@app.route('/api/real_time_data', methods=['GET'])
def get_real_time_data():
    return jsonify({
        "heart_rate": heart_rate,
        "spo2": spo2,
        "temperature": Temperature,
        "distance": Distance,
        "sugar_level": sugar_level,
        "GSR": GSR,
        "seizure_prediction": seizure_prediction,
        "fall_prediction": fall_prediction
    })

# Serve the HTML page
@app.route('/')
def index():
    return render_template('D:\moh\Jops\mostaqel\Moaaz\AI Codes\index.html')

# Start the thread to fetch sensor data
sensor_thread = threading.Thread(target=fetch_sensor_data, daemon=True)
sensor_thread.start()

# if __name__ == '__main__':
#     app.run(debug=True)
