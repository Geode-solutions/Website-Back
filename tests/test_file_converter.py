import os
import base64

import geode_objects
geode_objects_list = geode_objects.objects_list()

ID = os.environ.get('ID')
base_route = f'/{ID}/file_converter'


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


def test_allowed_objects(client):
    # Normal test with dymamic extension
    for geode_object in geode_objects_list.keys():
        inputs = geode_objects_list[geode_object]['input']
        for input in inputs:
            for input_extension in input.list_creators():
                response = client.post(
                    f'{base_route}/allowed_objects', data={'filename': f'test.{input_extension}'})
                assert response.status_code == 200
                allowed_objects = response.json['allowed_objects']
                assert type(allowed_objects) is list
                assert len(allowed_objects) > 0

    # Test with stupid filename
    response = client.post(
        f'{base_route}/allowed_objects', data={'filename': 'toto.tutu'})
    assert response.status_code == 200
    allowed_objects = response.json['allowed_objects']
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(f'{base_route}/allowed_objects')
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No file sent'


def test_output_file_extensions(client):

    # Normal test with object
    for geode_object in geode_objects_list.keys():
        response = client.post(
            f'{base_route}/output_file_extensions', data={'geode_object': geode_object})
        assert response.status_code == 200
        output_file_extensions = response.json['output_file_extensions']
        assert type(output_file_extensions) is list
        assert len(output_file_extensions) > 0

    # Test without object
    response = client.post(f'{base_route}/output_file_extensions')
    assert response.status_code == 400
    error_message = response.json['error_message']
    assert error_message == 'No geode_object sent'


def test_convert_file(client):
    for geode_object in geode_objects_list.keys():
        if geode_object != 'BRep':
            print(f'{geode_object=}')
            inputs = geode_objects_list[geode_object]['input']

            for input in inputs:
                for input_extension in input.list_creators():
                    print(f'{input_extension=}')
                    filename = f'corbi.{input_extension}'
                    file = base64.b64encode(
                        open(f'./tests/data/test.{input_extension}', 'rb').read())
                    filesize = int(os.path.getsize(
                        f'./tests/data/test.{input_extension}'))

                    outputs = geode_objects_list[geode_object]['output']

                    for output in outputs:
                        for output_extension in output.list_creators():
                            print(f'{output_extension=}')

                            # Normal test with object/file/filename/filesize/extension
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'geode_object': geode_object,
                                                       'file': file,
                                                       'filename': filename,
                                                       'filesize': filesize,
                                                       'extension': output_extension
                                                   }
                                                   )

                            assert response.status_code == 200
                            assert type((response.data)) is bytes
                            assert len((response.data)) > 0

                            # Test without object
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'file': file,
                                                       'filename': filename,
                                                       'filesize': filesize,
                                                       'extension': output_extension
                                                   }
                                                   )

                            assert response.status_code == 400
                            error_description = response.json['description']
                            assert error_description == 'No geode_object sent'

                            # Test without file
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'geode_object': geode_object,
                                                       'filename': filename,
                                                       'filesize': filesize,
                                                       'extension': output_extension
                                                   }
                                                   )

                            assert response.status_code == 400
                            error_description = response.json['description']
                            assert error_description == 'No file sent'

                            # Test without filename
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'geode_object': geode_object,
                                                       'file': file,
                                                       'filesize': filesize,
                                                       'extension': output_extension
                                                   }
                                                   )

                            assert response.status_code == 400
                            error_description = response.json['description']
                            assert error_description == 'No filename sent'

                            # Test without filesize
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'geode_object': geode_object,
                                                       'file': file,
                                                       'filename': filename,
                                                       'extension': output_extension
                                                   }
                                                   )

                            assert response.status_code == 400
                            error_description = response.json['description']
                            assert error_description == 'No filesize sent'

                            # Test without extension
                            response = client.post(f'{base_route}/convert_file',
                                                   data={
                                                       'geode_object': geode_object,
                                                       'file': file,
                                                       'filename': filename,
                                                       'filesize': filesize
                                                   }
                                                   )

                            assert response.status_code == 400
                            error_description = response.json['description']
                            assert error_description == 'No extension sent'
