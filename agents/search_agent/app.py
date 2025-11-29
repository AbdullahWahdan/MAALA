import streamlit as st
import os
from dotenv import load_dotenv
from core import SearchAgent
from langchain_community.callbacks import StreamlitCallbackHandler

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

st.set_page_config(page_title="Search Agent", page_icon="🔍", layout="wide")

st.title("🔍 Search Agent - Chat with Web Tools")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Try to get key from env
    env_api_key = os.getenv("GROQ_API_KEY")
    
    if env_api_key:
        st.success("API Key loaded from environment")
        api_key = env_api_key
    else:
        api_key = st.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.warning("Please enter your Groq API Key to proceed.")
    st.stop()

# Initialize Agent
if 'search_agent' not in st.session_state:
    st.session_state.search_agent = SearchAgent(api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat Input
if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        # We pass the prompt directly to the agent run method, or the messages list if that's what we decided in core.py
        # In core.py I kept it as passing 'messages'. 
        # However, standard AgentExecutor.run() expects a string query. 
        # If I pass a list of dicts, it might just stringify it which is messy.
        # Better to pass the prompt.
        # Let's check core.py again. I defined run(messages).
        # I will modify core.py to handle this better or just pass the prompt here.
        # Let's pass the prompt here for clarity.
        
        response = st.session_state.search_agent.run(prompt, callbacks=[st_cb])
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.write(response)
