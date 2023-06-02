import os
import base64

ID = os.environ.get('ID')
base_route = f'/{ID}/crs_converter'

def test_versions(client):
    response = client.get(f'{base_route}/versions')
    assert response.status_code == 200
    versions = response.json['versions']
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict

def test_allowed_files(client):
    response = client.get(f'{base_route}/allowed_files')
    assert response.status_code == 200
    extensions = response.json['extensions']
    assert type(extensions) is list
    list_extensions = ['dat', 'dev', 'dxf', 'lso', 'ml', 'msh', 'obj', 'og_brep', 'og_edc2d', 'og_edc3d', 'og_grp', 'og_hso3d', 'og_psf2d', 'og_psf3d', 'og_pso3d', 'og_pts2d', 'og_pts3d', 'og_rgd2d', 'og_rgd3d', 'og_sctn', 'og_strm', 'og_tsf2d', 'og_tsf3d', 'og_tso3d', 'og_vts', 'og_xsctn', 'ply', 'smesh', 'stl', 'svg', 'ts', 'txt', 'vtp', 'vtu', 'wl']
    for extension in list_extensions:
        assert extension in extensions

def test_allowed_objects(client):
    route = f'{base_route}/allowed_objects'

    # Normal test with filename 'corbi.og_brep'
    response = client.post(route, data={'filename': 'corbi.og_brep'})
    assert response.status_code == 200
    allowed_objects = response.json['allowed_objects']
    assert type(allowed_objects) is list
    assert 'BRep' in allowed_objects

    # Normal test with filename .vtu
    response = client.post(route, data={'filename': 'toto.vtu'})
    assert response.status_code == 200
    allowed_objects = response.json['allowed_objects']
    list_objects = ['HybridSolid3D', 'PolyhedralSolid3D', 'TetrahedralSolid3D']
    for geode_object in list_objects:
        assert geode_object in allowed_objects

    # Test with stupid filename
    response = client.post(route, data={'filename': 'toto.tutu'})
    assert response.status_code == 200
    allowed_objects = response.json['allowed_objects']
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No file sent'

def test_geographic_coordinate_systems(client):
    route = f'{base_route}/geographic_coordinate_systems'

    # Normal test with geode_object 'BRep'
    response = client.post(route, data={'geode_object': 'BRep'})
    assert response.status_code == 200
    crs_list = response.json['crs_list']
    assert type(crs_list) is list
    for crs in crs_list:
        assert type(crs) is dict

    # Test without geode_object
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No geode_object sent'

def test_output_file_extensions(client):
    route = f'{base_route}/output_file_extensions'

    # Normal test with geode_object
    response = client.post(route, data={'geode_object': 'BRep'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['msh', 'og_brep']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with geode_object
    response = client.post(route, data={'geode_object': 'TriangulatedSurface3D'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['obj', 'og_tsf3d', 'stl', 'vtp']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with geode_object
    response = client.post(route, data={'geode_object': 'StructuralModel'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['lso', 'ml', 'msh', 'og_brep', 'og_strm']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Test without object
    response = client.post(route)
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No geode_object sent'

def test_convert_file(client):
    # Normal test with object/file/filename/extension
    geode_object = 'BRep'
    filename = 'corbi.og_brep'
    file = base64.b64encode(open('./tests/corbi.og_brep', 'rb').read())
    filesize = int(os.path.getsize('./tests/corbi.og_brep'))
    input_crs_authority = 'EPSG'
    input_crs_code = '2000'
    input_crs_name = 'Anguilla 1957 / British West Indies Grid'
    output_crs_authority = 'EPSG'
    output_crs_code = '2001'
    output_crs_name = 'Antigua 1943 / British West Indies Grid'

    extension = 'msh'

    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    # Test without geode_object
    response = client.post(f'{base_route}/convert_file',
        data = {
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No geode_object sent'

    # Test without file
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No file sent'

    # Test without filename
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No filename sent'

    # Test without filesize
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No filesize sent'

    # Test without input_crs_authority
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No input_crs_authority sent'

    # Test without input_crs_code
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No input_crs_code sent'

    # Test without input_crs_name
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No input_crs_name sent'

    # Test without output_crs_authority
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No output_crs_authority sent'

    # Test without output_crs_code
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_name': output_crs_name,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No output_crs_code sent'

    # Test without output_crs_name
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No output_crs_name sent'

    # Test without extension
    response = client.post(f'{base_route}/convert_file',
        data = {
            'geode_object': geode_object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs_authority': input_crs_authority,
            'input_crs_code': input_crs_code,
            'input_crs_name': input_crs_name,
            'output_crs_authority': output_crs_authority,
            'output_crs_code': output_crs_code,
            'output_crs_name': output_crs_name
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No extension sent'
