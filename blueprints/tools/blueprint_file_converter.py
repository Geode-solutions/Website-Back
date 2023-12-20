# Standard library imports
import json
import os

# Third party imports
import flask
import flask_cors
import werkzeug
from opengeodeweb_back import geode_functions

file_converter_routes = flask.Blueprint("file_converter_routes", __name__)
flask_cors.CORS(file_converter_routes)


with open("blueprints/tools/file_converter_versions.json", "r") as file:
    file_converter_versions_json = json.load(file)


@file_converter_routes.route(
    file_converter_versions_json["route"],
    methods=file_converter_versions_json["methods"],
)
def file_converter_versions():
    geode_functions.validate_request(flask.request, file_converter_versions_json)
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
    ]

    return flask.make_response(
        {"versions": geode_functions.versions(list_packages)}, 200
    )


with open("blueprints/tools/file_converter_convert_file.json", "r") as file:
    file_converter_convert_file_json = json.load(file)


@file_converter_routes.route(
    file_converter_convert_file_json["route"],
    methods=file_converter_convert_file_json["methods"],
)
async def file_converter_convert_file():
    geode_functions.validate_request(flask.request, file_converter_convert_file_json)
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    secure_filename = werkzeug.utils.secure_filename(flask.request.json["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(flask.request.json["input_geode_object"], file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + "." + flask.request.json["output_extension"]

    saved_files = geode_functions.save(
        flask.request.json["output_geode_object"],
        data,
        os.path.abspath(UPLOAD_FOLDER),
        new_file_name,
    )
    return geode_functions.send_file(UPLOAD_FOLDER, saved_files, new_file_name)
