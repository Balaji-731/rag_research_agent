from src.llm.generator_pipeline import GeneratorPipeline
from src.retrieval.retrieval_pipeline import RetrievalPipeline


def main():

    # INITIALIZE PIPELINE
    ret_pipeline = RetrievalPipeline()
    gen_pipeline = GeneratorPipeline()

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

            # RUN PIPELINE
            reranked_docs = ret_pipeline.retrieve_run(query)
            response = gen_pipeline.run(query, reranked_docs)

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