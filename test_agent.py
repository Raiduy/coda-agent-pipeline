from src.agents.study_metadata_agent import study_metadata_node

from dotenv import load_dotenv

load_dotenv()

def test_metadata_extraction():
    print("Initializing Standalone Agent Test...")

    # 2. Mock the text that Docling would extract from a PDF first page
    # You can paste actual text from one of your target PDFs here to test it realistically!
    mock_pdf_context = """
    Journal of Data Science, Vol. 14, No. 2, 2025, pp. 120-135
    
    A Deep Learning Approach to Academic Feature Extraction
    By Sarah Jenkins, David Miller, and Elena Rostova
    Department of Computer Science, University of Technology
    
    Abstract: 
    Extracting structured metadata from unstructured PDF documents remains a significant challenge. 
    This study evaluates multi-agent architectures...
    
    This research was supported by the Global Science Foundation under Grant Series NCT0982731.
    """

    # 3. Mock the LangGraph state dictionary that the agent expects to receive
    mock_state = {
        "paper_id": "test_paper_001",
        "paper_context": mock_pdf_context,
        "extracted_features": []
    }

    print("\nSending context to StudyMetadataAgent...")
    
    # 4. Invoke the agent directly (remember, __call__ makes it behave like a function)
    result = study_metadata_node(mock_state)

    print("\nExtraction Complete! Results:")
    print("-" * 50)
    
    # Extract the payload from the state update format
    extracted_item = result["extracted_features"][0]
    print(f"Agent Name: {extracted_item['agent_name']}")
    
    # Pretty print the structured data dictionary
    import json
    print(json.dumps(extracted_item["data"], indent=4))
    print("-" * 50)

if __name__ == "__main__":
    test_metadata_extraction()
