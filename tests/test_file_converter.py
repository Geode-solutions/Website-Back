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


def test_upload_file(client):
    file = base64.b64encode(open("./tests/corbi.og_brep", "rb").read())
    filename = "corbi.og_brep"
    filesize = os.path.getsize("./tests/corbi.og_brep")

    # Test with file
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": file,
            "filename": filename,
            "filesize": filesize,
        },
    )

    assert response.status_code == 200

    # Test without file
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "filename": filename,
            "filesize": filesize,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No file sent"

    # Test without filename
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": file,
            "filesize": filesize,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"

    # Test without filesize
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": file,
            "filename": filename,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filesize sent"


def test_allowed_objects(client):
    # Normal test with filename 'corbi.og_brep'
    response = client.post(
        f"{base_route}/allowed_objects", data={"filename": "corbi.og_brep"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert "BRep" in allowed_objects

    # Normal test with filename .vtu
    response = client.post(
        f"{base_route}/allowed_objects", data={"filename": "toto.vtu"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    list_objects = ["HybridSolid3D", "PolyhedralSolid3D", "TetrahedralSolid3D"]
    for geode_object in allowed_objects:
        assert geode_object in allowed_objects

    # Test with stupid filename
    response = client.post(
        f"{base_route}/allowed_objects", data={"filename": "toto.tutu"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(f"{base_route}/allowed_objects")
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No filename sent"


def test_missing_files(client):
    geode_object = "BRep"
    filename = "corbi.og_brep"

    data = {"geode_object": geode_object, "filename": filename}
    response = client.post(
        f"{base_route}/missing_files",
        data=data,
    )


def test_output_file_extensions(client):
    route = f"{base_route}/output_file_extensions"

    def get_full_data():
        return {"input_geode_object": "BRep"}

    response = client.post(route, data=get_full_data())

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
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No input_geode_object sent"


def test_convert_file(client):
    route = f"{base_route}/convert_file"

    def get_full_data():
        return {
            "input_geode_object": "BRep",
            "filename": "corbi.og_brep",
            "output_geode_object": "BRep",
            "output_extension": "msh",
        }

    response = client.post(route, data=get_full_data())

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    for key, value in get_full_data().items():
        data = get_full_data()
        data.pop(key)
        response = client.post(route, data=data)
        assert response.status_code == 400
        error_description = response.json["description"]
        assert error_description == f"No {key} sent"

    # # Normal test with object/file/filename/extension
    # geode_object = "BRep"
    # filename = "corbi.og_brep"
    # file = base64.b64encode(open("./tests/corbi.og_brep", "rb").read())
    # filesize = int(os.path.getsize("./tests/corbi.og_brep"))
    # extension = "msh"

    # response = client.post(
    #     f"{base_route}/convert_file",
    #     data={
    #         "geode_object": geode_object,
    #         "filename": filename,
    #         "extension": extension,
    #     },
    # )

    # assert response.status_code == 200
    # assert type((response.data)) is bytes
    # assert len((response.data)) > 0

    # # Test without object
    # response = client.post(
    #     f"{base_route}/convert_file",
    #     data={
    #         "filename": filename,
    #         "extension": extension,
    #     },
    # )

    # assert response.status_code == 400
    # error_description = response.json["description"]
    # assert error_description == "No geode_object sent"

    # # Test without filename
    # response = client.post(
    #     f"{base_route}/convert_file",
    #     data={
    #         "geode_object": geode_object,
    #         "extension": extension,
    #     },
    # )

    # assert response.status_code == 400
    # error_description = response.json["description"]
    # assert error_description == "No filename sent"

    # # Test without extension
    # response = client.post(
    #     f"{base_route}/convert_file",
    #     data={
    #         "geode_object": geode_object,
    #         "filename": filename,
    #     },
    # )

    # assert response.status_code == 400
    # error_description = response.json["description"]
    # assert error_description == "No extension sent"
