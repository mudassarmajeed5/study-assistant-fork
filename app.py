import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)
hii
# Define pages in order
PAGES = ["Home", "Create Quiz", "Flash Cards", "Settings", "About"]

# Initialize session state for current page
if "current_page" not in st.session_state:
    st.session_state.current_page = 0


def get_current_page_index():
    """Get the current page index from session state."""
    return st.session_state.current_page


def set_current_page(index):
    """Set the current page index in session state."""
    st.session_state.current_page = index


def navigate_to_page(page_name):
    """Navigate to a specific page by name."""
    if page_name in PAGES:
        st.session_state.current_page = PAGES.index(page_name)


def render_navigation():
    """Render the navigation buttons at the bottom of each page."""
    current_index = get_current_page_index()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Back button (show previous page name)
        if current_index > 0:
            prev_page = PAGES[current_index - 1]
            if st.button(f"← {prev_page}", key="back_btn", use_container_width=True):
                set_current_page(current_index - 1)
                st.rerun()
    
    with col2:
        # Page indicator
        st.markdown(
            f"<div style='text-align: center; color: gray;'>Page {current_index + 1} of {len(PAGES)}</div>",
            unsafe_allow_html=True
        )
    
    with col3:
        # Next button (show next page name)
        if current_index < len(PAGES) - 1:
            next_page = PAGES[current_index + 1]
            if st.button(f"{next_page} →", key="next_btn", use_container_width=True):
                set_current_page(current_index + 1)
                st.rerun()


def render_home():
    """Render the Home page content."""
    st.title("🏠 Home")
    st.markdown("---")
    st.write("Welcome to the AI Study Assistant!")
    st.write("This application helps you study more effectively using AI-powered tools.")
    
    st.markdown("### Features")
    st.write("- **Create Quiz**: Generate quizzes to test your knowledge")
    st.write("- **Flash Cards**: Create and review flash cards for memorization")
    st.write("- **Settings**: Customize your study experience")
    st.write("- **About**: Learn more about this application")
    
    st.markdown("---")
    st.info("Use the navigation buttons below to explore different features!")


def render_create_quiz():
    """Render the Create Quiz page content."""
    st.title("📝 Create Quiz")
    st.markdown("---")
    st.write("Create custom quizzes to test your knowledge.")
    
    st.markdown("### Quiz Options")
    topic = st.text_input("Enter a topic for your quiz:", placeholder="e.g., Python Programming")
    num_questions = st.slider("Number of questions:", 5, 20, 10)
    difficulty = st.selectbox("Difficulty level:", ["Easy", "Medium", "Hard"])
    
    if st.button("Generate Quiz", type="primary"):
        if topic:
            st.info(f"Quiz preview: '{topic}' with {num_questions} {difficulty} questions")
            st.warning("Quiz generation feature coming soon - AI integration in progress...")
        else:
            st.warning("Please enter a topic for your quiz.")


def render_flash_cards():
    """Render the Flash Cards page content."""
    st.title("🃏 Flash Cards")
    st.markdown("---")
    st.write("Create and review flash cards for effective memorization.")
    
    st.markdown("### Create New Flash Card")
    front = st.text_area("Front of card (Question):", placeholder="What is the capital of France?")
    back = st.text_area("Back of card (Answer):", placeholder="Paris")
    
    if st.button("Add Flash Card", type="primary"):
        if front and back:
            st.success("Flash card added successfully!")
        else:
            st.warning("Please fill in both sides of the card.")
    
    st.markdown("---")
    st.markdown("### Your Flash Cards")
    st.info("No flash cards yet. Create your first one above!")


def render_settings():
    """Render the Settings page content."""
    st.title("⚙️ Settings")
    st.markdown("---")
    st.write("Customize your study experience.")
    
    st.markdown("### Preferences")
    st.checkbox("Enable dark mode", value=False)
    st.checkbox("Show hints during quizzes", value=True)
    st.checkbox("Enable notifications", value=True)
    
    st.markdown("### Quiz Settings")
    st.slider("Default quiz timer (minutes):", 5, 60, 15)
    st.selectbox("Preferred difficulty:", ["Easy", "Medium", "Hard"])
    
    st.markdown("### Flash Card Settings")
    st.slider("Cards per session:", 5, 50, 20)
    st.checkbox("Shuffle cards", value=True)
    
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")


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


# Page render functions mapping
PAGE_RENDERERS = {
    0: "render_home",
    1: "render_create_quiz",
    2: "render_flash_cards",
    3: "render_settings",
    4: "render_about",
}


def main():
    """Main function to render the application."""
    # Sidebar with page selector
    st.sidebar.title("📚 AI Study Assistant")
    st.sidebar.markdown("---")
    
    # Quick navigation in sidebar
    st.sidebar.markdown("### Quick Navigation")
    for i, page in enumerate(PAGES):
        if st.sidebar.button(page, key=f"sidebar_{page}", use_container_width=True):
            set_current_page(i)
            st.rerun()
    
    st.sidebar.markdown("---")
    current_page = PAGES[get_current_page_index()]
    st.sidebar.info(f"Current page: **{current_page}**")
    
    # Render the current page content using function mapping
    page_index = get_current_page_index()
    render_functions = {
        0: render_home,
        1: render_create_quiz,
        2: render_flash_cards,
        3: render_settings,
        4: render_about,
    }
    
    if page_index in render_functions:
        render_functions[page_index]()
    
    # Render navigation buttons at the bottom
    st.markdown("---")
    render_navigation()


if __name__ == "__main__":
    main()
