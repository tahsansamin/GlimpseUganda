from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.embeddings import OpenAIEmbeddings
# pyrefly: ignore [missing-import]
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import SentenceTransformerEmbeddings
from ragas.testset import TestsetGenerator
from dotenv import load_dotenv, find_dotenv
import os
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_community.embeddings import HuggingFaceEmbeddings
load_dotenv()



def generate_test_set(docs, testset_size=10):
    """
    Generates a RAG test set using Ragas and Groq.
    
    Parameters:
    - docs: A list of LangChain documents.
    - testset_size (int): The number of test cases to generate (default is 10).
    
    Returns:
    - pd.DataFrame: The generated test set as a pandas DataFrame.
    """
    generator_llm = LangchainLLMWrapper(
        ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0
        ))
    hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


    embedding_model = LangchainEmbeddingsWrapper(hf_embeddings)

    generator = TestsetGenerator(llm=generator_llm, embedding_model=embedding_model)
    dataset = generator.generate_with_langchain_docs(docs, testset_size=testset_size)
    return dataset.to_pandas()

