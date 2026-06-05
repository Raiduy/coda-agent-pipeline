from config.settings import settings
from src.storage.embedder import ResearchPaperEmbedder

from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma

class VectorStoreManager:
    def __init__(self, embedder: ResearchPaperEmbedder = None):
        """
        Args:
            embedder: An instance of ResearchPaperEmbedder. If None, it instantiates one.
        """
        # Inject the modular embedder dependency
        self.embedder = embedder or ResearchPaperEmbedder()
    

    def create_vector_store(self, chunks: List[Document]) -> Chroma:
        """
        Creates an in-memory Chroma vector store populated with document chunks.
        """
        print(f"🧬 Generating embeddings using {settings.EMBEDDING_MODEL}...")
        
        # 2. Initialize Chroma dynamically with the documents and embedding engine
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedder.get_client()
        )
        
        print("💾 Vector store successfully initialized in memory.")
        return vector_store
