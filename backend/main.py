import uvicorn
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import dataloader, embedding, vectorstore, retriever
from embedding import EmbeddingManager
from dataloader import process_all_pdfs, process_all_word_docs
from vectorstore import VectorStore
from retriever import RAGretriever
from langchain_groq import ChatGroq
from dotenv import load_dotenv,find_dotenv
from supabase import create_client, Client
import fitz
dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set. Please set it before running.")
llm = ChatGroq(groq_api_key = API_KEY, model_name = "llama-3.1-8b-instant", temperature=0.1, max_tokens= 1024)

class PromptRequest(BaseModel):
    prompt: str

class DocumentVerificationRequest(BaseModel):
    document: bytes  # The actual file content
    filename: str
    category: str  # location/category for the document

def rag_simple(query, retriever, llm, top_k = 3):
    results =retriever.retrieve(query, top_k = top_k)
    context = "\n\n".join([doc['content'] for doc in results]) if results else ""
    if not context:
        return "no relevant context found"
    prompt = f""" Use the following context to answer the question concisely. Limit your a
    Context: {context},
    question: {query}   
    answer: """ 
    response = llm.invoke([prompt.format(context = context, query = query)])
    return response.content

#setting up supabase client

supabase: Client = create_client(os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_KEY"))



def download_folder(bucket_name, folder_name, supabase_folder):
    os.makedirs(folder_name, exist_ok=True)
    
    files = supabase.storage.from_(bucket_name).list(supabase_folder)
    
    for file in files:
        file_path = f"{supabase_folder}/{file['name']}"
        data = supabase.storage.from_(bucket_name).download(file_path)
        
        with open(f"{folder_name}/{file['name']}", 'wb') as f:
            f.write(data)

        supabase.storage.from_(bucket_name).remove([file_path])
    supabase.storage.from_(bucket_name).upload(f"{supabase_folder}/.keep", b"")

    
    print(f"Downloaded {len(files)} files from {supabase_folder} and deleted them from supabase storage.")

# Download all location PDFs from Supabase
download_folder('test bucket', './pdfs/kampala_pdfs', 'kampala')
download_folder('test bucket', './pdfs/entebbe_pdfs', 'entebbe')
download_folder('test bucket', './pdfs/jinja_pdfs', 'jinja')
download_folder('test bucket', './pdfs/murchison_falls_national_park_pdfs', 'murchison_falls_national_park')
download_folder('test bucket', './pdfs/bwindi_forest_pdfs', 'bwindi_forest')
download_folder('test bucket', './pdfs/mbarara_pdfs', 'mbarara')
download_folder('test bucket', './pdfs/queen_elizabeth_national_park_pdfs', 'queen_elizabeth_national_park')
download_folder('test bucket', './pdfs/gulu_pdfs', 'gulu')
download_folder('test bucket', './pdfs/kidepo_valley_national_park_pdfs', 'kidepo_valley_national_park')
download_folder('test bucket', './pdfs/kibale_national_park_pdfs', 'kibale_national_park')
download_folder('test bucket', './pdfs/rwenzori_mountains_pdfs', 'rwenzori_mountains')
download_folder('test bucket', './pdfs/lake_bunyonyi_pdfs', 'lake_bunyonyi')
download_folder('test bucket', './pdfs/sipi_falls_pdfs', 'sipi_falls')
download_folder('test bucket', './pdfs/lake_mburo_national_park_pdfs', 'lake_mburo_national_park')
download_folder('test bucket', './pdfs/kabale_pdfs', 'kabale')

Kampala = VectorStore(persist_directory="kampala")
Entebbe = VectorStore(persist_directory="entebbe")
Jinja = VectorStore(persist_directory="jinja")
murchison_falls_national_park = VectorStore(persist_directory="murchison_falls_national_park")
bwindi_forest = VectorStore(persist_directory="bwindi_forest")
mbarara = VectorStore(persist_directory="mbarara")
queen_elizabeth_national_park = VectorStore(persist_directory="queen_elizabeth_national_park")
gulu = VectorStore(persist_directory="gulu")
kidepo_valley_national_park = VectorStore(persist_directory="kidepo_valley_national_park")
kibale_national_park = VectorStore(persist_directory="kibale_national_park")
rwenzori_mountains = VectorStore(persist_directory="rwenzori_mountains")
lake_bunyonyi = VectorStore(persist_directory="lake_bunyonyi")
sipi_falls = VectorStore(persist_directory="sipi_falls")
lake_mburo_national_park = VectorStore(persist_directory="lake_mburo_national_park")
kabale = VectorStore(persist_directory="kabale")
embedding_manager = EmbeddingManager()
rag_retriever_kampala = RAGretriever(vector_store=Kampala,
                                    embedding_manager=embedding_manager)
rag_retriever_entebbe = RAGretriever(vector_store=Entebbe,
                                    embedding_manager=embedding_manager)
rag_retriever_jinja = RAGretriever(vector_store=Jinja,
                                    embedding_manager=embedding_manager)
rag_retriever_murchison_falls_national_park = RAGretriever(vector_store=murchison_falls_national_park, embedding_manager=embedding_manager)
rag_retriever_bwindi_forest = RAGretriever(vector_store=bwindi_forest, embedding_manager=embedding_manager)
rag_retriever_mbarara = RAGretriever(vector_store=mbarara, embedding_manager=embedding_manager)
rag_retriever_queen_elizabeth_national_park = RAGretriever(vector_store=queen_elizabeth_national_park, embedding_manager=embedding_manager)
rag_retriever_gulu = RAGretriever(vector_store=gulu, embedding_manager=embedding_manager)
rag_retriever_kidepo_valley_national_park = RAGretriever(vector_store=kidepo_valley_national_park, embedding_manager=embedding_manager)
rag_retriever_kibale_national_park = RAGretriever(vector_store=kibale_national_park, embedding_manager=embedding_manager)
rag_retriever_rwenzori_mountains = RAGretriever(vector_store=rwenzori_mountains, embedding_manager=embedding_manager)
rag_retriever_lake_bunyonyi = RAGretriever(vector_store=lake_bunyonyi, embedding_manager=embedding_manager)
rag_retriever_sipi_falls = RAGretriever(vector_store=sipi_falls, embedding_manager=embedding_manager)
rag_retriever_lake_mburo_national_park = RAGretriever(vector_store=lake_mburo_national_park, embedding_manager=embedding_manager)
rag_retriever_kabale = RAGretriever(vector_store=kabale, embedding_manager=embedding_manager)

#adding word documents for each city
def process_city_documents(city_obj, folder_path):
    word_documents = dataloader.process_all_word_docs(folder_path)
    word_split_documents = embedding_manager.chunk_documents(word_documents)
    word_embeddings = embedding_manager.generate_embeddings([doc.page_content for doc in word_split_documents])
    city_obj.add_documents(word_split_documents, word_embeddings)

process_city_documents(Kampala, "./pdfs/kampala_pdfs")
process_city_documents(Entebbe, "./pdfs/entebbe_pdfs")
process_city_documents(Jinja, "./pdfs/jinja_pdfs")
process_city_documents(murchison_falls_national_park, "./pdfs/murchison_falls_national_park_pdfs")
process_city_documents(bwindi_forest, "./pdfs/bwindi_forest_pdfs")
process_city_documents(mbarara, "./pdfs/mbarara_pdfs")
process_city_documents(queen_elizabeth_national_park, "./pdfs/queen_elizabeth_national_park_pdfs")
process_city_documents(gulu, "./pdfs/gulu_pdfs")
process_city_documents(kidepo_valley_national_park, "./pdfs/kidepo_valley_national_park_pdfs")
process_city_documents(kibale_national_park, "./pdfs/kibale_national_park_pdfs")
process_city_documents(rwenzori_mountains, "./pdfs/rwenzori_mountains_pdfs")
process_city_documents(lake_bunyonyi, "./pdfs/lake_bunyonyi_pdfs")
process_city_documents(sipi_falls, "./pdfs/sipi_falls_pdfs")
process_city_documents(lake_mburo_national_park, "./pdfs/lake_mburo_national_park_pdfs")
process_city_documents(kabale, "./pdfs/kabale_pdfs")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

@app.post("/Kampala_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_kampala, llm)
    return answer

@app.post("/Entebbe_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_entebbe, llm)
    return answer

@app.post("/Jinja_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_jinja, llm)
    return answer

@app.post("/Murchison Falls National Park_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_murchison_falls_national_park, llm)
    return answer

@app.post("/Bwindi Forest_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_bwindi_forest, llm)
    return answer

@app.post("/Mbarara_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_mbarara, llm)
    return answer

@app.post("/Queen Elizabeth National Park_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_queen_elizabeth_national_park, llm)
    return answer

@app.post("/Gulu_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_gulu, llm)
    return answer

@app.post("/Kidepo Valley National Park_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_kidepo_valley_national_park, llm)
    return answer

@app.post("/Kibale National Park_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_kibale_national_park, llm)
    return answer

@app.post("/Rwenzori Mountains_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_rwenzori_mountains, llm)
    return answer

@app.post("/Lake Bunyonyi_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_lake_bunyonyi, llm)
    return answer

@app.post("/Sipi Falls_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_sipi_falls, llm)
    return answer

@app.post("/Lake Mburo National Park_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_lake_mburo_national_park, llm)
    return answer

@app.post("/Kabale_query")
def query_prompt(request: PromptRequest):
    answer = rag_simple(request.prompt, rag_retriever_kabale, llm)
    return answer


def get_pdf_text(path):
    doc = fitz.open(path)
    full_text = ""
    
    for page in doc:
        full_text += page.get_text()
        
    doc.close()
    return full_text

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

    doc.close()
    return {"status": "verified", "text_preview": text[:100]} # return a snippet

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#kill -9 $(lsof -ti:8000)