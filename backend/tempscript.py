import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import dataloader
from embedding import EmbeddingManager
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

# Load environment variables
dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)

PINECONE_KEY = os.getenv("PINECONE_KEY")
if not PINECONE_KEY:
    raise RuntimeError("PINECONE_KEY environment variable not set. Please set it before running.")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("tourismindex")

# Initialize models and managers
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
embedding_manager = EmbeddingManager()

def ingest_all_city_documents_to_pinecone():
    downloads_dir = Path.home() / "Downloads" / "uganda_tourism_pdfs"
    print(f"Checking for documents in: {downloads_dir}")
    if not downloads_dir.exists():
        print(f"Downloads folder does not exist at {downloads_dir}")
        return

    # Find all subdirectories (each corresponds to a city/location slug)
    subdirs = sorted([d for d in downloads_dir.iterdir() if d.is_dir()])
    if not subdirs:
        print("No subdirectories found under uganda_tourism_pdfs.")
        return

    for actual_path in subdirs:
        city = actual_path.name
        print(f"Ingesting documents for {city} from {actual_path}")

        # Process all PDFs and Word documents in the folder
        pdf_docs = dataloader.process_all_pdfs(str(actual_path))
        word_docs = dataloader.process_all_word_docs(str(actual_path))

        if not pdf_docs and not word_docs:
            print(f"  No documents found for {city} in {actual_path}, skipping.")
            continue

        all_docs = []
        if pdf_docs:
            all_docs.extend(pdf_docs)
        if word_docs:
            all_docs.extend(word_docs)

        # Chunk the documents
        split_docs = embedding_manager.chunk_documents(all_docs)
        
        # Initialize the Pinecone store for this specific namespace
        store = PineconeVectorStore(
            index=index,
            embedding=embedding_model,
            namespace=city,
        )
        
        # Upload chunks to the Pinecone index namespace
        store.add_documents(documents=split_docs)
        print(f"  Successfully added {len(split_docs)} chunks for {city} to Pinecone namespace '{city}'\n")

if __name__ == "__main__":
    ingest_all_city_documents_to_pinecone()
