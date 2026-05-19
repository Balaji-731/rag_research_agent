from src.ingestion.embeddings import Embeddings
from src.ingestion.vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embeddings = Embeddings()

    def retrieve(self, query):
        embed_query=self.embeddings.embed_query(query)
        results=self.vector_store.search(embed_query)

        retrieved_docs = []

        for doc in results:
            retrieved_docs.append({
                "id": doc.id,
                "content": doc.page_content,
                "metadata": doc.metadata
            })

        return retrieved_docs

    
if __name__ == "__main__":
    query = "Use Case Modelling"
    retriever=Retriever()
    retrieved_docs=retriever.retrieve(query)
    print(retrieved_docs)