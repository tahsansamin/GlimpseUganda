from unittest.mock import patch, MagicMock

def make_mock_doc(content):
    doc = MagicMock()
    doc.page_content = content
    return doc

def test_run_query_returns_llm_answer():
    mock_docs = [make_mock_doc("Kampala is the capital city of Uganda.")]

    with patch("app_main.PineconeVectorStore") as mock_vs, \
         patch("app_main.cohere_rerank_documents", return_value=mock_docs), \
         patch("app_main.llm") as mock_llm:

        mock_vs.return_value.as_retriever.return_value.invoke.return_value = mock_docs
        mock_llm.invoke.return_value = MagicMock(content="Kampala is a vibrant city.")

        from app_main import run_query
        result = run_query("kampala", "Kampala", "What is Kampala like?", [])

    assert result == "Kampala is a vibrant city."

def test_run_query_no_reranked_docs_calls_llm():
    mock_docs = [make_mock_doc("Some content")]

    with patch("app_main.PineconeVectorStore") as mock_vs, \
         patch("app_main.cohere_rerank_documents", return_value=[]), \
         patch("app_main.llm") as mock_llm:

        mock_vs.return_value.as_retriever.return_value.invoke.return_value = mock_docs
        mock_llm.invoke.return_value = MagicMock(content="Internal knowledge answer.")

        from app_main import run_query
        result = run_query("kampala", "Kampala", "What is Kampala like?", [])

    assert result == "Internal knowledge answer."
    mock_llm.invoke.assert_called_once()

def test_run_query_context_passed_to_llm():
    mock_docs = [
        make_mock_doc("Kampala has Owino market."),
        make_mock_doc("Kampala has Boda bodas."),
    ]

    with patch("app_main.PineconeVectorStore") as mock_vs, \
         patch("app_main.cohere_rerank_documents", return_value=mock_docs), \
         patch("app_main.llm") as mock_llm:

        mock_vs.return_value.as_retriever.return_value.invoke.return_value = mock_docs
        mock_llm.invoke.return_value = MagicMock(content="Answer based on context.")

        from app_main import run_query
        run_query("kampala", "Kampala", "What markets does Kampala have?", [])

        # Check that the system message contained both doc contents
        call_args = mock_llm.invoke.call_args[0][0]
        system_message_content = call_args[0].content
        assert "Owino market" in system_message_content
        assert "Boda bodas" in system_message_content