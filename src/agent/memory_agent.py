from langchain_ollama import OllamaLLM

MEMORY_PROMPT = """
You are a conversation memory assistant for a Document Q&A system.

Your task is to answer the user's question using ONLY the conversation history below.

========================
RULES
========================

1. Answer strictly from the conversation history — do NOT make up information.
2. If the conversation history is empty or does not contain the answer, say:
   "We haven't discussed that yet in this conversation."
3. Be concise and direct.
4. If the user asks for a summary, provide a brief overview of the key topics discussed.

========================
CONVERSATION HISTORY
========================

{history}

========================
QUESTION
========================

{query}

========================
ANSWER
========================
"""

class MemoryAgent:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def answer_from_memory(self,query,history):
        prompt = MEMORY_PROMPT.format(query=query, history=history)
        response=self.llm.invoke(prompt)
        return response.strip()