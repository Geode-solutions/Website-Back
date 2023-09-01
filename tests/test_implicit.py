import os
import json
import base64

base_route = f"/workflows/implicit"


def test_step0(client):
    response = client.post(f"{base_route}/step0")
    assert response.status_code == 200
    constraints = eval(response.json["constraints"])
    assert type(constraints) is list
    for constraint in constraints:
        assert type(constraint) is list


def test_step1(client):
    constraints = '[{ "x": "5", "y": "6.25", "z": "9.5", "value": "0" },{ "x": "29.5", "y": "30.3", "z": "9.5", "value": "0" },{ "x": "12.1", "y": "24.9", "z": "9.5", "value": "0" },{ "x": "27.3", "y": "17.9", "z": "9.5", "value": "0" },{ "x": "14", "y": "14.6", "z": "9.5", "value": "0" },{ "x": "17", "y": "21.95", "z": "9.5", "value": "0" },{ "x": "22.14", "y": "14.22", "z": "9.5", "value": "0" },{ "x": "17.2", "y": "5.5", "z": "9.5", "value": "0" },{ "x": "26.6", "y": "9.27", "z": "9.5", "value": "0" },{ "x": "23.9", "y": "24.5", "z": "9.5", "value": "0" },{ "x": "8.6", "y": "27.2", "z": "25.5", "value": "1" },{ "x": "13.6", "y": "15", "z": "25.5", "value": "1" },{ "x": "13.7", "y": "6.55", "z": "25.5", "value": "1" },{ "x": "23.1", "y": "26.98", "z": "25.5", "value": "1" },{ "x": "24.1", "y": "10.2", "z": "25.5", "value": "1" },{ "x": "16.3", "y": "25.7", "z": "25.5", "value": "1" },{ "x": "35.1", "y": "34.9", "z": "25.5", "value": "1" }]'
    isovalues = json.dumps([0, 1, 2])

    # Normal test with constraints/isovalues
    response = client.post(
        f"{base_route}/step1",
        data={
            "constraints": constraints,
            "isovalues": isovalues,
        },
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without constraints
    response = client.post(
        f"{base_route}/step1",
        data={
            "isovalues": isovalues,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No constraints sent"

    # Test without isovalues
    response = client.post(
        f"{base_route}/step1",
        data={
            "constraints": constraints,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No isovalues sent"

    # Test with stupid constraints value
    constraints_stupid = '[{ "x": "5", "y": "toto", "z": "9.5", "value": "0" }]'
    response = client.post(
        f"{base_route}/step1",
        data={
            "constraints": constraints_stupid,
            "isovalues": isovalues,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for the constraint point"


def test_step2(client):
    axis = "0"
    coordinate = "2"

    # Normal test with axis/diretcion
    response = client.post(
        f"{base_route}/step2", data={"axis": axis, "coordinate": coordinate}
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without axis
    response = client.post(f"{base_route}/step2", data={"coordinate": coordinate})
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No axis sent"

    # Test with stupid axis value
    axis_stupid = "Toto"
    response = client.post(
        f"{base_route}/step2", data={"axis": axis_stupid, "coordinate": coordinate}
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for the axis"

    # Test with stupid coordinate value
    coordinate_stupid = "Toto"
    response = client.post(
        f"{base_route}/step2", data={"axis": axis, "coordinate": coordinate_stupid}
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for the coordinate"


def test_step3(client):
    metric = "1"

    # Normal test with metric
    response = client.post(
        f"{base_route}/step3",
        data={
            "metric": metric,
        },
    )
    assert response.status_code == 200
    viewable_file_name = response.json["viewable_file_name"]
    id = response.json["id"]
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without metric
    response = client.post(f"{base_route}/step3", data={})
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No metric sent"

    # Test with stupid metric value
    metric_stupid = "Toto"
    response = client.post(
        f"{base_route}/step3",
        data={
            "metric": metric_stupid,
        },
    )
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "Invalid data format for the metric"
