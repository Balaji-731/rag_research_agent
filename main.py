from src.llm.generator_pipeline import GeneratorPipeline
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.agent.query_router import QueryRouter
from src.agent.conversational_agent import ConversationalAgent

def main():

    # INITIALIZE PIPELINE
    ret_pipeline = RetrievalPipeline()
    gen_pipeline = GeneratorPipeline()
    router = QueryRouter()
    conversational_agent = ConversationalAgent()
    


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
            route = router.route_query(query)
            print(
                f"\n[ROUTE]: {route}\n"
            )
            if route == "conversation":
                response = conversational_agent.generate_response(query,history="")
                
            elif route == "rag":

                # RUN PIPELINE
                reranked_docs = ret_pipeline.retrieve_run(query)
                response = gen_pipeline.run(query, reranked_docs, mode="rag")

            else:
                
                reranked_docs = ret_pipeline.retrieve_run(query)
                response = gen_pipeline.run(query, reranked_docs, mode="hybrid_rag")

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