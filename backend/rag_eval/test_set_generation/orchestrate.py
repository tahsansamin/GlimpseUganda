from load import load_vector_db
from load import get_pinecone_index
from generate import generate_test_set
import os
from dotenv import load_dotenv

load_dotenv()

def gen_test_to_csv():
    docs = load_vector_db(namespace="kampala")
    test_set = generate_test_set(docs, testset_size=20)
    test_set.to_csv("testset.csv", index=False)
    


if __name__ == "__main__":
    gen_test_to_csv()

    


