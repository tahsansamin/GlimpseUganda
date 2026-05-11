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
from pydantic import BaseModel
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
def query_prompt(prompt: str):
    # Create a vectorstore scoped to the kampala namespace
    kampala_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="kampala"
    )
    kampala_retriever = kampala_store.as_retriever(search_type="similarity")
    kampala_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=kampala_retriever,
        return_source_documents=True
    )
    result = kampala_qa({"query": prompt})
    return result["result"]

@app.post("/Entebbe_query")
def query_prompt(prompt: str):
    # Create a vectorstore scoped to the entebbe namespace
    entebbe_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="entebbe"
    )
    entebbe_retriever = entebbe_store.as_retriever(search_type="similarity")
    entebbe_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=entebbe_retriever,
        return_source_documents=True
    )
    result = entebbe_qa({"query": prompt})
    return result["result"]


@app.post("/Jinja_query")
def jinja_query(prompt: str):
    jinja_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="jinja"
    )
    jinja_retriever = jinja_store.as_retriever(search_type="similarity")
    jinja_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=jinja_retriever,
        return_source_documents=True
    )
    result = jinja_qa({"query": prompt})
    return result["result"]


@app.post("/Murchison Falls National Park_query")
def murchison_falls_national_park_query(prompt: str):
    murchison_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="murchison_falls_national_park"
    )
    murchison_retriever = murchison_store.as_retriever(search_type="similarity")
    murchison_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=murchison_retriever,
        return_source_documents=True
    )
    result = murchison_qa({"query": prompt})
    return result["result"]


@app.post("/Bwindi Forest_query")
def bwindi_forest_query(prompt: str):
    bwindi_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="bwindi_forest"
    )
    bwindi_retriever = bwindi_store.as_retriever(search_type="similarity")
    bwindi_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=bwindi_retriever,
        return_source_documents=True
    )
    result = bwindi_qa({"query": prompt})
    return result["result"]


@app.post("/Mbarara_query")
def mbarara_query(prompt: str):
    mbarara_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="mbarara"
    )
    mbarara_retriever = mbarara_store.as_retriever(search_type="similarity")
    mbarara_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=mbarara_retriever,
        return_source_documents=True
    )
    result = mbarara_qa({"query": prompt})
    return result["result"]


@app.post("/Queen Elizabeth National Park_query")
def queen_elizabeth_national_park_query(prompt: str):
    queen_elizabeth_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="queen_elizabeth_national_park"
    )
    queen_elizabeth_retriever = queen_elizabeth_store.as_retriever(search_type="similarity")
    queen_elizabeth_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=queen_elizabeth_retriever,
        return_source_documents=True
    )
    result = queen_elizabeth_qa({"query": prompt})
    return result["result"]


@app.post("/Gulu_query")
def gulu_query(prompt: str):
    gulu_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="gulu"
    )
    gulu_retriever = gulu_store.as_retriever(search_type="similarity")
    gulu_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=gulu_retriever,
        return_source_documents=True
    )
    result = gulu_qa({"query": prompt})
    return result["result"]


@app.post("/Kidepo Valley National Park_query")
def kidepo_valley_national_park_query(prompt: str):
    kidepo_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="kidepo_valley_national_park"
    )
    kidepo_retriever = kidepo_store.as_retriever(search_type="similarity")
    kidepo_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=kidepo_retriever,
        return_source_documents=True
    )
    result = kidepo_qa({"query": prompt})
    return result["result"]


@app.post("/Kibale National Park_query")
def kibale_national_park_query(prompt: str):
    kibale_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="kibale_national_park"
    )
    kibale_retriever = kibale_store.as_retriever(search_type="similarity")
    kibale_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=kibale_retriever,
        return_source_documents=True
    )
    result = kibale_qa({"query": prompt})
    return result["result"]


@app.post("/Rwenzori Mountains_query")
def rwenzori_mountains_query(prompt: str):
    rwenzori_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="rwenzori_mountains"
    )
    rwenzori_retriever = rwenzori_store.as_retriever(search_type="similarity")
    rwenzori_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=rwenzori_retriever,
        return_source_documents=True
    )
    result = rwenzori_qa({"query": prompt})
    return result["result"]


@app.post("/Lake Bunyonyi_query")
def lake_bunyonyi_query(prompt: str):
    lake_bunyonyi_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="lake_bunyonyi"
    )
    lake_bunyonyi_retriever = lake_bunyonyi_store.as_retriever(search_type="similarity")
    lake_bunyonyi_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=lake_bunyonyi_retriever,
        return_source_documents=True
    )
    result = lake_bunyonyi_qa({"query": prompt})
    return result["result"]


@app.post("/Sipi Falls_query")
def sipi_falls_query(prompt: str):
    sipi_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="sipi_falls"
    )
    sipi_retriever = sipi_store.as_retriever(search_type="similarity")
    sipi_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=sipi_retriever,
        return_source_documents=True
    )
    result = sipi_qa({"query": prompt})
    return result["result"]


@app.post("/Lake Mburo National Park_query")
def lake_mburo_national_park_query(prompt: str):
    lake_mburo_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="lake_mburo_national_park"
    )
    lake_mburo_retriever = lake_mburo_store.as_retriever(search_type="similarity")
    lake_mburo_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=lake_mburo_retriever,
        return_source_documents=True
    )
    result = lake_mburo_qa({"query": prompt})
    return result["result"]


@app.post("/Kabale_query")
def kabale_query(prompt: str):
    kabale_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace="kabale"
    )
    kabale_retriever = kabale_store.as_retriever(search_type="similarity")
    kabale_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=kabale_retriever,
        return_source_documents=True
    )
    result = kabale_qa({"query": prompt})
    return result["result"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

