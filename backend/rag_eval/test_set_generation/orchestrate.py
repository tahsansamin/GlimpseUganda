from load import load_vector_db
from load import get_pinecone_index
from generate import generate_test_set
import os
from dotenv import load_dotenv

load_dotenv()
docs = load_vector_db(namespace="kampala")
test_set = generate_test_set(docs, testset_size=10)
print(test_set)

