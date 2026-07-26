import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = f"""🛢️ Bangladesh Oil Tanker Intelligence

✅ Bot is running successfully!

📅 {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

This is a test message from GitHub Actions.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
