import json
import operator
from config.settings import settings
from src.graph.workflow import build_workflow

# Assuming these modules exist in your codebase for document parsing and storage
from src.ingestion.parser import PaperParser
from src.storage.vector_store import VectorStoreManager
from src.storage.embedder import ResearchPaperEmbedder

def run_extraction_pipeline(pdf_paths: list[str], paper_id: str = "paper_001"):
    pdf_paths = [pdf_paths] if isinstance(pdf_paths, str) else pdf_paths
    print(f"🚀 [Pipeline] Launching extraction workflow for: {pdf_paths}")
    
    # -------------------------------------------------------------
    # Phase 1: Document Ingestion & Chunking
    # -------------------------------------------------------------
    print("⏳ Parsing research paper PDFs...")
    parser = PaperParser()
    all_chunks = []
    for pdf_path in pdf_paths:
        chunks = parser.parse_pdf(pdf_path)
        all_chunks.extend(chunks)
    print(f"✅ Extracted {len(all_chunks)} total text chunks from papers.")

    # -------------------------------------------------------------
    # Phase 2: Create Vector Database Instance
    # -------------------------------------------------------------
    print("⏳ Generating text embeddings & spinning up Chroma DB...")
    embedder = ResearchPaperEmbedder()
    # Ensure VectorStoreManager returns an active langchain_chroma.Chroma instance
    vstore_manager = VectorStoreManager(embedder=embedder)
    vector_db = vstore_manager.create_vector_store(all_chunks)
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
    extraction_results = final_state.get("translated_cookbook_record", {})
    return extraction_results


if __name__ == "__main__":
    # Specify the local path to the research article you intend to meta-analyze
    target_pdfs = ["./pdfs/Abatayo et al. - 2018 - Facebook-to-Facebook online communication and eco.pdf"]
                   # "./pdfs/Abatayo et al. - 2018 - Facebook-to-Facebook online communication and eco-Supplementary materials.pdf"]
    
    try:
        results = run_extraction_pipeline(target_pdfs, paper_id="study_smith_2021")
        
        # Pretty print the final dictionary containing variables 1 to 60
        print("\n======================= METADATA EXTRACTION RESULTS =======================")
        print(json.dumps(results, indent=4))
        print("===========================================================================")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed during execution: {e}")
