import dataloader
import embedding
from embedding import EmbeddingManager
from dataloader import process_all_pdfs
import vectorstore
from vectorstore import VectorStore
import retriever
from retriever import RAGretriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
vectorstore = VectorStore() 
def split_documents(documents, chunk_size = 1000, chunk_overlap = 200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size,
                                                   chunk_overlap = chunk_overlap,
                                                   length_function = len,
                                                   separators = ["\n\n", "\n", " ", ""])
    split_docs = text_splitter.split_documents(documents)
    print(f"split {len(documents)} documents into {len(split_docs)} chunks")
    
    return split_docs
embedding_manager = EmbeddingManager()
rag_retriever = RAGretriever(vector_store=vectorstore,
                                embedding_manager=embedding_manager)


all_pdf_documents = process_all_pdfs(".")
split_documents = embedding_manager.chunk_documents(all_pdf_documents)
texts = [doc.page_content for doc in split_documents]

embeddings = embedding_manager.generate_embeddings([doc.page_content for doc in split_documents])
vectorstore.add_documents(split_documents, embeddings)
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

answer = rag_simple("What is the Namugongo Martyrs Shrine?", rag_retriever,llm)
print(answer)
