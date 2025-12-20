import streamlit as st
import sqlite3
import uuid
from pathlib import Path

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ Settings")

# Initialize session ID
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8].upper()

# Initialize database
DB_PATH = Path("database/settings.db")
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

# Session code management
st.markdown("### 📌 Your Session Code")
st.code(st.session_state.session_id)
st.info("💡 Save this code to access your data later")

st.markdown("### 🔄 Restore Previous Session")
restore_code = st.text_input("Enter a previous session code to restore:", placeholder="e.g., ABC12345")
if restore_code:
    st.session_state.session_id = restore_code.upper()
    st.success(f"✅ Session restored: {st.session_state.session_id}")

st.markdown("---")

# Load API key from database
if 'api_key' not in st.session_state:
    st.session_state.api_key = get_api_key()

st.markdown("### 🔑 API Key")
# UI
api_key = st.text_input("API Key:", type="password", value=st.session_state.api_key)

if st.button("Save"):
    save_api_key(api_key)
    st.session_state.api_key = api_key
    st.success("✅ API Key saved!")