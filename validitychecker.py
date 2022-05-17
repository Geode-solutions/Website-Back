import flask
import flask_cors
import os
import base64
import functions
import GeodeObjects
import InspectorFunctions
import werkzeug
import pkg_resources

validitychecker_routes = flask.Blueprint('validitychecker_routes', __name__)
flask_cors.CORS(validitychecker_routes)

@validitychecker_routes.route('/versions', methods=['GET'])
def validitychecker_versions():
    list_packages = ['OpenGeode-core', 'OpenGeode-IO', 'OpenGeode-Geosciences', 'OpenGeode-GeosciencesIO', 'OpenGeode-Inspector']
    list_with_versions = []
    for package in list_packages:
        list_with_versions.append({"package": package, "version": pkg_resources.get_distribution(package).version})
    return flask.make_response({"versions": list_with_versions}, 200)

@validitychecker_routes.route('/allowedfiles', methods=['GET'])
def vaditychecker_allowedfiles():
    extensions = functions.ListAllInputExtensions()
    return {"status": 200, "extensions": extensions}

@validitychecker_routes.route('/allowedobjects', methods=['POST'])
def validitychecker_allowedobjects():
    filename = flask.request.form.get('filename')
    if filename is None:
        return flask.make_response({"error_message": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    objects = functions.ListObjects(file_extension)
    return flask.make_response({"objects": objects}, 200)

@validitychecker_routes.route('/testnames', methods=['POST'])
def vaditychecker_testnames():
    try:
        object = flask.request.form.get('object')
        if object is None:
            return flask.make_response({"error_message": "No object sent"}, 400)

        modelChecks = InspectorFunctions.GetTestNames()[object]
        print(modelChecks)
        return flask.make_response({"modelChecks": modelChecks}, 200)

    except Exception as e:
        print("error : ", str(e))
        return flask.make_response({"error_message": str(e)}, 500)

@validitychecker_routes.route('/inspectfile/<string:object>/<string:test_type>/<string:test_name>', methods=['POST'])
def vaditychecker_inspectfile(object:str, test_type:str, test_name:str):
    try:
        Result = InspectorFunctions.GetTestResult(object, test_type, test_name)
        return flask.make_response({"Result": Result}, 200)

        # UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
        # object = flask.request.form.get('object')
        # file = flask.request.form.get('file')
        # filename = flask.request.form.get('filename')
        
        # if object is None:
        #     return flask.make_response({"error_message": "No object sent"}, 400)
        # elif file is None:
        #     return flask.make_response({"error_message": "No file sent"}, 400)
        # elif filename is None:
        #     return flask.make_response({"error_message": "No filename sent"}, 400)
        # fileDecoded = base64.b64decode(file.split(',')[-1])
        # filename = werkzeug.utils.secure_filename(filename)
        # filePath = os.path.join(UPLOAD_FOLDER, filename)
        # f = open(filePath, "wb")
        # f.write(fileDecoded)
        # f.close()
        # model = GeodeObjects.ObjectsList()[object]['load'](filePath)
        # modelIsValid = GeodeObjects_2.ObjectsList(model)[object]['"is_valid"']()
        # modelIsValid = inspector.EdgedCurveColocation3D(model).mesh_has_colocated_points()
        # inspectorResults = inspector.EdgedCurveColocation3D(model).colocated_points_groups()
        # print(modelIsValid)
        # print(inspectorResults)
        # inspectorResults = GeodeObjects_2.ObjectsList(model)[object]['inspect']
        # "inspectorResults": inspectorResults

        # return flask.make_response({"modelChecks": modelChecks}, 200)
        # return flask.make_response({"message": "Okay"}, 200)

    except RuntimeError as e:
        print("error : ", str(e))
        return flask.make_response({"error_message": str(e)}, 500)
    except Exception as e:
        print("error : ", str(e))
        return flask.make_response({"error_message": str(e)}, 500)