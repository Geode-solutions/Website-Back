# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import json

with open("blueprints/ID_healthcheck.json") as file:
    ID_healthcheck_json = json.load(file)

with open("blueprints/ID_ping.json") as file:
    ID_ping_json = json.load(file)

ID_routes = flask.Blueprint("ID_routes", __name__)
flask_cors.CORS(ID_routes)


@ID_routes.route(ID_healthcheck_json["route"], methods=ID_healthcheck_json["methods"])
def root():
    return flask.make_response({"message": "healthy"}, 200)


@ID_routes.route(ID_ping_json["route"], methods=ID_ping_json["methods"])
def ping():
    LOCK_FOLDER = flask.current_app.config["LOCK_FOLDER"]
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    if not os.path.isfile(LOCK_FOLDER + "/ping.txt"):
        f = open(LOCK_FOLDER + "/ping.txt", "a")
        f.close()
    return flask.make_response({"message": "Flask server is running"}, 200)
