import json
import streamlit as st
from helpers.ai_models import generate_quiz
import pandas as pd
from helpers.ai_models import generate_flashcards
from helpers.concept_extractor import ConceptExtractor
from helpers.difficulty_planner import DifficultyPlanner
# Configure page
st.set_page_config(page_title="Create Quiz - AI Study Assistant", page_icon="📝")

st.title("📝 Create Quiz")
st.markdown("---")

# Initialize concept extractor for DFS analysis and difficulty planner for BFS
extractor = ConceptExtractor()
difficulty_planner = DifficultyPlanner()

if "selected_summary" not in st.session_state:
    st.info("No summary available. Go to Home and select a summary from the list.")
else:
    st.success(f"📖 Currently viewing: {st.session_state.get('selected_summary_title', 'Summary')}")
    st.markdown("---")
    st.write("Create custom quizzes to test your knowledge.")
    
    # DFS Analysis of Summary Structure
    st.markdown("---")
    st.markdown("### 🧠 Summary Structure Analysis (DFS)")
    
    # Extract concepts using DFS
    topics = extractor.build_quiz_topics(st.session_state["selected_summary"])
    analysis = extractor.analyze_concept_relationships(st.session_state["selected_summary"])
    
    # Display analysis in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Main Concepts", analysis["total_main_concepts"])
    with col2:
        st.metric("Sub-Topics", analysis["total_subconcepts"])
    with col3:
        st.metric("Total Topics", analysis["total_main_concepts"] + analysis["total_subconcepts"])
    
    # Show complexity breakdown
    st.write("**Concept Complexity Breakdown:**")
    complexity_df = pd.DataFrame({
        "Complexity": ["Simple", "Moderate", "Complex"],
        "Count": [
            analysis["concepts_by_complexity"]["simple"],
            analysis["concepts_by_complexity"]["moderate"],
            analysis["concepts_by_complexity"]["complex"]
        ]
    })
    st.bar_chart(complexity_df.set_index("Complexity"))
    
    # Display topics in hierarchical order (DFS order)
    st.write("**Topics (in DFS order):**")
    for topic in topics:
        difficulty = extractor.get_concept_difficulty(topic)
        difficulty_emoji = "🟢" if difficulty == "Easy" else "🟡" if difficulty == "Medium" else "🔴"
        
        st.write(f"{difficulty_emoji} **{topic['main']}** ({difficulty})")
        if topic['subtopics']:
            for sub in topic['subtopics']:
                st.write(f"   └─ {sub}")
    
    # K-Means Clustering Analysis
    st.markdown("---")
    st.markdown("### 📊 Topics Grouped by Similarity (K-Means)")
    
    clustered_topics = difficulty_planner.get_topic_clusters_by_difficulty(topics)
    
    tab1, tab2, tab3 = st.tabs(["🟢 Cluster 1 (Easy)", "🟡 Cluster 2 (Medium)", "🔴 Cluster 3 (Hard)"])
    
    with tab1:
        if clustered_topics["Easy"]:
            for topic in clustered_topics["Easy"]:
                st.write(f"✓ {topic}")
        else:
            st.info("No topics in this cluster")
    
    with tab2:
        if clustered_topics["Medium"]:
            for topic in clustered_topics["Medium"]:
                st.write(f"✓ {topic}")
        else:
            st.info("No topics in this cluster")
    
    with tab3:
        if clustered_topics["Hard"]:
            for topic in clustered_topics["Hard"]:
                st.write(f"✓ {topic}")
        else:
            st.info("No topics in this cluster")
    
    st.markdown("---")
    progressive_sequence = difficulty_planner.get_progressive_quiz_sequence(topics)
    st.write("**Recommended Quiz Order:**")
    for idx, topic in enumerate(progressive_sequence, 1):
        st.write(f"{idx}. {topic}")
    
    st.markdown("---")
    st.markdown("### Generate Quiz from Summary")
    st.write("A quiz will be generated based on the selected summary.")

    if st.button("Create QUIZ"):
        with st.spinner("Generating quiz from your summary..."):
            quiz_text = generate_quiz(st.session_state["selected_summary"])
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
    