fetch('https://engtig-iot-ess.hf.space/gradio_api/call/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "data": [] })
})
.then(response => response.json())
.then(data => {
    console.log("Data from Gradio API:", data);

    if (data.معدل_ضربات_القلب) {
        $("#heart_rate_value").text(data.معدل_ضربات_القلب + " bpm");
    } else {
        $("#heart_rate_value").text("N/A");
    }

    if (data.نسبة_الأكسجين_في_الدم) {
        $("#spo2_value").text(data.نسبة_الأكسجين_في_الدم + "%");
    } else {
        $("#spo2_value").text("N/A");
    }

    if (data.درجة_الحرارة) {
        $("#temperature_value").text(data.درجة_الحرارة + "°C");
    } else {
        $("#temperature_value").text("N/A");
    }

    if (data.مستوى_السكر) {
        $("#sugar_level_value").text(data.مستوى_السكر + " mg/dL");
    } else {
        $("#sugar_level_value").text("N/A");
    }

    if (data.معدل_التعرق) {
        $("#gsr_value").text(data.معدل_التعرق + "%");
    } else {
        $("#gsr_value").text("N/A");
    }

    if (data.حالة_النوبات) {
        $("#seizure_prediction_value").text(data.حالة_النوبات);
    } else {
        $("#seizure_prediction_value").text("N/A");
    }

    if (data.حالة_السقوط) {
        $("#fall_prediction_value").text(data.حالة_السقوط);
    } else {
        $("#fall_prediction_value").text("N/A");
    }
})
.catch(error => {
    console.error("Error fetching data:", error);
    alert("Error fetching data. Please try again.");
});
