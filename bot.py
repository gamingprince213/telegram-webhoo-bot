from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN")
SECRET = os.environ.get("WEBHOOK_SECRET", "mysecret")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "mybot")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{SECRET}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message_text = update.message.text

    chat_id = update.message.chat.id

    if message_text == "/start":
        bot.send_message(chat_id=chat_id, text="🔥 Bot চালু আছে, Welcome!")
    else:
        bot.send_message(chat_id=chat_id, text=f"তুমি লিখেছো: {message_text}")

    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "🌐 Telegram Bot is running via Webhook!"

if __name__ == "__main__":
    app.run()
