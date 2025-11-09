from pathlib import Path

from dotenv import load_dotenv

OUTPUT_PATH = Path("output/digest.html")


def run() -> None:
    load_dotenv()

    from news_feed.config import SOURCES
    from news_feed.fetchers import fetch_all
    from news_feed.html_formatter import format_html_digest
    from news_feed.ranker import build_digest_articles

    articles = fetch_all(SOURCES)
    grouped_articles = build_digest_articles(articles)
    html = format_html_digest(grouped_articles)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")

    total = sum(len(items) for items in grouped_articles.values())
    print(f"Wrote {OUTPUT_PATH.resolve()}")
    print(f"Selected {total} stories")


if __name__ == "__main__":
    run()
