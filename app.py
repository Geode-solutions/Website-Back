''' Packages '''
import os
import dotenv

import flask
import flask_cors

import blueprint_fileconverter
import blueprint_validitychecker
import blueprint_ID

import functions

if os.path.isfile('./.env'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))

''' Global config '''
app = flask.Flask(__name__)

''' Config variables '''
FLASK_ENV = os.environ.get('FLASK_ENV', default=None)

if FLASK_ENV == "production" or FLASK_ENV == "test":
    app.config.from_object('config.ProdConfig')
    functions.set_interval(functions.kill_task, 60)
else:
    app.config.from_object('config.DevConfig')

ID = app.config.get('ID')
PORT = int(app.config.get('PORT'))
DEBUG = app.config.get('DEBUG')
TESTING = app.config.get('TESTING')
ORIGINS = app.config.get('ORIGINS')
SSL = app.config.get('SSL')

if ID != None:
    app.register_blueprint(blueprint_fileconverter.fileconverter_routes, url_prefix=f'/{ID}/fileconverter')
    app.register_blueprint(blueprint_validitychecker.validitychecker_routes, url_prefix=f'/{ID}/validitychecker')
    app.register_blueprint(blueprint_ID.ID_routes, url_prefix=f'/{ID}/')
else:
    app.register_blueprint(blueprint_fileconverter.fileconverter_routes, url_prefix='/fileconverter')
    app.register_blueprint(blueprint_validitychecker.validitychecker_routes, url_prefix='/validitychecker')
    app.register_blueprint(blueprint_ID.ID_routes, url_prefix='/')

flask_cors.CORS(app, origins=ORIGINS)

@app.route('/tools/createbackend', methods=['POST'])
def create_backend():
    return flask.make_response({"ID": str("123456")}, 200)

# ''' Main '''
if __name__ == '__main__':
    print('Python is running in ' + FLASK_ENV + ' mode')
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT, ssl_context=SSL)
