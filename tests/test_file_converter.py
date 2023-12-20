import os
import base64
from werkzeug.datastructures import FileStorage

base_route = "/tools/file_converter"


def test_versions(client):
    response = client.get(f"{base_route}/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict


def test_convert_file(client):
    route = f"{base_route}/convert_file"

    filename = "corbi.og_brep"
    response = client.put(
        "tools/upload_file",
        data={"file": FileStorage(open(f"./tests/{filename}", "rb"))},
    )
    assert response.status_code == 201

    def get_full_data():
        return {
            "input_geode_object": "BRep",
            "filename": "corbi.og_brep",
            "output_geode_object": "BRep",
            "output_extension": "msh",
        }

    response = client.post(route, json=get_full_data())

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    for key, value in get_full_data().items():
        json = get_full_data()
        json.pop(key)
        response = client.post(route, json=json)
        assert response.status_code == 400
        error_description = response.json["description"]
        assert error_description == f"Validation error: '{key}' is a required property"
