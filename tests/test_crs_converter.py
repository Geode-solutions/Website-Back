import os
import base64

base_route = "/tools/crs_converter"


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
    route = f"{base_route}/allowed_objects"

    # Normal test with filename 'corbi.og_brep'
    response = client.post(route, data={"filename": "corbi.og_brep"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert "BRep" in allowed_objects

    # Normal test with filename .vtu
    response = client.post(route, data={"filename": "toto.vtu"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    list_objects = ["HybridSolid3D", "PolyhedralSolid3D", "TetrahedralSolid3D"]
    for geode_object in list_objects:
        assert geode_object in allowed_objects

    # Test with stupid filename
    response = client.post(route, data={"filename": "toto.tutu"})
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No filename sent"


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


def test_geographic_coordinate_systems(client):
    route = f"{base_route}/geographic_coordinate_systems"

    # Normal test with geode_object 'BRep'
    response = client.post(route, data={"geode_object": "BRep"})
    assert response.status_code == 200
    crs_list = response.json["crs_list"]
    assert type(crs_list) is list
    for crs in crs_list:
        assert type(crs) is dict

    # Test without geode_object
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No geode_object sent"


def test_output_file_extensions(client):
    route = f"{base_route}/output_file_extensions"

    # Normal test with geode_object
    response = client.post(route, data={"geode_object": "BRep"})
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["msh", "og_brep"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with geode_object
    response = client.post(route, data={"geode_object": "TriangulatedSurface3D"})
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["obj", "og_tsf3d", "stl", "vtp"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with geode_object
    response = client.post(route, data={"geode_object": "StructuralModel"})
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["lso", "ml", "msh", "og_brep", "og_strm"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Test without object
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No geode_object sent"


def test_convert_file(client):
    # Normal test with object/file/filename/extension

    route = f"{base_route}/convert_file"
    geode_object = "BRep"
    filename = "corbi.og_brep"
    input_crs_authority = "EPSG"
    input_crs_code = "2000"
    input_crs_name = "Anguilla 1957 / British West Indies Grid"
    output_crs_authority = "EPSG"
    output_crs_code = "2001"
    output_crs_name = "Antigua 1943 / British West Indies Grid"
    extension = "msh"

    file = base64.b64encode(open(f"./tests/{filename}", "rb").read())
    filesize = int(os.path.getsize(f"./tests/{filename}"))

    response = client.post(
        route,
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    # Test without geode_object
    response = client.post(
        route,
        data={
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No geode_object sent"

    # Test without filename
    response = client.post(
        route,
        data={
            "geode_object": geode_object,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"

    # Test without input_crs_authority
    response = client.post(
        route,
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No input_crs_authority sent"

    # Test without input_crs_code
    response = client.post(
        route,
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No input_crs_code sent"

    # Test without input_crs_name
    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No input_crs_name sent"

    # Test without output_crs_authority
    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No output_crs_authority sent"

    # Test without output_crs_code
    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_name": output_crs_name,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No output_crs_code sent"

    # Test without output_crs_name
    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "extension": extension,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No output_crs_name sent"

    # Test without extension
    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "input_crs_authority": input_crs_authority,
            "input_crs_code": input_crs_code,
            "input_crs_name": input_crs_name,
            "output_crs_authority": output_crs_authority,
            "output_crs_code": output_crs_code,
            "output_crs_name": output_crs_name,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No extension sent"
