import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/file_converter"


def test_get_brep_info(client):
    response = client.get(f'{base_route}/get_brep_info')
    assert response.status_code == 200
    

def test_remesh(client):
    response = client.post(f'{base_route}/remesh', data={'filename': 'toto.tutu'})
    assert response.status_code == 200