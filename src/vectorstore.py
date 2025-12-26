import chromadb
from typing import List, Dict, Any, Tuple
import uuid
import numpy as np
import os
class VectorStore:
    def __init__(self, collection_name: str = "pdf_documents", presist_directory = "vector_store"):
        self.collection_name = collection_name
        self.persist_directory = presist_directory
        self.client = None
        self.collection = None
        self._initialize_store()
    def _initialize_store(self):
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path = self.persist_directory)
            self.collection = self.client.get_or_create_collection(name = self.collection_name,
                                                                   metadata= {"description": "pdf document embeddings"})
            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Exisiting documents in collection {self.collection.count()}")
        except Exception as e:
            print(f"Error encounterd: {e}")
            raise
    def add_documents(self, documents: List[Any], embeddings: np.array):
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents not equal to number of embeddings")
        print(f"adding {len(documents)} to vector store")

        ids = []
        metadatas = []
        documents_texts = []
        embeddings_list = []
        for i, (doc, embedding) in enumerate(zip(documents,embeddings)):
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)

            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)

            documents_texts.append(doc.page_content)

            embeddings_list.append(embedding.tolist())
        try:
            self.collection.add(
                ids = ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_texts
            )
            print(f"successifuly added {len(documents)} to vector db")
            print(f"total documents in collection are {self.collection.count()}")
        except Exception as e:
            print(f"error in adding doc {e}")
            raise

vectorstore = VectorStore()