import streamlit as st


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
