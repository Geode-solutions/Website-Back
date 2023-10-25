# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import werkzeug
from opengeodeweb_back import geode_functions, inspector_functions


validity_checker_routes = flask.Blueprint("validity_checker_routes", __name__)
flask_cors.CORS(validity_checker_routes)


@validity_checker_routes.route("/versions", methods=["GET"])
def validity_checker_versions():
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
    ]

    return flask.make_response(
        {"versions": geode_functions.versions(list_packages)}, 200
    )


@validity_checker_routes.route("/allowed_files", methods=["GET"])
def validity_checker_allowed_files():
    extensions = geode_functions.list_input_extensions("inspector")

    return flask.make_response({"extensions": extensions}, 200)


@validity_checker_routes.route("/allowed_objects", methods=["POST"])
def validity_checker_allowed_objects():
    array_variables = ["filename"]
    variables_dict = geode_functions.form_variables(flask.request.form, array_variables)
    file_extension = os.path.splitext(variables_dict["filename"])[1][1:]
    allowed_objects = geode_functions.list_geode_objects(file_extension, "inspector")

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@validity_checker_routes.route("/missing_files", methods=["POST"])
def validity_checker_missing_files():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    array_variables = ["input_geode_object", "filename"]
    variables_dict = geode_functions.form_variables(flask.request.form, array_variables)

    missing_files = geode_functions.missing_files(
        variables_dict["input_geode_object"],
        os.path.join(UPLOAD_FOLDER, variables_dict["filename"]),
    )
    has_missing_files = missing_files.has_missing_files()
    mandatory_files = missing_files.mandatory_files
    additional_files = missing_files.additional_files

    mandatory_files_list = []
    for mandatory_file in mandatory_files:
        mandatory_files_list.append(os.path.basename(mandatory_file))

    additional_files_list = []
    for additional_file in additional_files:
        additional_files_list.append(os.path.basename(additional_file))

    return flask.make_response(
        {
            "has_missing_files": has_missing_files,
            "mandatory_files": mandatory_files_list,
            "additional_files": additional_files_list,
        },
        200,
    )


@validity_checker_routes.route("/upload_file", methods=["POST"])
def validity_checker_upload_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    array_variables = ["file", "filename", "filesize"]
    variables_dict = geode_functions.form_variables(flask.request.form, array_variables)
    geode_functions.upload_file(
        variables_dict["file"],
        variables_dict["filename"],
        UPLOAD_FOLDER,
        variables_dict["filesize"],
    )

    return flask.make_response({"message": "File uploaded"}, 200)


@validity_checker_routes.route("/tests_names", methods=["POST"])
def validity_checker_test_names():
    array_variables = ["input_geode_object"]
    variables_dict = geode_functions.form_variables(flask.request.form, array_variables)
    model_checks = inspector_functions.json_return(
        inspector_functions.inspectors()[variables_dict["input_geode_object"]][
            "tests_names"
        ]
    )

    return flask.make_response({"model_checks": model_checks}, 200)


@validity_checker_routes.route("/inspect_file", methods=["POST"])
def validity_checker_inspect_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    array_variables = ["input_geode_object", "filename", "test"]
    variables_dict = geode_functions.form_variables(flask.request.form, array_variables)

    secure_filename = werkzeug.utils.secure_filename(variables_dict["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(variables_dict["input_geode_object"], file_path)
    inspector = geode_functions.inspector(variables_dict["input_geode_object"], data)
    test_result = getattr(inspector, variables_dict["test"])()

    if type(test_result) == int:
        expected_result = 0
    elif type(test_result) == list:
        expected_result = []
    elif type(test_result) == dict:
        expected_result = {}

    if test_result != expected_result or type(test_result) != type(expected_result):
        if type(test_result) is list:
            if type(test_result[0]) is tuple:
                temp_test_result = []
                for tuple_item in test_result:
                    temp_list = []
                    for index in range(len(tuple_item)):
                        temp_list.append(tuple_item[index].string())
                    temp_test_result.append(temp_list)
                test_result = temp_test_result
    result = test_result == expected_result and type(test_result) == type(
        expected_result
    )

    if result is False:
        test_name = variables_dict["test"]
        print(f"Wrong test result: {test_name}", flush=True)

    return flask.make_response(
        {"result": result, "list_invalidities": str(test_result)}, 200
    )
