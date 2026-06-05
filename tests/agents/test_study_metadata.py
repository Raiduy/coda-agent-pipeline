from src.agents.study_metadata_agent import study_metadata_node

def test_parser_to_metadata_agent_pipeline(shared_parser, sample_pdf_path):
    # 1. Parse the actual test document
    chunks = shared_parser.parse_pdf(sample_pdf_path)
    first_chunk_text = chunks[0].page_content

    # 2. Build the state payload the agent expects
    state = {
        "paper_id": "test_doc",
        "paper_context": first_chunk_text,
        "extracted_features": []
    }

    # 3. Invoke the metadata agent
    result = study_metadata_node(state)

    # 4. Assertions on the global LangGraph state update
    assert "extracted_features" in result, "Agent must return an updated features key"

    payload = result["extracted_features"][0]
    assert payload["agent_name"] == "StudyMetadataAgent"

    data = payload["data"]
    # Verify the output schema keys are fully present and populated
    for field in ["title", "authors_and_year", "study_number", "published_status"]:
        assert field in data, f"Missing required schema field: {field}"

    assert isinstance(data["published_status"], int), "Published status must be parsed as an integer"
