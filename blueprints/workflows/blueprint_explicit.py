import os
import opengeode as geode
import opengeode_io as og_io
import geode_explicit
import geode_common
import geode_simplex
from opengeodeweb_back import geode_functions, geode_objects
import flask
import flask_cors


explicit_routes = flask.Blueprint("explicit_routes", __name__)
flask_cors.CORS(explicit_routes)


@explicit_routes.route("/get_base_data", methods=["POST"])
def sendBaseData():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    model_A1 = geode_functions.load(
        "BRep", os.path.abspath(WORKFLOWS_DATA_FOLDER + "model_A1.og_brep")
    )
    topo = geode_functions.load(
        "TriangulatedSurface3D",
        os.path.abspath(WORKFLOWS_DATA_FOLDER + "topo_good.og_tsf3d"),
    )

    viewable_1 = geode_functions.save_viewable(
        model_A1, "BRep", os.path.abspath(DATA_FOLDER), "model_A1"
    )
    viewable_2 = geode_functions.save_viewable(
        topo, "TriangulatedSurface3D", os.path.abspath(DATA_FOLDER), "topo"
    )
    return flask.make_response(
        {
            "viewable_1": os.path.basename(viewable_1),
            "id1": "model_A1",
            "viewable_2": os.path.basename(viewable_2),
            "id2": "topo",
        },
        200,
    )


@explicit_routes.route("/get_brep_stats", methods=["POST"])
def sendBRepStats():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    model_A1 = geode_functions.load(
        "BRep", os.path.abspath(WORKFLOWS_DATA_FOLDER + "model_A1.og_brep")
    )
    topo = geode_functions.load(
        "TriangulatedSurface3D",
        os.path.abspath(WORKFLOWS_DATA_FOLDER + "topo_good.og_tsf3d"),
    )
    bbox = model_A1.bounding_box()
    bbox.add_box(topo.bounding_box())
    modeler = geode_explicit.BRepExplicitModeler(bbox)
    for surface in model_A1.surfaces():
        modeler.add_triangulated_surface(surface.triangulated_mesh())
    modeler.add_triangulated_surface(topo)
    brep_explicit = modeler.build()
    geode.filter_brep_components_with_regards_to_blocks(brep_explicit)
    nb_corners = brep_explicit.nb_corners()
    nb_lines = brep_explicit.nb_lines()
    nb_surfaces = brep_explicit.nb_surfaces()
    nb_blocks = brep_explicit.nb_blocks()
    geode_functions.save(
        brep_explicit, "BRep", os.path.abspath(DATA_FOLDER), "explicit_brep.og_brep"
    )
    viewable_file_name = geode_functions.save_viewable(
        brep_explicit, "BRep", os.path.abspath(DATA_FOLDER), "explicit_brep"
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "explicit_brep",
            "nb_corners": nb_corners,
            "nb_lines": nb_lines,
            "nb_surfaces": nb_surfaces,
            "nb_blocks": nb_blocks,
        },
        200,
    )


@explicit_routes.route("/remesh", methods=["POST"])
def remesh():
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = geode_functions.get_form_variables(flask.request.form, ["metric"])
    min_metric = 50
    max_metric = 500
    brep = geode_functions.load(
        "BRep", os.path.abspath(DATA_FOLDER + "explicit_brep.og_brep")
    )
    flask.request.json["metric"]
    brep_metric = geode_common.ConstantMetric3D(metric)
    brep_remeshed, _ = geode_simplex.simplex_remesh_brep(brep, brep_metric)
    viewable_file_name = geode_functions.save_viewable(
        brep_remeshed, "BRep", os.path.abspath(DATA_FOLDER), "remeshed_simplex_brep"
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "remeshed_simplex_brep",
        },
        200,
    )
