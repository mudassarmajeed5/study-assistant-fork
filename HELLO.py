import streamlit as st
from helpers.db import get_all_summaries, get_summary_by_id, init_db

init_db()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 AI Study Assistant")
st.markdown("---")
st.markdown("### 📚 Select a Summary")

summaries = get_all_summaries()
if summaries:
    summary_dict = {title: sid for sid, title in summaries}
    selected_title = st.selectbox("Choose a lecture/slide:", list(summary_dict.keys()))
    
    summary_id = summary_dict[selected_title]
    content = get_summary_by_id(summary_id)
    st.session_state["selected_summary"] = content
    st.session_state["selected_summary_title"] = selected_title
    st.success(f"✅ Selected: {selected_title}")
else:
    st.info("No saved summaries yet. Go to Home and create one!")
