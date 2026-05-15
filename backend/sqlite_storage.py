import sqlite3

class SQLiteStorage:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name,check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):

    # USERS TABLE
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ITEMS TABLE
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT,
        priority INTEGER DEFAULT 0,
        state TEXT DEFAULT 'draft',
        owner TEXT NOT NULL
    )
    """)

    # ACTIVITY TABLE
        self.conn.execute(""" CREATE TABLE IF NOT EXISTS item_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
    )
    """)

        self.conn.commit()

    def execute(self, query, params=()):
        return self.conn.execute(query, params)

    def fetch_one(self, query, params=()):
        return self.conn.execute(query, params).fetchone()

    def fetch_all(self, query, params=()):
        return self.conn.execute(query, params).fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()