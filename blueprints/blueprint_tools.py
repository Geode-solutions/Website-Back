import os
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


@tools_routes.route("/allowed_files", methods=["POST"])
def allowed_files():
    geode_functions.validate_request(flask.request, ["key"])
    extensions = geode_functions.list_input_extensions(flask.request.json["key"])
    return {"status": 200, "extensions": extensions}


@tools_routes.route("/upload_file", methods=["OPTIONS", "PUT"])
def upload_file():
    if flask.request.method == "OPTIONS":
        return flask.make_response({}, 200)

    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    files = flask.request.files.getlist("content")

    for file in files:
        filename = werkzeug.utils.secure_filename(os.path.basename(file.filename))
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    return flask.make_response({"message": "File uploaded"}, 201)


@tools_routes.route("/allowed_objects", methods=["POST"])
def allowed_objects():
    geode_functions.validate_request(flask.request, ["filename", "key"])
    file_extension = os.path.splitext(flask.request.json["filename"])[1][1:]
    allowed_objects = geode_functions.list_geode_objects(
        file_extension, flask.request.json["key"]
    )

    return flask.make_response({"allowed_objects": allowed_objects}, 200)


@tools_routes.route("/missing_files", methods=["POST"])
def missing_files():
    UPLOAD_FOLDER = flask.current_app.config["UPLOAD_FOLDER"]
    geode_functions.validate_request(flask.request, ["input_geode_object", "filename"])

    missing_files = geode_functions.missing_files(
        flask.request.json["input_geode_object"],
        os.path.join(UPLOAD_FOLDER, flask.request.json["filename"]),
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


@tools_routes.route("/geode_objects_and_output_extensions", methods=["POST"])
def geode_objects_and_output_extensions():
    geode_functions.validate_request(flask.request, ["input_geode_object"])
    geode_objects_output_extensions = geode_functions.geode_objects_output_extensions(
        flask.request.json["input_geode_object"]
    )
    geode_objects_and_output_extensions = (
        geode_functions.geode_objects_output_extensions(
            flask.request.json["input_geode_object"]
        )
    )

    return flask.make_response(
        {"geode_objects_and_output_extensions": geode_objects_and_output_extensions},
        200,
    )
