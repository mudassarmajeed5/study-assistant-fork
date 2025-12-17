import json
import streamlit as st
from helpers.ai_models import generate_quiz
import pandas as pd
from helpers.ai_models import generate_flashcards
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
        with st.spinner("Generating quiz from your slides..."):
            quiz_text = generate_quiz(st.session_state["extracted_text"])
        # Store and display the quiz
        st.session_state["generated_quiz"] = quiz_text
        st.success("Quiz generated from your content!")
    # Initialize session state variables for quiz
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    # If a quiz was generated earlier in this session, display it
    if "generated_quiz" in st.session_state:
        try:
            quiz_data = json.loads(st.session_state["generated_quiz"])
            
            if quiz_data and len(quiz_data) > 0:
                st.markdown("---")
                st.markdown("### Quiz Interface")
                
                current_idx = st.session_state.current_question_index
                total_questions = len(quiz_data)
                current_question = quiz_data[current_idx]
                
                # Progress indicator
                st.progress((current_idx + 1) / total_questions)
                st.subheader(f"Question {current_idx + 1} of {total_questions}")
                
                # Display question
                st.write("**" + current_question['question'] + "**")
                st.write("")
                
                # Display options as radio buttons
                options = ["A", "B", "C", "D"]
                option_labels = [f"{opt}: {current_question['options'][opt]}" for opt in options]
                
                selected_answer = st.radio(
                    "Select your answer:",
                    options,
                    format_func=lambda x: f"{x}: {current_question['options'][x]}",
                    key=f"question_{current_idx}",
                    index=None
                )
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                # Submit answer button
                if selected_answer and not st.session_state.answer_submitted:
                    if col2.button("Submit Answer", type="primary"):
                        st.session_state.user_answers[current_idx] = selected_answer
                        st.session_state.answer_submitted = True
                        st.rerun()
                
                # Show result after submission
                if st.session_state.answer_submitted:
                    user_answer = st.session_state.user_answers.get(current_idx)
                    correct_answer = current_question['correct_option']
                    
                    if user_answer == correct_answer:
                        st.success("✅ Correct!")
                        
                        # Show explanation button for correct answers
                        if col2.button("Show Explanation"):
                            st.session_state.show_explanation = True
                            st.rerun()
                            
                    else:
                        st.error(f"❌ Incorrect! The correct answer is {correct_answer}")
                        st.session_state.show_explanation = True
                    
                    # Show explanation if needed
                    if st.session_state.show_explanation:
                        st.info("**Explanation:** " + current_question.get('answer_explanation', 'No explanation provided.'))
                
                # Navigation buttons
                nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
                
                # Previous button
                if current_idx > 0:
                    if nav_col1.button("← Previous"):
                        st.session_state.current_question_index -= 1
                        st.session_state.answer_submitted = False
                        st.session_state.show_explanation = False
                        st.rerun()
                
                # Next button
                if current_idx < total_questions - 1:
                    # Only show next button if answer is submitted
                    if st.session_state.answer_submitted:
                        if nav_col3.button("Next →"):
                            st.session_state.current_question_index += 1
                            st.session_state.answer_submitted = False
                            st.session_state.show_explanation = False
                            st.rerun()
                    else:
                        nav_col3.button("Next →", disabled=True, help="Submit your answer first")
                
                # Show completion message
                if current_idx == total_questions - 1 and st.session_state.answer_submitted:
                    st.balloons()
                    correct_count = sum(1 for i, answer in st.session_state.user_answers.items() 
                                      if i < len(quiz_data) and answer == quiz_data[i]['correct_option'])
                    st.success(f"🎉 Quiz completed! You got {correct_count} out of {len(st.session_state.user_answers)} questions correct.")
                    total_answered = len(st.session_state.user_answers)
                    if total_answered > 0:
                        incorrect_count = total_answered - correct_count
                        df = pd.DataFrame({"count": [correct_count, incorrect_count]}, index=["Correct", "Incorrect"])
                        st.markdown("### Quiz Results")
                        st.bar_chart(df)
                    else:
                        st.info("No answers to chart yet.")
                    
                    # Reset quiz button
                    if st.button("Start Over"):
                        st.session_state.current_question_index = 0
                        st.session_state.user_answers = {}
                        st.session_state.show_explanation = False
                        st.session_state.answer_submitted = False
                        st.rerun()
                        
            else:
                st.warning("No quiz questions found in the generated quiz.")
                
        except Exception as e:
            st.error("Error parsing quiz data. Please generate a new quiz.")
            st.code(st.session_state["generated_quiz"], language="json")
    