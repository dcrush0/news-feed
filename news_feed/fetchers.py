from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable, List, Optional
from urllib.parse import urljoin

import feedparser
import requests
from bs4 import BeautifulSoup

from news_feed.config import Source
from news_feed.models import Article


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; PersonalNewsFeed/1.0; "
        "+https://example.local/news-feed)"
    )
}
TIMEOUT_SECONDS = 20


def fetch_articles(source: Source) -> List[Article]:
    if source.source_type == "web":
        return fetch_web_section(source)
    return fetch_rss(source)


def fetch_all(sources: Iterable[Source]) -> List[Article]:
    articles: List[Article] = []
    for source in sources:
        try:
            articles.extend(fetch_articles(source))
        except Exception as exc:
            print(f"Could not fetch {source.name}: {exc}")
    return articles


def fetch_rss(source: Source) -> List[Article]:
    response = requests.get(source.url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    articles: List[Article] = []

    for entry in feed.entries[:30]:
        title = clean_text(entry.get("title", ""))
        link = entry.get("link", "")
        if not title or not link:
            continue

        summary = clean_text(entry.get("summary", ""))
        published_at = parse_entry_date(entry)
        articles.append(
            Article(
                title=title,
                url=link,
                source=source.name,
                section=source.section,
                published_at=published_at,
                summary=summary,
            )
        )
    return articles


def fetch_web_section(source: Source) -> List[Article]:
    response = requests.get(source.url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    articles: List[Article] = []

    for anchor in soup.select("a[href]"):
        title = clean_text(anchor.get_text(" ", strip=True))
        href = anchor.get("href", "")
        if len(title) < 28 or not href:
            continue

        if href.startswith("/"):
            href = urljoin(source.url, href)
        if not href.startswith("http"):
            continue

        articles.append(
            Article(
                title=title,
                url=href,
                source=source.name,
                section=source.section,
                published_at=None,
            )
        )

    return articles[:40]


def parse_entry_date(entry) -> Optional[datetime]:
    for key in ("published", "updated", "created"):
        value = entry.get(key)
        if not value:
            continue
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except (TypeError, ValueError):
            continue
    return None


def clean_text(value: str) -> str:
    value = value or ""
    if "<" in value and ">" in value:
        value = BeautifulSoup(value, "html.parser").get_text(" ")
    return " ".join(value.split())
