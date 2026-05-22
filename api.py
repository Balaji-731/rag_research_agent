from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import tempfile

from src.ingestion.ingestion_pipeline import IngestionPipeline
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.llm.generator_pipeline import GeneratorPipeline
from src.agent.orchestrator import Orchestrator
from src.agent.conversational_agent import ConversationalAgent
from src.agent.memory_agent import MemoryAgent
from src.memory.chat_memory import ChatMemory
from src.memory.memory_formatter import MemoryFormatter

app = FastAPI(title="Document Q&A Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ret_pipeline = RetrievalPipeline()
gen_pipeline = GeneratorPipeline()
orchestrator = Orchestrator()
conversational_agent = ConversationalAgent()
memory_agent = MemoryAgent()
formatter = MemoryFormatter()
memory = ChatMemory()

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results=[]
    for file in files:
        tmp_dir=tempfile.mkdtemp()
        tmp_path=os.path.join(tmp_dir,file.filename)

        with open(tmp_path,"wb") as f:
            content=await file.read()
            f.write(content)

        pipeline = IngestionPipeline(tmp_path)
        status = pipeline.run()
        results.append({"file": file.filename, "status": status})

        os.remove(tmp_path)
        os.rmdir(tmp_dir)

    return {"message": "Files ingested successfully", "details": results}

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    """Ask a question about the uploaded documents."""
    query = req.question
    history = memory.get_history()
    formatted_history = formatter.format_memory(history)
    route = orchestrator.decide(query, formatted_history)
    if route == "conversation":
        response = conversational_agent.generate_response(query, formatted_history)
    elif route == "memory":
        response = memory_agent.answer_from_memory(query, formatted_history)
    elif route == "rag":
        reranked_docs = ret_pipeline.retrieve_run(query)
        response = gen_pipeline.run(query, reranked_docs, formatted_history, mode="rag")
    else:
        reranked_docs = ret_pipeline.retrieve_run(query)
        response = gen_pipeline.run(query, reranked_docs, formatted_history, mode="hybrid_rag")
    memory.add_message("user", query)
    memory.add_message("assistant", response)
    return {"route": route, "response": response}

@app.get("/history")
async def get_history():
    """Return the current chat history."""
    return {"history": memory.get_history()}

@app.post("/clear")
async def clear_session():
    """Clear chat history."""
    memory.clear_history()
    return {"message": "Session cleared"}
