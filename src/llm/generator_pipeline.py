from src.llm.context_builder import ContextBuilder
from src.llm.citation_builder import CitationBuilder    
from src.llm.response_generator import ResponseGenerator
from src.llm.formatter import ResponseFormatter
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.memory.chat_memory import ChatMemory
from src.memory.memory_formatter import MemoryFormatter

class GeneratorPipeline:
    def __init__(self):
        self.context_builder = ContextBuilder()
        self.citation_builder = CitationBuilder()
        self.response_generator = ResponseGenerator()
        self.formatter = ResponseFormatter()
        self.chat_memory = ChatMemory()
        self.memory_formatter = MemoryFormatter()

    def run(self,query,reranked_docs):
        context = self.context_builder.build_context(reranked_docs)
        history = self.chat_memory.get_history()
        formatted_history = self.memory_formatter.format_memory(history)
        response = self.response_generator.generate_response(query, context, formatted_history)
        citations = self.citation_builder.build_citation(reranked_docs)
        formatted_response = self.formatter.format_response(response, citations)

        self.chat_memory.add_message("user",query)
        self.chat_memory.add_message("assistant",formatted_response)

        return formatted_response
    
if __name__ == "__main__":

    retrieval_pipeline = RetrievalPipeline()
    generator_pipeline = GeneratorPipeline()
    query = "Class Diagram"
    reranked_docs = retrieval_pipeline.retrieve_run(query)
    final_response = generator_pipeline.run(query, reranked_docs)
    print(final_response)