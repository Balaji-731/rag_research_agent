class MemoryFormatter:
   
    def format_memory(self,history):
        formatted_history=""
        for message in history:
            role=message["role"]
            content=message["content"]
            formatted_history+=f"{role}: {content}\n"
        return formatted_history
