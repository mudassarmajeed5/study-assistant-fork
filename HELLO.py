import streamlit as st
# Configure the main page
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🎓 AI Study Assistant")
st.markdown("---")

st.markdown("""
Welcome to your AI-powered study companion! This application helps you enhance your learning experience with intelligent tools.

## Features

### 🏠 Home
Upload PDF files and generate AI-powered summaries from your study materials.

### 📝 Create Quiz
Generate custom quizzes from your study materials using AI to test your knowledge and understanding.

### 🃏 Flash Cards
Create interactive flashcards for efficient memorization and spaced repetition learning.

### ⚙️ Settings
Customize your study experience with personalized preferences and configurations.

### ℹ️ About
Learn more about the AI Study Assistant and its capabilities.

---

**Get started by selecting "Home" from the sidebar to upload your study materials!**
""")

# Add some styling and footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>AI Study Assistant v1.0.0</p>
        <p>Enhance your learning with artificial intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)
