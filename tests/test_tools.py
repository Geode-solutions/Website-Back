import os
import base64

base_route = "/tools"


def test_upload_file(client):
    response = client.put(
        f"{base_route}/upload_file",
        data={"content": (open("./tests/corbi.og_brep", "rb"))},
    )

    assert response.status_code == 201
