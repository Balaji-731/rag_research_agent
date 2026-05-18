from langchain_community.document_loaders.pdf import PyMuPDFLoader

class PDFLoader:
    def __init__(self,path):
        self.path=path

    def load(self):
        loader=PyMuPDFLoader(self.path)
        documents=loader.load()
        return documents
    
if __name__=="__main__":
    path="Week 1.pdf"
    loader=PDFLoader(path)
    documents=loader.load()
    print(documents)
    