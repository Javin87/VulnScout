import sqlite3
from loguru import logger
from utils import utc_now

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(
            db_file,
            check_same_thread=False,
            timeout=10
        )
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT,
            url TEXT UNIQUE,
            summary TEXT,
            published_at TEXT,
            discovered_at TEXT
        )
        """
        with self.conn:
            self.conn.execute(query)
        logger.info("Database table ready.")

    def add_post(self, post_id, source, title, url, summary, published_at):
        now = utc_now()
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """INSERT OR IGNORE INTO posts
                       (id, source, title, url, summary, published_at, discovered_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (post_id, source, title, url, summary, published_at, now)
                )
                return cursor.rowcount == 1
        except sqlite3.IntegrityError as e:
            logger.debug(f"Unique constraint error adding post: {e}")
            return False

    def close(self):
        self.conn.close()