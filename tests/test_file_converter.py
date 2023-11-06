import os
import base64

base_route = "/tools/file_converter"


def test_versions(client):
    response = client.get(f"{base_route}/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict


def test_allowed_files(client):
    response = client.get(f"{base_route}/allowed_files")
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list
    for extension in extensions:
        assert type(extension) is str


def test_allowed_objects(client):
    # Normal test with filename 'corbi.og_brep'
    response = client.post(
        f"{base_route}/allowed_objects", json={"filename": "corbi.og_brep"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert "BRep" in allowed_objects

    # Normal test with filename .vtu
    response = client.post(
        f"{base_route}/allowed_objects", json={"filename": "toto.vtu"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    list_objects = ["HybridSolid3D", "PolyhedralSolid3D", "TetrahedralSolid3D"]
    for geode_object in allowed_objects:
        assert geode_object in allowed_objects

    # Test with stupid filename
    response = client.post(
        f"{base_route}/allowed_objects", json={"filename": "toto.tutu"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(f"{base_route}/allowed_objects", json={})
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No filename sent"


def test_output_file_extensions(client):
    # Normal test with object
    response = client.post(
        f"{base_route}/output_file_extensions", json={"geode_object": "BRep"}
    )
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    for output_file_extension in output_file_extensions:
        assert type(output_file_extension) is str

    # Test without object
    response = client.post(f"{base_route}/output_file_extensions", json={})
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No geode_object sent"


def test_convert_file(client):
    # Normal test with object/file/filename/extension
    geode_object = "BRep"
    filename = "corbi.og_brep"
    file = str(base64.b64encode(open("./tests/corbi.og_brep", "rb").read()))
    filesize = int(os.path.getsize("./tests/corbi.og_brep"))
    extension = "msh"

    response = client.put(
        "tools/upload_file",
        data={"content": (open(f"./tests/{filename}", "rb"), filename)},
    )
    assert response.status_code == 201

    response = client.post(
        f"{base_route}/convert_file",
        json={
            "geode_object": geode_object,
            "filename": filename,
            "extension": extension,
        },
    )

    assert response.status_code == 200
    # assert type((response.data)) is bytes
    # assert len((response.data)) > 0

    # Test without object
    response = client.post(
        f"{base_route}/convert_file",
        json={
            "filename": filename,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No geode_object sent"

    # Test without filename
    response = client.post(
        f"{base_route}/convert_file",
        json={
            "geode_object": geode_object,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"

    # Test without extension
    response = client.post(
        f"{base_route}/convert_file",
        json={
            "geode_object": geode_object,
            "filename": filename,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No extension sent"
