import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/workflows/explicit"


def test_get_base_data(client):
    response = client.post(f'{base_route}/get_base_data')
    assert response.status_code == 200
    viewable_1 = response.json['viewable_1']
    id1 = response.json['id1']
    viewable_2 = response.json['viewable_2']
    id2 = response.json['id2']
    viewable_3 = response.json['viewable_3']
    id3 = response.json['id3']
    assert type(viewable_1) is str
    assert type(id1) is str
    assert type(viewable_2) is str
    assert type(id2) is str
    assert type(viewable_3) is str
    assert type(id3) is str


def test_get_brep_stats(client):
    response = client.post(f'{base_route}/get_brep_stats')
    assert response.status_code == 200
    nb_corners = response.json['nb_corners']
    nb_lines = response.json['nb_lines']
    nb_surfaces = response.json['nb_surfaces']
    nb_blocks = response.json['nb_blocks']
    viewable_file_name = response.json['viewable_file_name']
    id = response.json['id']
    assert type(viewable_file_name) is str
    assert type(id) is str
    assert type(nb_corners) is int
    assert type(nb_lines) is int
    assert type(nb_surfaces) is int
    assert type(nb_blocks) is int