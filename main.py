from scraper.scraper import scrape_matches
from bot.telegram_bot import send_daily_report

if __name__ == "__main__":
    scrape_matches()
    send_daily_report()
