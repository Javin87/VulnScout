import time
from loguru import logger
from config import CHECK_INTERVAL, LOG_LEVEL, DATABASE_FILE
from database import Database
from fetchers import fetch_all_sources
from telegram import send_telegram_message, format_posts_for_telegram
from utils import passes_filter

logger.remove()
logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)
logger.add("monitor.log", rotation="10 MB", retention="30 days", level=LOG_LEVEL)

def check_for_new_posts(db):
    logger.info("Starting to check sources...")
    all_posts = fetch_all_sources()
    logger.info(f"Total posts fetched: {len(all_posts)}")

    new_posts = []
    for post in all_posts:
        if not passes_filter(post['title'], post.get('summary', '')):
            logger.debug(f"Post '{post['title']}' rejected due to keyword filter.")
            continue

        if db.add_post(
            post['id'],
            post['source'],
            post['title'],
            post['url'],
            post.get('summary', ''),
            post['published_at']
        ):
            new_posts.append(post)
            logger.info(f"New post from {post['source']}: {post['title']}")

    if new_posts:
        messages = format_posts_for_telegram(new_posts)
        for msg in messages:
            send_telegram_message(msg)
        logger.info(f"Sent {len(new_posts)} new posts.")
    else:
        logger.info("No new posts found.")

def main():
    logger.info("VulnScout monitoring bot started...")
    db = Database(DATABASE_FILE)
    try:
        while True:
            try:
                check_for_new_posts(db)
            except Exception as e:
                logger.exception(f"Unexpected error in main loop: {e}")
            logger.info(f"Waiting {CHECK_INTERVAL} seconds until next check...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
    finally:
        db.close()

if __name__ == "__main__":
    main()