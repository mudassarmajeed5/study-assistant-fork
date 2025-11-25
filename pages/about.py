import streamlit as st


def render_about():
    """Render the About page content."""
    st.title("ℹ️ About")
    st.markdown("---")
    st.write("AI Study Assistant - Your intelligent learning companion")
    
    st.markdown("### About This Application")
    st.write("""
    The AI Study Assistant is designed to help students and learners of all ages
    improve their study habits and retention through interactive study tools.
    """)
    
    st.markdown("### Technologies Used")
    st.write("- **Python** - Core programming language")
    st.write("- **Streamlit** - Web application framework")
    
    st.markdown("### Planned Integrations")
    st.write("- **Gemini** - AI model for content generation (coming soon)")
    st.write("- **HuggingFace** - NLP models and transformers (coming soon)")
    
    st.markdown("### Version")
    st.write("Version 1.0.0")
