import os
import base64

base_route = "/workflows/simplex"


def test_initialize(client):
    response = client.post(f"{base_route}/initialize")
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str


def test_remesh(client):
    metric = 150
    faults_metric = 50

    # Normal test
    response = client.post(
        f"{base_route}/remesh",
        json={
            "metric": metric,
            "faults_metric": faults_metric,
        },
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without faults_metric
    response = client.post(
        f"{base_route}/remesh",
        json={
            "metric": metric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No faults_metric sent"

    # Test without metric
    response = client.post(
        f"{base_route}/remesh",
        json={
            "faults_metric": faults_metric,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No metric sent"
