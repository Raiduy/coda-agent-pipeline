from typing import List
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

class PaperParser:
    def __init__(self):
        # 1. Explicitly configure pipeline options to shut off deprecated/unneeded image generation
        pipeline_options = PdfPipelineOptions()
        pipeline_options.allow_external_plugins = True
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True
        pipeline_options.generate_table_images = True  # explicitly disables the deprecated path
        
        # 2. Attach options to the PDF format configuration
        format_options = {
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
        
        # 3. Initialize DocumentConverter with your clean options
        self.converter = DocumentConverter(format_options=format_options)
        
        # Keep your text splitting configuration exactly the same
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, 
            strip_headers=False
        )

    def parse_pdf(self, pdf_path: str) -> List[Document]:
        """Converts a local PDF file into structurally split LangChain Documents."""
        print(f"📄 Docling is parsing layout for: {pdf_path}...")
        result = self.converter.convert(pdf_path)
        markdown_text = result.document.export_to_markdown()
        
        print("✂️ Splitting document by structural headers...")
        chunks = self.splitter.split_text(markdown_text)
        print(f"✅ Successfully split paper into {len(chunks)} chunks.")
        return chunks

