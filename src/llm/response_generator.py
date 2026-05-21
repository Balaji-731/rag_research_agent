from langchain_ollama import OllamaLLM
from src.llm.prompt import RAG_PROMPT
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.llm.context_builder import ContextBuilder

class ResponseGenerator:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def generate_response(self,query,context,history):
        prompt=RAG_PROMPT.format(context=context,question=query,history=history)
        response=self.llm.invoke(prompt)
        return response.strip()
    
if __name__ == "__main__":
    retrieval_pipeline = RetrievalPipeline()
    context_builder = ContextBuilder()
    query = "Class Diagram"
    reranked_docs = retrieval_pipeline.retrieve_run(query)
    context = context_builder.build_context(reranked_docs)
    response_generator = ResponseGenerator()
    response = response_generator.generate_response(query, context)
    print(response)