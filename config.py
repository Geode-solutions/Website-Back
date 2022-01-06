''' Flask configuration '''
import os
import dotenv

if os.path.isfile('./.env'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    dotenv.load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV', default=None)
    PORT = '5000'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = './uploads'


class ProdConfig(Config):
    ID = os.environ.get('ID', default=None)
    DEBUG = False
    TESTING = False
    ORIGINS = 'https://test.geode-solutions.com'


class DevConfig(Config):
    ID = None
    DEBUG = True
    TESTING = True
    ORIGINS = 'https://localhost:3000'
