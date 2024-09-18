# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import json

with open("blueprints/ID_healthcheck.json") as file:
    ID_healthcheck_json = json.load(file)


ID_routes = flask.Blueprint("ID_routes", __name__)
flask_cors.CORS(ID_routes)


@ID_routes.route(ID_healthcheck_json["route"], methods=ID_healthcheck_json["methods"])
def root():
    return flask.make_response({"message": "healthy"}, 200)

