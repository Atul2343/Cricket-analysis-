import os
import asyncio
from telegram import Bot

# Secrets ke names same rakho GitHub Actions me aur Python me
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # <-- CHANNEL_ID nahi, ye hi use hoga

async def _send_daily_report(report: str):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,  # yahi id chahiye
        text=report
    )

def send_daily_report(report: str):
    """
    Sync wrapper so GitHub Actions / normal Python
    can call async telegram code safely
    """
    asyncio.run(_send_daily_report(report))
