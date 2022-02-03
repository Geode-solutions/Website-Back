''' Flask configuration '''
import os
import dotenv

if os.path.isfile('./.env'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV', default=None)
    ID = os.environ.get('ID', default=None)
    PORT = '5000'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = './uploads'

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    ORIGINS = 'https://geode-solutions.com'

class TestConfig(Config):
    DEBUG = False
    TESTING = False
    ORIGINS = 'http://localhost:3000'
    


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    ORIGINS = 'http://localhost:3000'
