from src.ingestion.embeddings import Embeddings
from src.ingestion.vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embeddings = Embeddings()

    def retrieve(self, query, n_results=5):
        embed_query=self.embeddings.embed_query(query)
        results=self.vector_store.search(embed_query)
        return results
    
if __name__ == "__main__":
    query = "Use Case Modelling"
    retriever=Retriever()
    results=retriever.retrieve(query)
    print(results)