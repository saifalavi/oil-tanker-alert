import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

url = (
    "https://newsapi.org/v2/everything?"
    "q=(oil OR tanker OR crude OR diesel OR petrol OR LNG)"
    "&language=en"
    "&sortBy=publishedAt"
    "&pageSize=5"
    f"&apiKey={NEWS_API_KEY}"
)

response = requests.get(url, timeout=30)
data = response.json()

message = (
    f"🛢️ Oil Intelligence Report\n"
    f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
)

articles = data.get("articles", [])

if not articles:
    message += "❌ No oil news found."
else:
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        source = article.get("source", {}).get("name", "Unknown")
        message += f"{i}. {title}\n🏢 {source}\n\n"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
