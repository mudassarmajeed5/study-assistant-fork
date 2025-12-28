import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "database/summaries.db"

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS summaries
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, created_at TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores
                 (id INTEGER PRIMARY KEY, 
                  summary_id INTEGER, 
                  score REAL,
                  total_questions INTEGER,
                  timestamp TEXT,
                  FOREIGN KEY(summary_id) REFERENCES summaries(id))''')
 
    c.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
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

def save_quiz_score(summary_id, score, total_questions):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO quiz_scores 
                 (summary_id, score, total_questions, timestamp) 
                 VALUES (?, ?, ?, ?)""",
              (summary_id, score, total_questions, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_quiz_scores_by_summary(summary_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT score, total_questions, timestamp 
                 FROM quiz_scores 
                 WHERE summary_id = ? 
                 ORDER BY timestamp DESC""", (summary_id,))
    scores = c.fetchall()
    conn.close()
    return scores

def get_summary_stats(summary_id):
    """Get average score, attempts for a summary"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT 
                 AVG(score) as avg_score,
                 COUNT(*) as attempts,
                 MAX(score) as best_score
                 FROM quiz_scores 
                 WHERE summary_id = ?""", (summary_id,))
    stats = c.fetchone()
    conn.close()
    return {
        "avg_score": stats[0] or 0,
        "attempts": stats[1] or 0,
        "best_score": stats[2] or 0
    } if stats else {"avg_score": 0, "attempts": 0, "best_score": 0}



def delete_summary(summary_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("DELETE FROM quiz_scores WHERE summary_id = ?", (summary_id,))
    c.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))
    
    conn.commit()
    conn.close()
