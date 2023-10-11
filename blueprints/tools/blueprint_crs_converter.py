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
        {"versions": geode_functions.get_versions(list_packages)}, 200
    )


@crs_converter_routes.route("/allowed_files", methods=["GET"])
def crs_converter_allowed_files():
    extensions = geode_functions.list_all_input_extensions()
    return {"status": 200, "extensions": extensions}


@crs_converter_routes.route("/allowed_objects", methods=["POST"])
def crs_converter_allowed_objects():
    array_variables = ["filename"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    print(variables_dict["filename"])
    file_extension = os.path.splitext(variables_dict["filename"])[1][1:]
    allowed_objects = geode_functions.list_objects(file_extension)

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@crs_converter_routes.route("/geographic_coordinate_systems", methods=["POST"])
def crs_converter_geographic_coordinate_systems():
    array_variables = ["geode_object"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    infos = geode_functions.get_geographic_coordinate_systems(
        variables_dict["geode_object"]
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
def crs_converter_output_file_extensions():
    array_variables = ["geode_object"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    output_file_extensions = geode_functions.list_output_file_extensions(
        variables_dict["geode_object"]
    )

    return flask.make_response({"output_file_extensions": output_file_extensions}, 200)


@crs_converter_routes.route("/convert_file", methods=["POST"])
async def crs_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    array_variables = [
        "geode_object",
        "file",
        "filename",
        "filesize",
        "input_crs_authority",
        "input_crs_code",
        "input_crs_name",
        "output_crs_authority",
        "output_crs_code",
        "output_crs_name",
        "extension",
    ]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )

    input_crs = {
        "authority": variables_dict["input_crs_authority"],
        "code": variables_dict["input_crs_code"],
        "name": variables_dict["input_crs_name"],
    }

    output_crs = {
        "authority": variables_dict["output_crs_authority"],
        "code": variables_dict["output_crs_code"],
        "name": variables_dict["output_crs_name"],
    }

    geode_functions.upload_file(
        variables_dict["file"],
        variables_dict["filename"],
        UPLOAD_FOLDER,
        variables_dict["filesize"],
    )

    secure_filename = werkzeug.utils.secure_filename(variables_dict["filename"])
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, secure_filename))
    data = geode_functions.load(variables_dict["geode_object"], file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + "." + variables_dict["extension"]

    geode_functions.assign_geographic_coordinate_system_info(
        variables_dict["geode_object"], data, input_crs
    )
    geode_functions.convert_geographic_coordinate_system_info(
        variables_dict["geode_object"], data, output_crs
    )

    geode_functions.save(
        data,
        variables_dict["geode_object"],
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
