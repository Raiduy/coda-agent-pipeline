from src.storage.embedder import ResearchPaperEmbedder
from src.storage.vector_store import VectorStoreManager

import pytest
from langchain_core.documents import Document

def test_vector_store_indexing_and_retrieval():
    # 1. Instantiate the modular embedder and manager explicitly
    embedder = ResearchPaperEmbedder()
    storage_manager = VectorStoreManager(embedder=embedder)
    
    mock_chunks = [
        Document(
            page_content="The methodology section describes using a random forest classifier with 100 estimators.",
            metadata={"Header 1": "Methodology"}
        )
    ]
    
    # 2. Build the store
    db = storage_manager.create_vector_store(mock_chunks)
    retriever = db.as_retriever(search_kwargs={"k": 1})
    
    # 3. Query & Verify
    relevant_docs = retriever.invoke("What classification algorithm?")
    assert len(relevant_docs) == 1
    assert "random forest" in relevant_docs[0].page_content

