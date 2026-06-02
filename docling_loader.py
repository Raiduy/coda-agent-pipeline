from langchain_docling.loader import DoclingLoader

FILE_PATH = "./pdfs/Sun et al. - 2023 - Intuitive thinking impedes cooperation by decreasi.pdf"

loader = DoclingLoader(file_path=FILE_PATH)

docs = loader.load()

for d in docs[:3]:
    print(f"- {d.page_content=}")

