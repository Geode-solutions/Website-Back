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


workflow_ong_routes = flask.Blueprint('workflow_ong_routes', __name__)
flask_cors.CORS(workflow_ong_routes)

def restoreBboxPoints(bbox_points):
    bbox_points["x_min"] = float(bbox_points["x_min"])
    bbox_points["y_min"] = float(bbox_points["y_min"])
    bbox_points["z_min"] = float(bbox_points["z_min"])
    bbox_points["x_max"] = float(bbox_points["x_max"])
    bbox_points["y_max"] = float(bbox_points["y_max"])
    bbox_points["z_max"] = float(bbox_points["z_max"])
    return bbox_points

def restoreConstraints(constraints):
    for i in range(len(constraints)):
        constraints[i] = eval(constraints[i])
        constraints[i]["x"] = float(constraints[i]["x"])
        constraints[i]["y"] = float(constraints[i]["y"])
        constraints[i]["z"] = float(constraints[i]["z"])
        constraints[i]["value"] = float(constraints[i]["value"])
        constraints[i]["weigth"] = float(constraints[i]["weigth"])
    return constraints

def restoreIsovalues(isovalues):
    for i in range(len(isovalues)):
        if isovalues[i] == None:
            return -1
        isovalues[i] = float(isovalues[i])
    if len(isovalues)==0:
        return [0,1,2]
    
    return isovalues


@workflow_ong_routes.route('/step1',methods = ['POST'])
def step1():
    bbox_points_input = eval(flask.request.form.get('bbox_points').replace('""', '"0"'))
    bbox_points = restoreBboxPoints(eval(bbox_points_input))
    constraints_input = eval(flask.request.form.get('constraints'))
    constraints = restoreConstraints(constraints_input)
    isovalues_input = flask.request.form.get('isovalues')
    isovalues = restoreIsovalues(eval(isovalues_input.replace('null', 'None')))
    if isovalues == -1:
        return flask.make_response({ 'name': 'Bad Request','description': 'Isovalue field(s) unfilled' }, 400)
    function_type = flask.request.form.get('function_type')

    if function_type == None:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong scalar function type' }, 400)

    output_folder = "./data/"

    data_constraints = geode_num.DataPointsManager3D()

    # getting data file
    constraint_file = './data/3DBenchmark_implicit_data_constraints.og_pts3d'
    data_constraints.load_data_points(constraint_file)

    for constraint in constraints:
        data_constraints.add_data_point( geode.Point3D( [ constraint["x"], constraint["y"], constraint["z"] ] ), constraint["value"], constraint["weight"] ) ###

    # configuring bbox
    bbox = geode.BoundingBox3D()
    bbox.add_point(geode.Point3D( [ bbox_points["x_min"], bbox_points["y_min"], bbox_points["z_min"]]))
    bbox.add_point(geode.Point3D( [ bbox_points["x_max"], bbox_points["y_max"], bbox_points["z_max"]]))



    # processing depending on function type
    if function_type == "Laplacian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_laplacian_minimization )
    elif function_type ==  "Hessian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_hessian_minimization )
    elif function_type ==  "Curvature":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_curvature_minimization )
    elif function_type ==  "Boundary free - Laplacian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_laplacian_minimization )
    elif function_type ==  "Boundary free - Hessian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_hessian_minimization )
    elif function_type == "Boundary free - Curvature":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, 1, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_curvature_minimization )
    else:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong scalar function type' }, 400)

    scalar_function_name = function_type
    function_computer.compute_scalar_function(scalar_function_name)
    # computing expliciter
    expliciter = geode_imp.RegularGridScalarFunctionExpliciter3D( function_computer.grid_with_functions(), scalar_function_name )

    # adding isovalues
    expliciter.add_scalar_isovalues( isovalues )

    # computing implicit model
    brep = expliciter.build_brep()
    implicit_model = og_geosciences.implicit_model_from_structural_model_scalar_field(og_geosciences.StructuralModel(brep),scalar_function_name)


    # saving implicit model
    og_geosciences.save_structural_model(implicit_model,output_folder + "implicit.og_strm")
    
    return flask.make_response({'stepOneSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step2',methods=['POST'])
def step2():
    axis = int(flask.request.form.get('axis'))
    direction = float(flask.request.form.get('direction'))


    output_folder = "./data/"

    if axis is None or axis < 0 or axis > 5:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong axis posted' }, 400)
    if direction is None or direction < 0 or direction > 5:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong direction posted' }, 400)

    # loading implicit model
    implicit_model = og_geosciences.ImplicitStructuralModel( og_geosciences.load_structural_model(output_folder + "implicit.og_strm"))

    extracted_cross_section = geode_imp.extract_implicit_cross_section_from_axis(implicit_model,axis,direction)

    og_geosciences.save_cross_section(extracted_cross_section,output_folder + "cross_section.og_xsctn")

    return flask.make_response({'stepTwoSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step3',methods=['POST'])
def step3():
    metric = float(flask.request.form.get("metric"))
    output_folder = "./data/"

    if metric is None or metric < 0 or metric > 5:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong metric posted' }, 400)

    extracted_cross_section = og_geosciences.load_cross_section(output_folder + "cross_section.og_xsctn")

    metric = geode_common.ConstantMetric2D( metric )
    remeshed_section,_ = geode_simp.simplex_remesh_section(extracted_cross_section,metric)

    # saving objects
    geode.save_section(remeshed_section,output_folder + 'section.vtm')

    return flask.make_response({'stepThreeSuccessful': "yes" }, 200)
