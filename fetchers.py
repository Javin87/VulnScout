import time
import requests
import feedparser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger
from datetime import datetime, timezone
from config import (
    USER_AGENT, REQUEST_TIMEOUT, RETRY_COUNT, RETRY_BACKOFF,
    RSS_FEEDS, PROXY
)
from utils import clean_html, utc_now

def create_session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    
    if PROXY:
        session.proxies = {
            "http": PROXY,
            "https": PROXY
        }
        logger.info(f"Using proxy for requests: {PROXY}")

    retry_strategy = Retry(
        total=RETRY_COUNT,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

session = create_session()

def fetch_feed(url, source_name):
    posts = []
    try:
        logger.debug(f"Fetching feed: {url}")
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        feed = feedparser.parse(response.text)

        for entry in feed.entries:
            post_id = entry.get("id") or entry.get("link") or entry.get("guid")
            if not post_id:
                continue

            title = entry.get("title", "No title")
            url = entry.get("link")
            if not url:
                continue

            published_str = entry.get("published") or entry.get("updated") or entry.get("created")
            if published_str:
                try:
                    published_dt = datetime(*published_str[:6], tzinfo=timezone.utc)
                    published = published_dt.isoformat()
                except:
                    published = utc_now()
            else:
                published = utc_now()

            raw_summary = entry.get("summary") or entry.get("description") or ""
            summary = clean_html(raw_summary)

            posts.append({
                "id": post_id,
                "source": source_name,
                "title": title,
                "url": url,
                "summary": summary,
                "published_at": published
            })

        logger.info(f"Fetched {len(posts)} posts from {source_name} ({url})")

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching feed {url} (source {source_name})")
    except Exception as e:
        logger.error(f"Error fetching feed {url} (source {source_name}): {e}")

    return posts

def fetch_all_sources():
    all_posts = []
    for source_name, urls in RSS_FEEDS.items():
        for url in urls:
            posts = fetch_feed(url, source_name)
            all_posts.extend(posts)
            time.sleep(0.5)

    all_posts.sort(key=lambda x: x["published_at"], reverse=True)
    return all_posts