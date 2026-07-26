import os
import requests
from datetime import datetime
from urllib.parse import quote

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

KEYWORDS = [
    '"oil tanker"',
    '"crude oil"',
    '"oil shipment"',
    '"oil terminal"',
    "petroleum",
    "refinery",
    "OPEC",
    '"fuel import"',
    '"Bangladesh fuel"',
    '"Bangladesh Petroleum Corporation"',
    "BPC",
    '"Jamuna Oil"',
    '"Padma Oil"',
    '"Meghna Petroleum"',
    "LPG",
    "diesel",
    "petrol",
    '"Strait of Hormuz"',
    "VLCC",
    "Suezmax",
    "Aframax"
]

ALLOWED_SOURCES = {
    "Reuters",
    "BBC News",
    "CNBC",
    "Bloomberg",
    "Business Insider",
    "OilPrice.com",
    "Rigzone",
    "The Maritime Executive",
    "Offshore Energy",
    "S&P Global"
}


def get_oil_news():

    query = (
        "(" + " OR ".join(KEYWORDS) + ")"
        " NOT (football OR soccer OR baseball OR basketball "
        "OR NFL OR NBA "
        "OR Disney OR Universal "
        "OR movie OR celebrity "
        "OR travel OR tourism "
        "OR car OR SUV OR auction "
        "OR entertainment)"
    )

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={quote(query)}"
        "&language=en"
        "&searchIn=title"
        "&sortBy=relevancy"
        "&pageSize=20"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:

        response = requests.get(url, timeout=30)
        data = response.json()

        if data.get("status") != "ok":
            return f"❌ NewsAPI Error:\n{data}"

        articles = data.get("articles", [])

        filtered = []
        seen_titles = set()

        for article in articles:

            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown")
            link = article.get("url", "")

            if source not in ALLOWED_SOURCES:
                continue

            if "consent.yahoo.com" in link:
                continue

            if title.lower() in seen_titles:
                continue

            seen_titles.add(title.lower())
            filtered.append(article)

        if not filtered:
            return "📰 No trusted oil news found."

        news = ""

        for i, article in enumerate(filtered[:5], 1):

            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown")
            link = article.get("url", "")

            news += (
                f"{i}. {title}\n"
                f"📰 Source: {source}\n"
                f"🔗 {link}\n\n"
            )

        return news

    except Exception as e:
        return f"❌ Error: {e}"


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "disable_web_page_preview": True
            },
            timeout=30
        )

        print(response.text)

    except Exception as e:
        print(f"Telegram Error: {e}")


def main():

    report = (
        "🛢️ Oil Intelligence Report\n"
        f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    )

    report += get_oil_news()

    send_telegram(report)


if __name__ == "__main__":
    main()
