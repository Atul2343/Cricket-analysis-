import os
import requests
from telegram import Bot

# ----------- Secrets load ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
CRICKETDATA_API_KEY = os.environ.get("CRICKETDATA_API_KEY")

if not BOT_TOKEN or not CHANNEL_ID or not CRICKETDATA_API_KEY:
    raise Exception("❌ ERROR: BOT_TOKEN, CHANNEL_ID, or CRICKETDATA_API_KEY not set!")

bot = Bot(BOT_TOKEN)
print("✅ Secrets loaded successfully")

# ----------- Fetch live matches -----------
def get_live_matches():
    url = "https://cricketdata.org/api/v1/matches?status=live"
    headers = {"x-api-key": CRICKETDATA_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("matches", [])
    except Exception as e:
        print("Error fetching matches:", e)
        return []

# ----------- AI Prediction (simple example) -----------
def predict_match(match):
    # Example: basic prediction based on toss + team strength
    team1 = match.get("team1", "Team1")
    team2 = match.get("team2", "Team2")
    toss_winner = match.get("toss_winner", team1)
    
    # Simple logic for demo
    predicted_winner = toss_winner  # Toss winner advantage
    return f"⚡ Match Prediction:\n{team1} vs {team2}\nToss Winner: {toss_winner}\nPredicted Winner: {predicted_winner}"

# ----------- Send to Telegram -----------
def send_to_telegram(message):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("✅ Message sent to Telegram")
    except Exception as e:
        print("Error sending message:", e)

# ----------- Main Runner -----------
def main():
    live_matches = get_live_matches()
    if not live_matches:
        print("No live matches found.")
        return

    for match in live_matches:
        prediction_msg = predict_match(match)
        send_to_telegram(prediction_msg)

if __name__ == "__main__":
    main()
