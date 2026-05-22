from langchain_ollama import OllamaLLM
class MemoryAgent:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def answer_from_memory(self,query,history):
        prompt = f"""
            You are a conversation memory assistant.

            Use conversation history
            to answer the user's question.

            =====================
            CONVERSATION HISTORY
            =====================

            {history}

            =====================
            QUESTION
            =====================

            {query}

            =====================
            ANSWER
            =====================
            """
        response=self.llm.invoke(prompt)
        return response.strip()