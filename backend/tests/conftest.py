import pytest
import os
from unittest.mock import MagicMock, patch

# Set fake env vars before anything imports main.py
os.environ.setdefault("GROQ_API_KEY", "fake-groq-key")
os.environ.setdefault("PINECONE_KEY", "fake-pinecone-key")
os.environ.setdefault("COHERE_API_KEY", "fake-cohere-key")
os.environ.setdefault("VITE_SUPABASE_URL", "https://fake.supabase.co")
os.environ.setdefault("VITE_SUPABASE_KEY", "fake-supabase-key")
os.environ.setdefault("WEBHOOK_SECRET", "fake-webhook-secret")

@pytest.fixture(scope="session")
def client():
    with patch("pinecone.Pinecone") as mock_pc, \
         patch("langchain_pinecone.PineconeVectorStore") as mock_vs, \
         patch("langchain_groq.ChatGroq") as mock_llm, \
         patch("cohere.Client") as mock_cohere, \
         patch("supabase.create_client") as mock_supabase, \
         patch("langchain_classic.chains.RetrievalQA.from_chain_type"):

        mock_pc.return_value.Index.return_value = MagicMock()
        mock_vs.return_value.as_retriever.return_value = MagicMock()
        mock_llm.return_value.invoke.return_value = MagicMock(content="Mocked answer")
        mock_cohere.return_value.rerank.return_value = MagicMock(results=[])
        mock_supabase.return_value = MagicMock()

        from fastapi.testclient import TestClient
        from app_main import app
        yield TestClient(app)