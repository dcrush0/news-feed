from datetime import datetime
from html import escape
from typing import Dict, List

from news_feed.config import SECTIONS
from news_feed.formatter import compact_summary
from news_feed.models import Article


SECTION_COLORS = {
    "barcelona": "#a50044",
    "tech": "#0f766e",
    "india_economy": "#7c3aed",
    "india_elections": "#c2410c",
    "funding": "#0369a1",
    "world": "#334155",
}


def format_html_digest(grouped_articles: Dict[str, List[Article]]) -> str:
    today = datetime.now().strftime("%d %b %Y")
    total_articles = sum(len(items) for items in grouped_articles.values())
    sections_html = "\n".join(
        format_section(section_key, articles)
        for section_key, articles in grouped_articles.items()
        if articles
    )

    if not sections_html:
        sections_html = """
        <section class="empty-state">
          <h2>No strong matches found</h2>
          <p>The fetch ran correctly, but no stories matched the current ranking window.</p>
        </section>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Personalized News Feed - {escape(today)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --text: #172033;
      --muted: #5b6475;
      --card: #ffffff;
      --line: #dde3eb;
      --accent: #0f766e;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    .page {{
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 48px;
    }}

    header {{
      display: grid;
      gap: 12px;
      padding: 28px 0 24px;
      border-bottom: 1px solid var(--line);
    }}

    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0;
      text-transform: uppercase;
    }}

    h1 {{
      margin: 0;
      max-width: 780px;
      font-size: clamp(32px, 5vw, 56px);
      line-height: 1.04;
      letter-spacing: 0;
    }}

    .subtitle {{
      max-width: 780px;
      margin: 0;
      color: var(--muted);
      font-size: 17px;
    }}

    .meta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 8px;
    }}

    .pill {{
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #ffffff;
      color: var(--muted);
      padding: 7px 12px;
      font-size: 13px;
      font-weight: 650;
    }}

    main {{
      display: grid;
      gap: 26px;
      padding-top: 28px;
    }}

    .section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 12px;
    }}

    h2 {{
      margin: 0;
      font-size: 22px;
      letter-spacing: 0;
    }}

    .section-count {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 650;
    }}

    .articles {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}

    article {{
      display: grid;
      align-content: start;
      gap: 10px;
      min-height: 210px;
      padding: 18px;
      border: 1px solid var(--line);
      border-top: 4px solid var(--section-color, var(--accent));
      border-radius: 8px;
      background: var(--card);
      box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }}

    .source {{
      color: var(--section-color, var(--accent));
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0;
      text-transform: uppercase;
    }}

    h3 {{
      margin: 0;
      font-size: 18px;
      line-height: 1.25;
      letter-spacing: 0;
    }}

    .summary {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}

    a {{
      color: #0f5e9c;
      font-weight: 700;
      text-decoration: none;
    }}

    a:hover {{
      text-decoration: underline;
    }}

    .empty-state {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--card);
      padding: 24px;
    }}

    @media (max-width: 680px) {{
      .page {{
        width: min(100% - 22px, 1120px);
        padding-top: 18px;
      }}

      header {{
        padding-top: 16px;
      }}

      .articles {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <div class="eyebrow">Daily dry run</div>
      <h1>Your personalized news feed</h1>
      <p class="subtitle">Stories selected from your Barcelona, AI and tech, Indian economy, elections, startup funding, and world geopolitics interests.</p>
      <div class="meta-row">
        <span class="pill">{escape(today)}</span>
        <span class="pill">{total_articles} stories selected</span>
        <span class="pill">WhatsApp-ready digest</span>
      </div>
    </header>
    <main>
      {sections_html}
    </main>
  </div>
</body>
</html>
"""


def format_section(section_key: str, articles: List[Article]) -> str:
    section = SECTIONS[section_key]
    color = SECTION_COLORS.get(section_key, "#0f766e")
    article_cards = "\n".join(format_article(article) for article in articles)

    return f"""
      <section style="--section-color: {color}">
        <div class="section-header">
          <h2>{escape(section.name)}</h2>
          <span class="section-count">{len(articles)} stories</span>
        </div>
        <div class="articles">
          {article_cards}
        </div>
      </section>
    """


def format_article(article: Article) -> str:
    summary = compact_summary(article.summary, max_length=220)
    summary_html = f'<p class="summary">{escape(summary)}</p>' if summary else ""

    return f"""
          <article>
            <div class="source">{escape(article.source)}</div>
            <h3>{escape(article.title)}</h3>
            {summary_html}
            <a href="{escape(article.url)}" target="_blank" rel="noopener noreferrer">Read story</a>
          </article>
    """
