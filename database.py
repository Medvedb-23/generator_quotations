import sqlite3
import logging

DB_NAME = "quotations.db"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def init_db(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quotations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    author TEXT,
                    category TEXT,
                    is_fav INTEGER DEFAULT 0,
                    date TEXT,
                    image_path TEXT
                )
            """)
            self.conn.commit()
            logger.info("Database initialized")
        except sqlite3.Error as e:
            logger.error(f"DB init error: {e}")
            raise

    def get_all(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM quotations ORDER BY text")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"get_all error: {e}")
            raise

    def get_by_author(self, author):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM quotations WHERE author = ? ORDER BY text", (author,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"get_by_author error: {e}")
            raise

    def get_by_category(self, category):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM quotations WHERE category = ? ORDER BY text", (category,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"get_by_category error: {e}")
            raise

    def get_by_id(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM quotations WHERE id = ?", (id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"get_by_id error: {e}")
            raise

    def insert(self, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO quotations (text, author, category, is_fav, date, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get('text', ''),
                data.get('author', ''),
                data.get('category', ''),
                int(data.get('is_fav', 0)),
                data.get('date', ''),
                data.get('image_path', '')
            ))
            self.conn.commit()
            logger.info("Inserted new quotation")
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"insert error: {e}")
            raise

    def update(self, data):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE quotations
                SET text = ?, author = ?, category = ?, is_fav = ?, date = ?, image_path = ?
                WHERE id = ?
            """, (
                data.get('text', ''),
                data.get('author', ''),
                data.get('category', ''),
                int(data.get('is_fav', 0)),
                data.get('date', ''),
                data.get('image_path', ''),
                data.get('id')
            ))
            self.conn.commit()
            logger.info(f"Updated quotation id={data.get('id')}")
        except sqlite3.Error as e:
            logger.error(f"update error: {e}")
            raise

    def delete(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM quotations WHERE id = ?", (id,))
            self.conn.commit()
            logger.info(f"Deleted quotation id={id}")
        except sqlite3.Error as e:
            logger.error(f"delete error: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")