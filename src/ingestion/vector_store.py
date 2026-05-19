from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.ingestion.loader import PDFLoader
from src.ingestion.splitter import TextSplitter
from src.ingestion.embeddings import Embeddings


class VectorStore:

    def __init__(self):
        self.vector_store = Chroma(
            collection_name="rag_research",
            persist_directory="vector_db"
        )

    def add_documents(self, chunks, embedded_texts):
        documents = [
            Document(
                page_content=chunk.page_content,
                metadata=chunk.metadata
            )
            for chunk in chunks
        ]
        ids = [str(i) for i in range(len(chunks))]
        self.vector_store._collection.add(
            documents=[doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            embeddings=embedded_texts,
            ids=ids
        )

    def search(self, query_embedding, n_results=5):
        results = self.vector_store.similarity_search_by_vector(
            embedding=query_embedding,
            k=n_results
        )
        return results


if __name__ == "__main__":

    path = "Week 1.pdf"
    loader = PDFLoader(path)
    documents = loader.load()
    print(len(documents))

    chunker = TextSplitter()
    chunks = chunker.split(documents)
    print(len(chunks))

    embeddings = Embeddings()
    embedded_texts = embeddings.embed(chunks)
    print("\nEmbedding Dimension:")
    print(
        len(embedded_texts),
        len(embedded_texts[0])
    )

    query = "Why are UML Models Required?"
    query_embedding = embeddings.embed_query(query)
    print("\nQuery Embedding Dimension:")
    print(len(query_embedding))

    vector_db = VectorStore()
    vector_db.add_documents(
        chunks,
        embedded_texts
    )
    results = vector_db.search(
        query_embedding
    )
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---\n")
        print(result.page_content[:500])