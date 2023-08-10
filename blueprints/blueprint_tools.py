import os
import flask
import flask_cors
from opengeodeweb_back import geode_functions, geode_objects

import tools.blueprint_file_converter as bp_file_converter
import tools.blueprint_validity_checker as bp_validity_checker
import tools.blueprint_crs_converter as bp_crs_converter

tools_routes = flask.Blueprint('crs_converter_routes', __name__)
flask_cors.CORS(tools_routes)


@tools_routes.before_request
def before_request():
    geode_functions.create_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))

@tools_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))
    geode_functions.create_time_file(os.path.abspath(flask.current_app.config["TIME_FOLDER"]))


tools_routes.register_blueprint(bp_file_converter.file_converter_routes, url_prefix='/file_converter')
tools_routes.register_blueprint(bp_validity_checker.validity_checker_routes, url_prefix='/validity_checker')
tools_routes.register_blueprint(bp_crs_converter.crs_converter_routes, url_prefix='/crs_converter')
