import os
import base64

base_route = "/tools"


def test_upload_file(client):
    response = client.post(
        f"{base_route}/upload_file",
        data={"file": (open("./tests/corbi.og_brep", "rb"), "corbi.og_brep")},
    )

    assert response.status_code == 200
