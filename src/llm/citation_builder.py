class CitationBuilder:
  def build_citation(self, reranked_docs):
    citations=[]
    for i,doc in enumerate(reranked_docs):
        metadata=doc['metadata']
        citation={
           "source":metadata.get("source","Unknown Source"),
           "page":metadata.get("page","Unknown Page"),
           "author":metadata.get("author","Unknown Author"),
        }
        citations.append(citation)
    return citations
  
from src.retrieval.retrieval_pipeline import RetrievalPipeline
if __name__ == "__main__":
    pipeline = RetrievalPipeline()
    query = "Class Diagram"
    results = pipeline.retrieve_run(query)
    print(results)
    print("\nCitations:\n")
    citations = CitationBuilder().build_citation(results)
    print(citations)