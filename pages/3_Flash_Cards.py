import json
import streamlit as st
from helpers.ai_models import generate_flashcards

# Configure page
st.set_page_config(page_title="Flash Cards - AI Study Assistant", page_icon="🃏")

st.title("🃏 Flash Cards")
st.markdown("---")
st.write("Create and review flash cards for effective memorization.")

# Check if extracted text is available
if "extracted_text" not in st.session_state:
    st.info("No content available. Go to Home and generate a summary from an uploaded PDF first.")
else:
    st.markdown("---")
    st.markdown("### Generate Flash Cards from Uploaded Content")
    st.write("Flash cards will be generated based on the extracted content.")

    if st.button("Generate Flash Cards", type="primary"):
        with st.spinner("Generating flash cards from your content..."):
            flashcards_text = generate_flashcards(st.session_state["extracted_text"])
        # Store the flash cards
        st.session_state["generated_flashcards"] = flashcards_text
        st.success("Flash cards generated from your content!")

    # Initialize session state for flashcard navigation
    if "current_flashcard_index" not in st.session_state:
        st.session_state.current_flashcard_index = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    # Display generated flash cards
    if "generated_flashcards" in st.session_state:
        try:
            flashcards_data = json.loads(st.session_state["generated_flashcards"])
            
            if flashcards_data and len(flashcards_data) > 0:
                st.markdown("---")
                st.markdown("### Flash Cards Review")
                
                current_idx = st.session_state.current_flashcard_index
                total_cards = len(flashcards_data)
                current_card = flashcards_data[current_idx]
                
                # Progress indicator
                st.progress((current_idx + 1) / total_cards)
                st.subheader(f"Card {current_idx + 1} of {total_cards}")
                
                # Flash card container with rotation animation
                card_container = st.container()
                with card_container:
                    # Add CSS for card rotation animation
                    st.markdown("""
                    <style>
                    .flashcard {
                        border: 2px solid #ddd;
                        border-radius: 10px;
                        padding: 2rem;
                        margin: 1rem 0;
                        min-height: 200px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        background: black;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        transition: transform 0.6s;
                        transform-style: preserve-3d;
                        cursor: pointer;
                    }
                    .flashcard.flipped {
                        transform: rotateY(180deg);
                    }
                    .card-content {
                        backface-visibility: hidden;
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        padding: 2rem;
                    }
                    .card-back {
                        transform: rotateY(180deg);
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Create unique key for this card to maintain animation state
                    flip_key = f"flip_card_{current_idx}"
                    
                    if not st.session_state.show_answer:
                        # Show question side
                        st.markdown(f"""
                        <div class="flashcard" id="{flip_key}">
                            <div class="card-content">
                                <div>
                                    <h3>{current_card['question']}</h3>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Show answer side with flip animation
                        st.markdown(f"""
                        <div class="flashcard flipped" id="{flip_key}">
                            <div class="card-content card-back">
                                <div>
                                    <h3>{current_card['answer']}</h3>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Control buttons
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    if not st.session_state.show_answer:
                        if col2.button("Show Answer", key=f"show_{current_idx}"):
                            st.session_state.show_answer = True
                    else:
                        if col2.button("Hide Answer", key=f"hide_{current_idx}"):
                            st.session_state.show_answer = False

                # Navigation buttons
                st.markdown("---")
                nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
                
                # Previous button
                if current_idx > 0:
                    if nav_col1.button("← Previous Card"):
                        st.session_state.current_flashcard_index -= 1
                        st.session_state.show_answer = False
                else:
                    nav_col1.empty()
                
                # Card counter in middle
                nav_col2.markdown(f"**{current_idx + 1} / {total_cards}**")
                
                # Next button
                if current_idx < total_cards - 1:
                    if nav_col3.button("Next Card →"):
                        st.session_state.current_flashcard_index += 1
                        st.session_state.show_answer = False
                else:
                    # Show completion message on last card
                    if nav_col3.button("🎉 Review Complete"):
                        st.balloons()
                        st.success("Great job! You've reviewed all flash cards.")
                        if st.button("Start Over"):
                            st.session_state.current_flashcard_index = 0
                            st.session_state.show_answer = False
                            
            else:
                st.warning("No flash cards found in the generated data.")
                
        except Exception as e:
            st.error("Error parsing flash cards data. Please generate new flash cards.")
            st.code(st.session_state["generated_flashcards"], language="json")
