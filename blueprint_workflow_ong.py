import re

import flask
import flask_cors

import opengeode as geode
import opengeode_io as og_io
import opengeode_geosciences as og_geosciences
import geode_numerics as geode_num
import geode_implicit as geode_imp
import geode_simplex as geode_simp
import geode_common
from opengeodeweb_back import geode_functions, geode_objects


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
        constraints[i] = eval(constraints[i].replace('""','"0"'))
        constraints[i]["x"] = float(constraints[i]["x"])
        constraints[i]["y"] = float(constraints[i]["y"])
        constraints[i]["z"] = float(constraints[i]["z"])
        constraints[i]["value"] = float(constraints[i]["value"])
        constraints[i]["weight"] = float(constraints[i]["weight"])
    return constraints

def restoreIsovalues(isovalues):
    for i in range(len(isovalues)):
        isovalues[i] = float(isovalues[i])
    if len(isovalues)==0:
        return [0,1,2]
    
    return isovalues


@workflow_ong_routes.route('/get_constraints',methods = ['POST'])
def sendConstraints():
    constraints = "["
    constraints += str( [ 2.5, 1, 2 , 0, 20 ]) + ","
    constraints += str( [ 3.5, 2, 3, 0, 20 ]) + ","
    constraints += str( [ 6, 3.5, 6.5, 0, 20 ]) + ","
    constraints += str( [ 4, 6.5, 5.9, 0, 20 ]) + ","  
    constraints += str( [ 6, 12, 2.5, 0, 20 ]) + ","  
    constraints += str( [ 3, 11.5, 2, 0, 20 ]) + ","  
    constraints += str( [ 7, 16, 3, 0, 20 ]) + ","  
    constraints += str( [ 3, 15.5, 3.5, 0, 20 ]) + ","  
    constraints += str( [ 1, 14, 6, 0, 20 ]) + ","  

    constraints += str( [ 3.5, 2, 4, 1, 20 ]) + ","  
    constraints += str( [ 5.5, 3.5, 7.5, 1, 20 ]) + ","  
    constraints += str( [ 2.5, 1, 3, 1, 20 ]) + ","  
    constraints += str( [ 4, 6.5, 8, 1, 20 ]) + ","  
    constraints += str( [ 7, 12, 3, 1, 20 ]) + ","  
    constraints += str( [ 1, 11.5, 5, 1, 20 ]) + ","  
    constraints += str( [ 7, 16, 4, 1, 20 ]) + ","  
    constraints += str( [ 3, 15.5, 4.5, 1, 20 ]) + ","  
    constraints += str( [ 1, 14, 7, 1, 20 ]) + ","  

    constraints += str( [ 2.5, 1, 7, 2, 20 ]) + ","  
    constraints += str( [ 3.5, 2, 9.7, 2, 20 ]) + ","  
    constraints += str( [ 7, 3.5, 10.9, 2, 20 ]) + ","  
    constraints += str( [ 4, 6.5, 10.5, 2, 20 ]) + ","  
    constraints += str( [ 6, 12, 7, 2, 20 ]) + ","  
    constraints += str( [ 3, 11.5, 6.9, 2, 20 ]) + ","  
    constraints += str( [ 7, 16, 8, 2, 20 ]) + ","  
    constraints += str( [ 3, 15.5, 8.5, 2, 20 ]) + ","  
    constraints += str( [ 1, 14, 9, 2, 20 ]) + "]"

    return flask.jsonify(constraints=constraints)

@workflow_ong_routes.route('/step1',methods = ['POST'])
def step1(): 

    variables = geode_functions.get_form_variables(flask.request.form,['bbox_points','constraints','isovalues','function_type','cell_size'])

    if variables['bbox_points'] == 'undefined':
        bbox_points = {"x_min":0., "y_min":0., "z_min":0., "x_max":8., "y_max":11., "z_max":17.}
    else:
        bbox_points = restoreBboxPoints(eval(eval(variables['bbox_points']).replace('""','"0"')))
    constraints = restoreConstraints(eval(variables['constraints']))
    isovalues = restoreIsovalues(eval(variables['isovalues'].replace('null', '"0"')))
    if variables['cell_size'] == '':
        cell_size = 1.
    else:
        cell_size = float(variables['cell_size'])
    
    data_folder = "/server/data/"

    data_constraints = geode_num.DataPointsManager3D()

    for constraint in constraints:
        data_constraints.add_data_point( geode.Point3D( [ constraint["x"], constraint["y"], constraint["z"] ] ), constraint["value"], constraint["weight"] )

    # configuring bbox
    bbox = geode.BoundingBox3D()
    bbox.add_point(geode.Point3D( [ bbox_points["x_min"], bbox_points["y_min"], bbox_points["z_min"]]))
    bbox.add_point(geode.Point3D( [ bbox_points["x_max"], bbox_points["y_max"], bbox_points["z_max"]]))



    # processing depending on function type
    if variables['function_type'] == "Laplacian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_laplacian_minimization )
    elif variables['function_type'] ==  "Hessian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_hessian_minimization )
    elif variables['function_type'] ==  "Curvature":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_curvature_minimization )
    elif variables['function_type'] ==  "Boundary free - Laplacian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_laplacian_minimization )
    elif variables['function_type'] ==  "Boundary free - Hessian":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_hessian_minimization )
    elif variables['function_type'] == "Boundary free - Curvature":
        function_computer = geode_imp.RegularGridScalarFunctionComputer3D( data_constraints, bbox, cell_size, geode_num.GridScalarFunctionComputerType.FDM_boundaryfree_curvature_minimization )
    else:
        return flask.make_response({ 'name': 'Bad Request','description': 'Wrong scalar function type' }, 400)

    scalar_function_name = variables['function_type']
    function_computer.compute_scalar_function(scalar_function_name)
    # computing expliciter
    expliciter = geode_imp.RegularGridScalarFunctionExpliciter3D( function_computer.grid_with_functions(), scalar_function_name )

    # adding isovalues
    expliciter.add_scalar_isovalues( isovalues )

    # computing implicit model
    brep = expliciter.build_brep()
    implicit_model = og_geosciences.implicit_model_from_structural_model_scalar_field(og_geosciences.StructuralModel(brep),scalar_function_name)


    # saving implicit model
    geode_functions.save(implicit_model, "StructuralModel", data_folder, "implicit.og_strm")
    
    return flask.make_response({'stepOneSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step2',methods=['POST'])
def step2():

    variables = geode_functions.get_form_variables(flask.request.form,['axis','direction'])
    if variables['axis'] == '':
        axis = 0.
    else:
        axis = int(variables['axis'])
    if variables['direction'] == '':
        direction = 2.
    else:
        direction = float(variables['direction'])

    data_folder = "/server/data/"

    implicit_model = og_geosciences.ImplicitStructuralModel( geode_functions.load("StructuralModel", data_folder + "implicit.og_strm"))

    extracted_cross_section = geode_imp.extract_implicit_cross_section_from_axis(implicit_model,axis,direction)

    geode_functions.save(extracted_cross_section, "CrossSection", data_folder, "cross_section.og_xsctn")

    return flask.make_response({'stepTwoSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step3',methods=['POST'])
def step3():
    variables = geode_functions.get_form_variables(flask.request.form,['metric'])
    if variables['metric'] == '':
        metric = 1.
    else:
        metric = float(variables['metric'])

    data_folder = "/server/data/"

    extracted_cross_section = og_geosciences.load_cross_section(data_folder + "cross_section.og_xsctn")

    constant_metric = geode_common.ConstantMetric2D( metric )
    remeshed_section,_ = geode_simp.simplex_remesh_section(extracted_cross_section,constant_metric)

    geode_functions.save(remeshed_section, "Section", data_folder, "section.vtm")

    return flask.make_response({'stepThreeSuccessful': "yes" }, 200)
