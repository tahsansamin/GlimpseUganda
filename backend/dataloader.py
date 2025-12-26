from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from pathlib import Path
def process_all_pdfs(pdf_directory):
    all_documents = []
    pdf_dir = Path(pdf_directory)
    pdf_files = list(pdf_dir.glob("**/*.pdf"))
    for pdf_file in pdf_files:
        print(f"processing {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()
            for page in pages:
                page.metadata['sourcefile'] = pdf_file.name
                page.metadata['file_type'] = 'pdf'
            all_documents.extend(pages)
            print(f"loaded {len(pages)} pages")
        except Exception as e:
            print(f"error is {e}")
    return all_documents