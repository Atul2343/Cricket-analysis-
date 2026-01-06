import os
import json
from telegram import Bot
from bot.formatter import generate_report
from datetime import date

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_daily_report():
    today = date.today().isoformat()
    try:
        with open(f"data/{today}_matches.json", "r", encoding="utf-8") as f:
            matches = json.load(f)
    except FileNotFoundError:
        matches = []

    if matches:
        bot = Bot(BOT_TOKEN)
        report = generate_report(matches)
        bot.send_message(chat_id=CHANNEL_ID, text=report)
        print("✅ Report sent successfully!")
    else:
        print("⚠️ No matches found today.")
