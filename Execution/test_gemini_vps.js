const { GoogleGenerativeAI } = require("@google/generative-ai");
const dotenv = require("dotenv");
dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

(async () => {
    try {
        console.log("Using key:", process.env.GOOGLE_API_KEY.slice(0, 10) + "...");
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContent("hello");
        console.log("Response:", result.response.text());
    } catch (e) {
        console.error("Error:", e.message);
    }
})();
