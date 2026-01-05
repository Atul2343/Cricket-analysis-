import os
from telegram import Bot

bot = Bot(token=os.environ.get("BOT_TOKEN"))
CHANNEL_ID = os.environ.get("CHANNEL_ID")

try:
    bot.send_message(chat_id=CHANNEL_ID, text="Test message ✅")
    print("Message sent successfully")
except Exception as e:
    print("Error:", e)
