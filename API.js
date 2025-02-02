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
    $("#heart_rate_value").text(data.heart_rate + " bpm");
    $("#spo2_value").text(data.spo2 + "%");
    $("#temperature_value").text(data.temperature + "°C");
    $("#gsr_value").text(data.gsr + "%");
    $("#sugar_level_value").text(data.sugar_level + " mg/dL");
    $("#seizure_prediction_value").text(data.seizure_prediction);
    $("#fall_prediction_value").text(data.fall_prediction);
})
.catch(error => {
    console.error("Error fetching data:", error);
    alert("Error fetching data. Please try again.");
});
