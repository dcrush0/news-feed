from datetime import datetime
from typing import Dict, List

from news_feed.config import SECTIONS
from news_feed.models import Article


def format_digest(grouped_articles: Dict[str, List[Article]]) -> str:
    today = datetime.now().strftime("%d %b %Y")
    lines = [
        f"Your Personalized News Feed - {today}",
        "",
        "Top stories selected from your Barcelona, tech, India economy, elections, startup funding, and world news interests.",
    ]

    for section_key, section in SECTIONS.items():
        articles = grouped_articles.get(section_key, [])
        if not articles:
            continue

        lines.extend(["", f"*{section.name}*"])
        for index, article in enumerate(articles, start=1):
            summary = compact_summary(article.summary)
            source_line = f"{index}. {article.title} ({article.source})"
            lines.append(source_line)
            if summary:
                lines.append(f"   {summary}")
            lines.append(f"   {article.url}")

    if len(lines) <= 3:
        lines.append("")
        lines.append("No strong matches were found in the latest fetch window.")

    return "\n".join(lines)


def split_for_whatsapp(message: str, max_chars: int = 1450) -> List[str]:
    if len(message) <= max_chars:
        return [message]

    chunks: List[str] = []
    current: List[str] = []
    current_length = 0

    for block in message.split("\n\n"):
        block_length = len(block) + 2
        if current and current_length + block_length > max_chars:
            chunks.append("\n\n".join(current))
            current = [block]
            current_length = block_length
        else:
            current.append(block)
            current_length += block_length

    if current:
        chunks.append("\n\n".join(current))
    return chunks


def compact_summary(summary: str, max_length: int = 180) -> str:
    cleaned = " ".join((summary or "").split())
    if not cleaned:
        return ""
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rsplit(" ", 1)[0] + "..."
