import flask
import flask_cors
import os
import base64
import functions
import werkzeug
import pkg_resources

fileconverter_routes = flask.Blueprint('fileconverter_routes', __name__)
flask_cors.CORS(fileconverter_routes)

@fileconverter_routes.route('/versions', methods=['GET'])
def fileconverter_versions():
    list_packages = ['OpenGeode-core', 'OpenGeode-IO', 'OpenGeode-Geosciences', 'OpenGeode-GeosciencesIO']
    list_with_versions = []
    for package in list_packages:
        list_with_versions.append({"package": package, "version": pkg_resources.get_distribution(package).version})
    return flask.make_response({"versions": list_with_versions}, 200)

@fileconverter_routes.route('/allowedfiles', methods=['GET'])
def fileconverter_allowedfiles():
    extensions = functions.ListAllInputExtensions()
    return {"status": 200, "extensions": extensions}

@fileconverter_routes.route('/allowedobjects', methods=['POST'])
def fileconverter_allowedobjects():
    filename = flask.request.form.get('filename')
    if filename is None:
        return flask.make_response({"error_message": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    objects = functions.ListObjects(file_extension)
    return flask.make_response({"objects": objects}, 200)

@fileconverter_routes.route('/outputfileextensions', methods=['POST'])
def fileconverter_outputfileextensions():
    object = flask.request.form.get('object')
    if object is None:
        return flask.make_response({"error_message": "No object sent"}, 400)
    list = functions.ListOutputFileExtensions(object)
    return flask.make_response({"outputfileextensions": list}, 200)

@fileconverter_routes.route('/convertfile', methods=['POST'])
async def fileconverter_convertfile():
    try:
        UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
        object = flask.request.form.get('object')
        file = flask.request.form.get('file')
        filename = flask.request.form.get('filename')
        extension = flask.request.form.get('extension')
        
        if object is None:
            return flask.make_response({"error_message": "No object sent"}, 400)
        elif file is None:
            return flask.make_response({"error_message": "No file sent"}, 400)
        elif filename is None:
            return flask.make_response({"error_message": "No filename sent"}, 400)
        elif extension is None:
            return flask.make_response({"error_message": "No extension sent"}, 400)

        fileDecoded = base64.b64decode(file.split(',')[-1])
        filename = werkzeug.utils.secure_filename(filename)
        filePath = os.path.join(UPLOAD_FOLDER, filename)
        f = open(filePath, "wb") # wb = WriteBinary
        f.write(fileDecoded)
        f.close()
        print("load")
        model = functions.GeodeObjects.ObjectsList()[object]['load'](filePath)
        strictFileName = os.path.splitext(filename)[0]
        newFileName = strictFileName + '.' + extension
        print("save")

        functions.GeodeObjects.ObjectsList()[object]['save'](model, os.path.join(UPLOAD_FOLDER, newFileName))
        return flask.send_from_directory(directory=UPLOAD_FOLDER, path=newFileName, as_attachment=True, mimetype = "application/octet-binary")
    except FileNotFoundError:
        return flask.make_response({"error_message": "File not found"}, 404)
    except RuntimeError as e:
        return flask.make_response({"error_message": str(e)}, 500)
    except Exception as e:
        print("error : ", str(e))
        return flask.make_response({"error_message": str(e)}, 500)
