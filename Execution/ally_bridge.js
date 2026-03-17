const { WebClient } = require('@slack/web-api');
const { SocketModeClient } = require('@slack/socket-mode');
const { Telegraf } = require('telegraf');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const dotenv = require('dotenv');
const fs = require('fs');

dotenv.config();

const SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN;
const SLACK_APP_TOKEN = process.env.SLACK_APP_TOKEN;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const GEMINI_API_KEY = process.env.GOOGLE_API_KEY;

function log(msg) {
    const timestamp = new Date().toISOString();
    const entry = `[${timestamp}] ${msg}\n`;
    process.stdout.write(entry);
    fs.appendFileSync('ally_bridge.log', entry);
}

log("Starting Ally Bridge v1.1...");

// Initialize Gemini
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
// Using gemini-2.5-flash as requested (confirmed in list_models)
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

// Initialize Slack
const slackWeb = new WebClient(SLACK_BOT_TOKEN);
const slackSocket = new SocketModeClient({ appToken: SLACK_APP_TOKEN });

// Initialize Telegram
const bot = new Telegraf(TELEGRAM_BOT_TOKEN);

async function generateResponse(prompt, context = "") {
    try {
        const fullPrompt = `System Context: You are Ally, an AI Executive Assistant. ${context}\n\nUser: ${prompt}`;
        const result = await model.generateContent(fullPrompt);
        const response = await result.response;
        return response.text();
    } catch (error) {
        log(`Gemini Error: ${error.message}`);
        return "I'm having trouble thinking right now. Please try again in a moment.";
    }
}

// --- Slack Handlers ---
slackSocket.on('message', async ({ event, ack }) => {
    await ack();
    if (event.bot_id) return;

    const isDM = event.channel_type === 'im';
    const botId = process.env.SLACK_BOT_USER_ID;
    const isMention = event.text && event.text.includes(`<@${botId}>`);

    if (isDM || isMention) {
        log(`Slack Event: Message in ${event.channel}`);
        const reply = await generateResponse(event.text, "You are replying via Slack.");
        await slackWeb.chat.postMessage({
            channel: event.channel,
            text: reply
        });
    }
});

// --- Telegram Handlers ---
bot.on('text', async (ctx) => {
    log(`Telegram Event: Message from ${ctx.from.username}`);
    const reply = await generateResponse(ctx.message.text, "You are replying via Telegram.");
    await ctx.reply(reply);
});

// --- Boot ---
(async () => {
    try {
        log("Connecting to Slack...");
        await slackSocket.start();
        log("✅ Slack Socket Mode connected.");

        log("Connecting to Telegram...");
        bot.launch().catch(err => {
            log(`❌ Telegram Launch Error: ${err.message}`);
        });
        log("✅ Telegram Bot started.");

        setInterval(() => log("Heartbeat: Ally is alive."), 600000); // Heartbeat every 10 mins

    } catch (error) {
        log(`❌ Boot Error: ${error.message}`);
    }
})();
