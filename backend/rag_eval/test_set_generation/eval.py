from IPython.core import display_functions
from IPython.core import display_functions
from sentence_transformers.sparse_encoder.losses import SparseMultipleNegativesRankingLoss
import pandas as pd
import requests
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from ragas.run_config import RunConfig

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

df = pd.read_csv("testset.csv")
user_queries = df["user_input"]
expected_responses = df["reference"]

dataset = []

for query,reference in zip(user_queries,expected_responses):

    response = requests.post("http://localhost:8000/evaluation_query", json={"prompt": query, "history": []})
    response_json = response.json()

    relevant_docs = [doc["page_content"] for doc in response_json["source_chunks"]]
    response = response_json["answer"]
    dataset.append(
        {
            "user_input":query,
            "retrieved_contexts":relevant_docs,
            "response":response,
            "reference":reference
        }
    )
   
import time
for query,reference in zip(user_queries,expected_responses):
    print(f'Processing query: {query}')
    time.sleep(5)  # Pause to avoid rate limits

    response = requests.post("http://localhost:8000/evaluation_query", json={"prompt": query, "history": []})
    response_json = response.json()

    relevant_docs = [doc["page_content"] for doc in response_json["source_chunks"]]
    response = response_json["answer"]
    dataset.append(
        {
            "user_input":query,
            "retrieved_contexts":relevant_docs,
            "response":response,
            "reference":reference
        }
    )

evaluation_dataset = EvaluationDataset.from_list(dataset)


evaluator_llm = LangchainLLMWrapper(ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_EVAL_KEY"),
    temperature=0
))


result = evaluate(dataset=evaluation_dataset,metrics=[LLMContextRecall(), Faithfulness()],llm=evaluator_llm,run_config=RunConfig(
        max_workers=1,   # 👈 one request at a time
        timeout=180,
        max_retries=10
    ))
print(result)

