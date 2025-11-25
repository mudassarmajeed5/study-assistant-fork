import streamlit as st


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
