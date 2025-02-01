from flask import Flask, jsonify, request, render_template
from tensorflow import keras
import numpy as np
import pandas as pd
import time
from firebase import firebase

app = Flask(__name__)

# Firebase configuration
config = {
    'apiKey': "AIzaSyDZCCMjd003FcPDRcik5jCHCEQL56pkeFY",
    'authDomain': "jsonfile-esp32-mohiot.firebaseapp.com",
    'databaseURL': "https://jsonfile-esp32-mohiot-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "jsonfile-esp32-mohiot",
    'storageBucket': "jsonfile-esp32-mohiot.firebasestorage.app",
    'messagingSenderId': "710233105459",
    'appId': "1:710233105459:web:6a5dd9b611e6f558c36f46"
}
firebase = firebase.FirebaseApplication(config['databaseURL'], None)

# Load CSV data
csv_data = pd.read_csv('sugar_level.csv')
sugar_levels = csv_data['Sugar level']  # Column name in your CSV file
current_csv_index = 0  # To keep track of the current position in the CSV file

# Load models
Seizure_Detection_model = keras.models.load_model("seizure_detection.h5")
Fall_Detection_model = keras.models.load_model("Fall_Detection.h5")

# Function to get the next sugar level
def get_next_sugar_level():
    global current_csv_index
    # If index exceeds CSV size, stick to the last value
    if current_csv_index >= len(sugar_levels):
        return sugar_levels.iloc[-1]  # Return the last value
    value = sugar_levels.iloc[current_csv_index]  # Get the current sugar level
    current_csv_index += 1  # Move to the next index for the next cycle
    return value

def process_sensor_data():
    try:
        data = firebase.get('/sensors', None)
        if not data:
            return "No data received from Firebase", 500

        heart_rate = data.get('MAX30102', 88)
        spo2 = data.get('MAX30102', 88)  # يجب تصحيح هذا!
        Temperature = data.get('MAX30205', 35)
        Distance = data.get('VL53L0X', 16)
        sugar_level = get_next_sugar_level()
        GSR = data.get('GSR', 0)

        # الكشف عن النوبات
        X_test_seizure = np.array([heart_rate, Temperature, spo2]).reshape(1, -1)
        seizure_prediction = Seizure_Detection_model.predict(X_test_seizure)
        seizure_result = "يوجد" if seizure_prediction[0][0] > 0.5 else "لا يوجد" # تحويل النتيجة إلى نص

        # الكشف عن السقوط
        X_test_fall = np.array([Distance, heart_rate, sugar_level, spo2]).reshape(1, -1)
        fall_prediction = Fall_Detection_model.predict(X_test_fall)

        fall_result = ""
        if fall_prediction[0][0] == 0:
          fall_result = "لا يوجد"
        elif fall_prediction[0][0] == 1:
          fall_result = "احتمال السقوط"
        elif fall_prediction[0][0] == 2:
          fall_result = "سقوط"

        return jsonify({
            "heart_rate": heart_rate,
            "spo2": spo2,
            "temperature": Temperature,
            "sugar_level": sugar_level,
            "gsr": GSR,
            "seizure_prediction": seizure_result,
            "fall_prediction": fall_result
        })

    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/process_data', methods=['POST'])
def process_data_route():
    return process_sensor_data()

@app.route('/')  # مسار الصفحة الرئيسية
def index():
    return render_template('index.html')  # عرض صفحة index.html

if __name__ == '__main__':
    app.run(debug=True)
