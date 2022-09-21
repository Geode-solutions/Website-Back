import os

ID = os.environ.get('ID')

def test_root(client):
    response = client.get(f'/{ID}/healthcheck')
    assert response.status_code == 200

def test_createbackend(client):
    response = client.post('/tools/createbackend')
    assert response.status_code == 200
    ID = response.json['ID']
    assert ID == '123456'

def test_ping(client):
    response = client.post(f'/{ID}/ping')
    assert response.status_code == 200
