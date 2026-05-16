import pytest
from unittest.mock import patch

def test_kampala_query(client):
   
    with patch("app_main.run_query", return_value="Kampala is Uganda's capital."):
        res = client.post("/Kampala_query", json={"prompt": "Tell me about Kampala"})
    assert res.status_code == 200
   
    assert "Kampala" in res.json()

def test_query_missing_prompt(client):
    res = client.post("/Kampala_query", json={})
    assert res.status_code == 422  

@pytest.mark.parametrize("endpoint,namespace", [
    ("/Entebbe_query", "entebbe"),
    ("/Jinja_query", "jinja"),
    ("/Gulu_query", "gulu"),
    ("/Kabale_query", "kabale"),
    ("/Mbarara_query", "mbarara"),
    ("/Sipi Falls_query", "sipi_falls"),
    ("/Lake Bunyonyi_query", "lake_bunyonyi"),
    ("/Rwenzori Mountains_query", "rwenzori_mountains"),
    ("/Kibale National Park_query", "kibale_national_park"),
    ("/Kidepo Valley National Park_query", "kidepo_valley_national_park"),
    ("/Queen Elizabeth National Park_query", "queen_elizabeth_national_park"),
    ("/Murchison Falls National Park_query", "murchison_falls_national_park"),
    ("/Lake Mburo National Park_query", "lake_mburo_national_park"),
    ("/Bwindi Forest_query", "bwindi_forest"),
])
def test_all_city_routes_call_correct_namespace(client, endpoint, namespace):
    with patch("app_main.run_query", return_value="Some answer") as mock_rq:
        res = client.post(endpoint, json={"prompt": "What can I do here?"})
    assert res.status_code == 200
    mock_rq.assert_called_once_with(namespace, "What can I do here?")

#test commit 


