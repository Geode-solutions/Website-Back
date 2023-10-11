import flask
import flask_cors
import os
import functions
import geode_objects
import inspector_functions
import werkzeug

validity_checker_routes = flask.Blueprint("validity_checker_routes", __name__)
flask_cors.CORS(validity_checker_routes)


@validity_checker_routes.before_request
def before_request():
    functions.create_lock_file()


@validity_checker_routes.teardown_request
def teardown_request(exception):
    functions.remove_lock_file()
    functions.create_time_file()


@validity_checker_routes.route("/versions", methods=["GET"])
def validity_checker_versions():
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
    ]

    return flask.make_response({"versions": functions.get_versions(list_packages)}, 200)


@validity_checker_routes.route("/allowed_files", methods=["GET"])
def validity_checker_allowed_files():
    extensions = functions.list_all_input_extensions()

    return flask.make_response({"extensions": extensions}, 200)


@validity_checker_routes.route("/allowed_objects", methods=["POST"])
def validity_checker_allowed_objects():
    filename = flask.request.form.get("filename")
    if filename is None:
        return flask.make_response({"description": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    allowed_objects = functions.list_objects(file_extension)

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@validity_checker_routes.route("/upload_file", methods=["POST"])
def validity_checker_upload_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    file = flask.request.form.get("file")
    filename = flask.request.form.get("filename")
    filesize = flask.request.form.get("filesize")
    if file is None:
        return flask.make_response({"description": "No file sent"}, 400)
    if filename is None:
        return flask.make_response({"description": "No filename sent"}, 400)
    if filesize is None:
        return flask.make_response({"description": "No filesize sent"}, 400)

    uploadedFile = functions.upload_file(file, filename, UPLOAD_FOLDER, filesize)
    if not uploadedFile:
        flask.make_response({"description": "File not uploaded"}, 500)

    return flask.make_response({"message": "File uploaded"}, 200)


@validity_checker_routes.route("/tests_names", methods=["POST"])
def validity_checker_test_names():
    geode_object = flask.request.form.get("geode_object")
    if geode_object is None:
        return flask.make_response({"description": "No geode_object sent"}, 400)
    model_checks = inspector_functions.json_return(
        inspector_functions.inspectors()[geode_object]["tests_names"]
    )

    return flask.make_response({"model_checks": model_checks}, 200)


@validity_checker_routes.route("/inspect_file", methods=["POST"])
def validity_checker_inspect_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_object = flask.request.form.get("geode_object")
    filename = flask.request.form.get("filename")
    test = flask.request.form.get("test")

    if geode_object is None:
        return flask.make_response({"error_message": "No geode_object sent"}, 400)
    if filename is None:
        return flask.make_response({"error_message": "No filename sent"}, 400)
    if test is None:
        return flask.make_response({"error_message": "No test sent"}, 400)

    secure_filename = werkzeug.utils.secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename)
    data = geode_objects.objects_list()[geode_object]["load"](file_path)
    inspector = inspector_functions.inspectors()[geode_object]["inspector"](data)
    test_result = getattr(inspector, test)()
    expected_value = inspector_functions.expected_results()[test]

    if test_result != expected_value or type(test_result) != type(expected_value):
        if type(test_result) is list:
            if type(test_result[0]) is tuple:
                temp_test_result = []
                for tuple_item in test_result:
                    temp_list = []
                    for index in range(len(tuple_item)):
                        temp_list.append(tuple_item[index].string())
                    temp_test_result.append(temp_list)
                test_result = temp_test_result
    result = test_result == expected_value and type(test_result) == type(expected_value)

    if result == False:
        print(f"{test=}", flush=True)

    return flask.make_response(
        {"result": result, "list_invalidities": str(test_result)}, 200
    )
