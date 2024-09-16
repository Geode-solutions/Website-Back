# Standard library imports
import json
import os

# Third party imports
import flask
import flask_cors
from opengeodeweb_back import utils_functions
import werkzeug

import blueprints.tools.blueprint_file_converter as bp_file_converter
import blueprints.tools.blueprint_validity_checker as bp_validity_checker
import blueprints.tools.blueprint_crs_converter as bp_crs_converter


tools_routes = flask.Blueprint("tools_routes", __name__)
flask_cors.CORS(tools_routes)


@tools_routes.before_request
def before_request():
    utils_functions.increment_request_counter(flask.current_app)


@tools_routes.teardown_request
def teardown_request(exception):
    utils_functions.decrement_request_counter(flask.current_app)
    utils_functions.update_last_request_time(flask.current_app)


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
