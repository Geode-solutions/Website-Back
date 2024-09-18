import os


def test_root(client):
    response = client.get(f"/healthcheck")
    assert response.status_code == 200


def test_createbackend(client):
    response = client.post("/createbackend")
    assert response.status_code == 200
    ID = response.json["ID"]
    assert ID == "123456"
