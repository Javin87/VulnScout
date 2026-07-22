import requests
import urllib3
import os
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PROXY = os.getenv("PROXY")

if not TOKEN or not CHAT_ID:
    print("❌ Token or Chat ID not found in .env!")
    exit(1)

proxies = None
if PROXY:
    proxies = {"http": PROXY, "https": PROXY}
    print(f"✅ Using proxy: {PROXY}")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "Hello from VulnScout! 🚀",
    "parse_mode": "HTML"
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=20,
        proxies=proxies,
        verify=False
    )
    response.raise_for_status()
    print("✅ Message sent successfully!")
    print(f"📨 Telegram response: {response.json()}")

except Exception as e:
    print(f"❌ Error sending message: {e}")