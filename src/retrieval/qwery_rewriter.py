from langchain_ollama import OllamaLLM

class QueryRewriter:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def rewrite_query(self, query):
        prompt = f"""
        You are a query rewriting assistant.

        Rewrite the user query for better
        semantic retrieval in a RAG system.

        Only return the rewritten query.

        User Query:
        {query}

        Rewritten Query:
        """
        response=self.llm.invoke(prompt)
        return response.strip()

if __name__ == "__main__":
    rewriter = QueryRewriter()

    response = rewriter.rewrite_query(
        "What is RL?"
    )

    print(response)