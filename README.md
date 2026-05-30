# Agentic RAG Document Q&A 📄

An advanced, multimodal Document Q&A Agent powered by Retrieval-Augmented Generation (RAG). This application allows users to upload PDF documents and ask questions about them through text or voice, utilizing an intelligent orchestrator to route queries to the appropriate processing pipeline (RAG, Conversation, or Memory).

## Features 🚀

- **Smart Query Routing:** Uses an Orchestrator agent to classify and route user queries to the best pipeline (`rag`, `hybrid_rag`, `conversation`, or `memory`).
- **Multimodal Interactions (Voice & Text):** 
  - Voice-to-Text: Speak your questions using the microphone integration.
  - Text-to-Speech: Listen to the assistant's responses generated via `edge-tts`.
- **Advanced Document Ingestion:** Process and chunk multiple PDF files using PyMuPDF and LangChain, indexing them into a local ChromaDB vector store.
- **Conversational Memory:** Retains chat history for contextual understanding and follow-up questions.
- **Decoupled Architecture:** 
  - A robust **FastAPI backend** serving inference, ingestion, and voice processing endpoints.
  - A responsive **Streamlit frontend** with a modern UI, chat interface, and audio playback.
- **CLI Mode:** Includes a lightweight `main.py` interface for interacting with the agent via the terminal.

## Tech Stack 🛠️

- **Backend:** FastAPI, Python 3.11+
- **Frontend:** Streamlit, Streamlit Audio Recorder
- **LLM & RAG:** LangChain, LangGraph, ChromaDB, Sentence-Transformers, HuggingFace
- **Voice Services:** `edge-tts`
- **Document Parsing:** PyMuPDF, PyPDF

## Project Structure 📂

```text
.
├── api.py                  # FastAPI backend server with endpoints
├── app.py                  # Streamlit web interface
├── main.py                 # CLI interface for the agent
├── src/
│   ├── agent/              # Orchestrator, Conversational & Memory agents
│   ├── ingestion/          # Document ingestion and vector DB indexing
│   ├── llm/                # Generator pipeline for responses
│   ├── memory/             # Chat memory management
│   ├── retrieval/          # Retrieval pipeline for fetching context
│   └── voice/              # Voice-to-text and Text-to-speech services
├── vector_db/              # Local ChromaDB storage
├── pyproject.toml          # Project dependencies (uv/pip)
└── README.md               # Project documentation
```

## Setup & Installation ⚙️

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd rag-agent
   ```

2. **Install dependencies:**
   This project uses `pyproject.toml`. You can install the dependencies using `pip` or `uv`:
   ```bash
   pip install .
   # OR if using uv
   uv pip install .
   ```

## Running the Application 🏃‍♂️

You need to run both the FastAPI backend and the Streamlit frontend.

### 1. Start the API Server
Open a terminal and run the FastAPI server:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
*The API will be available at `http://localhost:8000`.*

### 2. Start the Web UI
Open a second terminal and start the Streamlit app:
```bash
streamlit run app.py
```
*The UI will open in your browser at `http://localhost:8501`.*

### (Optional) CLI Mode
If you prefer a terminal-based interaction without the web UI, run:
```bash
python main.py
```

## Usage Guide 💡

1. **Upload Documents:** Use the sidebar in the Streamlit app to upload one or more PDF files. Click **"Ingest Documents"** to parse and index them.
2. **Ask Questions:** 
   - Type your question in the chat input.
   - Or click the microphone icon to record your voice.
3. **View the Routing:** The app will display a caption indicating which route the orchestrator selected (e.g., `🔀 Route: rag`).
4. **Listen:** If available, an audio player will appear below the response to read it aloud.
5. **Clear History:** Use the sidebar button to reset the conversational memory.
