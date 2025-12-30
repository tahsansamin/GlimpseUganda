from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader 
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
def process_all_word_docs(data_directory):
    documents = []
    data_path = Path(data_directory)
    docx_files = list(data_path.glob('**/*.docx'))
    print(f"[DEBUG] Found {len(docx_files)} Word files: {[str(f) for f in docx_files]}")
    for docx_file in docx_files:
        print(f"[DEBUG] Loading Word: {docx_file}")
        try:
            loader = Docx2txtLoader(str(docx_file))
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} Word docs from {docx_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load Word {docx_file}: {e}")
    return documents

