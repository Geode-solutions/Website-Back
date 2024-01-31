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
import geode_conversion
from opengeodeweb_back import geode_functions, geode_objects


implicit_routes = flask.Blueprint("implicit_routes", __name__)
flask_cors.CORS(implicit_routes)

with open("blueprints/workflows/implicit_step0.json", "r") as file:
    step0_json = json.load(file)


@implicit_routes.route(step0_json["route"], methods=step0_json["methods"])
def step0():
    WORKFLOWS_DATA_FOLDER = flask.current_app.config["WORKFLOWS_DATA_FOLDER"]
    constraints = "["
    data_constraints = geode_numerics.DataPointsManager3D()
    constraint_file = WORKFLOWS_DATA_FOLDER + "data_constraints.og_pts3d"
    data_constraints.load_data_points(constraint_file)
    for i in range(data_constraints.nb_data_points()):
        constraint = []
        point = data_constraints.data_point_position(i)
        constraint.append(point.value(0))
        constraint.append(point.value(1))
        constraint.append(point.value(2))
        constraint.append(data_constraints.data_point_value(i))
        constraints += str(constraint) + ","
    constraints = constraints[: len(constraints) - 1] + "]"
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    data_constraints.save_data_points_manager(
        os.path.join(os.path.abspath(DATA_FOLDER), "implicit_points.og_pts3d")
    )
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


with open("blueprints/workflows/implicit_update_value.json", "r") as file:
    update_value_json = json.load(file)


@implicit_routes.route(update_value_json["route"], methods=update_value_json["methods"])
def update_value():
    geode_functions.validate_request(
        flask.request,
        update_value_json,
    )
    point = int(flask.request.json["point"])
    value = float(flask.request.json["value"])

    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    data_constraints = geode_numerics.DataPointsManager3D()
    constraint_file = os.path.join(
        os.path.abspath(DATA_FOLDER), "implicit_points.og_pts3d"
    )
    data_constraints.load_data_points(constraint_file)
    data_constraints.change_data_point_value(point, value)
    data_constraints.save_data_points_manager(
        os.path.join(os.path.abspath(DATA_FOLDER), "implicit_points.og_pts3d")
    )
    data_constraints.save_data_points_manager(
        os.path.join(os.path.abspath(DATA_FOLDER), "implicit_points.vtp")
    )
    return flask.make_response(
        {
            "viewable_points": "implicit_points.vtp",
            "points": "implicit_points",
        },
        200,
    )


with open("blueprints/workflows/implicit_step1.json", "r") as file:
    step1_json = json.load(file)


@implicit_routes.route(step1_json["route"], methods=step1_json["methods"])
def step1():
    geode_functions.validate_request(
        flask.request,
        step1_json,
    )
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    data_constraints = geode_numerics.DataPointsManager3D()
    constraint_file = os.path.join(
        os.path.abspath(DATA_FOLDER), "implicit_points.og_pts3d"
    )
    data_constraints.load_data_points(constraint_file)
    bbox = og.BoundingBox3D()
    bbox.add_point(og.Point3D([0, 0, 0]))
    bbox.add_point(og.Point3D([40, 40, 40]))
    function_computer = geode_implicit.ScalarFunctionComputer3D(
        data_constraints, bbox, 10
    )

    scalar_function_name = "Boundary free - Curvature"
    function_computer.compute_scalar_function(scalar_function_name)
    expliciter = geode_implicit.GridScalarFunctionExpliciter3D(
        function_computer.grid_with_results(), scalar_function_name
    )
    expliciter.add_scalar_isovalues(flask.request.json["isovalues"])
    brep = expliciter.build_brep()
    implicit_model = og_geosciences.implicit_model_from_structural_model_scalar_field(
        og_geosciences.StructuralModel(brep), scalar_function_name
    )
    builder = og_geosciences.ImplicitStructuralModelBuilder(implicit_model)
    geode_functions.save(
        "StructuralModel",
        implicit_model,
        os.path.abspath(DATA_FOLDER),
        "implicit.og_strm",
    )
    viewable_file_name = geode_functions.save_viewable(
        "StructuralModel",
        implicit_model,
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


with open("blueprints/workflows/implicit_step2.json", "r") as file:
    step2_json = json.load(file)


@implicit_routes.route(step2_json["route"], methods=step2_json["methods"])
def step2():
    geode_functions.validate_request(flask.request, step2_json)
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    implicit_model = og_geosciences.ImplicitStructuralModel(
        geode_functions.load(
            "StructuralModel", os.path.abspath(DATA_FOLDER + "implicit.og_strm")
        )
    )

    extracted_cross_section = geode_implicit.extract_implicit_cross_section_from_axis(
        implicit_model, flask.request.json["axis"], flask.request.json["coordinate"]
    )
    geode_functions.save(
        "CrossSection",
        extracted_cross_section,
        os.path.abspath(DATA_FOLDER),
        "cross_section.og_xsctn",
    )
    viewable_file_name = geode_functions.save_viewable(
        "CrossSection",
        extracted_cross_section,
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


with open("blueprints/workflows/implicit_step3.json", "r") as file:
    step3_json = json.load(file)


@implicit_routes.route(step3_json["route"], methods=step3_json["methods"])
def step3():
    geode_functions.validate_request(flask.request, step3_json)
    DATA_FOLDER = flask.current_app.config["DATA_FOLDER"]
    extracted_cross_section = geode_functions.load(
        "CrossSection", os.path.abspath(DATA_FOLDER + "cross_section.og_xsctn")
    )
    metric = float(flask.request.json["metric"])
    sharp_section = geode_conversion.add_section_sharp_features(
        extracted_cross_section, 120
    )
    constant_metric = geode_common.ConstantMetric2D(metric)
    remeshed_section, _ = geode_simplex.simplex_remesh_section(
        sharp_section, constant_metric
    )
    viewable_file_name = geode_functions.save_viewable(
        "Section",
        remeshed_section,
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
