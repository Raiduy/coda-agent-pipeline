import os

from dotenv import load_dotenv

from langchain_core.vectorstores import InMemoryVectorStore

from langchain_docling.loader import DoclingLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()


embeddings_model = OpenAIEmbeddings(
    model=os.environ.get("EMBEDDING_MODEL"),
    api_key=os.environ.get("LITELLM_API_KEY"),
    base_url=os.environ.get("LITELLM_BASE_URL"),

    # NOTE: Disables LangChain's local tokenization forcing it to pass your raw text string to LiteLLM instead.
    check_embedding_ctx_length=False
)


FILE_PATH = "./pdfs/Sun et al. - 2023 - Intuitive thinking impedes cooperation by decreasi.pdf"

loader = DoclingLoader(file_path=FILE_PATH)

docs = loader.load()

vector_store = InMemoryVectorStore(embeddings_model)

doc_ids = vector_store.add_documents(documents=docs)

retriever = vector_store.as_retriever()
docs = retriever.invoke("What does Experiment 2 explore?")
print(docs[0].page_content)
