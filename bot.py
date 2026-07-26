import os
import json
import requests
from urllib.parse import quote

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

SENT_FILE = "sent_news.json"

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


def load_sent():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            return json.load(f)
    return []


def save_sent(data):
    with open(SENT_FILE, "w") as f:
        json.dump(data, f)


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
        "&sortBy=publishedAt"
        "&pageSize=20"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url, timeout=30)
    data = response.json()

    if data.get("status") != "ok":
        return f"❌ NewsAPI Error:\n{data}"

    sent = load_sent()

    news = ""
    count = 0

    for article in data.get("articles", []):

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        link = article.get("url", "")

        if source not in ALLOWED_SOURCES:
            continue

        if "consent.yahoo.com" in link.lower():
            continue

        if title in sent:
            continue

        news += (
            f"{count+1}. {title}\n"
            f"📰 Source: {source}\n"
            f"🔗 {link}\n\n"
        )

        sent.append(title)
        count += 1

        if count == 5:
            break

    save_sent(sent[-200:])

    if count == 0:
        return "📰 No new oil news found."

    return news


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True
        },
        timeout=30
    )


def main():

    report = "🛢️ Oil Intelligence Report\n\n"

    report += get_oil_news()

    send_telegram(report)


if __name__ == "__main__":
    main()
