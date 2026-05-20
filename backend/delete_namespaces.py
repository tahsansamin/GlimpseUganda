import os
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone

# Load environment variables
dotenvpath = find_dotenv()
print(f"Loading environment variables from: {dotenvpath}")
load_dotenv(dotenv_path=dotenvpath)

PINECONE_KEY = os.getenv("PINECONE_KEY")
if not PINECONE_KEY:
    raise RuntimeError("PINECONE_KEY environment variable not set. Please set it in your .env file.")

# Initialize Pinecone and connect to the index
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index("tourismindex")

# List of all namespaces in the project
NAMESPACES = [
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

def delete_all_namespaces():
    print(f"Starting deletion of all {len(NAMESPACES)} namespaces...\n")
    for namespace in NAMESPACES:
        print(f"Deleting all vectors in namespace: '{namespace}'...")
        try:
            index.delete(delete_all=True, namespace=namespace)
            print(f"  -> Successfully deleted namespace: '{namespace}'\n")
        except Exception as e:
            print(f"  -> Error deleting namespace '{namespace}': {e}\n")

if __name__ == "__main__":
    # To execute the deletions, run this file directly or call delete_all_namespaces()
    delete_all_namespaces()
    print("Script loaded. Uncomment 'delete_all_namespaces()' in the main block to execute.")
