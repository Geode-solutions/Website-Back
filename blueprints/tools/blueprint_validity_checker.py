# Standard library imports
#

# Third party imports
import flask
import flask_cors
from opengeodeweb_back import geode_functions, utils_functions
import json

validity_checker_routes = flask.Blueprint("validity_checker_routes", __name__)
flask_cors.CORS(validity_checker_routes)


with open("blueprints/tools/validity_checker_versions.json", "r") as file:
    validity_checker_versions_json = json.load(file)


@validity_checker_routes.route(
    validity_checker_versions_json["route"],
    methods=validity_checker_versions_json["methods"],
)
def validity_checker_versions():
    utils_functions.validate_request(flask.request, validity_checker_versions_json)
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
    ]
    return flask.make_response(
        {"versions": utils_functions.versions(list_packages)}, 200
    )
