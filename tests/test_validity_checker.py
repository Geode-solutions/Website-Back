import os
import base64
from werkzeug.datastructures import FileStorage

base_route = "/tools/validity_checker"


def test_versions(client):
    response = client.get(f"{base_route}/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict


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
            f"{base_route}/tests_names",
            json={"input_geode_object": geode_object},
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
                        json={
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

    filename = "corbi.og_brep"

    response = client.put(
        "tools/upload_file",
        data={"file": FileStorage(open(f"./tests/{filename}", "rb"))},
    )
    assert response.status_code == 201

    response = client.post(
        f"{base_route}/inspect_file",
        json={
            "filename": filename,
        },
    )
