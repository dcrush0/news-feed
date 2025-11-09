# Personalized WhatsApp News Feed

A small Python app that fetches news from selected sources, ranks stories by personal interests, and sends a daily digest to WhatsApp through Twilio.

## Topics

- FC Barcelona from Barca Universal
- AI, tech companies, and consumer social apps from TechCrunch
- Indian economy from The Hindu
- Indian elections from The Hindu and Google News RSS
- Startup funding from TechCrunch, Inc42, Entrackr, and Google News RSS
- World geopolitics and economy from Google News RSS and BBC World

RSS is used wherever possible because it is more stable than scraping. Lightweight page scraping is used only for source pages that do not expose a useful RSS feed.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your Twilio WhatsApp credentials.

## Run

Print a terminal digest:

```bash
python -m news_feed.main
```

Create an HTML preview at `output/digest.html`:

```bash
python -m news_feed.html_preview
```

To send on WhatsApp, set this in `.env`:

```bash
SEND_WHATSAPP=true
```

Then run:

```bash
python -m news_feed.main
```

## Schedule

Example cron job for 8:00 AM India time:

```cron
TZ=Asia/Kolkata
0 8 * * * cd /path/to/news-feed && /path/to/news-feed/.venv/bin/python -m news_feed.main >> /path/to/news-feed/news-feed.log 2>&1
```

## Project Structure

- `news_feed/config.py`: topics, keywords, limits, and source URLs
- `news_feed/fetchers.py`: RSS and webpage fetching
- `news_feed/ranker.py`: deduping, recency filtering, and scoring
- `news_feed/formatter.py`: WhatsApp text formatting
- `news_feed/html_formatter.py`: browser preview formatting
- `news_feed/sender.py`: Twilio WhatsApp delivery
- `news_feed/main.py`: main daily digest command
