import sqlite3
from datetime import datetime

DB_PATH = "summaries.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS summaries
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

def save_summary(title, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO summaries (title, content, created_at) VALUES (?, ?, ?)",
              (title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_summaries():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM summaries ORDER BY created_at DESC")
    summaries = c.fetchall()
    conn.close()
    return summaries

def get_summary_by_id(summary_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM summaries WHERE id = ?", (summary_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
