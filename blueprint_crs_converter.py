import shutil
import flask
import flask_cors
import os
import werkzeug
import functions
import zipfile
import geode_objects


crs_converter_routes = flask.Blueprint('crs_converter_routes', __name__)
flask_cors.CORS(crs_converter_routes)


@crs_converter_routes.before_request
def before_request():
    functions.create_lock_file()

@crs_converter_routes.teardown_request
def teardown_request(exception):
    functions.remove_lock_file()
    functions.create_time_file()

@crs_converter_routes.route('/versions', methods=['GET'])
def crs_converter_versions():
    list_packages = ['OpenGeode-core', 'OpenGeode-IO', 'OpenGeode-Geosciences', 'OpenGeode-GeosciencesIO']
    
    return flask.make_response({'versions': functions.get_versions(list_packages)}, 200)

@crs_converter_routes.route('/allowed_files', methods=['GET'])
def crs_converter_allowed_files():
    extensions = functions.list_all_input_extensions()
    
    return {'status': 200, 'extensions': extensions}

@crs_converter_routes.route('/allowed_objects', methods=['POST'])
def crs_converter_allowed_objects():
    filename = flask.request.form.get('filename')
    if filename is None:
        return flask.make_response({'error_message': 'No file sent'}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    objects = functions.list_objects(file_extension)
    
    return flask.make_response({'objects': objects}, 200)

@crs_converter_routes.route('/geographic_coordinate_systems', methods=['POST'])
def crs_converter_geographic_coordinate_systems():
    geode_object = flask.request.form.get('geode_object')
    if geode_object is None:
        return flask.make_response({'error_message': 'No geode_object sent'}, 400)
        
    infos = geode_objects.get_geographic_coordinate_systems(geode_object)
    crs_list = []

    for info in infos:
        crs = {}
        crs['name'] = info.name
        crs['code'] = info.code
        crs['authority'] = info.authority
        crs_list.append(crs)

    return flask.make_response({'crs_list': crs_list}, 200)

@crs_converter_routes.route('/output_file_extensions', methods=['POST'])
def crs_converter_output_file_extensions():
    geode_object = flask.request.form.get('geode_object')
    if geode_object is None:
        return flask.make_response({'error_message': 'No geode_object sent'}, 400)
    output_file_extensions = functions.list_output_file_extensions(geode_object)

    return flask.make_response({'output_file_extensions': output_file_extensions}, 200)

@crs_converter_routes.route('/convert_file', methods=['POST'])
async def crs_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
    geode_object= flask.request.form.get('object')
    file = flask.request.form.get('file')
    filename = flask.request.form.get('filename')
    filesize = flask.request.form.get('filesize')
    input_crs_authority = flask.request.form.get('input_crs_authority')
    input_crs_code = flask.request.form.get('input_crs_code')
    output_crs_authority = flask.request.form.get('output_crs_authority')
    output_crs_code = flask.request.form.get('output_crs_code')
    extension = flask.request.form.get('extension')

    if geode_object is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No geode_objectsent' }, 400)
    if file is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No file sent' }, 400)
    if filename is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No filename sent' }, 400)
    if filesize is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No filesize sent' }, 400)
    if input_crs_authority is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No input_crs_authority sent' }, 400)
    if input_crs_code is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No input_crs_code sent' }, 400)
    if output_crs_authority is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No output_crs_authority sent' }, 400)
    if output_crs_code is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No output_crs_code sent' }, 400)
    if extension is None:
        return flask.make_response({ 'name': 'Bad Request','description': 'No extension sent' }, 400)

    print(f'{geode_object=}', flush=True)
    print(f'{file=}', flush=True)
    print(f'{filename=}', flush=True)
    print(f'{filesize=}', flush=True)
    print(f'{input_crs_authority=}', flush=True)
    print(f'{input_crs_code=}', flush=True)
    print(f'{output_crs_authority=}', flush=True)
    print(f'{output_crs_code=}', flush=True)
    print(f'{extension=}', flush=True)

    uploadedFile = functions.upload_file(file, filename, UPLOAD_FOLDER, filesize)
    if not uploadedFile:
        flask.make_response({ 'name': 'Internal Server Error','description': 'File not uploaded' }, 500)

    secure_filename = werkzeug.utils.secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename).replace('\\','/')
    model = functions.geode_objects.objects_list()[object]['load'](file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + '.' + extension

    mimetype = 'application/octet-binary'
    response = flask.send_from_directory(directory=UPLOAD_FOLDER, path=new_file_name, as_attachment=True, mimetype = mimetype)
    response.headers['new-file-name'] = new_file_name
    response.headers['Access-Control-Expose-Headers'] = 'new-file-name'
    
    return response

