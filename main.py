import requests
import os
import json
from datetime import datetime
from telegram import Bot

API_KEY = os.getenv("CRICKETDATA_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

POSTED_FILE = "posted_matches.json"

if not os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "w") as f:
        json.dump([], f)

with open(POSTED_FILE, "r") as f:
    posted_matches = json.load(f)

def save_posted(match_id):
    posted_matches.append(match_id)
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_matches, f)

def get_matches():
    url = f"https://api.cricketdata.org/v1/matches?apikey={API_KEY}"
    return requests.get(url).json().get("data", [])

def predict(match):
    team1 = match["team1"]
    team2 = match["team2"]

    score1 = 0
    score2 = 0

    # AI-style weighted logic (FREE)
    if match.get("tossWinner") == team1:
        score1 += 10
    elif match.get("tossWinner") == team2:
        score2 += 10

    if "India" in team1:
        score1 += 8
    if "India" in team2:
        score2 += 8

    if match.get("venue", "").lower().find(team1.lower()) != -1:
        score1 += 5
    if match.get("venue", "").lower().find(team2.lower()) != -1:
        score2 += 5

    winner = team1 if score1 >= score2 else team2
    confidence = min(95, 50 + abs(score1 - score2))

    return winner, confidence

def send_message(match):
    match_id = match["id"]

    if match_id in posted_matches:
        return

    winner, confidence = predict(match)

    text = f"""🏏 *AI Match Prediction*

📅 {match['date']}
🏟 {match.get('venue','Unknown')}

⚔️ {match['team1']} vs {match['team2']}

🤖 *AI Pick:* {winner}
📊 *Confidence:* {confidence}%

⚠️ _Prediction based on free AI logic_
"""

    bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="Markdown")
    save_posted(match_id)

def main():
    matches = get_matches()
    count = 0

    for match in matches:
        if count >= 2:
            break
        if match["id"] not in posted_matches:
            send_message(match)
            count += 1

if __name__ == "__main__":
    main()
