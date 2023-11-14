# Standard library imports
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


@crs_converter_routes.route("/versions", methods=["GET"])
def crs_converter_versions():
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
    ]
    return flask.make_response(
        {"versions": geode_functions.versions(list_packages)}, 200
    )


@crs_converter_routes.route("/geographic_coordinate_systems", methods=["POST"])
def crs_converter_geographic_coordinate_systems():
    geode_functions.validate_request(flask.request, ["input_geode_object"])
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


@crs_converter_routes.route("/convert_file", methods=["POST"])
async def crs_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_functions.validate_request(
        flask.request,
        [
            "input_geode_object",
            "filename",
            "input_crs",
            "output_crs",
            "output_geode_object",
            "output_extension",
        ],
    )

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
