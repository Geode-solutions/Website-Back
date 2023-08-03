import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/file_converter"


def test_get_brep_stats(client):
    response = client.get(f'{base_route}/get_brep_stats')
    assert response.status_code == 200