import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import dataloader, embedding, vectorstore, retriever
from embedding import EmbeddingManager
from dataloader import process_all_pdfs
from vectorstore import VectorStore
from retriever import RAGretriever
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
API_KEY = "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"
llm = ChatGroq(groq_api_key = API_KEY, model_name = "llama-3.1-8b-instant", temperature=0.1, max_tokens= 1024)

def rag_simple(query, retriever, llm, top_k = 3):
    results =retriever.retrieve(query, top_k = top_k)
    context = "\n\n".join([doc['content'] for doc in results]) if results else ""
    if not context:
        return "no relevant context found"
    prompt = f""" Use the following context to answer the question concisely.
    Context: {context},
    question: {query}   
    answer: """
    response = llm.invoke([prompt.format(context = context, query = query)])
    return response.content

vectorstore = VectorStore()
embedding_manager = EmbeddingManager()
rag_retriever = RAGretriever(vector_store=vectorstore,
                                    embedding_manager=embedding_manager)


all_pdf_documents = process_all_pdfs(".")
split_documents = embedding_manager.chunk_documents(all_pdf_documents)
texts = [doc.page_content for doc in split_documents]

embeddings = embedding_manager.generate_embeddings([doc.page_content for doc in split_documents])
vectorstore.add_documents(split_documents, embeddings)


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/prompts")
def query_prompt(prompt: str):
    
    answer = rag_simple("What is the Namugongo Martyrs Shrine?", rag_retriever,llm)
    return answer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)