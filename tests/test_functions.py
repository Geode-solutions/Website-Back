import os


def test_root(client):
    response = client.get(f"/healthcheck")
    assert response.status_code == 200


def test_createbackend(client):
    response = client.post("/tools/createbackend")
    assert response.status_code == 200
    ID = response.json["ID"]
    assert ID == "123456"


def test_ping(client):
    response = client.post(f"/ping")
    assert response.status_code == 200
