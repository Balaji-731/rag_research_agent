import json
import re

from langchain_ollama import OllamaLLM

from src.agent.orchestrator_prompt import ORCHESTRATOR_PROMPT


class Orchestrator:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2",temperature=0)

    def decide(self,query,history):
        prompt = ORCHESTRATOR_PROMPT.format(query=query,history=history)
        response = self.llm.invoke(prompt)

        print(f"\n[ORCHESTRATOR RAW]: {response}\n")

        try:
            # EXTRACT JSON
            match = re.search(r'\{.*?\}',response,re.DOTALL)

            if match:
                json_text = (match.group())
                parsed = json.loads(json_text)
                action = parsed.get("action","rag")
                return action

        except Exception as e:
            print(f"\n[PARSER ERROR]: {e}\n")
            
        return "rag"