import sqlite3
import os

DB_NAME = "quotations.db"

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def init_db(self):
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

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotations ORDER BY text")
        return cursor.fetchall()

    def get_by_author(self, author):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotations WHERE author = ? ORDER BY text", (author,))
        return cursor.fetchall()

    def get_by_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotations WHERE category = ? ORDER BY text", (category,))
        return cursor.fetchall()

    def get_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quotations WHERE id = ?", (id,))
        return cursor.fetchone()

    def insert(self, data):
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
        return cursor.lastrowid

    def update(self, data):
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

    def delete(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM quotations WHERE id = ?", (id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()