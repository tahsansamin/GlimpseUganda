import pytest
from unittest.mock import patch

def test_kampala_query(client):
   
    with patch("app_main.run_query", return_value="Kampala is Uganda's capital.") as mock_rq:
        res = client.post("/Kampala_query", json={"prompt": "Tell me about Kampala"})
    assert res.status_code == 200
    mock_rq.assert_called_once_with("kampala", "Kampala", "Tell me about Kampala", [])
    assert "Kampala" in res.json()

def test_query_missing_prompt(client):
    res = client.post("/Kampala_query", json={})
    assert res.status_code == 422  

@pytest.mark.parametrize("endpoint,namespace,city_name", [
    ("/Entebbe_query", "entebbe", "Entebbe"),
    ("/Jinja_query", "jinja", "Jinja"),
    ("/Gulu_query", "gulu", "Gulu"),
    ("/Kabale_query", "kabale", "Kabale"),
    ("/Mbarara_query", "mbarara", "Mbarara"),
    ("/Sipi Falls_query", "sipi_falls", "Sipi Falls"),
    ("/Lake Bunyonyi_query", "lake_bunyonyi", "Lake Bunyonyi"),
    ("/Rwenzori Mountains_query", "rwenzori_mountains", "Rwenzori Mountains"),
    ("/Kibale National Park_query", "kibale_national_park", "Kibale National Park"),
    ("/Kidepo Valley National Park_query", "kidepo_valley_national_park", "Kidepo Valley National Park"),
    ("/Queen Elizabeth National Park_query", "queen_elizabeth_national_park", "Queen Elizabeth National Park"),
    ("/Murchison Falls National Park_query", "murchison_falls_national_park", "Murchison Falls National Park"),
    ("/Lake Mburo National Park_query", "lake_mburo_national_park", "Lake Mburo National Park"),
    ("/Bwindi Forest_query", "bwindi_forest", "Bwindi Forest"),
])
def test_all_city_routes_call_correct_namespace(client, endpoint, namespace, city_name):
    with patch("app_main.run_query", return_value="Some answer") as mock_rq:
        res = client.post(endpoint, json={"prompt": "What can I do here?"})
    assert res.status_code == 200
    mock_rq.assert_called_once_with(namespace, city_name, "What can I do here?", [])

#test commit 


