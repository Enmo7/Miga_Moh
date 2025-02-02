fetch('https://engtig-iot-ess.hf.space/gradio_api/call/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "data": [] }) // Or your actual input data
})
.then(response => response.json())
.then(data => {
    console.log("Data from Gradio API:", data);
    // Update your website with the received data
    $("#heart_rate_value").text(data.معدل_ضربات_القلب + " bpm");
    $("#spo2_value").text(data.نسبة_الأكسجين_في_الدم + "%");
    $("#temperature_value").text(data.درجة_الحرارة + "°C");
    $("#gsr_value").text(data.معدل_التعرق + "%");
    $("#sugar_level_value").text(data.مستوى_السكر + " mg/dL");
    $("#seizure_prediction_value").text(data.حالة_النوبات);
    $("#fall_prediction_value").text(data.حالة_السقوط);
})
.catch(error => {
    console.error("Error fetching data:", error);
    alert("Error fetching data. Please try again.");
});
