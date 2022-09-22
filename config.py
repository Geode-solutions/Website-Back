''' Flask configuration '''
import os

class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV', default=None)
    ID = os.environ.get('ID', default=None)
    PORT = '5000'
    CORS_HEADERS = 'Content-Type'
    UPLOAD_FOLDER = './uploads'
    LOCK_FOLDER = './lock'
    TIME_FOLDER = './time'

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SSL = 'adhoc'
    ORIGINS = ['https://geode-solutions.com', 'https://next.geode-solutions.com']
    MINUTES_BEFORE_TIMEOUT = '10'
    SECONDS_BETWEEN_SHUTDOWNS = '60'

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SSL = None
    ORIGINS = 'http://localhost:3000'
    MINUTES_BEFORE_TIMEOUT = '1000'
    SECONDS_BETWEEN_SHUTDOWNS = '60'
