import os

import flask
import flask_cors

import functions

ID_routes = flask.Blueprint('ID_routes', __name__)
flask_cors.CORS(ID_routes)

@ID_routes.route('/', methods=['GET'])
def root():
    return flask.make_response({"message": "root"}, 200)
@ID_routes.route('/kill', methods=['POST'])
def test_kill():
    functions.kill_task()
    return flask.make_response({"message": "Task killed"}, 200)
@ID_routes.route('/ping', methods=['POST'])
def ping():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    if not os.path.isfile(LOCK_FOLDER + '/ping.txt'):
        f = open(LOCK_FOLDER + '/ping.txt', 'a')
        f.close()
    return flask.make_response({"message": "Flask server is running"}, 200)
