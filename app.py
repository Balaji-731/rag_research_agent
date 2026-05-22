import streamlit as st
import requests

API_URL = "http://localhost:8000"

# ---- Page Config ----
st.set_page_config(
    page_title="Document Q&A Agent",
    page_icon="📄",
    layout="wide"
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

# ---- Display Chat History ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and "route" in msg:
            st.caption(f"🔀 Route: {msg['route']}")
        st.markdown(msg["content"])

# ---- Chat Input ----
if prompt := st.chat_input("Ask a question about your documents..."):

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
                else:
                    st.error(f"Error: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI is running on port 8000.")