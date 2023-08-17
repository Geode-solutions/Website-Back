import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/workflows/explicit_modeling"


def test_get_brep_stats(client):
    response = client.post(f'{base_route}/get_brep_stats')
    assert response.status_code == 200
    nb_corners = response.json['nb_corners']
    nb_lines = response.json['nb_lines']
    nb_surfaces = response.json['nb_surfaces']
    nb_blocks = response.json['nb_blocks']
    assert type(nb_corners) is int
    assert type(nb_lines) is int
    assert type(nb_surfaces) is int
    assert type(nb_blocks) is int