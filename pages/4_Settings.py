import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ Settings")

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "Gemini"
if 'loaded' not in st.session_state:
    st.session_state.loaded = False

# Load from localStorage only once
if not st.session_state.loaded:
    loaded = components.html("""
    <script>
        const apiKey = localStorage.getItem('api_key') || '';
        const mode = localStorage.getItem('mode') || 'Gemini';
        const data = {api_key: apiKey, mode: mode};
        window.parent.postMessage({type: 'streamlit:setComponentValue', data: data}, '*');
    </script>
    """, height=0)
    
    if loaded:
        st.session_state.api_key = loaded.get('api_key', '')
        st.session_state.mode = loaded.get('mode', 'Gemini')
        st.session_state.loaded = True

# Choose mode
mode = st.radio("Choose:", ["Gemini", "Ollama"], 
                index=0 if st.session_state.mode == "Gemini" else 1)

# Gemini settings
if mode == "Gemini":
    api_key = st.text_input("API Key:", type="password", value=st.session_state.api_key)
    
    if st.button("Save"):
        st.session_state.api_key = api_key
        st.session_state.mode = "Gemini"
        
        # Save to localStorage
        components.html(f"""
        <script>
            localStorage.setItem('api_key', `{api_key}`);
            localStorage.setItem('mode', 'Gemini');
        </script>
        """, height=0)
        st.success("Saved!")

# Ollama settings
else:
    st.session_state.mode = "Ollama"
    components.html("""
    <script>
        localStorage.setItem('mode', 'Ollama');
    </script>
    """, height=0)
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        models = [m["name"] for m in response.json()["models"]]
        
        if models:
            model = st.selectbox("Model:", models)
            st.info(f"Using: {model}")
        else:
            st.warning("No models found")
    except:
        st.error("Ollama not running")