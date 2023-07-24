import re

import opengeode as geode
import opengeode_io as og_io
import opengeode_geosciences as og_geosciences
import geode_numerics as geode_num
import geode_implicit as geode_imp
import geode_simplex as geode_simp
import geode_explicit

import flask
import flask_cors

import logging
logging.basicConfig(level=logging.INFO)


explicit_modeling_routes = flask.Blueprint('explicit_modeling_routes', __name__)
flask_cors.CORS(explicit_modeling_routes)
@explicit_modeling_routes.route('/',methods=['POST'])
def sendBRepStats():
    data_folder = "./data/"
    id1 = geode.load_triangulated_surface3D(data_folder + 'ID1.og_tsf3d')
    id2 = geode.load_triangulated_surface3D(data_folder + 'ID2.og_tsf3d')
    id3 = geode.load_triangulated_surface3D(data_folder + 'ID3.og_tsf3d')

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

    geode.save_brep(brep_explicit,data_folder + 'explicit_brep.og_brep')

    return flask.jsonify(nb_corners=nb_corners, nb_lines=nb_lines, nb_surfaces=nb_surfaces, nb_blocks=nb_blocks)
