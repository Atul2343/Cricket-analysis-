import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHAT_ID")

async def _send_daily_report(report: str):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=report
    )

def send_daily_report(report: str):
    """
    Sync wrapper so GitHub Actions / normal Python
    can call async telegram code safely
    """
    asyncio.run(_send_daily_report(report))
