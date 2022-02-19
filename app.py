''' Packages '''
import flask
import flask_cors
import os
from blueprint import routes
import threading
import dotenv

if os.path.isfile('./.env'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))

''' Global config '''
app = flask.Flask(__name__)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t

def kill():
    if not os.path.isfile('./ping.txt'):
        os._exit(0)
    else:
        os.remove('./ping.txt')

''' Config variables '''
FLASK_ENV = os.environ['FLASK_ENV']

if FLASK_ENV == "production":
    app.config.from_object('config.ProdConfig')
    set_interval(kill, 45)
else:
    app.config.from_object('config.DevConfig')

ID = app.config.get('ID')
PORT = int(app.config.get('PORT'))
CORS_HEADERS = app.config.get('CORS_HEADERS')
UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER')
DEBUG = app.config.get('DEBUG')
TESTING = app.config.get('TESTING')
ORIGINS = app.config.get('ORIGINS')
SSL = app.config.get('SSL')


if ID != None:
    app.register_blueprint(routes, url_prefix="/" + ID)
else:
    app.register_blueprint(routes, url_prefix="/")

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

flask_cors.CORS(app, origins=ORIGINS)

# For development
@app.route('/tools/createbackend', methods=['POST'])
def createbackend():
    return flask.jsonify({"status": 200, "ID": str("123456")})

# ''' Main '''
if __name__ == '__main__':
    print('Python is running in ' + FLASK_ENV + ' mode')
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT, ssl_context=SSL)