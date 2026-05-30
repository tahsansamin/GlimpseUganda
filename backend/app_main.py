from datetime import datetime
from http.client import HTTPException
import os
from pathlib import Path
import tempfile
import cohere
from dotenv import load_dotenv, find_dotenv
import supabase
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
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from fastapi import FastAPI, Request, UploadFile, File, Form, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz
import json 
from supabase import create_client, Client
from pydantic import BaseModel
from datetime import datetime
import time
from functools import wraps
dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)

#creating supabase client
supabase: Client = create_client(os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_KEY"))

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set. Please set it before running.")

PINECONE_KEY = os.getenv("PINECONE_KEY")
if not PINECONE_KEY:
    raise RuntimeError("PINECONE_KEY environment variable not set. Please set it before running.")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY environment variable not set. Please set it before running.")

RETRIEVAL_K = 8
RERANK_TOP_N = 4
COHERE_RERANK_MODEL = "rerank-english-v3.0"

cohere_client = cohere.Client(api_key=COHERE_API_KEY)

pc = Pinecone(api_key=PINECONE_KEY)

index = pc.Index("tourismindex")

embedding_manager = EmbeddingManager()
BACKEND_ROOT = Path(__file__).resolve().parent
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
vectorstore = PineconeVectorStore(index=index, embedding=embedding_model)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": RETRIEVAL_K},
)
llm = ChatGroq(groq_api_key = API_KEY, model_name = "llama-3.3-70b-versatile", temperature=0, max_tokens= 1024)
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

def setup_namespaces():
    return setup_pinecone_namespaces()
# setup_namespaces()

def rate_limited(max_calls: int, time_frame: int):
    """
    :param max_calls: Maximum number of calls allowed in the specified time frame.
    :param time_frame: The time frame (in seconds) for which the limit applies.
    :return: Decorator function.
    """
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                    detail="Rate limit exceeded."
                )
                
            calls.append(now)
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator

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



    




# setup_namespaces()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 





class QueryRequest(BaseModel):
    prompt: str
    history: list = []

NAMESPACE_MAP = {
    "Kampala": "kampala",
    "Entebbe": "entebbe",
    "Jinja": "jinja",
    "Murchison Falls National Park": "murchison_falls_national_park",
    "Bwindi Forest": "bwindi_forest",
    "Mbarara": "mbarara",
    "Queen Elizabeth National Park": "queen_elizabeth_national_park",
    "Gulu": "gulu",
    "Kidepo Valley National Park": "kidepo_valley_national_park",
    "Kibale National Park": "kibale_national_park",
    "Rwenzori Mountains": "rwenzori_mountains",
    "Lake Bunyonyi": "lake_bunyonyi",
    "Sipi Falls": "sipi_falls",
    "Lake Mburo National Park": "lake_mburo_national_park",
    "Kabale": "kabale",
}


def cohere_rerank_documents(query: str, documents: list) -> list:
    if not documents:
        return []
    texts = [d.page_content for d in documents]
    resp = cohere_client.rerank(
        model=COHERE_RERANK_MODEL,
        query=query,
        documents=texts,
        top_n=min(RERANK_TOP_N, len(texts)),
    )
    out = [documents[r.index] for r in resp.results]
    index_order = [r.index for r in resp.results]
    print(
        f"[rerank] Cohere {COHERE_RERANK_MODEL}: "
        f"{len(documents)} vector hits -> top_n={len(resp.results)} for LLM; "
        f"pinecone_index_order={list(range(len(documents)))} "
        f"rerank_winner_index_order={index_order}"
    )
    for i, r in enumerate(resp.results, start=1):
        score = getattr(r, "relevance_score", None)
        if score is None:
            score = getattr(r, "score", None)
        score_str = f"{float(score):.4f}" if isinstance(score, (int, float)) else str(score)
        preview = documents[r.index].page_content[:100].replace("\n", " ")
        print(f"[rerank]   #{i} pinecone_idx={r.index} score={score_str} preview={preview!r}...")
    return out


from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def run_query(namespace: str, city_name: str, prompt: str, history: list = []) -> str:
    store = PineconeVectorStore(index=index, embedding=embedding_model, namespace=namespace)
    results = store.similarity_search_with_score(prompt, k=8)
    results.sort(key=lambda x: x[0].metadata.get("uploaded_at_ts", 0), reverse=True)
    docs = [doc for doc, score in results[:RETRIEVAL_K]]
    print(
        f"[rerank] query start namespace={namespace!r} "
        f"pinecone_k={RETRIEVAL_K} retrieved_docs={len(docs)}"
    )
    reranked = cohere_rerank_documents(prompt, docs)
    
    # Prettify namespace for logs (still useful)
    # city_display_name = namespace.replace('_', ' ').title() 

    context_str = "\n\n---\n\n".join(d.page_content for d in reranked) if reranked else "No specific documents found in the database for this query."
    
    # Construct the message sequence
    messages = [
        SystemMessage(
            content=(
                f"You are a knowledgeable Uganda tourism assistant specializing in {city_name}. "
                "Answer the user's question using the provided context whenever possible. "
                "Prioritize retrieved context over prior knowledge.\n\n"

                "If the context contains relevant information, base your answer primarily on it. "
                "If the context is incomplete, you may supplement with general knowledge about Uganda tourism, "
                "but do not invent specific facts such as prices, schedules, contact details, distances, or business information.\n\n"

                "If the answer cannot be determined reliably from the context or general knowledge, "
                "say that you are unsure instead of guessing.\n\n"

                "Only answer questions related to Uganda, travel, tourism, culture, transport, accommodation, food, attractions, or local experiences. "
                "Politely decline unrelated questions.\n\n"

                f"Context:\n{context_str}"
            )
        )
    ]
    
    # Add history (last 6 messages / 3 turns)
    for msg in history[-6:]:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg.get("content", "")))
        else:
            messages.append(AIMessage(content=msg.get("content", "")))
            
    # Add current prompt
    messages.append(HumanMessage(content=prompt))
    
    answer = llm.invoke(messages)
    return answer.content

def run_query_test(namespace: str, city_name: str, prompt: str, history: list = []) -> str:
    store = PineconeVectorStore(index=index, embedding=embedding_model, namespace=namespace)
    base_retriever = store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_K},
    )
    docs = base_retriever.invoke(prompt)
    print(
        f"[rerank] query start namespace={namespace!r} "
        f"pinecone_k={RETRIEVAL_K} retrieved_docs={len(docs)}"
    )
    reranked = cohere_rerank_documents(prompt, docs)
    
    # Prettify namespace for logs (still useful)
    # city_display_name = namespace.replace('_', ' ').title() 

    context_str = "\n\n---\n\n".join(d.page_content for d in reranked) if reranked else "No specific documents found in the database for this query."
    
    # Construct the message sequence
    messages = [
        SystemMessage(
            content=(
                f"You are a knowledgeable Uganda tourism assistant specializing in {city_name}. "
                "Use the provided context to answer the user's question. "
                "If the context does not contain the answer, use your own knowledge to provide a helpful and accurate response, "
                f"as long as it is relevant to {city_name} or Uganda tourism. "
                "If the question is completely unrelated to tourism or the location, politely decline to answer. "
                "Prioritize information from the context if it is available.\n\n"
                f"Context:\n{context_str}"
            )
        )
    ]
    
    # Add history (last 6 messages / 3 turns)
    for msg in history[-6:]:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg.get("content", "")))
        else:
            messages.append(AIMessage(content=msg.get("content", "")))
            
    # Add current prompt
    messages.append(HumanMessage(content=prompt))
    
    answer = llm.invoke(messages)
    answer_object = {
        "answer": answer.content,
        "source_chunks": reranked,
        }
    return answer_object




@app.post("/Kampala_query")
@rate_limited(max_calls = 10, time_frame = 60)
def kampala_query(request: QueryRequest):
    return run_query("kampala", "Kampala", request.prompt, request.history)

@app.post("/Entebbe_query")
@rate_limited(max_calls = 10, time_frame = 60)
def entebbe_query(request: QueryRequest):
    return run_query("entebbe", "Entebbe", request.prompt, request.history)

@app.post("/Jinja_query")
@rate_limited(max_calls = 10, time_frame = 60)
def jinja_query(request: QueryRequest):
    return run_query("jinja", "Jinja", request.prompt, request.history)

@app.post("/Murchison Falls National Park_query")
@rate_limited(max_calls = 10, time_frame = 60)
def murchison_falls_query(request: QueryRequest):
    return run_query("murchison_falls_national_park", "Murchison Falls National Park", request.prompt, request.history)

@app.post("/Bwindi Forest_query")
@rate_limited(max_calls = 10, time_frame = 60)
def bwindi_forest_query(request: QueryRequest):
    return run_query("bwindi_forest", "Bwindi Forest", request.prompt, request.history)

@app.post("/Mbarara_query")
@rate_limited(max_calls = 10, time_frame = 60)
def mbarara_query(request: QueryRequest):
    return run_query("mbarara", "Mbarara", request.prompt, request.history)

@app.post("/Queen Elizabeth National Park_query")
@rate_limited(max_calls = 10, time_frame = 60)
def queen_elizabeth_query(request: QueryRequest):
    return run_query("queen_elizabeth_national_park", "Queen Elizabeth National Park", request.prompt, request.history)

@app.post("/Gulu_query")
@rate_limited(max_calls = 10, time_frame = 60)
def gulu_query(request: QueryRequest):
    return run_query("gulu", "Gulu", request.prompt, request.history)

@app.post("/Kidepo Valley National Park_query")
@rate_limited(max_calls = 10, time_frame = 60)
def kidepo_query(request: QueryRequest):
    return run_query("kidepo_national_park", "Kidepo Valley National Park", request.prompt, request.history)

@app.post("/Kibale National Park_query")
@rate_limited(max_calls = 10, time_frame = 60)
def kibale_query(request: QueryRequest):
    return run_query("kibale_national_park", "Kibale National Park", request.prompt, request.history)

@app.post("/Rwenzori Mountains_query")
@rate_limited(max_calls = 10, time_frame = 60)
def rwenzori_query(request: QueryRequest):
    return run_query("rwenzori_mountains", "Rwenzori Mountains", request.prompt, request.history)

@app.post("/Lake Bunyonyi_query")
@rate_limited(max_calls = 10, time_frame = 60)
def lake_bunyonyi_query(request: QueryRequest):
    return run_query("lake_bunyonyi", "Lake Bunyonyi", request.prompt, request.history)

@app.post("/Sipi Falls_query")
@rate_limited(max_calls = 10, time_frame = 60)
def sipi_falls_query(request: QueryRequest):
    return run_query("sipi_falls", "Sipi Falls", request.prompt, request.history)

@app.post("/Lake Mburo National Park_query")
@rate_limited(max_calls = 10, time_frame = 60)
def lake_mburo_query(request: QueryRequest):
    return run_query("lake_mburo_national_park", "Lake Mburo National Park", request.prompt, request.history)

@app.post("/Kabale_query")
@rate_limited(max_calls = 10, time_frame = 60)
def kabale_query(request: QueryRequest):
    return run_query("kabale", "Kabale", request.prompt, request.history)

@app.post("/evaluation_query")
@rate_limited(max_calls = 10, time_frame = 60)
def evaluation_query(request: QueryRequest):
    return run_query_test("kampala", "Kampala", request.prompt, request.history)




def get_pdf_text(path):
    doc = fitz.open(path)
    full_text = ""
    
    for page in doc:
        full_text += page.get_text()
        
    doc.close()
    return full_text



class DocumentVerificationRequest(BaseModel):
    document: bytes  # The actual file content
    filename: str
    category: str  # location/category for the document

class CategoryRelevance(BaseModel):
    category_focus_percentage: int
    is_directly_related: bool
    reasoning: str

def parse_category_relevance(result_data: dict) -> CategoryRelevance:
    """Parse result_data into CategoryRelevance object"""
    return CategoryRelevance(
        category_focus_percentage=result_data.get("category_focus_percentage", 0),
        is_directly_related=result_data.get("is_directly_related", False),
        reasoning=result_data.get("reasoning", "")
    )


@app.post("/verify_document")
async def verify_document(
    document: UploadFile = File(...), 
    filename: str = Form(...), 
    category: str = Form(...)
):
    # 1. Read the bytes from the UploadFile object
    file_bytes = await document.read()
    
    # 2. Open with PyMuPDF
    doc = fitz.open(stream=file_bytes, filetype=filename.split('.')[-1])
    
    if doc.is_encrypted:
        return {"status": "error", "message": "Document is encrypted."}
        
    text = ""
    for page in doc:
        text += page.get_text()
        
    prompt = f"""
        Analyze the document below for its focus on the specific category: "{category}".

        STRICT CRITERIA:
        1. "Directly Related" means the text is specifically zoned in on {category}. 
        2. If the text is general jargon about Ugandan cities, geography, or broad tourism without focusing at least 50% of its content specifically on {category}, it fails.
        3. If the document covers multiple topics and {category} is just a minor mention, it fails.

        TASK:
        - Calculate the percentage of the text dedicated specifically to {category}.
        - Determine if it meets the 50% threshold.

        Return ONLY a JSON object in this format:
        {{
        "category_focus_percentage": <integer>,
        "is_directly_related": <boolean>,
        "reasoning": "<1-sentence explanation of the focus ratio>"
        }}

        Document text: 
        {text}
    """
    
    from langchain_core.messages import HumanMessage
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Robust JSON extraction (removing markdown fences if present)
    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    result_data = parse_category_relevance(json.loads(content))

    doc.close()
    
    return {
        "status": "verified", 
        "summary": result_data,
        "text_preview": text  
    }


@app.post("/transfer_to_pinecone")
async def process_document(request: Request):
    # 1. Verify it's actually from Supabase
    secret = request.headers.get("x-webhook-secret")
    if secret != os.environ["WEBHOOK_SECRET"]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()
    record = payload["record"]

    city = record["city"]          # folder name / city name
    file_name = record["file_name"]
    file_path = f"{city}/{file_name}"

    # 2. Skip unsupported files
    if not (file_name.endswith(".pdf") or file_name.endswith(".docx") or file_name.endswith(".doc")):
        return {"message": f"Skipping unsupported file: {file_name}"}

    print(f"Processing {file_path} for city {city}")

    # 3. Download from Supabase Storage
    file_bytes = supabase.storage.from_("test bucket").download(file_path)

    # 4. Write to temp file
    suffix = os.path.splitext(file_name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        # 5. Process the file
        if file_name.endswith(".pdf"):
            docs = dataloader.process_pdf(tmp_path)
        else:
            docs = dataloader.process_word_doc(tmp_path)

        if not docs:
            return {"message": "No content extracted"}

        # 6. Chunk + upload to Pinecone
        split_docs = embedding_manager.chunk_documents(docs)
        # add time metadata to each document for potential future use
        for doc in split_docs:
            doc.metadata["uploaded_at_ts"] = int(datetime.utcnow().timestamp())
        store = PineconeVectorStore(
            index=index,
            embedding=embedding_model,
            namespace=city,
        )
        store.add_documents(documents=split_docs)

        # 7. Mark as ready in DB
        supabase.table("pinecone_docs").update({"status": "ready"}).eq("id", record["id"]).execute()

        print(f"Added {len(split_docs)} chunks for {city}")
        print(f"Finished processing {file_path}")

        return {"success": True, "chunks": len(split_docs)}
    
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        supabase.table("documents").update({"status": "failed"}).eq("id", record["id"]).execute()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.unlink(tmp_path)
    





if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)