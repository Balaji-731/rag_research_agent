from src.llm.generator_pipeline import GeneratorPipeline
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.agent.orchestrator import Orchestrator
from src.agent.conversational_agent import ConversationalAgent
from src.agent.memory_agent import MemoryAgent
from src.memory.chat_memory import ChatMemory
from src.memory.memory_formatter import MemoryFormatter

def main():

    # INITIALIZE PIPELINE
    ret_pipeline = RetrievalPipeline()
    gen_pipeline = GeneratorPipeline()
    orchestrator = Orchestrator()
    conversational_agent = ConversationalAgent()
    memory_agent = MemoryAgent()
    formatter = MemoryFormatter()
    memory = ChatMemory()


    print("\n========== AGENTIC RAG ==========\n")

    print(
        "Type 'exit' to quit\n"
    )

    while True:

        # USER QUERY
        query = input(
            "\nAsk Question: "
        )

        # EXIT CONDITION
        if query.lower() == "exit":

            print("\nExiting...\n")

            break

        try:
            history = memory.get_history()
            formatted_history = formatter.format_memory(history)
            route = orchestrator.decide(query,formatted_history)
            print(
                f"\n[ROUTE]: {route}\n"
            )

            if route == "conversation":
                response = conversational_agent.generate_response(query,formatted_history)
                
            elif route == "memory":
                response = memory_agent.answer_from_memory(query,formatted_history)
                
            elif route == "rag":
                reranked_docs = ret_pipeline.retrieve_run(query)
                response = gen_pipeline.run(query, reranked_docs, formatted_history, mode="rag")

            else:
                reranked_docs = ret_pipeline.retrieve_run(query)
                response = gen_pipeline.run(query, reranked_docs, formatted_history, mode="hybrid_rag")

            memory.add_message("user",query)
            memory.add_message("assistant",response)

            # PRINT RESPONSE
            print(
                "\n========== RESPONSE ==========\n"
            )

            print(response)

        except Exception as e:

            print(
                "\nERROR:\n"
            )

            print(str(e))


if __name__ == "__main__":

    main()