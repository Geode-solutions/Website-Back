import os
import opengeode as geode
import opengeode_io as og_io
import geode_simplex
from opengeodeweb_back import geode_functions, utils_functions
import flask
import flask_cors
import json

with open("blueprints/workflows/simplex_initialize.json", "r") as file:
    simplex_initialize_json = json.load(file)

with open("blueprints/workflows/simplex_remesh.json", "r") as file:
    simplex_remesh_json = json.load(file)

simplex_routes = flask.Blueprint("simplex_routes", __name__)
flask_cors.CORS(simplex_routes)

with open("blueprints/workflows/simplex_initialize.json", "r") as file:
    simplex_initialize_json = json.load(file)


@simplex_routes.route(
    simplex_initialize_json["route"], methods=simplex_initialize_json["methods"]
)
def initialize():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    brep = geode_functions.load(
        "StructuralModel", os.path.abspath(WORKFLOWS_DATA_FOLDER + "corbi.og_strm")
    )
    viewable_file_name = geode_functions.save_viewable(
        "BRep", brep, os.path.abspath(DATA_FOLDER), "simplex_brep"
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "simplex_brep",
        },
        200,
    )


with open("blueprints/workflows/simplex_remesh.json", "r") as file:
    simplex_remesh_json = json.load(file)


@simplex_routes.route(
    simplex_remesh_json["route"], methods=simplex_remesh_json["methods"]
)
def remesh():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = utils_functions.validate_request(flask.request, simplex_remesh_json)
    min_metric = 10
    max_metric = 300
    brep = geode_functions.load(
        "StructuralModel", os.path.abspath(WORKFLOWS_DATA_FOLDER + "corbi.og_strm")
    )
    brep_metric = geode_simplex.BRepMetricConstraints(brep)
    metric = float(flask.request.json["metric"])
    if min_metric <= metric <= max_metric:
        brep_metric.set_default_metric(metric)
    else:
        return flask.make_response(
            {
                "name": "Bad Request",
                "description": "Wrong metric value, should be between {min_metric} and {max_metric}",
            },
            400,
        )

    faults_metric = float(flask.request.json["faults_metric"])
    if min_metric <= faults_metric <= max_metric:
        for fault in brep.faults():
            for surface in brep.fault_items(fault):
                brep_metric.set_surface_metric(surface, faults_metric)
    else:
        return flask.make_response(
            {
                "name": "Bad Request",
                "description": "Wrong faults_metric value, should be between {min_metric} and {max_metric}",
            },
            400,
        )

    metric = brep_metric.build_metric()
    brep_remeshed, _ = geode_simplex.brep_simplex_remesh(brep, metric)
    viewable_file_name = geode_functions.save_viewable(
        "BRep", brep_remeshed, os.path.abspath(DATA_FOLDER), "remeshed_simplex_brep"
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "remeshed_simplex_brep",
        },
        200,
    )
