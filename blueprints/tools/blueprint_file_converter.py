# Standard library imports
import json
import os
import shutil
import zipfile

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

    sub_folder = f"{UPLOAD_FOLDER}/{strict_file_name}/"
    if os.path.exists(sub_folder):
        shutil.rmtree(sub_folder)

    geode_functions.save(
        flask.request.json["output_geode_object"],
        data,
        os.path.abspath(UPLOAD_FOLDER),
        new_file_name,
    )
    mimetype = "application/octet-binary"

    list_exceptions = ["triangle", "vtm"]
    if flask.request.json["output_extension"] in list_exceptions:
        if flask.request.json["output_extension"] == "triangle":
            os.mkdir(sub_folder)
            os.chdir(sub_folder)
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            shutil.move(generated_files + ".ele", sub_folder)
            shutil.move(generated_files + ".neigh", sub_folder)
            shutil.move(generated_files + ".node", sub_folder)
            os.chdir("..")
        elif flask.request.json["output_extension"] == "vtm":
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            shutil.move(generated_files + ".vtm", sub_folder)
        new_file_name = strict_file_name + ".zip"
        mimetype = "application/zip"
        with zipfile.ZipFile(f"{UPLOAD_FOLDER}/{new_file_name}", "w") as zipObj:
            for folder_name, sub_folders, file_names in os.walk(sub_folder):
                for flask.request.json["filename"] in file_names:
                    file_path = os.path.join(
                        folder_name, flask.request.json["filename"]
                    )
                    zipObj.write(file_path, os.path.basename(file_path))

    response = flask.send_from_directory(
        directory=UPLOAD_FOLDER,
        path=new_file_name,
        as_attachment=True,
        mimetype=mimetype,
    )
    response.headers["new-file-name"] = new_file_name
    response.headers["Access-Control-Expose-Headers"] = "new-file-name"

    return response
