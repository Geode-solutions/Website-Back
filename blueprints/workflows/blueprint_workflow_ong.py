import os

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
    try:
        bbox_points["x_min"] = float(bbox_points["x_min"])
        bbox_points["y_min"] = float(bbox_points["y_min"])
        bbox_points["z_min"] = float(bbox_points["z_min"])
        bbox_points["x_max"] = float(bbox_points["x_max"])
        bbox_points["y_max"] = float(bbox_points["y_max"])
        bbox_points["z_max"] = float(bbox_points["z_max"])
    except ValueError:
        flask.abort(400, "Invalid data format for the BBox points")
    return bbox_points

def restoreConstraints(constraints):
    try:
        for i in range(len(constraints)):
            constraints[i] = eval(str(constraints[i]).replace('""','"0"'))
            constraints[i]["x"] = float(constraints[i]["x"])
            constraints[i]["y"] = float(constraints[i]["y"])
            constraints[i]["z"] = float(constraints[i]["z"])
            constraints[i]["value"] = float(constraints[i]["value"])
            constraints[i]["weight"] = float(constraints[i]["weight"])
    except ValueError:
        flask.abort(400, "Invalid data format for the constraints")
    return constraints

def restoreIsovalues(isovalues):
    try:
        for i in range(len(isovalues)):
            isovalues[i] = float(isovalues[i])
        if len(isovalues)==0:
            return [0,1,2]
    except ValueError:
        flask.abort(400, "Invalid data format for the isovalues")
    return isovalues



@workflow_ong_routes.before_request
def before_request():
    geode_functions.create_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))

@workflow_ong_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))
    geode_functions.create_time_file(os.path.abspath(flask.current_app.config["TIME_FOLDER"]))

@workflow_ong_routes.route('/get_constraints',methods = ['POST'])
def sendConstraints():
    constraints = "["

    data_constraints = geode_num.DataPointsManager3D()
    constraint_file = './data/3DBenchmark_implicit_data_constraints.og_pts3d'
    data_constraints.load_data_points(constraint_file)
    for i in range(data_constraints.nb_data_points()):
        constraint = []
        point = data_constraints.data_point_position(i).string().split(" ")
        constraint.append(float(point[0]))
        constraint.append(float(point[1]))
        constraint.append(float(point[2]))
        constraint.append(data_constraints.data_point_value(i))
        constraint.append(data_constraints.data_point_weight(i))

        constraints += str(constraint) + ","
    
    constraints = constraints[:len(constraints)-1] + "]"

    return flask.jsonify(constraints=constraints)

@workflow_ong_routes.route('/step1',methods = ['POST'])
def step1(): 

    variables = geode_functions.get_form_variables(flask.request.form,['bbox_points','constraints','isovalues','function_type','cell_size'])

    try:
        bbox_replaced = str(variables['bbox_points']).replace('""','"0"')
        if type(eval(bbox_replaced)) == str:
            bbox_str = eval(bbox_replaced)
        else:
            bbox_str = bbox_replaced
        bbox_points = restoreBboxPoints(eval(bbox_str))
    except NameError:
        flask.abort(400, "No BBox points filled")

    try:
        constraints = restoreConstraints(eval(variables['constraints']))
    except NameError:
        flask.abort(400, "Invalid constraints format")

    

    isovalues = restoreIsovalues(eval(str(variables['isovalues']).replace('null', '"0"')))

    try:
        cell_size = float(variables['cell_size'])
    except ValueError:
        flask.abort(400, "Invalid data format for the cell size")
    
    data_folder = "./data/"
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
        return flask.make_response({ 'name': 'Bad Request','description': 'Invalid minimization scheme value' }, 400)

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
    geode_functions.save(implicit_model, "StructuralModel", os.path.abspath(data_folder), "implicit.og_strm")
    
    return flask.make_response({'stepOneSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step2',methods=['POST'])
def step2():

    variables = geode_functions.get_form_variables(flask.request.form,['axis','direction'])
    try:
        axis = int(variables['axis'])
        direction = float(variables['direction'])
    except ValueError:
        flask.abort(400, "Invalid data format for the 'axis' or 'metric' variables")

    data_folder = "./data/"

    implicit_model = og_geosciences.ImplicitStructuralModel( geode_functions.load("StructuralModel", os.path.abspath(data_folder + "implicit.og_strm")))

    extracted_cross_section = geode_imp.extract_implicit_cross_section_from_axis(implicit_model,axis,direction)

    geode_functions.save(extracted_cross_section, "CrossSection", os.path.abspath(data_folder), "cross_section.og_xsctn")

    return flask.make_response({'stepTwoSuccessful': "yes" }, 200)


@workflow_ong_routes.route('/step3',methods=['POST'])
def step3():
    variables = geode_functions.get_form_variables(flask.request.form,['metric'])
    try:
        metric = int(variables['metric'])
    except ValueError:
        flask.abort(400, "Invalid data format for the 'metric' variable")

    data_folder = "./data/"
    extracted_cross_section = geode_functions.load('CrossSection', os.path.abspath(data_folder + "cross_section.og_xsctn"))

    constant_metric = geode_common.ConstantMetric2D( metric )
    remeshed_section,_ = geode_simp.simplex_remesh_section(extracted_cross_section,constant_metric)

    geode_functions.save(remeshed_section, "Section", os.path.abspath(data_folder), "section.vtm")

    return flask.make_response({'stepThreeSuccessful': "yes" }, 200)