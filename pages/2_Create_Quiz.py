import json
import streamlit as st
from helpers.ai_models import generate_quiz
import pandas as pd
from helpers.ai_models import generate_flashcards
from helpers.concept_extractor import ConceptExtractor
from helpers.difficulty_planner import DifficultyPlanner
from helpers.db import save_quiz_score, save_topic_performance, init_db
from helpers.naive_bayes import NaiveBayesClassifier

st.set_page_config(page_title="Create Quiz - AI Study Assistant", page_icon="📝")

init_db()

st.title("📝 Create Quiz")
st.markdown("---")

extractor = ConceptExtractor()
difficulty_planner = DifficultyPlanner()

if "selected_summary" not in st.session_state:
    st.info("No summary available. Go to Home and select a summary from the list.")
else:
    st.success(f"📖 Currently viewing: {st.session_state.get('selected_summary_title', 'Summary')}")
    st.markdown("---")
    
    topics = extractor.build_quiz_topics(st.session_state["selected_summary"])
    analysis = extractor.analyze_concept_relationships(st.session_state["selected_summary"])
    
    st.markdown("### 🧠 Summary Structure Analysis (DFS)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Main Concepts", analysis["total_main_concepts"])
    with col2:
        st.metric("Sub-Topics", analysis["total_subconcepts"])
    with col3:
        st.metric("Total Topics", analysis["total_main_concepts"] + analysis["total_subconcepts"])
    
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
    
    st.markdown("---")
    st.markdown("### 📊 Topics Grouped by Similarity (K-Means)")
    
    clustered_topics = difficulty_planner.get_topic_clusters_by_difficulty(topics)
    
    tab1, tab2, tab3 = st.tabs(["🟢 Easy", "🟡 Medium", "🔴 Hard"])
    
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
    st.markdown("### Generate Quiz from Summary")
    
    # Extract topics for Gemini constraint
    topics_for_quiz = [t["main"].lower() for t in topics]
    
    if st.button("Create QUIZ", type="primary", width='stretch'):
        with st.spinner("Generating quiz..."):
            quiz_text = generate_quiz(st.session_state["selected_summary"], topics_for_quiz)
            st.session_state["generated_quiz"] = quiz_text
            st.session_state["current_question_index"] = 0
            st.session_state["user_answers"] = {}
            st.session_state["quiz_performance"] = []
            st.session_state["show_results"] = False
        st.success("Quiz generated!")

    
    # Initialize session state for quiz
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_performance" not in st.session_state:
        st.session_state.quiz_performance = []
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "quiz_saved" not in st.session_state:
        st.session_state.quiz_saved = False
    
    # Display quiz
    if "generated_quiz" in st.session_state and not st.session_state.show_results:
        try:
            quiz_data = json.loads(st.session_state["generated_quiz"])
            
            if quiz_data and len(quiz_data) > 0:
                st.markdown("---")
                st.markdown("### Quiz Interface")
                
                current_idx = st.session_state.current_question_index
                current_question = quiz_data[current_idx]
                
                st.progress((current_idx + 1) / len(quiz_data))
                st.subheader(f"Question {current_idx + 1}/{len(quiz_data)}")
                
                # Display topic (normalized to lowercase)
                topic = current_question.get('topic', 'general').lower()
                st.markdown(f"**📚 Topic:** {topic}")
                st.write(current_question['question'])
                
                selected_answer = st.radio(
                    "Select answer:",
                    list(current_question['options'].values()),
                    key=f"answer_{current_idx}"
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("← Previous", width='stretch'):
                        if current_idx > 0:
                            st.session_state.current_question_index -= 1
                            st.rerun()
                
                with col2:
                    if st.button("Submit Answer", type="primary", width='stretch'):
                        st.session_state.user_answers[current_idx] = selected_answer
                        is_correct = selected_answer == current_question['options'][current_question['correct_option']]
                        st.session_state.quiz_performance.append(1.0 if is_correct else 0.0)
                        
                        if current_idx < len(quiz_data) - 1:
                            st.session_state.current_question_index += 1
                        else:
                            st.session_state.show_results = True
                        st.rerun()
                
                with col3:
                    if st.button("Skip →", width='stretch'):
                        if current_idx < len(quiz_data) - 1:
                            st.session_state.current_question_index += 1
                            st.rerun()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Show results
    if st.session_state.get("show_results", False) and "generated_quiz" in st.session_state:
        quiz_data = json.loads(st.session_state["generated_quiz"])
        
        st.markdown("---")
        st.markdown("### 📊 Quiz Results")
        
        score = sum(st.session_state.quiz_performance) / len(st.session_state.quiz_performance)
        st.metric("Score", f"{score * 100:.1f}%")
        
        # Save score to database (only once)
        summary_id = st.session_state.get("selected_summary_id")
        if summary_id and not st.session_state.quiz_saved:
            save_quiz_score(summary_id, score, len(quiz_data))
            
            # Naive Bayes analysis with normalized topics
            classifier = NaiveBayesClassifier()
            topic_results = []
            
            for i, q in enumerate(quiz_data):
                topic = q.get("topic", f"question {i+1}").lower()
                is_correct = st.session_state.quiz_performance[i] == 1.0
                topic_results.append((topic, is_correct))
                save_topic_performance(summary_id, topic, int(is_correct), 1)
            
            classifier.train(topic_results)
            st.session_state.quiz_saved = True
        
        # Display analysis
        if st.session_state.quiz_saved:
            classifier = NaiveBayesClassifier()
            topic_results = [(q.get("topic", f"question {i+1}").lower(), st.session_state.quiz_performance[i] == 1.0) 
                           for i, q in enumerate(quiz_data)]
            classifier.train(topic_results)
            
            col1, col2 = st.columns(2)
            with col1:
                weak = classifier.predict_weak_topics()
                if weak:
                    st.warning("🔴 **Topics to Review:**")
                    for w in weak:
                        st.write(f"- **{w['topic']}**: {w['accuracy']*100:.0f}% accuracy ({w['questions']} Q)")
            
            with col2:
                st.info(f"📈 **Mastery Level:** {classifier.get_mastery_level()}")
        
        if st.button("Take Another Quiz"):
            st.session_state.show_results = False
            st.session_state.generated_quiz = None
            st.session_state.quiz_saved = False
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_performance = []
            st.rerun()

    