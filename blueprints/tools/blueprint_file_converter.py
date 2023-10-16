# Standard library imports
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


@file_converter_routes.route("/versions", methods=["GET"])
def file_converter_versions():
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
    ]

    return flask.make_response(
        {"versions": geode_functions.get_versions(list_packages)}, 200
    )


@file_converter_routes.route("/allowed_files", methods=["GET"])
def file_converter_allowed_files():
    extensions = geode_functions.list_input_extensions()
    return {"status": 200, "extensions": extensions}


@file_converter_routes.route("/upload_file", methods=["POST"])
def validity_checker_upload_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    array_variables = ["file", "filename", "filesize"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    geode_functions.upload_file(
        variables_dict["file"],
        variables_dict["filename"],
        UPLOAD_FOLDER,
        variables_dict["filesize"],
    )

    return flask.make_response({"message": "File uploaded"}, 200)


@file_converter_routes.route("/allowed_objects", methods=["POST"])
def file_converter_allowed_objects():
    array_variables = ["filename"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    file_extension = os.path.splitext(variables_dict["filename"])[1][1:]
    allowed_objects = geode_functions.list_geode_objects(file_extension)

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@file_converter_routes.route("/missing_files", methods=["POST"])
def file_converter_missing_files():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    array_variables = ["geode_object", "filename"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )

    missing_files = geode_functions.missing_files(
        variables_dict["geode_object"],
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


@file_converter_routes.route("/output_file_extensions", methods=["POST"])
def file_converter_output_file_extensions():
    array_variables = ["geode_object"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )
    output_file_extensions = geode_functions.get_geode_object_output_extensions(
        variables_dict["geode_object"]
    )
    return flask.make_response({"output_file_extensions": output_file_extensions}, 200)


@file_converter_routes.route("/convert_file", methods=["POST"])
async def file_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]

    array_variables = ["geode_object", "file", "filename", "filesize", "extension"]
    variables_dict = geode_functions.get_form_variables(
        flask.request.form, array_variables
    )

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

    sub_folder = f"{UPLOAD_FOLDER}/{strict_file_name}/"
    if os.path.exists(sub_folder):
        shutil.rmtree(sub_folder)

    geode_functions.save(
        variables_dict["geode_object"],
        data,
        os.path.abspath(UPLOAD_FOLDER),
        new_file_name,
    )
    mimetype = "application/octet-binary"

    list_exceptions = ["triangle", "vtm"]
    if variables_dict["extension"] in list_exceptions:
        if variables_dict["extension"] == "triangle":
            os.mkdir(sub_folder)
            os.chdir(sub_folder)
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            shutil.move(generated_files + ".ele", sub_folder)
            shutil.move(generated_files + ".neigh", sub_folder)
            shutil.move(generated_files + ".node", sub_folder)
            os.chdir("..")
        elif variables_dict["extension"] == "vtm":
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            print(f"{generated_files=}")
            shutil.move(generated_files + ".vtm", sub_folder)
            # shutil.move(strict_file_name, sub_folder)
        new_file_name = strict_file_name + ".zip"
        print(f"{new_file_name=}")
        mimetype = "application/zip"
        with zipfile.ZipFile(f"{UPLOAD_FOLDER}/{new_file_name}", "w") as zipObj:
            for folder_name, sub_folders, file_names in os.walk(sub_folder):
                for variables_dict["filename"] in file_names:
                    file_path = os.path.join(folder_name, variables_dict["filename"])
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
