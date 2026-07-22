import re
import html
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from config import MAX_SUMMARY_LENGTH, KEYWORDS_REGEX

def clean_html(text):
    if not text:
        return ""
    if len(text) > MAX_SUMMARY_LENGTH:
        text = text[:MAX_SUMMARY_LENGTH]
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def escape_html(text):
    return html.escape(text)

def escape_url(url):
    return html.escape(url, quote=True)

def truncate_text(text, max_len=200):
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."

def split_message_by_length(text, max_len):
    parts = []
    while len(text) > max_len:
        split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            split_at = max_len
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        parts.append(text)
    return parts

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def passes_filter(title, summary):
    combined = f"{title} {summary}".lower()
    return bool(KEYWORDS_REGEX.search(combined))