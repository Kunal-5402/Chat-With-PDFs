from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.vectorstores.chroma import Chroma
import argparse
import warnings
import os


warnings.filterwarnings("ignore")

os.environ['HUGGINGFACEHUB_API_TOKEN'] = ""

CHROMA_PATH = "chroma"


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = HuggingFaceEmbeddings()

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=1)

    # print(results)

    if len(results) == 0:
        print(f"Unable to find matching results.")
        return

    
    model = HuggingFaceHub(huggingfacehub_api_token=os.environ['HUGGINGFACEHUB_API_TOKEN'],
                            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
                            model_kwargs={"temperature":0.6, "max_new_tokens":100})
    
    response_text = model.predict(query_text)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text} \n\n Sources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
