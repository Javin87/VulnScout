import os
from dotenv import load_dotenv

load_dotenv()

# ================== Database ==================
DATABASE_FILE = "posts.db"

# ================== Proxy ==================
PROXY = os.getenv("PROXY")

# ================== Telegram ==================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the .env file.")

# ================== RSSHub Base URL ==================
RSSHUB_BASE_URL = os.getenv("RSSHUB_BASE_URL", "https://rsshub.app")

# ================== RSS Feeds ==================
RSS_FEEDS = {
    "medium": [
        "https://medium.com/feed/tag/bug-bounty",
        "https://medium.com/feed/tag/writeup",
        "https://medium.com/feed/tag/cybersecurity",
        "https://medium.com/feed/tag/xss",
        "https://medium.com/feed/tag/ctf",
    ],
    "hackerone": [
        "https://hackerone.com/hacktivity.rss",
    ],
    "bugcrowd": [
        "https://bugcrowd.com/engagements.rss",
    ],
    "twitter": [
        f"{RSSHUB_BASE_URL}/twitter/user/disclosedh1",
        f"{RSSHUB_BASE_URL}/twitter/user/h1Disclosed",
        f"{RSSHUB_BASE_URL}/twitter/user/Bugcrowd",
        f"{RSSHUB_BASE_URL}/twitter/user/theXSSrat",
        f"{RSSHUB_BASE_URL}/twitter/user/codingo_",
        f"{RSSHUB_BASE_URL}/twitter/user/d0nutptr",
        f"{RSSHUB_BASE_URL}/twitter/user/orange_8361",
    ],
    "portswigger": [
        "https://portswigger.net/research/rss"
    ],
    "projectdiscovery": [
        "https://projectdiscovery.io/feed.xml"
    ],
    "intigriti": [
        "https://blog.intigriti.com/feed/"
    ],
}

# ================== Keyword Filter (Regex) ==================
import re
KEYWORDS_REGEX = re.compile(
    r'\b(?:xss|xxe|csrf|ssti|lfi|rce|sqli|idor|cve|0day|zeroday|'
    r'bypass|escalation|writeup|bugbounty|hackerone|bugcrowd|intigriti|'
    r'redteam|blueteam|ssrf|deserialization|log4shell|spring4shell|'
    r'disclosure|poc|proof.of.concept|ctf|pentest|owasp)\b',
    re.IGNORECASE
)

# ================== HTTP Settings ==================
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_TIMEOUT = 30
RETRY_COUNT = 3
RETRY_BACKOFF = 2

# ================== Telegram Settings ==================
MAX_POSTS_PER_MESSAGE = 5
MAX_MESSAGE_LENGTH = 4096
TELEGRAM_RETRY_DELAY = 5

# ================== Check Interval ==================
CHECK_INTERVAL = 300  # 5 minutes

# ================== Logging ==================
LOG_LEVEL = "INFO"

# ================== Summary Limit ==================
MAX_SUMMARY_LENGTH = 10000

# ================== Watermark ==================
WATERMARK = '— Javin · <a href="https://t.me/P1rateParr0t">@P1rateParr0t</a> · <a href="https://github.com/Javin87">github.com/Javin87</a>'