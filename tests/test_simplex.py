import os
import base64

base_route = f"/workflows/simplex"


def test_get_brep_info(client):
    response = client.post(f"{base_route}/get_brep_info")
    assert response.status_code == 200
    surfacesID = response.json["surfacesIDS"]
    blocksIDS = response.json["blocksIDS"]
    assert type(surfacesID) is list
    assert type(blocksIDS) is list


def test_remesh(client):
    surfaceMetrics = '{"00000000-fe86-4d4c-8000-000048049966":"200"}'
    blockMetrics = '{"00000000-e121-4f75-8000-0000676a61c8":"200"}'
    globalMetric = "150"

    # Normal test with surfaceMetrics/blockMetrics/globalmetric
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 200

    # Test without surfaceMetrics
    response = client.post(
        f"{base_route}/remesh",
        data={
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No surfaceMetrics sent"

    # Test without blockMetrics
    response = client.post(
        f"{base_route}/remesh",
        data={"surfaceMetrics": surfaceMetrics, "globalMetric": globalMetric},
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No blockMetrics sent"

    # Test without globalMetric
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockMetrics,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No globalMetric sent"

    # Test with stupid surface metric
    surfaceMetrics_stupid = '{"00000000-fe86-4d4c-8000-000048049966":"toto"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics_stupid,
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for an individual metric variable"

    # Test with stupid surface metric ID
    surfaceID_stupid = '{"toto":"200"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceID_stupid,
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid ID for an individual metric variable"

    # Test with non-existent surface metric ID
    surfaceID_nonexistent = '{"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx":"200"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceID_nonexistent,
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid UUID for an individual metric variable"

    # Test with stupid surface metric
    blockMetrics_stupid = '{"00000000-e121-4f75-8000-0000676a61c8":"toto"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockMetrics_stupid,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for an individual metric variable"

    # Test with stupid surface metric ID
    blockID_stupid = '{"toto":"200"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockID_stupid,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid ID for an individual metric variable"

    # Test with non-existent block metric ID
    blockID_nonexistent = '{"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx":"200"}'
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockID_nonexistent,
            "globalMetric": globalMetric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid UUID for an individual metric variable"

    # Test with stupid surface metric
    globalMetric_stupid = "Toto"
    response = client.post(
        f"{base_route}/remesh",
        data={
            "surfaceMetrics": surfaceMetrics,
            "blockMetrics": blockMetrics,
            "globalMetric": globalMetric_stupid,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for the global metric variable"
