from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-V2"):
        self.model_name = model_name
        self.model  = None
        self._load_model()
    def _load_model(self):
        try:
            print(f"Loading {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded. Embedding dimensons {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Encountered error {e}")
            raise
    def chunk_documents(self,documents, chunk_size = 1000, chunk_overlap = 200):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size,
                                                   chunk_overlap = chunk_overlap,
                                                   length_function = len,
                                                   separators = ["\n\n", "\n", " ", ""])
        split_docs = text_splitter.split_documents(documents)
        print(f"split {len(documents)} documents into {len(split_docs)} chunks")
    
        return split_docs

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model not loaded")
        print(f"generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts)
        print(f"generated embeddings with shape {embeddings.shape}")
        return embeddings