from src.ingestion.loader import PDFLoader
from src.ingestion.splitter import TextSplitter
from src.ingestion.embeddings import Embeddings
from src.ingestion.vector_store import VectorStore

class IngestionPipeline:
    def __init__(self,path):
        self.path=path
        self.loader=PDFLoader(path)
        self.chunker=TextSplitter()
        self.embeddings=Embeddings()
        self.vector_store=VectorStore()

    def run(self):
        documents=self.loader.load()
        chunks=self.chunker.split(documents)
        embedded_texts=self.embeddings.embed(chunks)
        self.vector_store.add_documents(chunks,embedded_texts)
        return "Ingestion Completed"
    
if __name__=="__main__":
    path="Week 2.pdf"
    pipeline=IngestionPipeline(path)
    result=pipeline.run()
    print(result)

        
        