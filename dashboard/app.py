import inspect
import streamlit as st
import os
import tempfile
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestrator.core import OrchestratorAgent
from dashboard.session_manager import SessionManager
from agents.video_agent import VideoAgent

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

st.set_page_config(page_title="Unified AI Agent", page_icon="🤖", layout="wide")

# Initialize Session Manager
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# Initialize Orchestrator
if 'orchestrator' not in st.session_state:
    # Try to get key from env
    env_api_key = os.getenv("GROQ_API_KEY")
    if not env_api_key:
        st.warning("GROQ_API_KEY not found in environment variables.")
        st.stop()
    st.session_state.orchestrator = OrchestratorAgent(env_api_key)
else:
    # Ensure the orchestrator has the latest methods (hot-reload fix)
    try:
        # Check clear_context signature
        sig_clear = inspect.signature(st.session_state.orchestrator.clear_context)
        # Check route_query signature
        sig_route = inspect.signature(st.session_state.orchestrator.route_query)
        
        if 'session_id' not in sig_clear.parameters or 'agent_type' not in sig_route.parameters:
            print("DEBUG: Stale Orchestrator detected (signature mismatch). Reloading...")
            del st.session_state.orchestrator
            st.rerun()
            
    except Exception as e:
        # If any error checking signature, just reload to be safe
        print(f"DEBUG: Error checking signature: {e}. Reloading...")
        del st.session_state.orchestrator
        st.rerun()

# Sidebar for Session Management
with st.sidebar:
    st.title("Project Options")
    mode = st.radio("Select Agent", ["Search Agent", "PDF Agent", "Video Summarizer"], key="agent_mode")
    st.divider()

    st.title("🗂️ Sessions")
    
    if st.button("➕ New Session", use_container_width=True):
        new_session_id = st.session_state.session_manager.create_new_session()
        st.session_state.current_session_id = new_session_id
        # Save immediately so it shows up in the list, with default greeting
        default_msgs = [{"role": "assistant", "content": "Hi! I can answer questions about your PDFs or search the web. What would you like to know?"}]
        st.session_state.session_manager.save_session(new_session_id, default_msgs, "New Session")
        st.session_state.messages = default_msgs
        
        if 'orchestrator' in st.session_state:
            st.session_state.orchestrator.clear_context(new_session_id)
        st.rerun()

    if st.button("🔄 Reload System", help="Click this if the agent behaves unexpectedly (updates code)", use_container_width=True):
        if 'orchestrator' in st.session_state:
            del st.session_state.orchestrator
        st.rerun()

    st.divider()
    
    sessions = st.session_state.session_manager.list_sessions()
    
    # Ensure current_session_id is set
    if 'current_session_id' not in st.session_state:
        if sessions:
            st.session_state.current_session_id = sessions[0]["id"]
        else:
            st.session_state.current_session_id = st.session_state.session_manager.create_new_session()

    # Session List
    for session in sessions:
        button_style = "primary" if session["id"] == st.session_state.current_session_id else "secondary"
        if st.button(f"📄 {session['name']}", key=session["id"], use_container_width=True, type=button_style):
            st.session_state.current_session_id = session["id"]
            st.rerun()

# Load messages for current session
current_session = st.session_state.session_manager.load_session(st.session_state.current_session_id)
if current_session:
    st.session_state.messages = current_session.get("messages", [])
    print(f"DEBUG: Loaded session {st.session_state.current_session_id} with {len(st.session_state.messages)} messages")
else:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can answer questions about your PDFs or search the web. What would you like to know?"}
    ]
    print(f"DEBUG: New/Empty session {st.session_state.current_session_id}")

# Main Chat Interface
st.title("🤖 Unified AI Agent")

# Debug logging
print(f"DEBUG: Mode={mode}, SessionID={st.session_state.current_session_id}")

if mode == "Video Summarizer":
    st.header("🎥 Video Summarizer")
    st.markdown("Enter a YouTube video URL to get a detailed summary.")
    
    video_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Summarize Video", type="primary"):
        if video_url:
            with st.spinner("Fetching transcript and summarizing..."):
                try:
                    # Initialize VideoAgent
                    video_agent = VideoAgent(groq_api_key=os.getenv("GROQ_API_KEY"))
                    summary = video_agent.summarize(video_url)
                    
                    st.markdown("### 📝 Summary")
                    st.write(summary)
                    
                except Exception as e:
                    st.error(f"Error processing video: {e}")
        else:
            st.warning("Please enter a valid URL.")
            
    # Stop execution here so we don't show the chat interface
    st.stop()

elif mode == "PDF Agent":
    st.header("📄 PDF Agent")
    
    # Display uploaded PDFs
    uploaded_pdfs = st.session_state.orchestrator.get_uploaded_pdfs(st.session_state.current_session_id)
    if uploaded_pdfs:
        st.success(f"📚 Active PDFs ({len(uploaded_pdfs)}/5): {', '.join(uploaded_pdfs)}")
    else:
        st.warning("⚠️ No PDFs uploaded. Please upload a PDF to start chatting.")

    # File Upload Area
    with st.expander("➕ Upload PDFs", expanded=not uploaded_pdfs):
        uploaded_files = st.file_uploader("Upload PDF files (Max 5 total)", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            if st.button("Process Files"):
                with st.spinner("Processing PDFs..."):
                    for uploaded_file in uploaded_files:
                        # Save to temp file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Process via Orchestrator
                        try:
                            # Pass session ID and original filename
                            result = st.session_state.orchestrator.process_pdf(
                                tmp_path, 
                                st.session_state.current_session_id, 
                                original_filename=uploaded_file.name
                            )
                            
                            if result == -1:
                                st.error(f"❌ Limit reached! Cannot add {uploaded_file.name}. Max 5 PDFs allowed.")
                            elif result == -2:
                                st.info(f"ℹ️ {uploaded_file.name} is already uploaded.")
                            elif result == 0:
                                st.warning(f"⚠️ Processed {uploaded_file.name} but found no text.")
                            else:
                                st.success(f"✅ Added {uploaded_file.name} ({result} chunks)")
                                
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {e}")
                        finally:
                            os.remove(tmp_path)
                    st.rerun()

elif mode == "Search Agent":
    st.header("🔍 Search Agent")
    st.caption("I can search the web, Wikipedia, and Arxiv to answer your questions.")

# Display chat messages
print(f"DEBUG: Displaying {len(st.session_state.messages)} messages")
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Display Thinking Process
        if "history" in msg and msg["history"]:
            with st.expander("💭 Thinking Process"):
                for item in msg["history"]:
                    if isinstance(item, tuple):
                        role, content = item
                        if role == "ai":
                            st.markdown(f"**AI:** {content}")
                        elif role == "human":
                            st.markdown(f"**Observation:** {content}")
                    else:
                        st.write(item)

        # Display Sources
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 Sources"):
                for source in msg["sources"]:
                    st.write(f"- {source}")

# Chat Input
if prompt := st.chat_input(placeholder="Ask a question...", key="main_chat_input"):
    # Check if PDF Agent has files
    if mode == "PDF Agent":
        uploaded_pdfs = st.session_state.orchestrator.get_uploaded_pdfs(st.session_state.current_session_id)
        if not uploaded_pdfs:
            st.error("Please upload a PDF first.")
            st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Update session name if it's the first user query
    current_sess_data = st.session_state.session_manager.load_session(st.session_state.current_session_id)
    if not current_sess_data or current_sess_data.get("name") == "New Session":
        new_name = prompt[:30] + "..." if len(prompt) > 30 else prompt
        st.session_state.session_manager.update_session_name(st.session_state.current_session_id, new_name)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Route query with specific agent type
                result = st.session_state.orchestrator.route_query(
                    prompt, 
                    st.session_state.current_session_id,
                    agent_type=mode
                )
                
                response_text = result["response"]
                sources = result.get("sources", [])
                history = result.get("history", [])
                source_agent = result.get("source", mode)
                
                st.write(response_text)
                
                # Show Thinking Process for Search Agent
                if history:
                    with st.expander("💭 Thinking Process"):
                        for item in history:
                            if isinstance(item, tuple):
                                role, content = item
                                if role == "ai":
                                    st.markdown(f"**AI:** {content}")
                                elif role == "human":
                                    st.markdown(f"**Observation:** {content}")
                            else:
                                st.write(item)
                
                # Show Sources
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.write(f"- {source}")
                
                # Append to messages
                st.session_state.messages.append({
                    'role': 'assistant', 
                    "content": response_text,
                    "sources": sources,
                    "history": history
                })
                
                # Save session
                st.session_state.session_manager.save_session(
                    st.session_state.current_session_id, 
                    st.session_state.messages
                )
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
                print(f"ERROR in chat loop: {e}")

