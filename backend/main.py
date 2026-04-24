import uvicorn
import os
from fastapi import FastAPI
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
dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set. Please set it before running.")
llm = ChatGroq(groq_api_key = API_KEY, model_name = "llama-3.1-8b-instant", temperature=0.1, max_tokens= 1024)
class PromptRequest(BaseModel):
    prompt: str

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

Kampala = VectorStore(persist_directory="kampala")
Entebbe = VectorStore(persist_directory="entebbe")
Jinja = VectorStore(persist_directory="jinja")
embedding_manager = EmbeddingManager()
rag_retriever_kampala = RAGretriever(vector_store=Kampala,
                                    embedding_manager=embedding_manager)
rag_retriever_entebbe = RAGretriever(vector_store=Entebbe,
                                    embedding_manager=embedding_manager)
rag_retriever_jinja = RAGretriever(vector_store=Jinja,
                                    embedding_manager=embedding_manager)

#adding word documents for each city
def process_city_documents(city_obj, folder_path):
    word_documents = dataloader.process_all_word_docs(folder_path)
    word_split_documents = embedding_manager.chunk_documents(word_documents)
    word_embeddings = embedding_manager.generate_embeddings([doc.page_content for doc in word_split_documents])
    city_obj.add_documents(word_split_documents, word_embeddings)

process_city_documents(Kampala, "./pdfs/kampala_pdfs")
process_city_documents(Entebbe, "./pdfs/entebbe_pdfs")
process_city_documents(Jinja, "./pdfs/jinja_pdfs")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:5174",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)