import os
import flask
import flask_cors
from opengeodeweb_back import geode_functions, geode_objects

import blueprints.workflows.blueprint_implicit as bp_implicit
import blueprints.workflows.blueprint_simplex as bp_simplex
import blueprints.workflows.blueprint_explicit as bp_explicit

workflows_routes = flask.Blueprint("crs_converter_routes", __name__)
flask_cors.CORS(workflows_routes)


@workflows_routes.before_request
def before_request():
    geode_functions.create_lock_file(
        os.path.abspath(flask.current_app.config["LOCK_FOLDER"])
    )


@workflows_routes.teardown_request
def teardown_request(exception):
    geode_functions.remove_lock_file(
        os.path.abspath(flask.current_app.config["LOCK_FOLDER"])
    )
    geode_functions.create_time_file(
        os.path.abspath(flask.current_app.config["TIME_FOLDER"])
    )


workflows_routes.register_blueprint(
    bp_implicit.implicit_routes, url_prefix="/implicit", name="implicit_blueprint"
)
workflows_routes.register_blueprint(
    bp_simplex.simplex_routes, url_prefix="/simplex", name="simplex_blueprint"
)
workflows_routes.register_blueprint(
    bp_explicit.explicit_routes, url_prefix="/explicit", name="explicit_blueprint"
)
