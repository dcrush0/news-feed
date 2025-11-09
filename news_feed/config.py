import os
from dataclasses import dataclass, field
from typing import Dict, List, Literal


SourceType = Literal["rss", "web"]


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    section: str
    source_type: SourceType = "rss"


@dataclass(frozen=True)
class Section:
    name: str
    keywords: List[str] = field(default_factory=list)
    negative_keywords: List[str] = field(default_factory=list)


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


MAX_ARTICLES_PER_SECTION = int(os.getenv("MAX_ARTICLES_PER_SECTION", "5"))
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "36"))
SEND_WHATSAPP = env_bool("SEND_WHATSAPP", False)


SECTIONS: Dict[str, Section] = {
    "barcelona": Section(
        name="Barcelona",
        keywords=[
            "barcelona",
            "barca",
            "xavi",
            "flick",
            "laporta",
            "la masia",
            "camp nou",
            "pedri",
            "gavi",
            "yamal",
            "araujo",
        ],
    ),
    "tech": Section(
        name="AI, Tech and Consumer Apps",
        keywords=[
            "ai",
            "artificial intelligence",
            "openai",
            "anthropic",
            "google",
            "meta",
            "apple",
            "consumer app",
            "social app",
            "creator",
            "chatbot",
            "agent",
            "model",
            "startup",
        ],
    ),
    "india_economy": Section(
        name="Indian Economy",
        keywords=[
            "india",
            "rbi",
            "inflation",
            "gdp",
            "fiscal",
            "rupee",
            "budget",
            "exports",
            "imports",
            "manufacturing",
            "tax",
            "economy",
            "policy",
        ],
    ),
    "india_elections": Section(
        name="Indian Elections",
        keywords=[
            "election",
            "poll",
            "bjp",
            "congress",
            "aap",
            "tmc",
            "dmk",
            "nda",
            "india bloc",
            "vote",
            "seat",
            "result",
            "leads",
            "assembly",
        ],
    ),
    "funding": Section(
        name="Startup Funding",
        keywords=[
            "funding",
            "raises",
            "raised",
            "series a",
            "series b",
            "series c",
            "seed",
            "venture",
            "valuation",
            "unicorn",
            "ipo",
            "acquisition",
            "breakout startup",
        ],
    ),
    "world": Section(
        name="World Geopolitics and Economy",
        keywords=[
            "war",
            "ceasefire",
            "china",
            "us",
            "russia",
            "ukraine",
            "middle east",
            "oil",
            "fed",
            "tariff",
            "trade",
            "sanction",
            "market",
            "geopolitics",
            "economy",
        ],
    ),
}


SOURCES: List[Source] = [
    Source("Barca Universal", "https://barcauniversal.com/feed/", "barcelona"),
    Source("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", "tech"),
    Source("TechCrunch Apps", "https://techcrunch.com/category/apps/feed/", "tech"),
    Source("TechCrunch Startups", "https://techcrunch.com/category/startups/feed/", "funding"),
    Source("TechCrunch Venture", "https://techcrunch.com/category/venture/feed/", "funding"),
    Source("The Hindu Economy", "https://www.thehindu.com/business/Economy/", "india_economy", "web"),
    Source("The Hindu Business RSS", "https://www.thehindu.com/business/feeder/default.rss", "india_economy"),
    Source("The Hindu Elections", "https://www.thehindu.com/elections/", "india_elections", "web"),
    Source(
        "Google News India Elections",
        "https://news.google.com/rss/search?q=India%20state%20elections%20contending%20parties%20winning&hl=en-IN&gl=IN&ceid=IN:en",
        "india_elections",
    ),
    Source("Inc42", "https://inc42.com/feed/", "funding"),
    Source("Entrackr", "https://entrackr.com/", "funding", "web"),
    Source(
        "Google News Startup Funding",
        "https://news.google.com/rss/search?q=India%20startup%20funding%20unicorn%20OR%20global%20startup%20funding&hl=en-IN&gl=IN&ceid=IN:en",
        "funding",
    ),
    Source(
        "Google News Geopolitics Economy",
        "https://news.google.com/rss/search?q=war%20OR%20ceasefire%20OR%20tariff%20OR%20oil%20OR%20%22global%20economy%22%20when%3A2d&hl=en-IN&gl=IN&ceid=IN:en",
        "world",
    ),
    Source("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml", "world"),
]
