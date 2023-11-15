# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import werkzeug
from opengeodeweb_back import geode_functions, inspector_functions
import json

with open("blueprints/tools/validity_checker_versions.json", "r") as file:
    validity_checker_versions_json = json.load(file)
with open("blueprints/tools/validity_checker_test_names.json", "r") as file:
    validity_checker_test_names_json = json.load(file)
with open("blueprints/tools/validity_checker_inspect_file.json", "r") as file:
    validity_checker_inspect_file_json = json.load(file)

validity_checker_routes = flask.Blueprint("validity_checker_routes", __name__)
flask_cors.CORS(validity_checker_routes)


@validity_checker_routes.route(
    validity_checker_versions_json["route"],
    methods=validity_checker_versions_json["methods"],
)
def validity_checker_versions():
    geode_functions.validate_request(flask.request, validity_checker_versions_json)
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


@validity_checker_routes.route(
    validity_checker_test_names_json["route"],
    methods=validity_checker_test_names_json["methods"],
)
def validity_checker_test_names():
    geode_functions.validate_request(flask.request, validity_checker_test_names_json)
    model_checks = inspector_functions.json_return(
        inspector_functions.inspectors()[flask.request.json["input_geode_object"]][
            "tests_names"
        ]
    )

    return flask.make_response({"model_checks": model_checks}, 200)


@validity_checker_routes.route(
    validity_checker_inspect_file_json["route"],
    methods=validity_checker_inspect_file_json["methods"],
)
def validity_checker_inspect_file():
    geode_functions.validate_request(flask.request, validity_checker_inspect_file_json)
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    secure_filename = werkzeug.utils.secure_filename(flask.request.json["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(flask.request.json["input_geode_object"], file_path)
    inspector = geode_functions.inspector(
        flask.request.json["input_geode_object"], data
    )
    test_result = getattr(inspector, flask.request.json["test"])()

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
        test_name = flask.request.json["test"]
        print(f"Wrong test result: {test_name}", flush=True)

    return flask.make_response(
        {"result": result, "list_invalidities": str(test_result)}, 200
    )
