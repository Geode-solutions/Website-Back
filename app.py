""" Packages """

import os
import dotenv

import flask
import flask_cors
import time

import blueprints.blueprint_tools as bp_tools
import blueprints.blueprint_workflows as bp_workflows
import blueprints.blueprint_ID as bp_ID

from opengeodeweb_back.routes import blueprint_routes
from opengeodeweb_back.utils_functions import handle_exception, kill_task, set_interval

from werkzeug.exceptions import HTTPException

from werkzeug.exceptions import HTTPException


if os.path.isfile("./.env"):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, ".env"))

""" Global config """
app = flask.Flask(__name__)


""" Config variables """
FLASK_DEBUG = True if os.environ.get("FLASK_DEBUG", default=None) == "True" else False

if FLASK_DEBUG == False:
    app.config.from_object("config.ProdConfig")
else:
    app.config.from_object("config.DevConfig")

ID = app.config.get("ID")
PORT = int(app.config.get("PORT"))
ORIGINS = app.config.get("ORIGINS")
SSL = app.config.get("SSL")
MINUTES_BEFORE_TIMEOUT = float(app.config.get("MINUTES_BEFORE_TIMEOUT"))
SECONDS_BETWEEN_SHUTDOWNS = float(app.config.get("SECONDS_BETWEEN_SHUTDOWNS"))

app.register_blueprint(
    bp_tools.tools_routes, url_prefix=f"/tools", name="tools_blueprint"
)
app.register_blueprint(
    bp_workflows.workflows_routes, url_prefix=f"/workflows", name="workflows_blueprint"
)
app.register_blueprint(
    blueprint_routes.routes,
    url_prefix="/opengeodeweb_back",
    name="blueprint_routes",
)

app.register_blueprint(bp_ID.ID_routes, url_prefix="/", name="ID_blueprint")

if FLASK_DEBUG == False:
    set_interval(kill_task, SECONDS_BETWEEN_SHUTDOWNS)
flask_cors.CORS(app, origins=ORIGINS)


@app.errorhandler(HTTPException)
def errorhandler(e):
    return handle_exception(e)


@app.route("/createbackend", methods=["POST"])
def create_backend():
    return flask.make_response({"ID": str("123456")}, 200)


# ''' Main '''
if __name__ == "__main__":
    print(f"Python is running in {FLASK_DEBUG} mode")
    app.run(debug=FLASK_DEBUG, host="0.0.0.0", port=PORT, ssl_context=SSL)
