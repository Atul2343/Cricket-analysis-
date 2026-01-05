import requests, os, json
from telegram import Bot

API_KEY = os.getenv("CRICKETDATA_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

bot = Bot(BOT_TOKEN)

STATE_FILE = "posted.json"

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump({}, f)

with open(STATE_FILE) as f:
    posted = json.load(f)

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(posted, f)

# ---------------- API ---------------- #

def get_matches():
    url = f"https://api.cricketdata.org/v1/currentMatches?apikey={API_KEY}"
    return requests.get(url).json().get("data", [])

def get_scorecard(match_id):
    url = f"https://api.cricketdata.org/v1/scorecard?apikey={API_KEY}&id={match_id}"
    res = requests.get(url).json()
    return res.get("data")

# ---------------- AI LOGIC ---------------- #

def pre_match_ai(match):
    team1, team2 = match["team1"], match["team2"]
    score1 = 50
    score2 = 50

    if "India" in team1: score1 += 10
    if "India" in team2: score2 += 10

    winner = team1 if score1 >= score2 else team2
    confidence = min(90, abs(score1 - score2) + 55)

    return winner, confidence

def inning_break_ai(match, scorecard):
    innings = scorecard.get("innings", [])
    if len(innings) < 1:
        return None

    inn = innings[0]
    runs = int(inn["runs"])
    batting = inn["team"]

    avg = 160  # T20 baseline
    diff = runs - avg

    team1, team2 = match["team1"], match["team2"]
    chasing = team2 if batting == team1 else team1

    if diff > 15:
        return batting, min(92, 60 + diff)
    else:
        return chasing, min(88, 55 + abs(diff))

# ---------------- TELEGRAM ---------------- #

def send(text):
    bot.send_message(CHANNEL_ID, text, parse_mode="Markdown")

# ---------------- MAIN ---------------- #

def main():
    matches = get_matches()
    sent = 0

    for match in matches:
        if sent >= 2:
            break

        mid = str(match["id"])
        if mid not in posted:
            posted[mid] = {"pre": False, "inning": False}

        # PRE MATCH
        if not posted[mid]["pre"] and match["status"] == "Scheduled":
            win, conf = pre_match_ai(match)
            send(f"""🏏 *AI PRE-MATCH PREDICTION*

⚔️ {match['team1']} vs {match['team2']}
🤖 Pick: *{win}*
📊 Confidence: *{conf}%*
""")
            posted[mid]["pre"] = True
            sent += 1

        # INNING BREAK
        if match["status"] == "Live" and not posted[mid]["inning"]:
            scorecard = get_scorecard(mid)
            if scorecard:
                res = inning_break_ai(match, scorecard)
                if res:
                    win, conf = res
                    send(f"""🔥 *INNING BREAK AI UPDATE*

⚔️ {match['team1']} vs {match['team2']}
🤖 AI Pick: *{win}*
📊 Confidence: *{conf}%*
""")
                    posted[mid]["inning"] = True
                    sent += 1

        save_state()

if __name__ == "__main__":
    main()
