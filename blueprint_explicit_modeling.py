import os

import opengeode as geode
import opengeode_io as og_io
import geode_explicit

from opengeodeweb_back import geode_functions, geode_objects


import flask
import flask_cors

import logging
logging.basicConfig(level=logging.INFO)


explicit_modeling_routes = flask.Blueprint('explicit_modeling_routes', __name__)
flask_cors.CORS(explicit_modeling_routes)


@explicit_modeling_routes.before_request
def before_request():
    geode_functions.create_lock_file()

@explicit_modeling_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file()
    geode_functions.create_time_file()

@explicit_modeling_routes.route('/get_brep_stats',methods=['POST'])
def sendBRepStats():
    data_folder = "./data/"
    id1 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(data_folder + 'ID1.og_tsf3d'))
    id2 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(data_folder + 'ID2.og_tsf3d'))
    id3 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(data_folder + 'ID3.og_tsf3d'))
    
    bbox = id1.bounding_box()
    bbox.add_box(id2.bounding_box())
    bbox.add_box(id3.bounding_box())

    modeler = geode_explicit.BRepExplicitModeler(bbox)

    modeler.add_triangulated_surface(id1)
    modeler.add_triangulated_surface(id2)
    modeler.add_triangulated_surface(id3)

    brep_explicit = modeler.build()

    nb_corners = brep_explicit.nb_corners()
    nb_lines = brep_explicit.nb_lines()
    nb_surfaces = brep_explicit.nb_surfaces()
    nb_blocks = brep_explicit.nb_blocks()

    geode_functions.save(brep_explicit, "BRep", os.path.abspath(data_folder), "explicit_brep.og_brep")

    return flask.jsonify(nb_corners=nb_corners, nb_lines=nb_lines, nb_surfaces=nb_surfaces, nb_blocks=nb_blocks)
