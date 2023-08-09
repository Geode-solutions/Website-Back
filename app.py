''' Packages '''
import os
import dotenv

import flask
import flask_cors
import time



import blueprints.blueprint_workflows as bp_workflows
import blueprints.blueprint_tools as bp_tools
import blueprints.blueprint_ID as bp_ID
import blueprints.tools.blueprint_file_converter as bp_file_converter
import blueprints.tools.blueprint_validity_checker as bp_validity_checker
import blueprints.tools.blueprint_crs_converter as bp_crs_converter
import blueprints.workflows.blueprint_workflow_ong as bp_workflow_ong
import blueprints.workflows.blueprint_simplex_remesh as bp_simplex_remesh
import blueprints.workflows.blueprint_explicit_modeling as bp_explicit_modeling


from opengeodeweb_back import geode_functions

from werkzeug.exceptions import HTTPException


if os.path.isfile('./.env'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))

''' Global config '''
app = flask.Flask(__name__)

def kill_task():
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    if not os.path.exists(TIME_FOLDER):
        os.mkdir(TIME_FOLDER)
    
    if len(os.listdir(LOCK_FOLDER)) == 0:
        print(f'No files in the {LOCK_FOLDER} folder, shutting down...', flush=True)
        os._exit(0)
    if not os.path.isfile(TIME_FOLDER + '/time.txt'):
        print('\'time.txt\' file doesn\'t exist, shutting down...', flush=True)
        os._exit(0)
    if os.path.isfile(TIME_FOLDER + '/time.txt'):
        with open(TIME_FOLDER + '/time.txt', 'r') as file:
            try:
                last_request_time = float(file.read())
            except Exception as e:
                print("error : ", str(e), flush=True)
                os._exit(0)
            current_time = time.time()
            if (current_time - last_request_time)/60 > MINUTES_BEFORE_TIMEOUT:
                print('Server timed out due to inactivity, shutting down...', flush=True)
                os._exit(0)
    if os.path.isfile(LOCK_FOLDER + '/ping.txt'):
        os.remove(LOCK_FOLDER + '/ping.txt')

''' Config variables '''
FLASK_DEBUG = True if os.environ.get('FLASK_DEBUG', default=None) == 'True' else False

if FLASK_DEBUG == False:
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.DevConfig')

ID = app.config.get('ID')
PORT = int(app.config.get('PORT'))
ORIGINS = app.config.get('ORIGINS')
SSL = app.config.get('SSL')
LOCK_FOLDER = app.config.get('LOCK_FOLDER')
TIME_FOLDER = app.config.get('TIME_FOLDER')
MINUTES_BEFORE_TIMEOUT = float(app.config.get('MINUTES_BEFORE_TIMEOUT'))
SECONDS_BETWEEN_SHUTDOWNS = float(app.config.get('SECONDS_BETWEEN_SHUTDOWNS'))


blueprint_tools = flask.Blueprint('tools', __name__)
blueprint_workflows = flask.Blueprint('workflows', __name__)

blueprint_file_converter = flask.Blueprint('file_converter', __name__)
blueprint_validity_checker = flask.Blueprint('validity_checker', __name__)
blueprint_crs_converter = flask.Blueprint('crs_converter', __name__)
blueprint_workflow_ong = flask.Blueprint('workflow_ong', __name__)
blueprint_simplex_remesh = flask.Blueprint('simplex_remesh', __name__)
blueprint_explicit_modeling = flask.Blueprint('explicit_modeling', __name__)

bp_tools.register_blueprint(bp_file_converter.file_converter_routes, url_prefix='/file_converter')
bp_tools.register_blueprint(bp_validity_checker.validity_checker_routes, url_prefix='/validity_checker')
bp_tools.register_blueprint(bp_crs_converter.crs_converter_routes, url_prefix='/crs_converter')

bp_workflows.register_blueprint(bp_workflow_ong.workflow_ong_routes, url_prefix='/ong')
bp_workflows.register_blueprint(bp_simplex_remesh.simplex_remesh_routes, url_prefix='/simplexRemesh')
bp_workflows.register_blueprint(bp_explicit_modeling.explicit_modeling_routes, url_prefix='/explicitModeling')

app.register_blueprint(bp_tools.tools_routes, url_prefix=f'/{ID}/tools')
app.register_blueprint(bp_workflows.workflows_routes, url_prefix=f'/{ID}/workflows')
app.register_blueprint(bp_ID.ID_routes, url_prefix=f'/{ID}')


if FLASK_DEBUG == False:
    geode_functions.set_interval(kill_task, SECONDS_BETWEEN_SHUTDOWNS)
flask_cors.CORS(app, origins=ORIGINS)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = flask.json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
    
@app.route('/tools/createbackend', methods=['POST'])
def create_backend():
    return flask.make_response({"ID": str("123456")}, 200)

# ''' Main '''
if __name__ == '__main__':
    print(f'Python is running in {FLASK_DEBUG} mode')
    
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=PORT, ssl_context=SSL)
