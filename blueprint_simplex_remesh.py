import re

import opengeode as geode
import opengeode_io as og_io
import opengeode_geosciences as og_geosciences
import geode_numerics as geode_num
import geode_implicit as geode_imp
import geode_simplex as geode_simp
import geode_common

import flask
import flask_cors

import logging
logging.basicConfig(level=logging.INFO)


simplex_remesh_routes = flask.Blueprint('simplex_remesh_routes', __name__)
flask_cors.CORS(simplex_remesh_routes)
@simplex_remesh_routes.route('/',methods=['POST'])
def sendBRep():
    output_folder = "./data/"
    brep = geode.load_brep(output_folder + "corbi.og_brep")

    surfacesID = []
    for surface in brep.surfaces():
        surfacesID.append(surface.id().string())
    blocksID = []
    for block in brep.blocks():
        blocksID.append(block.id().string())

    return flask.jsonify(surfacesIDS=surfacesID, blocksIDS=blocksID)




@simplex_remesh_routes.route('/remesh',methods=['POST'])
def remesh():
    globalMetric = flask.request.form.get("globalMetric")
    surfaceMetrics = eval(flask.request.form.get("surfaceMetrics"))
    blockMetrics = eval(flask.request.form.get("blockMetrics"))
    output_folder = "./data/"

    brep_input = geode.load_brep(output_folder + "corbi.og_brep")
    brep_metric = geode_simp.BRepMetricConstraints(brep_input)

    #modifying individual surface metrics 

    if (globalMetric != "undefined") and (10 <= float(globalMetric) <= 300):
        brep_metric.set_default_metric(float(globalMetric))
    elif globalMetric == "undefined":
        brep_metric.set_default_metric(50.0)  #better to set BRep current metric maybe
    else:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong metric value, should be between 10 and 300' }, 400)

    for id in list(surfaceMetrics.keys()):
        tmp_surface = brep_input.surface(geode.uuid(id))
        brep_metric.set_surface_metric(tmp_surface,float(surfaceMetrics[id]))
    for id in list(blockMetrics.keys()):
        tmp_block = brep_input.block(geode.uuid(id))
        brep_metric.set_block_metric(tmp_block,float(blockMetrics[id]))
    
    metric = brep_metric.build_metric()

    brep_remeshed,_ = geode_simp.simplex_remesh_brep(brep_input, metric)


    # saving objects
    geode.save_brep(brep_remeshed,output_folder + 'remeshed_corbi.vtm')

    return flask.make_response({'simplexRemeshSuccessful': "yes" }, 200)
