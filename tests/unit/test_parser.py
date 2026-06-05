from langchain_core.documents import Document

def test_parser_returns_valid_chunks(shared_parser, sample_pdf_path):
    # Act: Run the parser
    chunks = shared_parser.parse_pdf(sample_pdf_path)
    
    # Assert: Verify the output matches expectations
    assert isinstance(chunks, list), "Parser should return a list"
    assert len(chunks) > 0, "Parser should extract at least one chunk"
    assert isinstance(chunks[0], Document), "Chunks must be LangChain Document objects"
    assert len(chunks[0].page_content) > 0, "Extracted text content should not be empty"
