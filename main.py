import os
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
API_KEY = os.getenv("CRICKETDATA_API_KEY")

bot = Bot(token=BOT_TOKEN)
LAST_MATCH_FILE = "last_match.txt"

def get_last_match_id():
    if os.path.exists(LAST_MATCH_FILE):
        with open(LAST_MATCH_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_match_id(match_id):
    with open(LAST_MATCH_FILE, "w") as f:
        f.write(str(match_id))

def fetch_latest_match():
    url = f"https://cricketdataapi.com/api/v1/latest?apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "matches" in data and data["matches"]:
            return data["matches"][0]  # latest match
    except Exception as e:
        print("Error fetching cricket data:", e)
    return None

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("Message sent:", message)
    except Exception as e:
        print("Error sending message:", e)

def main():
    latest_match = fetch_latest_match()
    if not latest_match:
        print("No match data found.")
        return

    last_match_id = get_last_match_id()
    current_match_id = latest_match.get("match_id")

    if current_match_id != last_match_id:
        message = f"🏏 Latest Match Update:\n{latest_match.get('title')}\nScore: {latest_match.get('score')}"
        send_telegram_message(message)
        set_last_match_id(current_match_id)
    else:
        print("No new match. Skipping message.")

if __name__ == "__main__":
    main()
