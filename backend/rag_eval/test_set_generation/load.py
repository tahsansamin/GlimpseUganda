from langchain_community.document_loaders import DirectoryLoader
import os
from pinecone import Pinecone
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()




def get_pinecone_index(index_name: str = "tourismindex"):
    #setting up pinecone connections
    PINECONE_KEY = os.getenv("PINECONE_KEY")
    if not PINECONE_KEY:
        raise RuntimeError("PINECONE_KEY environment variable not set. Please set it before running.")

    pc = Pinecone(api_key=PINECONE_KEY)
    return pc.Index(index_name)


#function to load data from pinecone namespace kampala

def load_vector_db(namespace: str, index_name: str = "tourismindex"):
    index = get_pinecone_index(index_name)
    results = index.query(
        vector=[0.0] * 384,  # Dummy vector for retrieval; adjust as needed
        top_k=30,
        include_metadata=True,
        namespace = namespace
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



