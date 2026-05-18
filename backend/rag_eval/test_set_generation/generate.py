from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.embeddings import OpenAIEmbeddings
# pyrefly: ignore [missing-import]
# pyrefly: ignore [missing-import]
from groq import Groq
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import SentenceTransformerEmbeddings
from ragas.testset import TestsetGenerator



def generate_test_set(docs, testset_size=10):
    """
    Generates a RAG test set using Ragas and Groq.
    
    Parameters:
    - docs: A list of LangChain documents.
    - testset_size (int): The number of test cases to generate (default is 10).
    
    Returns:
    - pd.DataFrame: The generated test set as a pandas DataFrame.
    """
    generator_llm = LangchainLLMWrapper(Groq("llama-3.1-8b-instant"))
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")

    generator = TestsetGenerator(llm=generator_llm, embedding_model=embedding_model)
    dataset = generator.generate_with_langchain_docs(docs, testset_size=testset_size)
    return dataset.to_pandas()

