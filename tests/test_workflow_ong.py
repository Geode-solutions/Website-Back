import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/ong"

def test_get_constraints(client):
    response = client.get(f'{base_route}/get_constraints')
    assert response.status_code == 200
    constraints = response.json['constraints']
    assert type(constraints) is list
    for constraint in constraints:
        assert type(constraint) is list
    
def test_step1(client):

    bbox_points = '{"x_min":"0", "y_min":"0", "z_min":"0", "x_max":"8", "y_max":"11", "z_max":"17"}'
    constraints = '[{"x":"0","y":"1","z":"2","value":4,"weight":"20"},{"x":"4","y":"5","z":"6","value":"9","weight":"20"}]'
    isovalues = '["4","5","6"]'
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

def test_step3(client):
    
    metric = "1"

    # Normal test with metric
    response = client.post(f'{base_route}/step3',
        data = {
            'metric': metric,
        }
    )
    assert response.status_code == 200

    # Test without metric
    response = client.post(f'{base_route}/step3',
        data = {}
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No metric sent'