import os
import base64
from werkzeug.datastructures import FileStorage

base_route = "/tools"


def test_upload_file(client):
    response = client.put(
        f"{base_route}/upload_file",
        data={"content": FileStorage(open("./tests/corbi.og_brep", "rb"))},
    )

    assert response.status_code == 201
