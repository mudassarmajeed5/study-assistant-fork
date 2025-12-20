import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import uuid
from helpers.db import (
    get_all_summaries, 
    get_summary_by_id, 
    init_db,
    get_summary_stats,
    get_quiz_scores_by_summary,
    get_weak_topics,
    delete_summary
)
from helpers.naive_bayes import NaiveBayesClassifier

init_db()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 AI Study Assistant")
st.markdown("---")

# Session code management
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8].upper()

st.sidebar.markdown("### 📌 Your Session Code")
st.sidebar.code(st.session_state.session_id)
st.sidebar.info("💡 Save this code to access your data later")

summaries = get_all_summaries(st.session_state.session_id)

if not summaries:
    st.info("📚 No saved summaries yet. Go to Upload and create one!")
else:
    # Summary Selection
    summary_dict = {title: sid for sid, title in summaries}
    selected = st.selectbox("📚 Select a Summary:", list(summary_dict.keys()))
    selected_id = summary_dict[selected]
    
    if st.button("📝 Select Summary"):
        content = get_summary_by_id(selected_id)
        st.session_state["selected_summary"] = content
        st.session_state["selected_summary_title"] = selected
        st.session_state["selected_summary_id"] = selected_id
        st.success(f"✅ Selected: {selected}")
    
    st.markdown("---")
    
    # Performance Dashboard
    st.markdown(f"### 📊 Performance Dashboard: {selected}")
    
    stats = get_summary_stats(selected_id)
    quiz_history = get_quiz_scores_by_summary(selected_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Score", f"{stats['avg_score']*100:.1f}%")
    
    with col2:
        st.metric("Attempts", stats['attempts'])
    
    with col3:
        st.metric("Best Score", f"{stats['best_score']*100:.1f}%")
    
    with col4:
        if stats['attempts'] > 0:
            avg = stats['avg_score']
            if avg >= 0.9:
                mastery = "Expert 🟢"
            elif avg >= 0.8:
                mastery = "Advanced 🟢"
            elif avg >= 0.7:
                mastery = "Intermediate 🟡"
            else:
                mastery = "Beginner 🔴"
        else:
            mastery = "No Data"
        st.metric("Mastery Level", mastery)
    
    st.markdown("---")
    
    # Performance Trend
    if quiz_history:
        st.markdown("### 📈 Performance Trend")
        
        df = pd.DataFrame(quiz_history, columns=["Score", "Total Questions", "Timestamp"])
        df["Score %"] = (df["Score"] * 100).round(1)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Timestamp"],
            y=df["Score %"],
            mode='lines+markers',
            name='Score',
            line=dict(color='#00D9FF', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title="Score History",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            hovermode='x unified',
            template='plotly_dark'
        )
        st.plotly_chart(fig, width='stretch')
        
        # Quiz history table
        st.markdown("### 📋 Quiz History")
        display_df = df[["Timestamp", "Score %", "Total Questions"]].copy()
        display_df.columns = ["Date", "Score %", "Questions"]
        st.dataframe(display_df, width='stretch', hide_index=True)
    else:
        st.info("No quiz attempts yet for this summary.")
    
    # Weak Topics Analysis (Naive Bayes)
    weak = get_weak_topics(selected_id)
    if weak:
        st.markdown("---")
        st.markdown("### 🎯 Topics to Review (Naive Bayes Analysis)")
        
        weak_df = pd.DataFrame(weak, columns=["Topic", "Accuracy %", "Questions"])
        weak_df["Accuracy %"] = (weak_df["Accuracy %"] * 100).round(1)
        st.dataframe(weak_df, width='stretch', hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Create Quiz", width='stretch'):
            st.switch_page("pages/2_Create_Quiz.py")
    
    with col2:
        if st.button("🃏 Flashcards", width='stretch'):
            st.switch_page("pages/3_Flash_Cards.py")
    
    with col3:
        if st.button("📄 Upload PDF", width='stretch'):
            st.switch_page("pages/1_Upload.py")
    
    with col4:
        if st.button("ℹ️ About", width='stretch'):
            st.switch_page("pages/5_About.py")
    
    st.markdown("---")
    st.markdown("### 🗑️ Manage Summaries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Current Summaries:** {len(summaries)}")
    
    with col2:
        if st.button("🗑️ Delete Selected Summary", type="secondary"):
            delete_summary(selected_id)
            del st.session_state["selected_summary"]
            del st.session_state["selected_summary_title"]
            del st.session_state["selected_summary_id"]
            st.success(f"✅ Deleted: {selected} and all related data")
            st.rerun()

