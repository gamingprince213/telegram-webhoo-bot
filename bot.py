from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN")
SECRET = os.environ.get("WEBHOOK_SECRET", "mysecret")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "your_bot_username")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{SECRET}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="👋 হ্যালো, আমি Render থেকে চলা বট!")
    else:
        bot.send_message(chat_id=chat_id, text=f"আপনি লিখেছেন: {text}")

    return "ok"

@app.route("/")
def index():
    return "🌐 Bot is live!"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))  # Render sets $PORT
    app.run(host="0.0.0.0", port=PORT)
