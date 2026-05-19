from src.llm.context_builder import ContextBuilder
from src.llm.citation_builder import CitationBuilder    
from src.llm.response_generator import ResponseGenerator
from src.llm.formatter import ResponseFormatter
from src.retrieval.retrieval_pipeline import RetrievalPipeline

class GeneratorPipeline:
    def __init__(self):
        self.context_builder = ContextBuilder()
        self.citation_builder = CitationBuilder()
        self.response_generator = ResponseGenerator()
        self.formatter = ResponseFormatter()
    
    def run(self,query,reranked_docs):
        context = self.context_builder.build_context(reranked_docs)
        response = self.response_generator.generate_response(query, context)
        citations = self.citation_builder.build_citation(reranked_docs)
        formatted_response = self.formatter.format_response(response, citations)
        return formatted_response
    
if __name__ == "__main__":

    retrieval_pipeline = RetrievalPipeline()
    generator_pipeline = GeneratorPipeline()
    query = "Class Diagram"
    reranked_docs = retrieval_pipeline.retrieve_run(query)
    final_response = generator_pipeline.run(query, reranked_docs)
    print(final_response)