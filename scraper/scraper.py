import requests
from bs4 import BeautifulSoup
from scraper.filters import is_relevant
import json
from datetime import date

# Example public cricket sites (replace with real ones)
SOURCES = [
    "https://www.cricbuzz.com/cricket-match-schedule",
    "https://www.espncricinfo.com/ci/engine/match/index.html"
]

def scrape_matches():
    matches = []

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ")

            if is_relevant(text):
                lines = [l.strip() for l in text.split("\n") if l.strip()]
                matches.extend(lines[:10])  # top 10 matches only
        except:
            continue

    # Save to JSON
    today = date.today().isoformat()
    with open(f"data/{today}_matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    return matches
