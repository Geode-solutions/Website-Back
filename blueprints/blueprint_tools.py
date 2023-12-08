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


tools_routes = flask.Blueprint("tools_routes", __name__)
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
    file = flask.request.files["file"]
    filename = werkzeug.utils.secure_filename(os.path.basename(file.filename))
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
    file_extension = os.path.splitext(flask.request.json["filename"])[1][1:]
    allowed_objects = geode_functions.list_geode_objects(
        file_extension, flask.request.json["key"]
    )
    print(f"{allowed_objects=}")
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

    missing_files = geode_functions.missing_files(
        flask.request.json["input_geode_object"],
        os.path.join(UPLOAD_FOLDER, flask.request.json["filename"]),
    )
    has_missing_files = missing_files.has_missing_files()

    mandatory_files = []
    for mandatory_file in missing_files.mandatory_files:
        mandatory_files.append(os.path.basename(mandatory_file))

    additional_files = []
    for additional_file in missing_files.additional_files:
        additional_files.append(os.path.basename(additional_file))

    return flask.make_response(
        {
            "has_missing_files": has_missing_files,
            "mandatory_files": mandatory_files,
            "additional_files": additional_files,
        },
        200,
    )


with open("blueprints/tools_geographic_coordinate_systems.json", "r") as file:
    tools_geographic_coordinate_systems_json = json.load(file)


@tools_routes.route(
    tools_geographic_coordinate_systems_json["route"],
    methods=tools_geographic_coordinate_systems_json["methods"],
)
def geographic_coordinate_systems():
    geode_functions.validate_request(
        flask.request, tools_geographic_coordinate_systems_json
    )
    infos = geode_functions.geographic_coordinate_systems(
        flask.request.json["input_geode_object"]
    )
    crs_list = []

    for info in infos:
        crs = {}
        crs["name"] = info.name
        crs["code"] = info.code
        crs["authority"] = info.authority
        crs_list.append(crs)

    return flask.make_response({"crs_list": crs_list}, 200)


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
    data = geode_functions.load(
        flask.request.json["input_geode_object"],
        os.path.join(UPLOAD_FOLDER, flask.request.json["filename"]),
    )
    geode_objects_and_output_extensions = (
        geode_functions.geode_objects_output_extensions(
            flask.request.json["input_geode_object"], data
        )
    )

    return flask.make_response(
        {"geode_objects_and_output_extensions": geode_objects_and_output_extensions},
        200,
    )
