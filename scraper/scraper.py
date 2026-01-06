import os
import json
from datetime import date, datetime


def scrape_matches():
    """
    Daily cricket matches + basic analysis
    No API, No AI
    Safe for GitHub Actions
    """

    # 🔹 Aaj ki date
    today = date.today().isoformat()
    now_time = datetime.now().strftime("%H:%M")

    # 🔹 data folder auto-create
    os.makedirs("data", exist_ok=True)

    # 🔹 DEMO DATA (abhi static hai, baad me real scraping add karenge)
    matches = [
        {
            "match": "India vs Australia",
            "format": "ODI",
            "time": "02:00 PM IST",
            "ground": "Mumbai",
            "analysis": "High-scoring match expected. Toss will be important."
        },
        {
            "match": "Pakistan vs South Africa",
            "format": "T20",
            "time": "07:30 PM IST",
            "ground": "Lahore",
            "analysis": "Spinners may dominate in middle overs."
        }
    ]

    report = {
        "date": today,
        "generated_at": now_time,
        "total_matches": len(matches),
        "matches": matches
    }

    # 🔹 File path
    file_path = f"data/{today}_matches.json"

    # 🔹 Save JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✅ Match data saved: {file_path}")

    return report
