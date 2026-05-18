from langchain_community.document_loaders import DirectoryLoader
import os
from pinecone import Pinecone


#setting up pinecone connections

PINECONE_KEY = os.getenv("PINECONE_KEY")
if not PINECONE_KEY:
    raise RuntimeError("PINECONE_KEY environment variable not set. Please set it before running.")

 
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("tourismindex")


#function to load data from pinecone namespace kampala
def download_data():
    results = index.query(
        vector=[0.0] * EMBEDDING_DIM,
        top_k=10000,
        include_metadata=True,
        namespace = "kampala"
    )
    documents = []
    for match in results["matches"]:
        metadata = match["metadata"].copy()
        text = metadata.pop("text", "")  # adjust key if yours is different
        documents.append(Document(
            page_content=text,
            metadata=metadata
        ))
    print(f"Loaded {len(documents)} chunks from namespace '{namespace}'")
    return documents



