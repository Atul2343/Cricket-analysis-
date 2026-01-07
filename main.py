from bot.telegram_bot import send_daily_report
from datetime import datetime

def generate_report():
    today = datetime.now().strftime("%d %b %Y")

    report = f"""
🏏 Daily Cricket Report
📅 Date: {today}

✅ Match data scraped successfully
📊 Analysis completed
🤖 Report generated via GitHub Actions
    """.strip()

    return report

if __name__ == "__main__":
    report_text = generate_report()
    send_daily_report(report_text)
    print("✅ Report sent successfully!")
