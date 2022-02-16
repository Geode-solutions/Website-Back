''' Flask configuration '''
import os

class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV', default=None)
    ID = os.environ.get('ID', default=None)
    PORT = '5000'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = './uploads'

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SSL = 'adhoc'
    ORIGINS = 'https://geode-solutions.com'

class TestConfig(Config):
    DEBUG = False
    TESTING = False
    SSL = 'adhoc'
    ORIGINS = 'https://next.geode-solutions.com'

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SSL = None
    ORIGINS = 'http://localhost:3000'
