import time
import requests
from loguru import logger
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    MAX_POSTS_PER_MESSAGE, MAX_MESSAGE_LENGTH,
    TELEGRAM_RETRY_DELAY,
    PROXY,
    WATERMARK
)
from utils import escape_html, escape_url, split_message_by_length

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SOURCE_ICONS = {
    "medium": "📝",
    "twitter": "🐦",
    "hackerone": "🟠",
    "bugcrowd": "🐞",
    "portswigger": "🔬",
    "projectdiscovery": "🚀",
    "intigriti": "🎯",
    "github": "🐙",
    "reddit": "🤖",
    "default": "📌"
}

def send_telegram_message(message, retries=4):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    proxies = None
    use_proxy = PROXY is not None
    if use_proxy:
        proxies = {"http": PROXY, "https": PROXY}
        logger.info(f"Using proxy: {PROXY}")

    for attempt in range(retries):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=25,
                proxies=proxies,
                verify=False
            )
            
            if response.status_code in (502, 503, 504):
                logger.warning(f"Received {response.status_code} error with proxy. Retrying without proxy...")
                if use_proxy:
                    proxies = None
                    use_proxy = False
                    continue
                else:
                    logger.error(f"Telegram server error: {response.status_code}")
                    time.sleep(TELEGRAM_RETRY_DELAY * (attempt + 1))
                    continue

            if response.status_code == 429:
                wait = int(response.json().get("parameters", {}).get("retry_after", TELEGRAM_RETRY_DELAY))
                logger.warning(f"Telegram returned 429, waiting {wait} seconds...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            logger.info("✅ Message successfully sent to Telegram.")
            return True

        except requests.exceptions.ConnectTimeout:
            logger.error(f"Connection to Telegram timed out (attempt {attempt+1}).")
            if attempt < retries - 1:
                time.sleep(TELEGRAM_RETRY_DELAY * (attempt + 1))
        except requests.exceptions.ProxyError as e:
            logger.error(f"❌ Proxy error (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                if use_proxy:
                    proxies = None
                    use_proxy = False
                    logger.info("🔄 Proxy disabled, retrying without proxy...")
                else:
                    time.sleep(TELEGRAM_RETRY_DELAY * (attempt + 1))
        except Exception as e:
            logger.error(f"❌ Error sending message (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                time.sleep(TELEGRAM_RETRY_DELAY * (attempt + 1))
    return False

def format_posts_for_telegram(posts):
    if not posts:
        return []

    chunks = []
    for i in range(0, len(posts), MAX_POSTS_PER_MESSAGE):
        chunk_posts = posts[i:i+MAX_POSTS_PER_MESSAGE]
        messages = []
        for post in chunk_posts:
            source = post.get('source', 'default').lower()
            icon = SOURCE_ICONS.get(source, SOURCE_ICONS['default'])
            
            title = escape_html(post['title'])
            summary = escape_html(post.get('summary', ''))[:200]
            safe_url = escape_url(post['url'])
            
            text = (
                f"{icon} <b>{source.capitalize()}</b>\n"
                f"📌 <a href='{safe_url}'>{title}</a>\n"
                f"📅 {post['published_at']}\n"
            )
            if summary:
                text += f"📄 {summary}...\n"
            messages.append(text)
        combined = "\n" + "─"*30 + "\n".join(messages)
        combined = combined + "\n\n" + WATERMARK
        chunks.append(combined)

    final_messages = []
    for chunk in chunks:
        if len(chunk) <= MAX_MESSAGE_LENGTH:
            final_messages.append(chunk)
        else:
            final_messages.extend(split_message_by_length(chunk, MAX_MESSAGE_LENGTH))
    return final_messages