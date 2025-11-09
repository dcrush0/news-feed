from dotenv import load_dotenv


def run() -> None:
    load_dotenv()
    from news_feed.config import SEND_WHATSAPP, SOURCES
    from news_feed.fetchers import fetch_all
    from news_feed.formatter import format_digest, split_for_whatsapp
    from news_feed.ranker import build_digest_articles
    from news_feed.sender import send_whatsapp_messages

    articles = fetch_all(SOURCES)
    grouped_articles = build_digest_articles(articles)
    digest = format_digest(grouped_articles)
    messages = split_for_whatsapp(digest)

    if SEND_WHATSAPP:
        send_whatsapp_messages(messages)
        print(f"Sent {len(messages)} WhatsApp message(s).")
        return

    print(digest)


if __name__ == "__main__":
    run()
