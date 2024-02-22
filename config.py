""" Flask configuration """

import os
from sys import platform


class Config(object):
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", default=False)
    ID = os.environ.get("ID", default=None)
    PORT = "5000"
    CORS_HEADERS = "Content-Type"
    UPLOAD_FOLDER = os.path.abspath("./uploads")
    WORKFLOWS_DATA_FOLDER = os.path.abspath("./data_workflows/")
    LOCK_FOLDER = os.path.abspath("./lock/")
    TIME_FOLDER = os.path.abspath("./time/")


class ProdConfig(Config):
    SSL = None
    ORIGINS = ["https://geode-solutions.com", "https://next.geode-solutions.com"]
    MINUTES_BEFORE_TIMEOUT = "5"
    SECONDS_BETWEEN_SHUTDOWNS = "150"
    DATA_FOLDER = "/data/"


class DevConfig(Config):
    SSL = None
    ORIGINS = "http://localhost:3000"
    MINUTES_BEFORE_TIMEOUT = "1000"
    SECONDS_BETWEEN_SHUTDOWNS = "60"
    if platform == "linux":
        DATA_FOLDER = "/temp/OpenGeodeWeb_Data/"
    elif platform == "win32":
        DATA_FOLDER = os.path.abspath(
            os.path.join("C:/Users", os.getlogin(), "OpenGeodeWeb_Data")
        )
    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)
