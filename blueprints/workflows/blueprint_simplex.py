import os
import opengeode as geode
import opengeode_io as og_io
import geode_simplex as geode_simp
from opengeodeweb_back import geode_functions, geode_objects
import flask
import flask_cors


simplex_routes = flask.Blueprint('simplex_routes', __name__)
flask_cors.CORS(simplex_routes)


@simplex_routes.route('/initialize',methods=['POST'])
def initialize():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    brep = geode_functions.load("BRep", os.path.abspath(WORKFLOWS_DATA_FOLDER + "corbi.og_brep"))
    surfacesID = []
    for surface in brep.surfaces():
        surfacesID.append(surface.id().string())
    blocksID = []
    for block in brep.blocks():
        blocksID.append(block.id().string())
    viewable_file_name = geode_functions.save_viewable(brep, "BRep", os.path.abspath(DATA_FOLDER), "simplex_brep")
    return flask.make_response({'viewable_file_name':viewable_file_name[6:], 'id':"simplex_brep", 'surfacesIDS':surfacesID, 'blocksIDS':blocksID }, 200)


@simplex_routes.route('/remesh',methods=['POST'])
def remesh():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = geode_functions.get_form_variables(flask.request.form,['globalMetric','surfaceMetrics','blockMetrics'])
    surfaceMetrics = eval(variables['surfaceMetrics'])
    blockMetrics = eval(variables['blockMetrics'])
    brep = geode_functions.load("BRep", os.path.abspath(WORKFLOWS_DATA_FOLDER + "corbi.og_brep"))
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
    except RuntimeError:
        flask.abort(400, "Invalid ID for an individual metric variable")
    except IndexError:
        flask.abort(400, "Invalid UUID for an individual metric variable")
    metric = brep_metric.build_metric()
    brep_remeshed,_ = geode_simp.simplex_remesh_brep(brep, metric)
    viewable_file_name = geode_functions.save_viewable(brep_remeshed, "BRep", os.path.abspath(DATA_FOLDER), "remeshed_simplex_brep")
    return flask.make_response({'viewable_file_name':viewable_file_name[6:], 'id':"remeshed_simplex_brep"}, 200)
