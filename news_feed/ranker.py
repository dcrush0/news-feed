from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List
from urllib.parse import urlsplit, urlunsplit

from news_feed.config import LOOKBACK_HOURS, MAX_ARTICLES_PER_SECTION, SECTIONS, Section
from news_feed.models import Article


def build_digest_articles(articles: Iterable[Article]) -> Dict[str, List[Article]]:
    grouped: Dict[str, List[Article]] = {key: [] for key in SECTIONS}
    for article in filter_recent(deduplicate(articles)):
        section = SECTIONS[article.section]
        article.score = score_article(article, section)
        if article.score > 0:
            grouped[article.section].append(article)

    for section_key, section_articles in grouped.items():
        grouped[section_key] = sorted(
            section_articles,
            key=lambda item: (item.score, item.published_at or datetime.min.replace(tzinfo=timezone.utc)),
            reverse=True,
        )[:MAX_ARTICLES_PER_SECTION]

    return grouped


def deduplicate(articles: Iterable[Article]) -> List[Article]:
    seen = set()
    unique: List[Article] = []
    for article in articles:
        key = canonical_key(article)
        if key in seen:
            continue
        seen.add(key)
        unique.append(article)
    return unique


def filter_recent(articles: Iterable[Article]) -> List[Article]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    recent: List[Article] = []
    for article in articles:
        if article.published_at is None or article.published_at >= cutoff:
            recent.append(article)
    return recent


def score_article(article: Article, section: Section) -> int:
    text = f"{article.title} {article.summary}".lower()
    score = 1

    for keyword in section.keywords:
        if keyword.lower() in text:
            score += 3

    for keyword in section.negative_keywords:
        if keyword.lower() in text:
            score -= 4

    if article.published_at:
        age_hours = (datetime.now(timezone.utc) - article.published_at).total_seconds() / 3600
        if age_hours <= 12:
            score += 2
        elif age_hours <= 24:
            score += 1

    return score


def canonical_key(article: Article) -> str:
    parsed = urlsplit(article.url)
    cleaned_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))
    title_key = " ".join(article.title.lower().split())[:90]
    return cleaned_url or title_key
