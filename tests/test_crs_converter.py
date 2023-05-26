import os
import base64

ID = os.environ.get('ID')
base_route = f"/{ID}/crs_converter"

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
    list_extensions = ["dat", "dev", "dxf", "lso", "ml", "msh", "obj", "og_brep", "og_edc2d", "og_edc3d", "og_grp", "og_hso3d", "og_psf2d", "og_psf3d", "og_pso3d", "og_pts2d", "og_pts3d", "og_rgd2d", "og_rgd3d", "og_sctn", "og_strm", "og_tsf2d", "og_tsf3d", "og_tso3d", "og_vts", "og_xsctn", "ply", "smesh", "stl", "svg", "ts", "txt", "vtp", "vtu", "wl"]
    for extension in list_extensions:
        assert extension in extensions

def test_allowed_objects(client):
    # Normal test with filename 'corbi.og_brep'
    response = client.post(f'{base_route}/allowed_objects', data={'filename': 'corbi.og_brep'})
    assert response.status_code == 200
    objects = response.json['objects']
    assert type(objects) is list
    assert 'BRep' in objects

    # Normal test with filename .vtu
    response = client.post(f'{base_route}/allowed_objects', data={'filename': 'toto.vtu'})
    assert response.status_code == 200
    objects = response.json['objects']
    list_objects = ['HybridSolid3D', 'PolyhedralSolid3D', 'TetrahedralSolid3D']
    for object in list_objects:
        assert object in objects

    # Test with stupid filename
    response = client.post(f'{base_route}/allowed_objects', data={'filename': 'toto.tutu'})
    assert response.status_code == 200
    objects = response.json['objects']
    assert type(objects) is list
    assert not objects

    # Test without filename
    response = client.post(f'{base_route}/allowed_objects')
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No file sent'

def test_output_file_extensions(client):
    # Normal test with object
    response = client.post(f'{base_route}/output_file_extensions', data={'object': 'BRep'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['msh', 'og_brep']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with object
    response = client.post(f'{base_route}/output_file_extensions', data={'object': 'TriangulatedSurface3D'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['obj', 'og_tsf3d', 'stl', 'vtp']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Normal test with object
    response = client.post(f'{base_route}/output_file_extensions', data={'object': 'StructuralModel'})
    assert response.status_code == 200
    output_file_extensions = response.json['output_file_extensions']
    assert type(output_file_extensions) is list
    list_output_file_extensions = ['lso', 'ml', 'msh', 'og_brep', 'og_strm']
    for output_file_extension in list_output_file_extensions:
        assert output_file_extension in output_file_extensions

    # Test without object
    response = client.post(f'{base_route}/output_file_extensions')
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No object sent.'

def test_convert_file(client):
    # Normal test with object/file/filename/extension
    object = 'BRep'
    filename = 'corbi.og_brep'
    file = base64.b64encode(open('./tests/corbi.og_brep', 'rb').read())
    filesize = int(os.path.getsize('./tests/corbi.og_brep'))
    input_crs = { 'authority': 'EPSG', 'code': '2000' }
    output_crs = { 'authority': 'EPSG', 'code': '2001' }
    extension = 'msh'

    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs': input_crs,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 200
    assert type((response.data)) is bytes
    assert len((response.data)) > 0

    # Test without object
    response = client.post(f'{base_route}/convert_file',
        data = {
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs': input_crs,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No object sent.'

    # Test without file
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'filename': filename,
            'filesize': filesize,
            'input_crs': input_crs,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No file sent.'

    # Test without filename
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filesize': filesize,
            'input_crs': input_crs,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No filename sent.'

    # Test without filesize
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filename': filename,
            'input_crs': input_crs,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No filesize sent.'

    # Test without input_crs
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'output_crs': output_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No input_crs sent.'

    # Test without output_crs
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs': input_crs,
            'extension': extension
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No output_crs sent.'

    # Test without extension
    response = client.post(f'{base_route}/convert_file',
        data = {
            'object': object,
            'file': file,
            'filename': filename,
            'filesize': filesize,
            'input_crs': input_crs,
            'output_crs': output_crs
        }
    )

    assert response.status_code == 400
    error_description = response.json['description']
    assert error_description == 'No extension sent.'
