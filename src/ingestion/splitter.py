from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import PDFLoader
class TextSplitter:
    def __init__(self,chunk_size=1000,chunk_overlap=200):
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
            )
    def split(self,documents):
        chunks=self.splitter.split_documents(documents)
        return chunks
    
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