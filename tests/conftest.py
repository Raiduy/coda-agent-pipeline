# tests/conftest.py
import os
import pytest
from src.ingestion.parser import PaperParser

@pytest.fixture(scope="session")
def sample_pdf_path():
    """Provides the absolute path to the test PDF."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "data", "sample.pdf")
    return path

@pytest.fixture(scope="session")
def shared_parser():
    """Initializes the Docling parser once for the entire test session."""
    return PaperParser()
