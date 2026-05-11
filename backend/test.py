import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import uvicorn
import dataloader
from embedding import EmbeddingManager
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import SentenceTransformerEmbeddings
# pyrefly: ignore [missing-import]
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import RetrievalQA
from vectorstore import VectorStore
from langchain_groq import ChatGroq
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set. Please set it before running.")

PINECONE_KEY = os.getenv("PINECONE_KEY")
if not PINECONE_KEY:
    raise RuntimeError("PINECONE_KEY environment variable not set. Please set it before running.")

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("tourismindex")
embedding_manager = EmbeddingManager()
BACKEND_ROOT = Path(__file__).resolve().parent
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
vectorstore = PineconeVectorStore(index=index, embedding=embedding_model)
retriever = vectorstore.as_retriever(search_type="similarity")
llm = ChatGroq(groq_api_key = API_KEY, model_name = "llama-3.1-8b-instant", temperature=0.1, max_tokens= 1024)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

CITY_NAMES = [
    "kampala",
    "entebbe",
    "jinja",
    "murchison_falls_national_park",
    "bwindi_forest",
    "mbarara",
    "queen_elizabeth_national_park",
    "gulu",
    "kidepo_valley_national_park",
    "kibale_national_park",
    "rwenzori_mountains",
    "lake_bunyonyi",
    "sipi_falls",
    "lake_mburo_national_park",
    "kabale",
]

CITY_PDF_FOLDERS = [
    ("kampala", "./pdfs/kampala_pdfs"),
    ("entebbe", "./pdfs/entebbe_pdfs"),
    ("jinja", "./pdfs/jinja_pdfs"),
    ("murchison_falls_national_park", "./pdfs/murchison_falls_national_park_pdfs"),
    ("bwindi_forest", "./pdfs/bwindi_forest_pdfs"),
    ("mbarara", "./pdfs/mbarara_pdfs"),
    ("queen_elizabeth_national_park", "./pdfs/queen_elizabeth_national_park_pdfs"),
    ("gulu", "./pdfs/gulu_pdfs"),
    ("kidepo_valley_national_park", "./pdfs/kidepo_valley_national_park_pdfs"),
    ("kibale_national_park", "./pdfs/kibale_national_park_pdfs"),
    ("rwenzori_mountains", "./pdfs/rwenzori_mountains_pdfs"),
    ("lake_bunyonyi", "./pdfs/lake_bunyonyi_pdfs"),
    ("sipi_falls", "./pdfs/sipi_falls_pdfs"),
    ("lake_mburo_national_park", "./pdfs/lake_mburo_national_park_pdfs"),
    ("kabale", "./pdfs/kabale_pdfs"),
]


def setup_pinecone_namespaces(city_names=None):
    if city_names is None:
        city_names = CITY_NAMES

    stores = {}

    for city in city_names:
        stores[city] = PineconeVectorStore(
            index=index,
            embedding=embedding_model,
            namespace=city,
        )

    return stores


def ingest_all_city_documents_to_pinecone():

    for city, folder_path in CITY_PDF_FOLDERS:
        actual_path = BACKEND_ROOT / folder_path
        print(f"Ingesting documents for {city} from {actual_path}")

        if not actual_path.exists():
            print(f"  Folder does not exist: {actual_path}, skipping.")
            continue

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

        split_docs = embedding_manager.chunk_documents(all_docs)
        store = PineconeVectorStore(
            index=index,
            embedding=embedding_model,
            namespace=city,
        )
        store.add_documents(documents=split_docs)
        print(f"  Added {len(split_docs)} chunks for {city} to Pinecone namespace '{city}'\n")

# To ingest every city PDF and Word document folder into Pinecone, call:
# ingest_all_city_documents_to_pinecone()



    

def setup_namespaces():
    return setup_pinecone_namespaces()


# setup_namespaces()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 


@app.post("/Kampala_query")
def query_prompt(prompt):
    

    result = qa({"query": prompt})

    
    return result["result"]




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

