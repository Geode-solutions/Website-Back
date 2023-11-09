import os
import json
import base64

base_route = "/workflows/implicit"


def test_step0(client):
    response = client.post(f"{base_route}/step0")
    assert response.status_code == 200
    constraints = eval(response.json["constraints"])
    assert type(constraints) is list
    for constraint in constraints:
        assert type(constraint) is list


def test_step1(client):
    isovalues = json.dumps([0, 0.5, 1])

    # Normal test with isovalues
    response = client.post(
        f"{base_route}/step1",
        json={
            "isovalues": isovalues,
        },
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without isovalues
    response = client.post(
        f"{base_route}/step1",
        json={},
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No isovalues sent"


def test_step2(client):
    axis = 0
    coordinate = 2

    # Normal test with axis/diretcion
    response = client.post(
        f"{base_route}/step2", json={"axis": axis, "coordinate": coordinate}
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without axis
    response = client.post(f"{base_route}/step2", json={"coordinate": coordinate})
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No axis sent"


def test_step3(client):
    metric = 1

    # Normal test with metric
    response = client.post(
        f"{base_route}/step3",
        json={
            "metric": metric,
        },
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without metric
    response = client.post(f"{base_route}/step3", json={})
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No metric sent"
