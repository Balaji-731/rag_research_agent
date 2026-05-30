import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder

API_URL = "http://localhost:8000"

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Document Q&A Agent",
    page_icon="📄",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stSidebar"] {
    border-right: 1px solid #2d2d2d;
}

.stChatMessage {
    border-radius: 12px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_query" not in st.session_state:
    st.session_state.voice_query = None

if "last_audio_processed" not in st.session_state:
    st.session_state.last_audio_processed = False

# =====================================================
# SIDEBAR
# =====================================================

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
                (
                    "files",
                    (
                        f.name,
                        f.getvalue(),
                        "application/pdf"
                    )
                )
                for f in uploaded_files
            ]

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"✅ {len(uploaded_files)} file(s) ingested!"
                    )

                    for detail in data["details"]:

                        st.write(
                            f"• {detail['file']}"
                        )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))

    st.divider()

    if st.button("🗑️ Clear Chat History"):

        try:

            requests.post(
                f"{API_URL}/clear"
            )

            st.session_state.messages = []
            st.session_state.voice_query = None
            st.session_state.last_audio_processed = False

            st.rerun()

        except Exception as e:

            st.error(str(e))

    st.divider()

    st.subheader("🎤 Voice Assistant")

    audio_bytes = audio_recorder(
        text="Start / Stop Recording",
        icon_name="microphone",
        icon_size="2x"
    )

    st.caption(
        "Click once to start recording and click again to stop."
    )

    voice_status_placeholder = st.empty()

# =====================================================
# VOICE PROCESSING
# =====================================================

if audio_bytes and not st.session_state.last_audio_processed:

    voice_status_placeholder.info(
        "🎤 Transcribing audio..."
    )

    try:

        files = {
            "audio": (
                "voice.wav",
                audio_bytes,
                "audio/wav"
            )
        }

        response = requests.post(
            f"{API_URL}/voice",
            files=files
        )

        if response.status_code == 200:

            transcript = (
                response.json()["query"]
            )

            st.session_state.voice_query = transcript
            st.session_state.last_audio_processed = True

            voice_status_placeholder.success(
                "✅ Audio transcribed"
            )

        else:

            voice_status_placeholder.error(
                "❌ Transcription failed"
            )

    except Exception as e:

        voice_status_placeholder.error(
            f"❌ {str(e)}"
        )

# =====================================================
# MAIN PAGE
# =====================================================

st.title("📄 Document Q&A Agent")

st.caption(
    "Upload your PDFs and ask questions about them"
)

# =====================================================
# CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if (
            msg["role"] == "assistant"
            and "route" in msg
        ):
            st.caption(
                f"🔀 Route: {msg['route']}"
            )

        st.markdown(
            msg["content"]
        )

# =====================================================
# CHAT INPUT
# =====================================================

text_prompt = st.chat_input(
    "Ask a question about your documents..."
)

prompt = None

if text_prompt:

    prompt = text_prompt

elif st.session_state.voice_query:

    prompt = st.session_state.voice_query

    st.session_state.voice_query = None
    st.session_state.last_audio_processed = False

# =====================================================
# PROCESS QUERY
# =====================================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": prompt
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data["response"]
                    route = data["route"]

                    st.caption(
                        f"🔀 Route: {route}"
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "route": route
                        }
                    )

                else:

                    st.error(
                        response.text
                    )

            except Exception as e:

                st.error(str(e))