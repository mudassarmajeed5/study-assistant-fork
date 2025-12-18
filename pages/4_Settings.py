import streamlit as st
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ Settings")

# Initialize database
DB_PATH = Path("data/settings.db")
DB_PATH.parent.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_api_key():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT value FROM config WHERE key = 'api_key'")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""

def save_api_key(key):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('api_key', ?)", (key,))
    conn.commit()
    conn.close()

init_db()

# Load API key from database
if 'api_key' not in st.session_state:
    st.session_state.api_key = get_api_key()

# UI
api_key = st.text_input("API Key:", type="password", value=st.session_state.api_key)

if st.button("Save"):
    save_api_key(api_key)
    st.session_state.api_key = api_key
    st.success("✅ API Key saved!")