import os
import base64

ID = os.environ.get('ID')

def test_createbackend(client):
    response = client.post("/tools/createbackend")
    assert response.status_code == 200
    ID = response.json["ID"]
    assert ID == "123456"

def test_root(client):
    response = client.get(f"/{ID}/")
    assert response.status_code == 200

def test_ping(client):
    response = client.post(f"/{ID}/ping")
    assert response.status_code == 200

def test_allowedfiles(client):
    response = client.post(f"/{ID}/allowedfiles")
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list
    assert "og_brep" in extensions

def test_allowedobjects(client):
    # Normal test with filename
    response = client.post(f"/{ID}/allowedobjects", data={"filename": "corbi.og_brep"})
    assert response.status_code == 200
    objects = response.json["objects"]
    assert type(objects) is list
    assert "BRep" in objects

    # Test with stupid filename
    response = client.post(f"/{ID}/allowedobjects", data={"filename": "toto.txt"})
    assert response.status_code == 200
    objects = response.json["objects"]
    assert type(objects) is list
    assert not objects

    # Test without filename
    response = client.post(f"/{ID}/allowedobjects")
    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No file sent"

def test_outputfileextensions(client):
    # Normal test with object
    response = client.post(f"/{ID}/outputfileextensions", data={"object": "BRep"})
    assert response.status_code == 200
    outputfileextensions = response.json["outputfileextensions"]
    assert type(outputfileextensions) is list
    assert "og_brep" in outputfileextensions
    assert "msh" in outputfileextensions

    # Test without object
    response = client.post(f"/{ID}/outputfileextensions")
    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No object sent"

def test_convertfile(client):
    # Normal test with object/file/filename/extension
    response = client.post(f"/{ID}/convertfile",
        data = {
            "object": "BRep",
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
            "extension": "msh"
        }
    )

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    # Test without object
    response = client.post(f"/{ID}/convertfile",
        data = {
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
            "extension": "msh"
        }
    )

    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No object sent"

    # Test without file
    response = client.post(f"/{ID}/convertfile",
        data = {
            "object": "BRep",
            "filename": "corbi.og_brep",
            "extension": "msh"
        }
    )

    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No file sent"

    # Test without filename
    response = client.post(f"/{ID}/convertfile",
        data = {
            "object": "BRep",
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "extension": "msh"
        }
    )

    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No filename sent"

    # Test without extension
    response = client.post(f"/{ID}/convertfile",
        data = {
            "object": "BRep",
            "file": base64.b64encode(open("./tests/corbi.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
        }
    )

    assert response.status_code == 400
    error_message = response.json["error_message"]
    assert error_message == "No extension sent"