from langchain_ollama import OllamaLLM

class ConversationalAgent:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def generate_response(self,query,history):
        prompt = f"""
            You are a helpful AI assistant.

            Respond naturally and conversationally.

            If conversation history is available,
            use it to maintain continuity.

            =====================
            CONVERSATION HISTORY
            =====================

            {history}

            =====================
            USER
            =====================

            {query}

            =====================
            ASSISTANT
            =====================
            """
        response=self.llm.invoke(prompt)
        return response.strip()