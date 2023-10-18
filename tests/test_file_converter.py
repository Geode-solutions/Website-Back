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
    list_extensions = [
        "dat",
        "dev",
        "dxf",
        "lso",
        "ml",
        "msh",
        "obj",
        "og_brep",
        "og_edc2d",
        "og_edc3d",
        "og_grp",
        "og_hso3d",
        "og_psf2d",
        "og_psf3d",
        "og_pso3d",
        "og_pts2d",
        "og_pts3d",
        "og_rgd2d",
        "og_rgd3d",
        "og_sctn",
        "og_strm",
        "og_tsf2d",
        "og_tsf3d",
        "og_tso3d",
        "og_vts",
        "og_xsctn",
        "ply",
        "smesh",
        "stl",
        "svg",
        "ts",
        "txt",
        "vtp",
        "vtu",
        "wl",
    ]
    for extension in list_extensions:
        assert extension in extensions


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
    # Normal test with object
    response = client.post(
        f"{base_route}/output_file_extensions", data={"geode_object": "BRep"}
    )
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["msh", "og_brep"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with object
    response = client.post(
        f"{base_route}/output_file_extensions",
        data={"geode_object": "TriangulatedSurface3D"},
    )
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["obj", "og_tsf3d", "stl", "vtp"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with object
    response = client.post(
        f"{base_route}/output_file_extensions", data={"geode_object": "StructuralModel"}
    )
    assert response.status_code == 200
    output_file_extensions = response.json["output_file_extensions"]
    assert type(output_file_extensions) is list
    list_output_file_extensions = ["lso", "ml", "msh", "og_brep", "og_strm"]
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Test without object
    response = client.post(f"{base_route}/output_file_extensions")
    assert response.status_code == 400
    error_message = response.json["description"]
    assert error_message == "No geode_object sent"


def test_convert_file(client):
    # Normal test with object/file/filename/extension
    geode_object = "BRep"
    filename = "corbi.og_brep"
    file = base64.b64encode(open("./tests/corbi.og_brep", "rb").read())
    filesize = int(os.path.getsize("./tests/corbi.og_brep"))
    extension = "msh"

    response = client.post(
        f"{base_route}/convert_file",
        data={
            "geode_object": geode_object,
            "filename": filename,
            "extension": extension,
        },
    )

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    # Test without object
    response = client.post(
        f"{base_route}/convert_file",
        data={
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
        data={
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
        data={
            "geode_object": geode_object,
            "filename": filename,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No extension sent"
