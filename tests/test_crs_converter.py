import os
import base64
from werkzeug.datastructures import FileStorage

base_route = "/tools/crs_converter"


def test_versions(client):
    response = client.get(f"{base_route}/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict


def test_geographic_coordinate_systems(client):
    route = f"{base_route}/geographic_coordinate_systems"

    # Normal test with geode_object 'BRep'
    response = client.post(route, json={"input_geode_object": "BRep"})
    assert response.status_code == 200
    crs_list = response.json["crs_list"]
    assert type(crs_list) is list
    for crs in crs_list:
        assert type(crs) is dict

    # Test without geode_object
    response = client.post(route, json={})
    assert response.status_code == 400
    error_message = response.json["description"]
    assert (
        error_message == "Validation error: 'input_geode_object' is a required property"
    )


def test_convert_file(client):
    route = f"{base_route}/convert_file"

    filename = "corbi.og_brep"
    response = client.put(
        "tools/upload_file",
        data={"content": FileStorage(open(f"./tests/{filename}", "rb"))},
    )
    assert response.status_code == 201

    def get_full_data():
        return {
            "input_geode_object": "BRep",
            "filename": "corbi.og_brep",
            "input_crs": {
                "authority": "EPSG",
                "code": "2000",
                "name": "Anguilla 1957 / British West Indies Grid",
            },
            "output_crs": {
                "authority": "EPSG",
                "code": "2001",
                "name": "Antigua 1943 / British West Indies Grid",
            },
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
