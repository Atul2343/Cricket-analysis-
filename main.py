import os
import json
import requests
from telegram import Bot

# ----------- Secrets -----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
CRICKETDATA_API_KEY = os.environ.get("CRICKETDATA_API_KEY")

if not BOT_TOKEN or not CHANNEL_ID or not CRICKETDATA_API_KEY:
    raise Exception("❌ ERROR: BOT_TOKEN, CHANNEL_ID, or CRICKETDATA_API_KEY not set!")

bot = Bot(BOT_TOKEN)
print("✅ Secrets loaded successfully")

# ----------- State file for duplicate prevention -----------
STATE_FILE = "posted_matches.json"
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump({}, f)

with open(STATE_FILE) as f:
    posted = json.load(f)

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(posted, f)

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

# ----------- Advanced AI Prediction Logic -----------
def predict_match(match):
    match_id = str(match.get("id", "0"))
    team1 = match.get("team1", {}).get("name", "Team1")
    team2 = match.get("team2", {}).get("name", "Team2")
    toss_winner = match.get("toss_winner", team1)

    # Inning-wise data
    innings = match.get("innings", [])
    first_inning = innings[0] if innings else {}
    second_inning = innings[1] if len(innings) > 1 else {}

    # First inning stats
    f_runs = first_inning.get("runs", 0)
    f_wickets = first_inning.get("wickets", 0)
    f_overs = first_inning.get("overs", 0)
    f_team = first_inning.get("batting_team", team1)

    # Second inning stats (if started)
    s_runs = second_inning.get("runs", 0)
    s_wickets = second_inning.get("wickets", 0)
    s_overs = second_inning.get("overs", 0)
    s_team = second_inning.get("batting_team", team2)

    # Run rates
    f_rr = f_runs / f_overs if f_overs > 0 else 0
    s_rr = s_runs / s_overs if s_overs > 0 else 0

    # Player form (basic simulation)
    team_strength = {team1: 50, team2: 50}
    # If first inning lead
    if f_rr > 6 and f_wickets < 5:
        team_strength[f_team] += 10
    # Second inning ongoing
    if s_overs > 0:
        team_strength[s_team] += int(s_rr * 2)

    # Predicted winner & confidence
    if team_strength[team1] > team_strength[team2]:
        predicted_winner = team1
        confidence = 50 + (team_strength[team1] - team_strength[team2])
    else:
        predicted_winner = team2
        confidence = 50 + (team_strength[team2] - team_strength[team1])
    confidence = min(confidence, 95)

    # Build message
    message = f"🏏 *{team1} vs {team2}*\n"
    message += f"🎯 Toss Winner: {toss_winner}\n"
    if f_overs > 0:
        message += f"1️⃣ First Inning: {f_runs}/{f_wickets} in {f_overs} overs\n"
        message += f"Run Rate: {f_rr:.2f}\n"
    if s_overs > 0:
        message += f"2️⃣ Second Inning: {s_runs}/{s_wickets} in {s_overs} overs\n"
        message += f"Run Rate: {s_rr:.2f}\n"
    message += f"💡 Predicted Winner: *{predicted_winner}*\n"
    message += f"📊 Confidence: *{confidence}%*"

    return match_id, message

# ----------- Send to Telegram -----------
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
