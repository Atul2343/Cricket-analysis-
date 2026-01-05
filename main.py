import os
import json
import requests
from telegram import Bot

# ----------- Secrets ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
CRICKETDATA_API_KEY = os.environ.get("CRICKETDATA_API_KEY")

if not BOT_TOKEN or not CHANNEL_ID or not CRICKETDATA_API_KEY:
    raise Exception("❌ ERROR: BOT_TOKEN, CHANNEL_ID, or CRICKETDATA_API_KEY not set!")

bot = Bot(BOT_TOKEN)
print("✅ Secrets loaded successfully")

# ----------- State File for duplicate prevention -----------
STATE_FILE = "posted_matches.json"
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump({}, f)

with open(STATE_FILE) as f:
    posted = json.load(f)

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(posted, f)

# ----------- Fetch Live Matches -----------
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

# ----------- Prediction Logic -----------
def predict_match(match):
    match_id = str(match.get("id", "0"))
    team1 = match.get("team1", {}).get("name", "Team1")
    team2 = match.get("team2", {}).get("name", "Team2")
    toss_winner = match.get("toss_winner", team1)

    # First inning data
    innings = match.get("innings", [])
    first_inning = innings[0] if innings else {}
    second_inning = innings[1] if len(innings) > 1 else {}

    runs = first_inning.get("runs", 0)
    wickets = first_inning.get("wickets", 0)
    overs = first_inning.get("overs", 0)

    if overs > 0:
        run_rate = runs / overs
    else:
        run_rate = 0

    # Confidence calculation
    confidence = 50
    if toss_winner == team1:
        confidence += 5
    if run_rate > 6:
        confidence += min(30, run_rate * 5)
    if wickets < 5:
        confidence += 10

    confidence = min(confidence, 95)

    # Predicted winner logic
    predicted_winner = toss_winner
    if overs > 0:
        if run_rate > 6 and wickets < 5:
            predicted_winner = first_inning.get("batting_team", team1)
        else:
            predicted_winner = team2 if first_inning.get("batting_team") == team1 else team1

    # Build message
    message = f"🏏 *{team1} vs {team2}*\n"
    message += f"🎯 Toss Winner: {toss_winner}\n"
    if overs > 0:
        message += f"1️⃣ First Inning: {runs}/{wickets} in {overs} overs\n"
        message += f"Run Rate: {run_rate:.2f}\n"
    message += f"💡 Predicted Winner: *{predicted_winner}*\n"
    message += f"📊 Confidence: *{confidence}%*"

    return match_id, message

# ----------- Send Telegram -----------
def send_message(msg):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")
        print("✅ Message sent")
    except Exception as e:
        print("Error sending message:", e)

# ----------- Main Runner -----------
def main():
    live_matches = get_live_matches()
    if not live_matches:
        print("No live matches.")
        return

    for match in live_matches:
        match_id, message = predict_match(match)

        # Prevent duplicate messages
        if match_id in posted and posted[match_id].get("sent"):
            print(f"Skipping already posted match {match_id}")
            continue

        send_message(message)
        posted[match_id] = {"sent": True}

    save_state()

if __name__ == "__main__":
    main()
