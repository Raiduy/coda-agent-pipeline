from config.settings import settings

from langchain_openai import OpenAIEmbeddings

class ResearchPaperEmbedder:
    def __init__(self):
        """
        Initializes the embedding engine targeting the LiteLLM proxy server.
        """
        self.client = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            base_url=settings.LITELLM_BASE_URL,
            api_key=settings.LITELLM_API_KEY,
            check_embedding_ctx_length=False
        )


    def get_client(self) -> OpenAIEmbeddings:
        """Returns the configured LangChain embeddings instance."""
        return self.client
