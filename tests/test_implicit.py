import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/workflows/implicit"

def test_get_constraints(client):
    response = client.post(f'{base_route}/get_constraints')
    assert response.status_code == 200
    constraints = eval(response.json['constraints'])
    assert type(constraints) is list
    for constraint in constraints:
        assert type(constraint) is list
    
def test_step1(client):

    bbox_points = '{"x_min":"0", "y_min":"0", "z_min":"0", "x_max":"8", "y_max":"11", "z_max":"17"}'
    constraints = '[{ "x": "5", "y": "6.25", "z": "9.5", "value": "0", "weight": "10" },{ "x": "29.5", "y": "30.3", "z": "9.5", "value": "0", "weight": "10" },{ "x": "12.1", "y": "24.9", "z": "9.5", "value": "0", "weight": "10" },{ "x": "27.3", "y": "17.9", "z": "9.5", "value": "0", "weight": "10" },{ "x": "14", "y": "14.6", "z": "9.5", "value": "0", "weight": "10" },{ "x": "17", "y": "21.95", "z": "9.5", "value": "0", "weight": "10" },{ "x": "22.14", "y": "14.22", "z": "9.5", "value": "0", "weight": "10" },{ "x": "17.2", "y": "5.5", "z": "9.5", "value": "0", "weight": "10" },{ "x": "26.6", "y": "9.27", "z": "9.5", "value": "0", "weight": "10" },{ "x": "23.9", "y": "24.5", "z": "9.5", "value": "0", "weight": "10" },{ "x": "8.6", "y": "27.2", "z": "25.5", "value": "1", "weight": "10" },{ "x": "13.6", "y": "15", "z": "25.5", "value": "1", "weight": "10" },{ "x": "13.7", "y": "6.55", "z": "25.5", "value": "1", "weight": "10" },{ "x": "23.1", "y": "26.98", "z": "25.5", "value": "1", "weight": "10" },{ "x": "24.1", "y": "10.2", "z": "25.5", "value": "1", "weight": "10" },{ "x": "16.3", "y": "25.7", "z": "25.5", "value": "1", "weight": "10" },{ "x": "35.1", "y": "34.9", "z": "25.5", "value": "1", "weight": "10" }]'
    isovalues = '["0","1","2"]'
    function_type = "Laplacian"
    cell_size = "1"

    # Normal test with bbox_points/constraints/isovalues/function_type/cell_size
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 200
    viewable_file_name = response.json['viewable_file_name']
    id = response.json['id']
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without bbox points
    response = client.post(f'{base_route}/step1',
        data = {
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No bbox_points sent'

    # Test without constraints
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No constraints sent'

    # Test without isovalues
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No isovalues sent'

    # Test without function_type
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No function_type sent'

    # Test without cell_size
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type,
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No cell_size sent'

    # Test with stupid bbox_points value
    bbox_points_stupid = '{"x_min":"0", "y_min":"toto", "z_min":"0", "x_max":"8", "y_max":"11", "z_max":"17"}'
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points_stupid,
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'Invalid data format for the BBox points'

    # Test with stupid constraints value
    constraints_stupid = '[{ "x": "5", "y": "toto", "z": "9.5", "value": "0", "weight": "10" }]'
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints_stupid,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'Invalid data format for the constraints'

    # Test with stupid isovalues value
    isovalues_stupid = '["0","toto","2"]'
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues_stupid,
            'function_type': function_type,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'Invalid data format for the isovalues'

    # Test with stupid function_type value
    function_type_stupid = "Toto"
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type_stupid,
            'cell_size': cell_size
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'Invalid minimization scheme value'

    # Test with stupid cell_size value
    cell_size_stupid = "Toto"
    response = client.post(f'{base_route}/step1',
        data = {
            'bbox_points': bbox_points,
            'constraints': constraints,
            'isovalues': isovalues,
            'function_type': function_type,
            'cell_size': cell_size_stupid
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'Invalid data format for the cell size'

def test_step2(client):
    
    axis = "0"
    direction = "2"

    # Normal test with axis/diretcion
    response = client.post(f'{base_route}/step2',
        data = {
            'axis': axis,
            'direction': direction
        }
    )
    assert response.status_code == 200
    viewable_file_name = response.json['viewable_file_name']
    id = response.json['id']
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without axis
    response = client.post(f'{base_route}/step2',
        data = {
            'direction': direction
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No axis sent'

    # Test without direction
    response = client.post(f'{base_route}/step2',
        data = {
            'axis': axis,
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No direction sent'

    # Test with stupid axis value
    axis_stupid = "Toto"
    response = client.post(f'{base_route}/step2',
        data = {
            'axis': axis_stupid,
            'direction': direction
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == "Invalid data format for the 'axis' or 'metric' variables"

    # Test with stupid direction value
    direction_stupid = "Toto"
    response = client.post(f'{base_route}/step2',
        data = {
            'axis': axis,
            'direction': direction_stupid
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == "Invalid data format for the 'axis' or 'metric' variables"

def test_step3(client):
    
    metric = "1"

    # Normal test with metric
    response = client.post(f'{base_route}/step3',
        data = {
            'metric': metric,
        }
    )
    assert response.status_code == 200
    viewable_file_name = response.json['viewable_file_name']
    id = response.json['id']
    assert type(viewable_file_name) is str
    assert type(id) is str

    # Test without metric
    response = client.post(f'{base_route}/step3',
        data = {}
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No metric sent'

    # Test with stupid metric value
    metric_stupid = "Toto"
    response = client.post(f'{base_route}/step3',
        data = {
            'metric': metric_stupid,
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == "Invalid data format for the 'metric' variable"