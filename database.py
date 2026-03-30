"""SQLite database layer for the items API."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "items.db"


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the items table if it does not exist."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def insert_items(items: list[dict]) -> list[dict]:
    """Insert one or more items into the database. Returns the inserted rows with id and created_at."""
    conn = get_connection()
    try:
        result = []
        for item in items:
            cursor = conn.execute(
                "INSERT INTO items (name, price) VALUES (?, ?)",
                (item["name"], item["price"]),
            )
            row = conn.execute(
                "SELECT id, name, price, created_at FROM items WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            result.append(dict(row))
        conn.commit()
        return result
    finally:
        conn.close()


def get_items(limit: int | None = None, offset: int | None = None) -> list[dict]:
    """Fetch items from the database. Optional limit and offset for pagination."""
    conn = get_connection()
    try:
        query = "SELECT id, name, price, created_at FROM items ORDER BY id"
        params: list = []
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset is not None:
            query += " OFFSET ?"
            params.append(offset)
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
