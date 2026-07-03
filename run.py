import json
import operator
from config.settings import settings
from src.graph.workflow import build_workflow

# Assuming these modules exist in your codebase for document parsing and storage
from src.ingestion.parser import PaperParser
from src.storage.vector_store import VectorStoreManager
from src.storage.embedder import ResearchPaperEmbedder

def run_extraction_pipeline(pdf_path: str, paper_id: str = "paper_001"):
    print(f"🚀 [Pipeline] Launching extraction workflow for: {pdf_path}")
    
    # -------------------------------------------------------------
    # Phase 1: Document Ingestion & Chunking
    # -------------------------------------------------------------
    print("⏳ Parsing research paper PDF...")
    parser = PaperParser()
    chunks = parser.parse_pdf(pdf_path)
    print(f"✅ Extracted {len(chunks)} text chunks from paper.")

    # -------------------------------------------------------------
    # Phase 2: Create Vector Database Instance
    # -------------------------------------------------------------
    print("⏳ Generating text embeddings & spinning up Chroma DB...")
    embedder = ResearchPaperEmbedder()
    # Ensure VectorStoreManager returns an active langchain_chroma.Chroma instance
    vstore_manager = VectorStoreManager(embedder=embedder)
    vector_db = vstore_manager.create_vector_store(chunks)
    print("✅ Chroma vector database successfully populated and live.")

    # -------------------------------------------------------------
    # Phase 3: Compile and Invoke the LangGraph Pipeline
    # -------------------------------------------------------------
    print("⏳ Compiling Multi-Agent StateGraph...")
    app = build_workflow()

    # Create the initial state structured exactly like AgentState
    initial_state = {
        "paper_id": paper_id,
        "vector_store": vector_db,        # Pass live Chroma object directly into state
        "extracted_features": []          # Start with an empty list for parallel workers
    }

    print("\n🧠 Running Parallel RAG Extraction Workers...")
    print("   [Metadata, Demographics, Game Design, Game Parameters, Results] running simultaneously...")
    
    # Run the graph synchronously.
    # The framework manages concurrent branch execution automatically!
    final_state = app.invoke(initial_state)
    
    print("\n🏁 Graph execution successfully finished!")
    
    # Extract the final consolidated data payload compiled by SynthesisAgent
    extraction_results = final_state.get("final_consolidated_record", {})
    return extraction_results


if __name__ == "__main__":
    # Specify the local path to the research article you intend to meta-analyze
    target_pdf = "./tests/data/sample.pdf"
    
    try:
        results = run_extraction_pipeline(target_pdf, paper_id="study_smith_2021")
        
        # Pretty print the final dictionary containing variables 1 to 60
        print("\n======================= METADATA EXTRACTION RESULTS =======================")
        print(json.dumps(results, indent=4))
        print("===========================================================================")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed during execution: {e}")
