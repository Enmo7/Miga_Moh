import { Client } from "@gradio/client";

async function getPrediction() {
    try {
        const client = await Client.connect("EngTig/IOT_ess");
        const result = await client.predict("/predict", {}); // لا تحتاج إلى تمرير أي بيانات هنا إذا كان النموذج يجلبها من Firebase
        return result.data;
    } catch (error) {
        console.error("Error in getPrediction:", error);
        return { error: "حدث خطأ في جلب البيانات." }; // إرجاع كائن خطأ
    }
}

// تصدير الدالة لاستخدامها في ملف HTML
window.getPrediction = getPrediction;