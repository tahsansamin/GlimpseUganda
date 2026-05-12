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
def process_pdf(pdf_path):
    """
    Processes a single PDF file and attaches metadata.
    """
    documents = []
    path_obj = Path(pdf_path)
    try:
        loader = PyPDFLoader(str(path_obj))
        pages = loader.load()
        for page in pages:
            # Consistent metadata tagging
            page.metadata['sourcefile'] = path_obj.name
            page.metadata['file_type'] = 'pdf'
        documents.extend(pages)
        print(f"Successfully loaded {len(pages)} pages from {path_obj.name}")
    except Exception as e:
        print(f"[ERROR] Failed to load PDF {pdf_path}: {e}")
    return documents


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

def process_word_doc(docx_path):
    """
    Processes a single Word (.docx) document and attaches metadata.
    """
    documents = []
    path_obj = Path(docx_path)
    try:
        loader = Docx2txtLoader(str(path_obj))
        loaded = loader.load()
        for doc in loaded:
            # Adding metadata consistency with your PDF function
            doc.metadata['sourcefile'] = path_obj.name
            doc.metadata['file_type'] = 'docx'
        documents.extend(loaded)
        print(f"Successfully loaded {path_obj.name}")
    except Exception as e:
        print(f"[ERROR] Failed to load Word doc {docx_path}: {e}")
    return documents



