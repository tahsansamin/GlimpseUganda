import fitz
from unittest.mock import patch, MagicMock

def make_pdf_bytes():
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This document is about Kampala tourism in Uganda.")
    return doc.tobytes()

def test_verify_document_relevant(client):
    mock_response = MagicMock()
    mock_response.content = '{"category_focus_percentage": 85, "is_directly_related": true, "reasoning": "Mostly about Kampala."}'

    with patch("app_main.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        res = client.post(
            "/verify_document",
            files={"document": ("test.pdf", make_pdf_bytes(), "application/pdf")},
            data={"filename": "test.pdf", "category": "Kampala"}
        )

    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "verified"
    assert body["summary"]["is_directly_related"] is True
    assert body["summary"]["category_focus_percentage"] == 85

def test_verify_document_not_relevant(client):
    mock_response = MagicMock()
    mock_response.content = '{"category_focus_percentage": 15, "is_directly_related": false, "reasoning": "Mostly general Uganda content."}'

    with patch("app_main.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        res = client.post(  
            "/verify_document",
            files={"document": ("test.pdf", make_pdf_bytes(), "application/pdf")},
            data={"filename": "test.pdf", "category": "Kampala"}
        )

    assert res.status_code == 200
    assert res.json()["summary"]["is_directly_related"] is False