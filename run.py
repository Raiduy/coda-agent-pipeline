import json
import operator
from config.settings import settings
from src.graph.workflow import build_workflow
from src.utils.logger import logger

# Assuming these modules exist in your codebase for document parsing and storage
from src.ingestion.parser import PaperParser
from src.storage.vector_store import VectorStoreManager
from src.storage.embedder import ResearchPaperEmbedder
from src.utils.helpers import export_dict_to_csv

def run_extraction_pipeline(pdf_paths: list[str], paper_id: str = "paper_001"):
    pdf_paths = [pdf_paths] if isinstance(pdf_paths, str) else pdf_paths
    logger.info(f"🚀 [Pipeline] Launching extraction workflow for: {pdf_paths}")
    
    # -------------------------------------------------------------
    # Phase 1: Document Ingestion & Chunking
    # -------------------------------------------------------------
    logger.info("⏳ Parsing research paper PDFs...")
    parser = PaperParser()
    all_chunks = []
    for pdf_path in pdf_paths:
        chunks = parser.parse_pdf(pdf_path)
        all_chunks.extend(chunks)
    logger.info(f"✅ Extracted {len(all_chunks)} total text chunks from papers.")

    # -------------------------------------------------------------
    # Phase 2: Create Vector Database Instance
    # -------------------------------------------------------------
    logger.info("⏳ Generating text embeddings & spinning up Chroma DB...")
    embedder = ResearchPaperEmbedder()
    # Ensure VectorStoreManager returns an active langchain_chroma.Chroma instance
    vstore_manager = VectorStoreManager(embedder=embedder)
    vector_db = vstore_manager.create_vector_store(all_chunks)
    logger.info("✅ Chroma vector database successfully populated and live.")

    # -------------------------------------------------------------
    # Phase 3: Compile and Invoke the LangGraph Pipeline
    # -------------------------------------------------------------
    logger.info("⏳ Compiling Multi-Agent StateGraph...")
    app = build_workflow()

    # Create the initial state structured exactly like AgentState
    initial_state = {
        "paper_id": paper_id,
        "vector_store": vector_db,        # Pass live Chroma object directly into state
        "extracted_features": []          # Start with an empty list for parallel workers
    }

    logger.info("\n🧠 Running Parallel RAG Extraction Workers...")
    logger.info("   [Metadata, Demographics, Game Design, Game Parameters, Results] running simultaneously...")
    
    # Run the graph synchronously.
    # The framework manages concurrent branch execution automatically!
    final_state = app.invoke(initial_state)
    
    logger.info("\n🏁 Graph execution successfully finished!")
    
    # Extract the final consolidated data payload compiled by SynthesisAgent
    extraction_results = final_state.get("translated_cookbook_record", {})
    return extraction_results


if __name__ == "__main__":
    # Specify the local path to the research article you intend to meta-analyze
                   # "./pdfs/Abatayo et al. - 2018 - Facebook-to-Facebook online communication and eco-Supplementary materials.pdf"]
    
    # target_pdfs = ["./pdfs/Abatayo et al. - 2018 - Facebook-to-Facebook online communication and eco.pdf"]
    target_pdfs = ["./pdfs/Barr et al. - 2020 - Collective management of an environmental threat w.pdf"]
    # target_pdfs = ["./pdfs/Gomez-Ruiz and Sánchez-Expósito - 2020 - The Impact of Team Identity and Gender on Free-Rid.pdf"]
    # target_pdfs = ["./pdfs/Häusser et al. - 2019 - Acute hunger does not always undermine prosocialit.pdf"]
    # target_pdfs = ["./pdfs/Hilbig et al. - 2018 - Lead Us (Not) into Temptation Testing the Motivat.pdf"]
    # target_pdfs = ["./pdfs/Irlenbusch et al. - 2019 - Designing feedback in voluntary contribution games.pdf"]
    # target_pdfs = ["./pdfs/Pfattheicher et al. - 2018 - The Advantage of Democratic Peer Punishment in Sus.pdf"]
    # target_pdfs = ["./pdfs/Reyna et al. - 2018 - Social Values Orientation Slider Measure Evidence.pdf"]
    # target_pdfs = ["./pdfs/Sun et al. - 2023 - Intuitive thinking impedes cooperation by decreasi.pdf"]
    # target_pdfs = ["./pdfs/Xia et al. - 2021 - Religious identity, between-group effects and pros.pdf"]
    #
    try:
        results = run_extraction_pipeline(target_pdfs, paper_id="study_smith_2021")
        
        # Pretty print the final dictionary containing variables 1 to 60
        print("\n======================= METADATA EXTRACTION RESULTS =======================")
        print(json.dumps(results, indent=4))
        print("===========================================================================")
        export_dict_to_csv(results, './outputs/barr-gemma4-0.0.csv')
        
    except Exception as e:
        print(f"\n❌ Pipeline failed during execution: {e}")
