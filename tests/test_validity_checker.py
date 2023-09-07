import os
import base64

base_route = "/tools/validity_checker"


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
    for geode_object in list_objects:
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
    error_description = response.json["description"]
    assert error_description == "No filename sent"


def test_upload_file(client):
    # Test with file
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
            "filesize": os.path.getsize("./tests/corbi.og_brep"),
        },
    )

    assert response.status_code == 200
    message = response.json["message"]
    assert message == "File uploaded"

    # Test without file
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "filename": "corbi.og_brep",
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No file sent"

    # Test without filename
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"


def test_test_names(client):
    ObjectArray = [
        "BRep",
        "CrossSection",
        "EdgedCurve2D",
        "EdgedCurve3D",
        "Graph",
        "HybridSolid3D",
        "PointSet2D",
        "PointSet3D",
        "PolygonalSurface2D",
        "PolygonalSurface3D",
        "PolyhedralSolid3D",
        "RegularGrid2D",
        "RegularGrid3D",
        "Section",
        "StructuralModel",
        "TetrahedralSolid3D",
        "TriangulatedSurface2D",
        "TriangulatedSurface3D",
        "VertexSet",
    ]

    for geode_object in ObjectArray:
        # Normal test with all objects
        response = client.post(
            f"{base_route}/tests_names", data={"geode_object": geode_object}
        )
        assert response.status_code == 200
        model_checks = response.json["model_checks"]

        assert type(model_checks) is list
        for model_check in model_checks:
            assert type(model_check) is dict
            is_leaf = model_check["is_leaf"]
            route = model_check["route"]
            children = model_check["children"]
            assert type(is_leaf) is bool
            assert type(route) is str
            assert type(children) is list
            for check in children:
                assert type(check) is dict
                if check["is_leaf"] == True:
                    print("is_leaf")
                    response_test = client.post(
                        f"{base_route}/inspect_file",
                        data={
                            "object": "BRep",
                            "filename": "corbi.og_brep",
                            "test": check["route"],
                        },
                    )

                    assert response_test.status_code == 200
                else:
                    print("not is_leaf")


def test_inspect_file(client):
    # Test with file
    response = client.post(
        f"{base_route}/inspect_file",
        data={
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
            "filesize": os.path.getsize("./tests/corbi.og_brep"),
        },
    )
