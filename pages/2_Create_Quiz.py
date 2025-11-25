import streamlit as st
from helpers.gemini import generate_quiz

# Configure page
st.set_page_config(page_title="Create Quiz - AI Study Assistant", page_icon="📝")

st.title("📝 Create Quiz")
st.markdown("---")
st.write("Create custom quizzes to test your knowledge.")

if "summary" not in st.session_state:
    st.info("No summary available. Go to Home and generate a summary from an uploaded PDF first.")
else:
    st.markdown("---")
    st.markdown("### Generate Quiz from Uploaded Summary")
    st.write("A quiz will be generated based on the extracted summary.")

    if st.button("Create QUIZ"):
        with st.spinner("Generating quiz from summary..."):
            quiz_text = generate_quiz(st.session_state["extracted_text"])
        # Store and display the quiz
        st.session_state["generated_quiz"] = quiz_text
        st.success("Quiz generated from your content!")

    # If a quiz was generated earlier in this session, display it
    if "generated_quiz" in st.session_state:
        st.markdown("---")
        st.markdown("### Generated Quiz (Raw JSON)")
    
        try:
            import json
            parsed = json.loads(st.session_state["generated_quiz"])
            st.json(parsed)   # <-- shows clean formatted JSON
        except Exception:
            st.code(st.session_state["generated_quiz"], language="json")

