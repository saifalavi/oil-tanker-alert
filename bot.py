import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = f"""
🛢️ Bangladesh Oil Tanker Intelligence

✅ GitHub Actions is working.

📅 Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

No new tanker data has been collected yet.

Next step:
• Connect approved public data sources
• Generate automatic tanker reports
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=30
)

print(response.status_code)
print(response.text)

response.raise_for_status()
