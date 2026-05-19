class ResponseFormatter:
    def format_response(self,response,citations):
        formatted_response="\nANSWER:\n\n"+response+"\n\nCitations:\n"
        for i,citation in enumerate(citations):
            formatted_response+=f"{i+1}. {citation['source']} - {citation['author']} (Page: {citation['page']})\n"
        return formatted_response
