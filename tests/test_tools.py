import os
import base64
from werkzeug.datastructures import FileStorage

base_route = "/tools"


def test_allowed_files(client):
    route = f"{base_route}/allowed_files"
    response = client.post(route, json={"key": None})
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list
    for extension in extensions:
        assert type(extension) is str


def test_allowed_objects(client):
    route = f"{base_route}/allowed_objects"

    def get_full_data():
        return {
            "filename": "corbi.og_brep",
            "key": None,
        }

    # Normal test with filename 'corbi.og_brep'
    response = client.post(route, json=get_full_data())
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    for allowed_object in allowed_objects:
        assert type(allowed_object) is str

    for key, value in get_full_data().items():
        json = get_full_data()
        json.pop(key)
        response = client.post(route, json=json)
        assert response.status_code == 400
        error_description = response.json["description"]
        assert error_description == f"No {key} sent"


def test_upload_file(client):
    response = client.put(
        f"{base_route}/upload_file",
        data={"content": FileStorage(open("./tests/corbi.og_brep", "rb"))},
    )

    assert response.status_code == 201


def test_missing_files(client):
    route = f"{base_route}/missing_files"

    def get_full_data():
        return {
            "input_geode_object": "BRep",
            "filename": "corbi.og_brep",
        }

    json = get_full_data()
    response = client.post(
        route,
        json=json,
    )

    assert response.status_code == 200
    has_missing_files = response.json["has_missing_files"]
    mandatory_files = response.json["mandatory_files"]
    additional_files = response.json["additional_files"]
    assert type(has_missing_files) is bool
    assert type(mandatory_files) is list
    assert type(additional_files) is list

    for key, value in get_full_data().items():
        json = get_full_data()
        json.pop(key)
        response = client.post(route, json=json)
        assert response.status_code == 400
        error_description = response.json["description"]
        assert error_description == f"No {key} sent"


def test_geode_objects_and_output_extensions(client):
    route = f"{base_route}/geode_objects_and_output_extensions"

    def get_full_data():
        return {"input_geode_object": "BRep"}

    response = client.post(route, json=get_full_data())

    assert response.status_code == 200
    geode_objects_and_output_extensions = response.json[
        "geode_objects_and_output_extensions"
    ]
    assert type(geode_objects_and_output_extensions) is list
    for geode_object_and_output_extensions in geode_objects_and_output_extensions:
        assert type(geode_object_and_output_extensions) is dict
        assert type(geode_object_and_output_extensions["geode_object"]) is str
        assert type(geode_object_and_output_extensions["output_extensions"]) is list

    # Test without input_geode_object
    response = client.post(route, json={})
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No input_geode_object sent"
