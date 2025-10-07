from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_get_sentiment():
    response = client.get("/sentiment?kw1=obama&kw2=romney")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    names = {item["name"].lower() for item in data}
    assert names.issubset({"obama", "romney"})
    assert all("date" in item and "score" in item for item in data)
