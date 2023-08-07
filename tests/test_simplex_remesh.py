import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/simplexRemesh"


def test_get_brep_info(client):
    response = client.post(f'{base_route}/get_brep_info')
    assert response.status_code == 200
    surfacesID = response.json['surfacesIDS']
    blocksIDS = response.json['blocksIDS']
    assert type(surfacesID) is list
    assert type(blocksIDS) is list
    

def test_remesh(client):
    
    surfaceMetrics = '{"00000000-fe86-4d4c-8000-000048049966":"200"}'
    blockMetrics = '{"00000000-e121-4f75-8000-0000676a61c8":"200"}'
    globalMetric = "150"

    # Normal test with surfaceMetrics/blockMetrics/globalmetric
    response = client.post(f'{base_route}/remesh',
        data = {
            'surfaceMetrics': surfaceMetrics,
            'blockMetrics': blockMetrics,
            'globalMetric': globalMetric,
        }
    )
    assert response.status_code == 200

    # Test without surfaceMetrics
    response = client.post(f'{base_route}/remesh',
        data = {
            'blockMetrics': blockMetrics,
            'globalMetric': globalMetric,
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No surfaceMetrics sent'

    # Test without blockMetrics
    response = client.post(f'{base_route}/remesh',
        data = {
            'surfaceMetrics': surfaceMetrics,
            'globalMetric': globalMetric
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No blockMetrics sent'

    # Test without globalMetric
    response = client.post(f'{base_route}/remesh',
        data = {
            'surfaceMetrics': surfaceMetrics,
            'blockMetrics': blockMetrics,
        }
    )
    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No globalMetric sent'
