import json
import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

url = (
    "https://newsapi.org/v2/everything?"
    "q=oil OR tanker OR crude OR diesel OR petrol OR LNG"
    "&language=en"
    "&sortBy=publishedAt"
    "&pageSize=5"
    f"&apiKey={NEWS_API_KEY}"
)

try:
    response = requests.get(url, timeout=30)
    data = response.json()

    message = f"🛢️ Oil Intelligence Report\n"
    message += f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"

    articles = data.get("articles", [])

    if articles:
        for i, article in enumerate(articles, 1):
            message += f"{i}. {article['title']}\n"
            message += f"📰 {article['source']['name']}\n\n"
    else:
        message += "No oil news found."

except Exception as e:
    message = f"❌ Error: {e}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
