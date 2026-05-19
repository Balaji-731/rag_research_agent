from src.retrieval.retrieval_pipeline import RetrievalPipeline

class ContextBuilder:
    def build_context(self,reranked_docs):
        context=""
        for i,doc in enumerate(reranked_docs):
            context+=f"\nDocument {i+1}:\n"
            context+=f"{doc['content']}\n"
            context+="\n\n"
        return context
    
if __name__ == "__main__":
    retrieval_pipeline = RetrievalPipeline()
    context_builder = ContextBuilder()
    query = "Class Diagram"
    reranked_docs = retrieval_pipeline.retrieve_run(query)
    context = context_builder.build_context(reranked_docs)
    print(context)