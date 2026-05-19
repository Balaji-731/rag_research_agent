from langchain_huggingface import HuggingFaceEmbeddings
from src.ingestion.loader import PDFLoader
from src.ingestion.splitter import TextSplitter

class Embeddings:
    def __init__(self,model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = HuggingFaceEmbeddings(
            model_name=model_name
        )
    
    def embed(self,chunks):
        texts = [chunk.page_content for chunk in chunks]
        embedded_texts = (
            self.model.embed_documents(texts)
        )
        return embedded_texts
    
    def embed_query(self,query):
        embedded_query=self.model.embed_query(query)
        return embedded_query
    
if __name__=="__main__":

    path="Week 1.pdf"
    loader=PDFLoader(path)
    documents=loader.load()
    print(len(documents))

    chunker=TextSplitter()
    chunks=chunker.split(documents)
    print(len(chunks))
    for i, chunk in enumerate(chunks[:10]):
        print(f"\n--- Chunk {i+1} ---\n")
        print(chunk.page_content)

    embeddings=Embeddings()
    embedded_texts=embeddings.embed(chunks)
    print("\nEmbedding Dimension:")
    print(
        len(embedded_texts),
        len(embedded_texts[0])
    )

    query = "What is attention mechanism?"
    query_embedding = (
        embeddings.embed_query(query)
    )
    print("\nQuery Embedding Dimension:")
    print(len(query_embedding))