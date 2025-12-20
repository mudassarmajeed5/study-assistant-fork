import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "database/summaries.db"

def init_db():
    # Ensure directory exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS summaries
                 (id INTEGER PRIMARY KEY, session_id TEXT, title TEXT, content TEXT, created_at TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores
                 (id INTEGER PRIMARY KEY, 
                  session_id TEXT,
                  summary_id INTEGER, 
                  score REAL,
                  total_questions INTEGER,
                  timestamp TEXT,
                  FOREIGN KEY(summary_id) REFERENCES summaries(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS topic_performance
                 (id INTEGER PRIMARY KEY,
                  session_id TEXT,
                  summary_id INTEGER,
                  topic TEXT,
                  correct INTEGER,
                  total INTEGER,
                  timestamp TEXT,
                  FOREIGN KEY(summary_id) REFERENCES summaries(id))''')
    
    conn.commit()
    conn.close()

def save_summary(title, content, session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO summaries (session_id, title, content, created_at) VALUES (?, ?, ?, ?)",
              (session_id, title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_summaries(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM summaries WHERE session_id = ? ORDER BY created_at DESC", (session_id,))
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

def save_quiz_score(summary_id, score, total_questions, session_id):
    """Save quiz score for a summary"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO quiz_scores 
                 (session_id, summary_id, score, total_questions, timestamp) 
                 VALUES (?, ?, ?, ?, ?)""",
              (session_id, summary_id, score, total_questions, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_quiz_scores_by_summary(summary_id):
    """Get all quiz scores for a summary"""
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

def save_topic_performance(summary_id, topic, correct, total, session_id):
    """Save performance for specific topic"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO topic_performance 
                 (session_id, summary_id, topic, correct, total, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (session_id, summary_id, topic, correct, total, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_weak_topics(summary_id, threshold=0.7):
    """Get topics with accuracy below threshold (aggregated across all quizzes)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT topic, 
                 CAST(SUM(correct) AS FLOAT) / SUM(total) as accuracy,
                 SUM(total) as total_questions
                 FROM topic_performance
                 WHERE summary_id = ?
                 GROUP BY topic
                 HAVING (CAST(SUM(correct) AS FLOAT) / SUM(total)) < ?
                 ORDER BY accuracy ASC""", (summary_id, threshold))
    weak_topics = c.fetchall()
    conn.close()
    return weak_topics

def delete_summary(summary_id):
    """Delete summary and cascade delete all related data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("DELETE FROM quiz_scores WHERE summary_id = ?", (summary_id,))
    c.execute("DELETE FROM topic_performance WHERE summary_id = ?", (summary_id,))
    c.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))
    
    conn.commit()
    conn.close()
