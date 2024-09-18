# Standard library imports
import os

# Third party imports
import flask
import flask_cors
from opengeodeweb_back import utils_functions

import blueprints.workflows.blueprint_implicit as bp_implicit
import blueprints.workflows.blueprint_simplex as bp_simplex
import blueprints.workflows.blueprint_explicit as bp_explicit

workflows_routes = flask.Blueprint("workflows_routes", __name__)
flask_cors.CORS(workflows_routes)


@workflows_routes.before_request
def before_request():
    utils_functions.before_request(flask.current_app)


@workflows_routes.teardown_request
def teardown_request(exception):
    utils_functions.teardown_request(flask.current_app)


workflows_routes.register_blueprint(
    bp_implicit.implicit_routes, url_prefix="/implicit", name="implicit_blueprint"
)
workflows_routes.register_blueprint(
    bp_simplex.simplex_routes, url_prefix="/simplex", name="simplex_blueprint"
)
workflows_routes.register_blueprint(
    bp_explicit.explicit_routes, url_prefix="/explicit", name="explicit_blueprint"
)
