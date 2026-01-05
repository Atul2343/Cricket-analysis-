import os
import requests
from telegram import Bot

# -------------------- Secrets --------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
API_KEY = os.environ.get("CRICKETDATA_API_KEY")

if not BOT_TOKEN or not CHANNEL_ID or not API_KEY:
    raise Exception("❌ BOT_TOKEN, CHANNEL_ID or CRICKETDATA_API_KEY missing!")

bot = Bot(token=BOT_TOKEN)

# -------------------- Duplicate Prevention --------------------
LAST_MATCH_FILE = "last_match.txt"

def get_last_match_id():
    if os.path.exists(LAST_MATCH_FILE):
        with open(LAST_MATCH_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_match_id(match_id):
    with open(LAST_MATCH_FILE, "w") as f:
        f.write(str(match_id))

# -------------------- Fetch Latest Match --------------------
def fetch_latest_match():
    url = f"https://cricketdataapi.com/api/v1/latest?apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "matches" in data and data["matches"]:
            return data["matches"][0]  # Latest match
    except Exception as e:
        print("Error fetching cricket data:", e)
    return None

# -------------------- Telegram Messaging --------------------
def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("Message sent successfully")
    except Exception as e:
        print("Error sending message:", e)

# -------------------- Main Logic --------------------
def main():
    latest_match = fetch_latest_match()
    if not latest_match:
        print("No match data found.")
        return

    last_match_id = get_last_match_id()
    current_match_id = latest_match.get("match_id")

    # Prevent duplicate messages
    if current_match_id == last_match_id:
        print("No new match. Skipping message.")
        return

    # Build Telegram message
    title = latest_match.get("title", "Unknown Match")
    score = latest_match.get("score", "Score not available")
    message = f"🏏 Latest Match Update:\n{title}\nScore: {score}"

    # Send message & save state
    send_telegram_message(message)
    set_last_match_id(current_match_id)

if __name__ == "__main__":
    main()
