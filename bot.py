import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_oil_news():
    url = (
        "https://newsapi.org/v2/everything?"
        "q=oil"
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=5"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if data.get("status") != "ok":
            return f"❌ NewsAPI Error:\n{data}"

        articles = data.get("articles", [])

        if not articles:
            return "📰 No oil news found."

        news = ""
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown")
            news += f"{i}. {title}\n📰 {source}\n\n"

        return news

    except Exception as e:
        return f"❌ Error: {e}"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

def main():
    report = (
        "🛢️ Oil Intelligence Report\n"
        f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    )

    report += get_oil_news()

    send_telegram(report)

if __name__ == "__main__":
    main()
