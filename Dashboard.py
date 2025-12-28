import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import markdown2
from weasyprint import HTML
from helpers.db import (
    get_all_summaries, 
    get_summary_by_id, 
    init_db,
    get_summary_stats,
    get_quiz_scores_by_summary,
    delete_summary
)

init_db()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 AI Study Assistant")
st.markdown("---")

summaries = get_all_summaries()

if not summaries:
    st.info("📚 No saved summaries yet. Go to Upload and create one!")
else:
    # Summary Selection with Cards
    st.markdown("### 📚 Select a Summary")
    summary_dict = {title: sid for sid, title in summaries}
    selected = st.session_state.get("selected_summary_title")
    
    # Display summary cards in 3 columns
    cols = st.columns(3)
    for idx, title in enumerate(summary_dict.keys()):
        with cols[idx % 3].container(border=True):
            # Show selected status
            if title == selected:
                st.markdown(f"✅ **{title}** (Selected)")
                button_label = "🔄 Switch"
            else:
                st.markdown(f"📖 {title}")
                button_label = "Select"
            
            # Select and Delete buttons side by side
            button_cols = st.columns(2)
            
            with button_cols[0]:
                if st.button(button_label, key=f"card_{idx}", use_container_width=True):
                    summary_id = summary_dict[title]
                    content = get_summary_by_id(summary_id)
                    st.session_state["selected_summary"] = content
                    st.session_state["selected_summary_title"] = title
                    st.session_state["selected_summary_id"] = summary_id
                    st.rerun()
            
            with button_cols[1]:
                if st.button("🗑️", key=f"delete_{idx}", use_container_width=True):
                    delete_summary(summary_dict[title])
                    if st.session_state.get("selected_summary_title") == title:
                        if "selected_summary" in st.session_state:
                            del st.session_state["selected_summary"]
                        if "selected_summary_title" in st.session_state:
                            del st.session_state["selected_summary_title"]
                        if "selected_summary_id" in st.session_state:
                            del st.session_state["selected_summary_id"]
                    st.success(f"✅ Deleted: {title}")
                    st.rerun()
    
   
    # Performance Dashboard (only show if a summary is selected)
    if st.session_state.get("selected_summary_title"):
        selected_id = st.session_state.get("selected_summary_id")
        st.markdown(f"### 📊 Performance Dashboard: {st.session_state.get('selected_summary_title')}")
        
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
                    mastery = "Platinum ⭐"
                elif avg >= 0.75:
                    mastery = "Gold 🏆"
                elif avg >= 0.6:
                    mastery = "Silver 🥈"
                else:
                    mastery = "Bronze 🥉"
            else:
                mastery = "No Data"
            st.metric("Rank", mastery)
        
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
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Create Quiz", use_container_width=True):
                st.switch_page("pages/2_Create_Quiz.py")
        
        with col2:
            if st.button("🃏 Flashcards", use_container_width=True):
                st.switch_page("pages/3_Flash_Cards.py")
        
        with col3:
            if st.button("📄 Upload PDF", use_container_width=True):
                st.switch_page("pages/1_Upload.py")
        
        with col4:
            if st.button("ℹ️ About", use_container_width=True):
                st.switch_page("pages/5_About.py")
        


    st.markdown("---")
    
    # Display Summary Content
    if st.session_state.get("selected_summary"):
        st.markdown(f"### 📄 Summary: {st.session_state.get('selected_summary_title')}")
        st.markdown(st.session_state.get("selected_summary"))
        
        # Download button
        summary_content = st.session_state.get("selected_summary")
        summary_title = st.session_state.get("selected_summary_title")
        
        html_content = markdown2.markdown(summary_content)
        pdf_bytes = HTML(string=html_content).write_pdf()
        if pdf_bytes is not None:
            st.download_button(
                label="📄 Download Summary as PDF",
                data=pdf_bytes,
                file_name=f"{summary_title}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        st.markdown("---")
    