import shutil
import flask
import flask_cors
import os
import werkzeug
import functions
import zipfile

file_converter_routes = flask.Blueprint("file_converter_routes", __name__)
flask_cors.CORS(file_converter_routes)


@file_converter_routes.before_request
def before_request():
    functions.create_lock_file()


@file_converter_routes.teardown_request
def teardown_request(exception):
    functions.remove_lock_file()
    functions.create_time_file()


@file_converter_routes.route("/versions", methods=["GET"])
def file_converter_versions():
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
    ]

    return flask.make_response({"versions": functions.get_versions(list_packages)}, 200)


@file_converter_routes.route("/allowed_files", methods=["GET"])
def file_converter_allowed_files():
    extensions = functions.list_all_input_extensions()

    return {"status": 200, "extensions": extensions}


@file_converter_routes.route("/allowed_objects", methods=["POST"])
def file_converter_allowed_objects():
    filename = flask.request.form.get("filename")
    if filename is None:
        return flask.make_response({"error_message": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    allowed_objects = functions.list_objects(file_extension)

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@file_converter_routes.route("/output_file_extensions", methods=["POST"])
def file_converter_output_file_extensions():
    geode_object = flask.request.form.get("geode_object")
    if geode_object is None:
        return flask.make_response({"error_message": "No geode_object sent"}, 400)
    list = functions.list_output_file_extensions(geode_object)

    return flask.make_response({"output_file_extensions": list}, 200)


@file_converter_routes.route("/convert_file", methods=["POST"])
async def file_converter_convert_file():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_object = flask.request.form.get("geode_object")
    file = flask.request.form.get("file")
    filename = flask.request.form.get("filename")
    filesize = flask.request.form.get("filesize")
    extension = flask.request.form.get("extension")

    if geode_object is None:
        return flask.make_response(
            {"name": "Bad Request", "description": "No geode_object sent"}, 400
        )
    if file is None:
        return flask.make_response(
            {"name": "Bad Request", "description": "No file sent"}, 400
        )
    if filename is None:
        return flask.make_response(
            {"name": "Bad Request", "description": "No filename sent"}, 400
        )
    if filesize is None:
        return flask.make_response(
            {"name": "Bad Request", "description": "No filesize sent"}, 400
        )
    if extension is None:
        return flask.make_response(
            {"name": "Bad Request", "description": "No extension sent"}, 400
        )

    uploaded_file = functions.upload_file(file, filename, UPLOAD_FOLDER, filesize)
    if not uploaded_file:
        flask.make_response(
            {"name": "Internal Server Error", "description": "File not uploaded"}, 500
        )

    secure_filename = werkzeug.utils.secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename)
    data = functions.geode_objects.objects_list()[geode_object]["load"](file_path)
    strict_file_name = os.path.splitext(secure_filename)[0]
    new_file_name = strict_file_name + "." + extension

    sub_folder = f"{UPLOAD_FOLDER}/{strict_file_name}/"
    if os.path.exists(sub_folder):
        shutil.rmtree(sub_folder)

    functions.geode_objects.objects_list()[geode_object]["save"](
        data, os.path.join(UPLOAD_FOLDER, new_file_name)
    )
    mimetype = "application/octet-binary"

    list_exceptions = ["triangle", "vtm"]
    if extension in list_exceptions:
        if extension == "triangle":
            os.mkdir(sub_folder)
            os.chdir(sub_folder)
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            shutil.move(generated_files + ".ele", sub_folder)
            shutil.move(generated_files + ".neigh", sub_folder)
            shutil.move(generated_files + ".node", sub_folder)
            os.chdir("..")
        elif extension == "vtm":
            generated_files = f"{UPLOAD_FOLDER}/{strict_file_name}"
            shutil.move(generated_files + ".vtm", sub_folder)
            shutil.move(strict_file_name, subFolder)
        new_file_name = strict_file_name + ".zip"
        mimetype = "application/zip"
        with zipfile.ZipFile(f"{UPLOAD_FOLDER}/{new_file_name}", "w") as zipObj:
            for folder_name, sub_folders, file_names in os.walk(sub_folder):
                for filename in file_names:
                    file_path = os.path.join(folder_name, filename)
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
