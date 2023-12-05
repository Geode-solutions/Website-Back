# Standard library imports
import json
import os

# Third party imports
import flask
import flask_cors
from opengeodeweb_back import geode_functions, geode_objects
import werkzeug

import blueprints.tools.blueprint_file_converter as bp_file_converter
import blueprints.tools.blueprint_validity_checker as bp_validity_checker
import blueprints.tools.blueprint_crs_converter as bp_crs_converter


tools_routes = flask.Blueprint("crs_converter_routes", __name__)
flask_cors.CORS(tools_routes)


@tools_routes.before_request
def before_request():
    geode_functions.create_lock_file(
        os.path.abspath(flask.current_app.config["LOCK_FOLDER"])
    )


@tools_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file(
        os.path.abspath(flask.current_app.config["LOCK_FOLDER"])
    )
    geode_functions.create_time_file(
        os.path.abspath(flask.current_app.config["TIME_FOLDER"])
    )


tools_routes.register_blueprint(
    bp_file_converter.file_converter_routes,
    url_prefix="/file_converter",
    name="file_converter_blueprint",
)
tools_routes.register_blueprint(
    bp_validity_checker.validity_checker_routes,
    url_prefix="/validity_checker",
    name="validity_checker_blueprint",
)
tools_routes.register_blueprint(
    bp_crs_converter.crs_converter_routes,
    url_prefix="/crs_converter",
    name="crs_converter_blueprint",
)


with open("blueprints/tools_allowed_files.json", "r") as file:
    tools_allowed_files_json = json.load(file)


@tools_routes.route(
    tools_allowed_files_json["route"],
    methods=tools_allowed_files_json["methods"],
)
def allowed_files():
    geode_functions.validate_request(flask.request, tools_allowed_files_json)
    extensions = geode_functions.list_input_extensions(flask.request.json["key"])
    return {"status": 200, "extensions": extensions}


with open("blueprints/tools_upload_file.json", "r") as file:
    tools_upload_file_json = json.load(file)


@tools_routes.route(
    tools_upload_file_json["route"],
    methods=tools_upload_file_json["methods"],
)
def upload_file():
    if flask.request.method == "OPTIONS":
        return flask.make_response({}, 200)

    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    files = flask.request.files.getlist("content")

    for file in files:
        filename = werkzeug.utils.secure_filename(os.path.basename(file.filename))
        print(f"{filename=}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    return flask.make_response({"message": "File uploaded"}, 201)


with open("blueprints/tools_allowed_objects.json", "r") as file:
    tools_allowed_objects_json = json.load(file)


@tools_routes.route(
    tools_allowed_objects_json["route"],
    methods=tools_allowed_objects_json["methods"],
)
def allowed_objects():
    geode_functions.validate_request(flask.request, tools_allowed_objects_json)
    filenames = flask.request.json["filenames"]
    for index, filename in enumerate(filenames):
        file_extension = os.path.splitext(filename)[1][1:]
        filename_allowed_objects = geode_functions.list_geode_objects(
            file_extension, flask.request.json["key"]
        )
        if index == 0:
            allowed_objects = filename_allowed_objects
        else:
            allowed_objects = list(set(allowed_objects) & set(filename_allowed_objects))

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


with open("blueprints/tools_missing_files.json", "r") as file:
    tools_missing_files_json = json.load(file)


@tools_routes.route(
    tools_missing_files_json["route"],
    methods=tools_missing_files_json["methods"],
)
def missing_files():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_functions.validate_request(flask.request, tools_missing_files_json)

    filenames = flask.request.json["filenames"]
    has_missing_files = False
    mandatory_files_list = []
    additional_files_list = []

    for index, filename in enumerate(filenames):
        file_missing_files = geode_functions.missing_files(
            flask.request.json["input_geode_object"],
            os.path.join(UPLOAD_FOLDER, filename),
        )
        file_has_missing_files = file_missing_files.has_missing_files()
        file_mandatory_files = file_missing_files.mandatory_files
        file_additional_files = file_missing_files.additional_files

        if file_has_missing_files:
            has_missing_files = True

        for mandatory_file in file_mandatory_files:
            mandatory_files_list.append(os.path.basename(mandatory_file))

        for additional_file in file_additional_files:
            additional_files_list.append(os.path.basename(additional_file))

    return flask.make_response(
        {
            "has_missing_files": has_missing_files,
            "mandatory_files": mandatory_files_list,
            "additional_files": additional_files_list,
        },
        200,
    )


with open("blueprints/tools_geode_objects_and_output_extensions.json", "r") as file:
    tools_geode_objects_and_output_extensions_json = json.load(file)


@tools_routes.route(
    tools_geode_objects_and_output_extensions_json["route"],
    methods=tools_geode_objects_and_output_extensions_json["methods"],
)
def geode_objects_and_output_extensions():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    geode_functions.validate_request(
        flask.request, tools_geode_objects_and_output_extensions_json
    )

    filenames = flask.request.json["filenames"]
    input_geode_object = flask.request.json["input_geode_object"]
    geode_objects_and_output_extensions = {}

    print(f"{ flask.request.json=}")
    for index, filename in enumerate(filenames):
        data = geode_functions.load(
            input_geode_object, os.path.join(UPLOAD_FOLDER, filename)
        )
        file_geode_objects_and_output_extensions = (
            geode_functions.geode_objects_output_extensions(input_geode_object, data)
        )
        print(f"{file_geode_objects_and_output_extensions=}")

        if index == 0:
            geode_objects_and_output_extensions = (
                file_geode_objects_and_output_extensions
            )
        else:
            for geode_object, value in file_geode_objects_and_output_extensions:
                for output_extension in value:
                    if not output_extension.is_saveable:
                        geode_objects_and_output_extensions[geode_object][
                            output_extension
                        ]["is_saveable"] = False

    print(geode_objects_and_output_extensions)
    return flask.make_response(
        {"geode_objects_and_output_extensions": geode_objects_and_output_extensions},
        200,
    )
