from src.retrieval.qwery_rewriter import QueryRewriter
from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker

class RetrievalPipeline:
    def __init__(self):
        self.query_rewriter = QueryRewriter()
        self.retriever = Retriever()
        self.reranker = Reranker()

    def retrieve_run(self, query):
        rewritten_query = self.query_rewriter.rewrite_query(query)
        retrieved_docs = self.retriever.retrieve(rewritten_query)
        reranked_docs = self.reranker.rerank(query, retrieved_docs)

        return reranked_docs
    
if __name__ == "__main__":
    pipeline = RetrievalPipeline()
    query = "Class Diagram"
    results = pipeline.retrieve_run(query)
    print(results)