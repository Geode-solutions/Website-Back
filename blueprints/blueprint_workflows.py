import os
import flask
import flask_cors
from opengeodeweb_back import geode_functions, geode_objects

import blueprints.workflows.blueprint_workflow_ong as bp_workflow_ong
import blueprints.workflows.blueprint_simplex_remesh as bp_simplex_remesh
import blueprints.workflows.blueprint_explicit_modeling as bp_explicit_modeling

workflows_routes = flask.Blueprint('crs_converter_routes', __name__)
flask_cors.CORS(workflows_routes)


@workflows_routes.before_request
def before_request():
    geode_functions.create_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))

@workflows_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file(os.path.abspath(flask.current_app.config["LOCK_FOLDER"]))
    geode_functions.create_time_file(os.path.abspath(flask.current_app.config["TIME_FOLDER"]))


workflows_routes.register_blueprint(bp_workflow_ong.workflow_ong_routes, url_prefix='/ong', name='workflow_ong_blueprint')
workflows_routes.register_blueprint(bp_simplex_remesh.simplex_remesh_routes, url_prefix='/simplex_remesh', name='simplex_remesh_blueprint')
workflows_routes.register_blueprint(bp_explicit_modeling.explicit_modeling_routes, url_prefix='/explicit_modeling', name='explicit_modeling_blueprint')