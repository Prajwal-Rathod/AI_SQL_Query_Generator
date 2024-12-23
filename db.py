import sqlite3
from datetime import datetime

DB_FILE = "queries.db"

def init_db():
    """Initialize the database and create a table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)
        conn.commit()

def save_query_to_db(query):
    """Save a query to the database with a timestamp."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO queries (query, timestamp) VALUES (?, ?)", (query, datetime.now()))
        conn.commit()

def get_saved_queries():
    """Retrieve all saved queries from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("SELECT id, query, timestamp FROM queries").fetchall()

def delete_query(query_id):
    """Delete a query from the database using its ID."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM queries WHERE id = ?", (query_id,))
        conn.commit()
