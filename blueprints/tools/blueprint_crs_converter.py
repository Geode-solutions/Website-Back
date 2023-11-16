# Standard library imports
import json
import os
import shutil
import uuid
import zipfile

# Third party imports
import flask
import flask_cors
import werkzeug
from opengeodeweb_back import geode_functions

crs_converter_routes = flask.Blueprint("crs_converter_routes", __name__)
flask_cors.CORS(crs_converter_routes)


with open("blueprints/tools/crs_converter_versions.json", "r") as file:
    crs_converter_versions_json = json.load(file)


@crs_converter_routes.route(
    crs_converter_versions_json["route"], methods=crs_converter_versions_json["methods"]
)
def crs_converter_versions():
    geode_functions.validate_request(flask.request, crs_converter_versions_json)
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
    ]
    return flask.make_response(
        {"versions": geode_functions.versions(list_packages)}, 200
    )


with open("blueprints/tools/crs_converter_convert_file.json", "r") as file:
    crs_converter_convert_file_json = json.load(file)


@crs_converter_routes.route(
    crs_converter_convert_file_json["route"],
    methods=crs_converter_convert_file_json["methods"],
)
async def crs_converter_convert_file():
    geode_functions.validate_request(
        flask.request,
        crs_converter_convert_file_json,
    )
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    secure_filename = werkzeug.utils.secure_filename(flask.request.json["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(flask.request.json["input_geode_object"], file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + "." + flask.request.json["output_extension"]

    geode_functions.assign_geographic_coordinate_system_info(
        flask.request.json["input_geode_object"], data, flask.request.json["input_crs"]
    )
    geode_functions.convert_geographic_coordinate_system_info(
        flask.request.json["input_geode_object"], data, flask.request.json["output_crs"]
    )

    geode_functions.save(
        flask.request.json["output_geode_object"],
        data,
        os.path.abspath(UPLOAD_FOLDER),
        new_file_name,
    )
    response = flask.send_from_directory(
        directory=UPLOAD_FOLDER,
        path=new_file_name,
        as_attachment=True,
        mimetype="application/octet-binary",
    )
    response.headers["new-file-name"] = new_file_name
    response.headers["Access-Control-Expose-Headers"] = "new-file-name"

    return response
