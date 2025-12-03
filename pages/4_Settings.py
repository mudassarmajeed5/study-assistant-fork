import streamlit as st
import requests

# Configure page
st.set_page_config(page_title="Settings - AI Study Assistant", page_icon="⚙️")

st.title("⚙️ Settings")
st.markdown("---")
st.write("Customize your study experience.")

st.markdown("### Preferences")
st.write("Enter your Gemini API Key ")
key = st.text_input("")
st.write()
st.write("Or", unsafe_allow_html=True)