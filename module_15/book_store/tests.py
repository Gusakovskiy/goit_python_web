def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_author(client):
    response = client.get("/authors")
    assert response.status_code == 200
    assert not response.json()