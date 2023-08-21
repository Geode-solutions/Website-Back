import os
import opengeode as geode
import opengeode_io as og_io
import geode_explicit
from opengeodeweb_back import geode_functions, geode_objects
import flask
import flask_cors


explicit_routes = flask.Blueprint('explicit_routes', __name__)
flask_cors.CORS(explicit_routes)


@explicit_routes.route('/get_brep_stats',methods=['POST'])
def sendBRepStats():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    id1 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(WORKFLOWS_DATA_FOLDER + '/ID1.og_tsf3d'))
    id2 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(WORKFLOWS_DATA_FOLDER + '/ID2.og_tsf3d'))
    id3 = geode_functions.load("TriangulatedSurface3D", os.path.abspath(WORKFLOWS_DATA_FOLDER + '/ID3.og_tsf3d'))
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
    geode_functions.save(brep_explicit, "BRep", os.path.abspath(DATA_FOLDER), "/explicit_brep.og_brep")
    return flask.make_response(flask.jsonify({'nb_corners':nb_corners, 'nb_lines':nb_lines, 'nb_surfaces':nb_surfaces, 'nb_blocks':nb_blocks }), 200)
