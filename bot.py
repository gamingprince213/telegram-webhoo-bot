from flask import Flask, request, send_from_directory
import telegram
import os

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")
SECRET = os.environ.get("WEBHOOK_SECRET", "mysecret")

# Validate token
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is not set!")

# Initialize bot and app
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Optional: handle favicon to prevent 404
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Webhook route
@app.route(f"/{SECRET}", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat_id
        text = update.message.text

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="👋 হ্যালো, আমি Render থেকে চলা বট!")
        else:
            bot.send_message(chat_id=chat_id, text=f"আপনি লিখেছেন: {text}")
    except Exception as e:
        print(f"❌ Error handling update: {e}")
    return "ok"

# Health check route
@app.route("/")
def index():
    return "🌐 Bot is live!"

# Start server and set webhook
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    WEBHOOK_URL = f"https://telegram-webhoo-bot.onrender.com/{SECRET}"  # ✅ ঠিক করা

    try:
        bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook set to: {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Failed to set webhook: {e}")

    app.run(host="0.0.0.0", port=PORT)
