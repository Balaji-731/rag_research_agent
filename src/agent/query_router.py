from langchain_ollama import OllamaLLM
from src.agent.router_prompt import ROUTER_PROMPT

class QueryRouter:
    def __init__(self):
        self.llm=OllamaLLM(model="llama3.2")
    
    def route_query(self,query):
        prompt=ROUTER_PROMPT.format(query=query)
        category=self.llm.invoke(prompt).strip().lower()
        return category.strip().lower()