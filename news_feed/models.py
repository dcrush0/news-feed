from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    title: str
    url: str
    source: str
    section: str
    published_at: Optional[datetime] = None
    summary: str = ""
    score: int = 0
