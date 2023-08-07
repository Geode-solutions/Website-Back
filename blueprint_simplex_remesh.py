import os

import opengeode as geode
import opengeode_io as og_io
import geode_simplex as geode_simp
from opengeodeweb_back import geode_functions, geode_objects

import flask
import flask_cors

import logging
logging.basicConfig(level=logging.INFO)


simplex_remesh_routes = flask.Blueprint('simplex_remesh_routes', __name__)
flask_cors.CORS(simplex_remesh_routes)
@simplex_remesh_routes.route('/get_brep_info',methods=['POST'])
def sendBRepInfo():
    data_folder = "./data/"
    brep = geode_functions.load("BRep", os.path.abspath(data_folder + "corbi.og_brep"))

    surfacesID = []
    for surface in brep.surfaces():
        surfacesID.append(surface.id().string())
    blocksID = []
    for block in brep.blocks():
        blocksID.append(block.id().string())

    return flask.jsonify(surfacesIDS=surfacesID, blocksIDS=blocksID)


@simplex_remesh_routes.route('/remesh',methods=['POST'])
def remesh():
    variables = geode_functions.get_form_variables(flask.request.form,['globalMetric','surfaceMetrics','blockMetrics'])
    surfaceMetrics = eval(variables['surfaceMetrics'])
    blockMetrics = eval(variables['blockMetrics'])

    data_folder = "./data/"

    brep = geode_functions.load("BRep", os.path.abspath(data_folder + "corbi.og_brep"))
    brep_metric = geode_simp.BRepMetricConstraints(brep)

    try:
        if (10 <= float(variables['globalMetric']) <= 300):
            brep_metric.set_default_metric(float(variables['globalMetric']))
        else:
            return flask.make_response({ 'name': 'Bad Request','description': 'Wrong metric value, should be between 10 and 300' }, 400)
    except ValueError:
        flask.abort(400, "Invalid data format for the global metric variable")

    
    try:
        for id in list(surfaceMetrics.keys()):
            tmp_surface = brep.surface(geode.uuid(id))
            brep_metric.set_surface_metric(tmp_surface,float(surfaceMetrics[id]))
        for id in list(blockMetrics.keys()):
            tmp_block = brep.block(geode.uuid(id))
            brep_metric.set_block_metric(tmp_block,float(blockMetrics[id]))
    except ValueError:
        flask.abort(400, "Invalid data format for an individual metric variable")

    metric = brep_metric.build_metric()

    brep_remeshed,_ = geode_simp.simplex_remesh_brep(brep, metric)

    geode_functions.save(brep_remeshed, "BRep", os.path.abspath(data_folder), "remeshed_corbi.vtm")

    return flask.make_response({'simplexRemeshSuccessful': "yes" }, 200)
