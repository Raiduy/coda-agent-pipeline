from src.agents.sample_demographics_agent import sample_demographics_node

def test_sample_demographics_agent_logic():
    mock_context = """
    Received for review on August 14, 2024. Accepted May 3, 2025.

    Methodology:
    We recruited an initial pool of 120 undergraduate students to participate in our behavioral trials at the 
    Ohio State University interaction lab located in the United States. 

    Data Cleaning:
    Out of the initial 120 participants, 20 participants were entirely excluded from final analyses due to failing 
    manipulation checks. The final regression models were fitted using the remaining dataset.
    """

    mock_state = {
        "paper_id": "test_audit_doc",
        "paper_context": mock_context,
        "extracted_features": []
    }
        
    # Run the agent
    result = sample_demographics_node(mock_state)
    
    # Assertions
    assert "extracted_features" in result
    data = result["extracted_features"][0]["data"]
    
    print("\n📊 Data Metadata Agent Extracted Payload:")
    import json
    print(json.dumps(data, indent=4))
    
    # Verify the fallback year was scraped from the 'Received' timestamp
    assert data["data_collection_year"] == 2024 | data["data_collection_year"] == '2024'
    assert data["source_of_year"] == 4
    
    # Verify ISO-3 mapping and explicit location sourcing
    assert data["country"] == "USA"
    assert data["source_of_country"] == 1
    
    # Verify mathematical exclusion logic
    assert data["sample_size"] == 100
