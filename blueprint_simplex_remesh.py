import re

import opengeode as geode
import opengeode_io as og_io
import opengeode_geosciences as og_geosciences
import geode_numerics as geode_num
import geode_implicit as geode_imp
import geode_simplex as geode_simp
from opengeodeweb_back import geode_functions, geode_objects

import flask
import flask_cors

import logging
logging.basicConfig(level=logging.INFO)


simplex_remesh_routes = flask.Blueprint('simplex_remesh_routes', __name__)
flask_cors.CORS(simplex_remesh_routes)
@simplex_remesh_routes.route('/',methods=['POST'])
def sendBRep():
    data_folder = "/server/data/"
    brep = geode_functions.load("BRep", data_folder + "corbi.og_brep")

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
    variables['surfaceMetrics'] = eval(variables['surfaceMetrics'])
    variables['blockMetrics'] = eval(variables['blockMetrics'])

    data_folder = "/server/data/"

    brep = geode_functions.load("BRep", data_folder + "corbi.og_brep")
    brep_metric = geode_simp.BRepMetricConstraints(brep)

    if (variables['globalMetric'] != "undefined") and (10 <= float(variables['globalMetric']) <= 300):
        brep_metric.set_default_metric(float(variables['globalMetric']))
    elif variables['globalMetric'] == "undefined":
        brep_metric.set_default_metric(50.0)  #better to set BRep current metric maybe
    else:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong metric value, should be between 10 and 300' }, 400)

    

    for id in list(variables['surfaceMetrics'].keys()):
        tmp_surface = brep.surface(geode.uuid(id))
        brep_metric.set_surface_metric(tmp_surface,float(variables['surfaceMetrics'][id]))
    for id in list(variables['blockMetrics'].keys()):
        tmp_block = brep.block(geode.uuid(id))
        brep_metric.set_block_metric(tmp_block,float(variables['blockMetrics'][id]))
    
    metric = brep_metric.build_metric()

    brep_remeshed,_ = geode_simp.simplex_remesh_brep(brep, metric)


    # saving objects
    geode_functions.save(brep_remeshed, "BRep", data_folder, "remeshed_corbi.vtm")

    return flask.make_response({'simplexRemeshSuccessful': "yes" }, 200)
