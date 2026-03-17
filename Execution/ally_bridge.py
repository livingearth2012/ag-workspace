import os
import logging
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AllyBridge")

# Load environment
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Slack Client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

async def generate_response(prompt, context=""):
    try:
        full_prompt = f"System Context: You are Ally, an AI Executive Assistant. {context}\n\nUser: {prompt}"
        response = await asyncio.to_thread(model.generate_content, full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        return "I'm having trouble thinking right now. Please try again in a moment."

# --- Slack Handlers ---
def process_slack_event(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload.get("event", {})
        if event.get("type") == "message" and not event.get("bot_id"):
            channel = event.get("channel")
            text = event.get("text")
            user = event.get("user")
            
            logger.info(f"Slack Message from {user} in {channel}: {text}")
            
            # Simple logic: avoid infinite loops, only respond to DMs or mentions
            if event.get("channel_type") == "im" or f"<@{client.web_client.auth_test()['user_id']}>" in text:
                asyncio.run_coroutine_threadsafe(handle_slack_message(channel, text), loop)

        # Acknowledge the event
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

async def handle_slack_message(channel, text):
    reply = await generate_response(text, context="You are replying via Slack.")
    slack_client.chat_postMessage(channel=channel, text=reply)

# --- Telegram Handlers ---
async def telegram_message_handler(update: telegram.Update, context):
    text = update.message.text
    user = update.message.from_user.username
    logger.info(f"Telegram Message from {user}: {text}")
    
    reply = await generate_response(text, context="You are replying via Telegram.")
    await update.message.reply_text(reply)

async def start_telegram():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), telegram_message_handler)
    application.add_handler(msg_handler)
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Telegram Polling started.")

async def start_slack():
    socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=slack_client)
    socket_client.socket_mode_request_listeners.append(process_slack_event)
    socket_client.connect()
    logger.info("Slack Socket Mode connected.")

async def main():
    global loop
    loop = asyncio.get_running_loop()
    
    # Run both Slack and Telegram simultaneously
    await asyncio.gather(
        start_slack(),
        start_telegram()
    )
    
    # Keep the script running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bridge shutting down...")
