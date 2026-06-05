from src.ingestion.parser import PaperParser
from src.storage.embedder import ResearchPaperEmbedder
from src.storage.vector_store import VectorStoreManager
from src.agents.study_metadata_agent import study_metadata_node

import pytest

def test_end_to_end_rag_extraction_flow(sample_pdf_path):
    print("\n🏁 Starting End-to-End RAG Integration Pipeline Test...")

    # ==========================================
    # Step 1: Ingestion Phase (Docling)
    # ==========================================
    parser = PaperParser()
    chunks = parser.parse_pdf(sample_pdf_path)
    
    assert len(chunks) > 0, "Ingestion failed: No text chunks extracted from the PDF."
    print(f"🔹 Docling extracted {len(chunks)} layout-aware chunks.")

    # ==========================================
    # Step 2: Storage Phase (Embeddings & Chroma)
    # ==========================================
    embedder = ResearchPaperEmbedder()
    storage_manager = VectorStoreManager(embedder=embedder)
    
    # Generate vectors and index them in our in-memory DB
    db = storage_manager.create_vector_store(chunks)
    
    # Create a standard retriever (fetch top 2 most relevant chunks)
    retriever = db.as_retriever(search_kwargs={"k": 5})

    # ==========================================
    # Step 3: Retrieval Phase (Simulate Agent Query)
    # ==========================================
    # We query for document metadata. The vector DB should surface the first page/header chunks.
    query_intent = "What is the title, publication year, author list, and study or trial identifier of this paper?"
    retrieved_docs = retriever.invoke(query_intent)
    
    assert len(retrieved_docs) > 0, "Retrieval failed: Chroma returned zero relevant documents."
    
    # Combine retrieved text snippets into a single context block for the agent
    combined_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    print(f"🔹 Retrieved {len(retrieved_docs)} relevant context blocks from the vector database.")

    # ==========================================
    # Step 4: Agent Phase (LiteLLM & Structured Output)
    # ==========================================
    # Mock the shared global state that our LangGraph architecture uses
    mock_state = {
        "paper_id": sample_pdf_path,
        "paper_context": combined_context,
        "extracted_features": []
    }
    
    print("🧠 Invoking StudyMetadataAgent with dynamically retrieved context...")
    agent_output = study_metadata_node(mock_state)

    # ==========================================
    # Step 5: Final Schema Validation
    # ==========================================
    assert "extracted_features" in agent_output, "Agent execution failed to output features."
    
    extraction_payload = agent_output["extracted_features"][0]
    assert extraction_payload["agent_name"] == "StudyMetadataAgent"
    
    extracted_data = extraction_payload["data"]
    print("\n🎉 Pipeline Execution Successful! Extracted Data:")
    import json
    print(json.dumps(extracted_data, indent=4))

    # Assert schema rules are strictly met
    assert "title" in extracted_data and len(extracted_data["title"]) > 0, "Failed to extract title."
    assert "authors_and_year" in extracted_data, "Failed to extract authors_and_year."
    assert isinstance(extracted_data["published_status"], int), "published_status must be a clean integer matching the schema rules."

    # # Assert quality
    # assert extracted_data["authors_and_year"] == "Sun, Qian; Luo, Shasha; Gao, Qianyun; Fan, Wenjian; Liu, Yongfang (2022)"
    # assert extracted_data["title"] == "Intuitive thinking impedes cooperation by decreasing cooperative expectations for pro-self but not for pro-social individuals"
    # assert extracted_data["published_status"] == 1

