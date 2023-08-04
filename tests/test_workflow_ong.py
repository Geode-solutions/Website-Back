import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/ong"


def test_get_constraints(client):
    response = client.get(f'{base_route}/get_constraints')
    assert response.status_code == 200
    

def test_step1(client):
    response = client.post(f'{base_route}/step1', data={'filename': 'toto.tutu'})
    assert response.status_code == 200


def test_step2(client):
    response = client.post(f'{base_route}/step2', data={'filename': 'toto.tutu'})
    assert response.status_code == 200


def test_step3(client):
    response = client.post(f'{base_route}/step3', data={'filename': 'toto.tutu'})
    assert response.status_code == 200