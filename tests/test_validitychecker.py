import os

ID = os.environ.get('ID')

def test_versions(client):
    response = client.get(f"/{ID}/validitychecker/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict

def test_allowedfiles(client):
    response = client.get(f"/{ID}/validitychecker/allowedfiles")
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list
    list_extensions = ["dxf", "lso", "ml", "msh", "obj", "og_brep", "og_edc2d", "og_edc3d", "og_grp", "og_hso3d", "og_psf2d", "og_psf3d", "og_pso3d", "og_pts2d", "og_pts3d", "og_rgd2d", "og_rgd3d", "og_sctn", "og_strm", "og_tsf2d", "og_tsf3d", "og_tso3d", "og_vts", "og_xsctn", "ply", "smesh", "stl", "svg", "ts", "vtp", "vtu", "wl"]
    for extension in list_extensions:
        assert extension in extensions

def test_allowedobjects(client):
    # Normal test with filename "corbi.og_brep"
    response = client.post(f"/{ID}/validitychecker/allowedobjects", data={"filename": "corbi.og_brep"})
    assert response.status_code == 200
    objects = response.json["objects"]
    assert type(objects) is list
    assert "BRep" in objects

    # Normal test with filename .vtu
    response = client.post(f"/{ID}/validitychecker/allowedobjects", data={"filename": "toto.vtu"})
    assert response.status_code == 200
    objects = response.json["objects"]
    list_objects = ["HybridSolid3D", "PolyhedralSolid3D", "TetrahedralSolid3D"]
    for object in list_objects:
        assert object in objects

    # Test with stupid filename
    response = client.post(f"/{ID}/validitychecker/allowedobjects", data={"filename": "toto.txt"})
    assert response.status_code == 200
    objects = response.json["objects"]
    assert type(objects) is list
    assert not objects

    # Test without filename
    response = client.post(f"/{ID}/validitychecker/allowedobjects")
    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No file sent"