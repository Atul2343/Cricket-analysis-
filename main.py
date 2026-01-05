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
POSTED_FILE = "posted_matches.txt"

def get_posted_matches():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_posted_match(match_id):
    with open(POSTED_FILE, "a") as f:
        f.write(f"{match_id}\n")

# -------------------- Fetch Matches --------------------
def fetch_upcoming_matches(limit=10):
    url = f"https://cricketdataapi.com/api/v1/upcoming?apikey={API_KEY}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "matches" in data and data["matches"]:
            return data["matches"][:limit]
    except Exception as e:
        print("Error fetching matches:", e)
    return []

# -------------------- Simple AI Prediction --------------------
def analyze_team_form(team):
    # Placeholder: normally fetch last 5 matches from API
    # For free API demo, using random wins
    import random
    wins = random.randint(2,5)
    losses = 5 - wins
    return wins, losses

def analyze_head_to_head(team1, team2):
    # Placeholder: fetch from API
    import random
    team1_wins = random.randint(0,5)
    team2_wins = 5 - team1_wins
    return team1_wins, team2_wins

def predict_winner(match):
    import random
    team1 = match.get("team1", "Team1")
    team2 = match.get("team2", "Team2")
    
    # Team form
    t1_wins, t1_losses = analyze_team_form(team1)
    t2_wins, t2_losses = analyze_team_form(team2)

    # Head-to-head
    h2h_t1, h2h_t2 = analyze_head_to_head(team1, team2)

    # Toss effect (random for free demo)
    toss_adv = random.choice([team1, team2, "None"])
    venue_adv = random.choice([team1, team2, "None"])

    # Key player (simplified random)
    key_player_adv = random.choice([team1, team2, "None"])

    # Compute score
    score_t1 = (t1_wins*6 + h2h_t1*5 + (2 if toss_adv==team1 else 0) + (2 if venue_adv==team1 else 0) + (3 if key_player_adv==team1 else 0))
    score_t2 = (t2_wins*6 + h2h_t2*5 + (2 if toss_adv==team2 else 0) + (2 if venue_adv==team2 else 0) + (3 if key_player_adv==team2 else 0))

    if score_t1 > score_t2:
        winner = team1
    else:
        winner = team2

    confidence = min(90, max(55, abs(score_t1 - score_t2)*5))  # scale confidence

    analysis = {
        "team1": team1,
        "team2": team2,
        "t1_form": f"{t1_wins}W-{t1_losses}L",
        "t2_form": f"{t2_wins}W-{t2_losses}L",
        "h2h": f"{team1} {h2h_t1} - {h2h_t2} {team2}",
        "toss_adv": toss_adv,
        "venue_adv": venue_adv,
        "key_player_adv": key_player_adv
    }

    return winner, confidence, analysis

# -------------------- Telegram Messaging --------------------
def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("Message sent successfully")
    except Exception as e:
        print("Error sending message:", e)

# -------------------- Main Logic --------------------
def main():
    posted_matches = get_posted_matches()
    matches = fetch_upcoming_matches(limit=10)

    if not matches:
        print("No upcoming matches found.")
        return

    for match in matches:
        match_id = str(match.get("match_id", "unknown"))
        if match_id in posted_matches:
            print(f"Skipping already posted match: {match.get('title', match_id)}")
            continue

        title = match.get("title", "Unknown Match")
        score = match.get("score", "Score not available")

        # AI Prediction
        winner, confidence, analysis = predict_winner(match)

        # Build message
        message = (
            f"🏏 Upcoming Match: {title}\n"
            f"Score: {score}\n\n"
            f"💡 Predicted Winner: {winner}\n"
            f"📊 Confidence: {confidence}%\n\n"
            f"🔹 Team Form:\n"
            f"- {analysis['team1']}: {analysis['t1_form']}\n"
            f"- {analysis['team2']}: {analysis['t2_form']}\n"
            f"🔹 Head-to-Head: {analysis['h2h']}\n"
            f"🔹 Toss Advantage: {analysis['toss_adv']}\n"
            f"🔹 Venue Advantage: {analysis['venue_adv']}\n"
            f"🔹 Key Player Advantage: {analysis['key_player_adv']}"
        )

        send_telegram_message(message)
        save_posted_match(match_id)

if __name__ == "__main__":
    main()
