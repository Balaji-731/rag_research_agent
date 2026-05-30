from sentence_transformers import CrossEncoder
from src.retrieval.retriever import Retriever  

class Reranker:
    def __init__(self,model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model=CrossEncoder(model_name,local_files_only=True)

    def rerank(self,query,retrieved_docs,top_k=3):
        pairs = [(query,doc["content"]) for doc in retrieved_docs]
        scores = self.model.predict(pairs)
        scored_docs = list(zip(retrieved_docs, scores))
        scored_docs = sorted(scored_docs,key=lambda x: x[1],reverse=True)

        top_docs = []
        for doc, score in scored_docs[:top_k]:
            doc["rerank_score"]=(float(score))
            top_docs.append(doc)
        return top_docs
        
if __name__ == "__main__":

    query = "Use Case Modelling"
    retriever = Retriever()
    retrieved_docs = retriever.retrieve(query)

    print("\n========== RETRIEVED DOCS ==========\n")
    for i, doc in enumerate(retrieved_docs):
        print(f"\n----- DOC {i+1} -----\n")
        print(doc["content"][:300])

    reranker = Reranker()
    reranked_docs = reranker.rerank(query=query,retrieved_docs=retrieved_docs,top_k=3)

    print("\n\n========== RERANKED DOCS ==========\n")
    for i, doc in enumerate(reranked_docs):
        print(f"\n===== RANK {i+1} =====\n")
        print(
            f"RERANK SCORE: "
            f"{doc['rerank_score']}"
        )
        print("\nCONTENT:\n")
        print(doc["content"][:500])
        print("\nMETADATA:\n")
        print(doc["metadata"])