import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

API_URL = "http://localhost:8000"

# ---- Page Config ----
st.set_page_config(
    page_title="Document Q&A Agent",
    page_icon="📄",
    layout="wide"
)

# ---- Custom CSS for Mic Button ----
st.markdown(
    """
    <style>
    /* 1. Decrease the chat input width to create a gap on the right */
    div[data-testid="stChatInput"] {
        width: calc(100% - 75px) !important; 
        margin-right: auto !important; 
    }
    
    /* 2. Target the container holding the mic_recorder iframe */
    [data-testid="stElementContainer"]:has(iframe[title*="streamlit_mic_recorder"]) {
        position: fixed;
        bottom: 0px; 
        right: 3rem; 
        z-index: 9999;
        width: 60px; 
        height: 0px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: transparent !important;
    }
    
    /* 3. Scale the iframe itself to bypass the internal component sizing */
    iframe[title*="streamlit_mic_recorder"] {
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        transform: scale(1.5); 
        transform-origin: center center;
    }
    
    /* 4. Hide Streamlit's default loading skeleton for this specific component */
    [data-testid="stElementContainer"]:has(iframe[title*="streamlit_mic_recorder"]) [data-testid="stSkeleton"] {
        display: none !important;
    }
    
    /* 5. Ensure any other child div backgrounds are transparent during load */
    [data-testid="stElementContainer"]:has(iframe[title*="streamlit_mic_recorder"]) > div {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 Document Q&A Agent")
st.caption("Upload your PDFs and ask questions about them")

# ---- Sidebar: Upload + Controls ----
with st.sidebar:
    st.header("📁 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("🚀 Ingest Documents") and uploaded_files:
        with st.spinner("Ingesting documents..."):
            files = [
                ("files", (f.name, f.getvalue(), "application/pdf"))
                for f in uploaded_files
            ]
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {len(uploaded_files)} file(s) ingested!")
                    for detail in data["details"]:
                        st.write(f"- {detail['file']}: {detail['status']}")
                else:
                    st.error(f"❌ Ingestion failed: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Is the FastAPI server running?")

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        try:
            requests.post(f"{API_URL}/clear")
            st.session_state.messages = []
            st.rerun()
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API.")

# ---- Initialize Chat History ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_query" not in st.session_state:
    st.session_state.voice_query = None

# ---- Display Chat History ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and "route" in msg:
            st.caption(f"🔀 Route: {msg['route']}")
        st.markdown(msg["content"])

# ---- Voice Input ----
mic_placeholder = st.empty()

with mic_placeholder:
    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="⏹️",
        just_once=True,
        key="voice_recorder_fixed"
    )

if audio:
    # Processing state for the voice pipeline
    with st.spinner("Processing voice..."):
        try:
            files = {
                "audio": (
                    "voice.wav",
                    audio["bytes"],
                    "audio/wav")}
            response = requests.post(f"{API_URL}/voice",files=files)
            if response.status_code == 200:
                st.session_state.voice_query = response.json()["query"]
            else:
                st.error("Voice transcription failed.")
        except Exception as e:
            st.error(str(e))

# ---- Chat Input ----
text_prompt = st.chat_input("Ask a question about your documents...")
prompt = None
if text_prompt:
    prompt = text_prompt
elif st.session_state.voice_query:
    prompt = st.session_state.voice_query
    st.session_state.voice_query = None
if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": prompt}
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["response"]
                    route = data["route"]

                    st.caption(f"🔀 Route: {route}")
                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "route": route
                    })
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI is running on port 8000.")