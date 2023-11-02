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


@crs_converter_routes.route("/allowed_files", methods=["GET"])
def crs_converter_allowed_files():
    extensions = geode_functions.list_input_extensions("crs")
    return {"status": 200, "extensions": extensions}


@crs_converter_routes.route("/allowed_objects", methods=["POST"])
def crs_converter_allowed_objects():
    geode_functions.validate_request(flask.request, ["filename"])
    file_extension = os.path.splitext(flask.request.json["filename"])[1][1:]
    allowed_objects = geode_functions.list_geode_objects(file_extension, "crs")

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@crs_converter_routes.route("/geographic_coordinate_systems", methods=["POST"])
def crs_converter_geographic_coordinate_systems():
    geode_functions.validate_request(flask.request, ["geode_object"])
    infos = geode_functions.geographic_coordinate_systems(
        flask.request.json["geode_object"]
    )
    crs_list = []

    for info in infos:
        crs = {}
        crs["name"] = info.name
        crs["code"] = info.code
        crs["authority"] = info.authority
        crs_list.append(crs)

    return flask.make_response({"crs_list": crs_list}, 200)


@crs_converter_routes.route("/output_file_extensions", methods=["POST"])
def crs_converter_output_file_extensiongeode_functionss():
    geode_functions.validate_request(flask.request, ["geode_object"])
    output_file_extensions = geode_functions.geode_object_output_extensions(
        flask.request.json["geode_object"]
    )

    return flask.make_response({"output_file_extensions": output_file_extensions}, 200)


@crs_converter_routes.route("/convert_file", methods=["POST"])
async def crs_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_functions.validate_request(
        flask.request,
        [
            "geode_object",
            "filename",
            "input_crs_authority",
            "input_crs_code",
            "input_crs_name",
            "output_crs_authority",
            "output_crs_code",
            "output_crs_name",
            "extension",
        ],
    )

    input_crs = {
        "authority": flask.request.json["input_crs_authority"],
        "code": flask.request.json["input_crs_code"],
        "name": flask.request.json["input_crs_name"],
    }

    output_crs = {
        "authority": flask.request.json["output_crs_authority"],
        "code": flask.request.json["output_crs_code"],
        "name": flask.request.json["output_crs_name"],
    }

    geode_functions.upload_file(
        flask.request.json["file"],
        flask.request.json["filename"],
        UPLOAD_FOLDER,
        flask.request.json["filesize"],
    )

    secure_filename = werkzeug.utils.secure_filename(flask.request.json["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(flask.request.json["geode_object"], file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + "." + flask.request.json["extension"]

    geode_functions.assign_geographic_coordinate_system_info(
        flask.request.json["geode_object"], data, input_crs
    )
    geode_functions.convert_geographic_coordinate_system_info(
        flask.request.json["geode_object"], data, output_crs
    )

    geode_functions.save(
        flask.request.json["geode_object"],
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
