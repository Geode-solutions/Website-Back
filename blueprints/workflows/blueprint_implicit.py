import os
import json
import flask
import flask_cors
import opengeode as og
import opengeode_io as og_io
import opengeode_geosciences as og_geosciences
import geode_common
import geode_numerics
import geode_implicit
import geode_simplex
from opengeodeweb_back import geode_functions, geode_objects

implicit_routes = flask.Blueprint("implicit_routes", __name__)
flask_cors.CORS(implicit_routes)


@implicit_routes.route("/step0", methods=["POST"])
def step0():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    constraints = "["
    data_constraints = geode_numerics.DataPointsManager3D()
    constraint_file = (
        WORKFLOWS_DATA_FOLDER + "3DBenchmark_implicit_data_constraints.og_pts3d"
    )
    data_constraints.load_data_points(constraint_file)
    for i in range(data_constraints.nb_data_points()):
        constraint = []
        point = data_constraints.data_point_position(i).string().split(" ")
        constraint.append(float(point[0]))
        constraint.append(float(point[1]))
        constraint.append(float(point[2]))
        constraint.append(data_constraints.data_point_value(i))
        constraints += str(constraint) + ","
    constraints = constraints[: len(constraints) - 1] + "]"
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    data_constraints.save_data_points_manager(
        os.path.join(os.path.abspath(DATA_FOLDER), "implicit_points.vtp")
    )
    curve = og.EdgedCurve3D.create()
    curve_builder = og.EdgedCurveBuilder3D.create(curve)
    pts_value = 40
    curve_builder.create_point(og.Point3D([0.0, 0.0, 0.0]))
    curve_builder.create_point(og.Point3D([pts_value, 0.0, 0.0]))
    curve_builder.create_point(og.Point3D([pts_value, pts_value, 0.0]))
    curve_builder.create_point(og.Point3D([0.0, pts_value, 0.0]))
    curve_builder.create_point(og.Point3D([0.0, 0.0, pts_value]))
    curve_builder.create_point(og.Point3D([pts_value, 0.0, pts_value]))
    curve_builder.create_point(og.Point3D([pts_value, pts_value, pts_value]))
    curve_builder.create_point(og.Point3D([0.0, pts_value, pts_value]))
    curve_builder.create_edge_with_vertices(0, 1)
    curve_builder.create_edge_with_vertices(1, 2)
    curve_builder.create_edge_with_vertices(2, 3)
    curve_builder.create_edge_with_vertices(3, 0)
    curve_builder.create_edge_with_vertices(4, 5)
    curve_builder.create_edge_with_vertices(5, 6)
    curve_builder.create_edge_with_vertices(6, 7)
    curve_builder.create_edge_with_vertices(7, 4)
    curve_builder.create_edge_with_vertices(0, 4)
    curve_builder.create_edge_with_vertices(1, 5)
    curve_builder.create_edge_with_vertices(2, 6)
    curve_builder.create_edge_with_vertices(3, 7)
    og.save_edged_curve3D(
        curve, os.path.join(os.path.abspath(DATA_FOLDER), "implicit_box.vtp")
    )
    return flask.make_response(
        {
            "constraints": constraints,
            "viewable_points": "implicit_points.vtp",
            "points": "implicit_points",
            "viewable_box": "implicit_box.vtp",
            "box": "implicit_box",
        },
        200,
    )


@implicit_routes.route("/step1", methods=["POST"])
def step1():
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = geode_functions.get_form_variables(
        flask.request.form,
        ["constraints", "isovalues"],
    )
    data_constraints = geode_numerics.DataPointsManager3D()
    for constraint in json.loads(variables["constraints"]):
        data_constraints.add_data_point(
            og.Point3D(
                [float(constraint["x"]), float(constraint["y"]), float(constraint["z"])]
            ),
            float(constraint["value"]),
            1,
        )
    bbox = og.BoundingBox3D()
    bbox.add_point(og.Point3D([0, 0, 0]))
    bbox.add_point(og.Point3D([40, 40, 40]))
    function_computer = geode_implicit.RegularGridScalarFunctionComputer3D(
        data_constraints,
        bbox,
        10,
        geode_numerics.GridScalarFunctionComputerType.FDM_boundaryfree_curvature_minimization,
    )

    scalar_function_name = "Boundary free - Curvature"
    function_computer.compute_scalar_function(scalar_function_name)
    expliciter = geode_implicit.RegularGridScalarFunctionExpliciter3D(
        function_computer.grid_with_functions(), scalar_function_name
    )
    print("###", json.loads(variables["isovalues"]))
    expliciter.add_scalar_isovalues(json.loads(variables["isovalues"]))
    brep = expliciter.build_brep()
    implicit_model = og_geosciences.implicit_model_from_structural_model_scalar_field(
        og_geosciences.StructuralModel(brep), scalar_function_name
    )
    geode_functions.save(
        implicit_model,
        "StructuralModel",
        os.path.abspath(DATA_FOLDER),
        "implicit.og_strm",
    )
    viewable_file_name = geode_functions.save_viewable(
        implicit_model,
        "StructuralModel",
        os.path.abspath(DATA_FOLDER),
        "implicit_structural_model",
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "implicit_structural_model",
        },
        200,
    )


@implicit_routes.route("/step2", methods=["POST"])
def step2():
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = geode_functions.get_form_variables(
        flask.request.form, ["axis", "coordinate"]
    )
    implicit_model = og_geosciences.ImplicitStructuralModel(
        geode_functions.load(
            "StructuralModel", os.path.abspath(DATA_FOLDER + "implicit.og_strm")
        )
    )
    extracted_cross_section = geode_implicit.extract_implicit_cross_section_from_axis(
        implicit_model, int(variables["axis"]), float(variables["coordinate"])
    )
    geode_functions.save(
        extracted_cross_section,
        "CrossSection",
        os.path.abspath(DATA_FOLDER),
        "cross_section.og_xsctn",
    )
    viewable_file_name = geode_functions.save_viewable(
        extracted_cross_section,
        "CrossSection",
        os.path.abspath(DATA_FOLDER),
        "implicit_cross_section",
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "implicit_cross_section",
        },
        200,
    )


@implicit_routes.route("/step3", methods=["POST"])
def step3():
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    variables = geode_functions.get_form_variables(flask.request.form, ["metric"])
    extracted_cross_section = geode_functions.load(
        "CrossSection", os.path.abspath(DATA_FOLDER + "cross_section.og_xsctn")
    )
    print("metric", float(variables["metric"]))
    constant_metric = geode_common.ConstantMetric2D(float(variables["metric"]))
    remeshed_section, _ = geode_simplex.simplex_remesh_section(
        extracted_cross_section, constant_metric
    )
    viewable_file_name = geode_functions.save_viewable(
        remeshed_section,
        "Section",
        os.path.abspath(DATA_FOLDER),
        "implicit_remeshed_section",
    )
    return flask.make_response(
        {
            "viewable_file_name": os.path.basename(viewable_file_name),
            "id": "implicit_remeshed_section",
        },
        200,
    )