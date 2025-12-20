import streamlit as st
import uuid

# Configure page
st.set_page_config(page_title="About - AI Study Assistant", page_icon="ℹ️")

# Initialize session ID
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8].upper()

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

st.markdown("### Current Integrations")
st.write("- **Gemini** - AI model for content generation")
st.write("- **PyPDF2** - PDF text extraction")
st.write("- **WeasyPrint** - PDF generation")

st.markdown("### Version")
st.write("Version 1.0.0")
