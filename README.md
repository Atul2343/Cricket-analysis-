# Ultimate Cricket AI Telegram Bot

🤖 Automated Cricket AI Prediction Bot for Telegram Channel

---

## Setup Instructions ⚡

### 1️⃣ GitHub Secrets
Go to **Repo → Settings → Secrets and Variables → Actions**  

Add these 3 secrets:

| Secret Name           | Value                               |
|-----------------------|-------------------------------------|
| `BOT_TOKEN`           | Your Telegram Bot token             |
| `CHANNEL_ID`          | Your Telegram channel username (`@xyz`) |
| `CRICKETDATA_API_KEY` | Your CricketData API key            |

> ⚠️ Use exact names (case sensitive). Bot must be **admin** in the channel.

---

### 2️⃣ Files

- `main.py` – Core bot + AI prediction  
- `bot.yml` – GitHub Actions workflow  
- `posted_matches.json` – Auto-generated to prevent duplicate messages  

---

### 3️⃣ Run Bot

#### Manual Run:
1. Go to **Actions → Ultimate Cricket AI Bot → Run workflow**  
2. Check logs → Telegram messages should appear  

#### Auto Run:
- Workflow is scheduled **every 10 minutes**  

---

### 4️⃣ Notes

- Duplicate matches are automatically prevented  
- Secrets must be correct to avoid errors  
- Telegram messages are Markdown formatted for better readability
