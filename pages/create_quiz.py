import streamlit as st
from gemini import generate_quiz

def render_create_quiz():
    """Render the Create Quiz page content."""
    st.title("📝 Create Quiz")
    st.markdown("---")
    st.write("Create custom quizzes to test your knowledge.")
    
    if "summary" not in st.session_state:
        st.info("No summary available. Go to Home and generate a summary from an uploaded PDF first.")
        return

    st.markdown("---")
    st.markdown("### Generate Quiz from Uploaded Summary")
    st.write("A quiz will be generated based on the extracted summary.")

    if st.button("Generate Quiz from Summary"):
        with st.spinner("Generating quiz from summary..."):
            quiz_text = generate_quiz(st.session_state["summary"])
        # Store and display the quiz
        st.session_state["generated_quiz"] = quiz_text
        st.success("Quiz generated from summary!")

    # If a quiz was generated earlier in this session, display it
    if "generated_quiz" in st.session_state:
        st.markdown("---")
        st.markdown("### Generated Quiz")
        st.markdown(st.session_state["generated_quiz"]) 
