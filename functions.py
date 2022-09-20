import os
import threading
import time
import base64
import werkzeug
import uuid

import flask
import pkg_resources

import GeodeObjects

def ListAllInputExtensions():
    """
    Purpose:
        Function that returns a list of all input extensions
    Returns:
        An ordered list of input file extensions
    """
    List = []
    ObjectsList = GeodeObjects.ObjectsList()

    for Object in ObjectsList.values():
        values = Object['input']
        for value in values:
            list_creators = value.list_creators()
            for creator in list_creators:
                if creator not in List:
                    List.append(creator)
    List.sort()
    return List

def ListObjects(extension: str):
    """
    Purpose:
        Function that returns a list of objects that can handle a file, given his extension
    Args:
        extension -- The extension of the file
    Returns:
        An ordered list of object's names
    """
    List = []
    ObjectsList = GeodeObjects.ObjectsList()

    for Object, values in ObjectsList.items():
        list_values = values['input']
        for value in list_values:
            if value.has_creator(extension):
                if Object not in List:
                    List.append(Object)
    List.sort()
    return List

def ListOutputFileExtensions(object: str):
    """
    Purpose:
        Function that returns a list of output file extensions that can be handled by an object
    Args:
        object -- The name of the object
    Returns:
        An ordered list of file extensions
    """
    List = []
    ObjectsList = GeodeObjects.ObjectsList()

    values = ObjectsList[object]['output']
    for value in values:
        list_creators = value.list_creators()
        for creator in list_creators:
            if creator not in List:
                List.append(creator)
    List.sort()
    return List


def GetVersions(list_packages: list):
    list_with_versions = []
    for package in list_packages:
        list_with_versions.append({"package": package, "version": pkg_resources.get_distribution(package).version})
    return list_with_versions

def UploadFile(file: str, filename: str, uploadFolder: str, filesize: int):
    if not os.path.exists(uploadFolder):
        os.mkdir(uploadFolder)
    fileDecoded = base64.b64decode(file.split(',')[-1])
    secureFilename = werkzeug.utils.secure_filename(filename)
    filePath = os.path.join(uploadFolder, secureFilename)
    f = open(filePath, "wb")
    f.write(fileDecoded)
    f.close()

    finalSize =  os.path.getsize(filePath)
    return int(filesize) == int(finalSize)

def create_lock_file():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    flask.g.UUID = uuid.uuid4()
    filePath = f'{LOCK_FOLDER}/{str(flask.g.UUID)}.txt'
    f = open(filePath, 'a')
    f.close()

def create_time_file():
    TIME_FOLDER = flask.current_app.config['TIME_FOLDER']
    if not os.path.exists(TIME_FOLDER):
        os.mkdir(TIME_FOLDER)
    filePath = f'{TIME_FOLDER}/time.txt'
    if not os.path.isfile(filePath):
        f = open(filePath, 'w')
        f.close()

    f = open(TIME_FOLDER + '/time.txt', 'w')
    f.write(str(time.time()))
    f.close()

def remove_lock_file():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    os.remove(f'{LOCK_FOLDER}/{str(flask.g.UUID)}.txt')

def kill_task():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    TIME_FOLDER = flask.current_app.config['TIME_FOLDER']

    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    
    if len(os.listdir(LOCK_FOLDER)) == 0:
        os._exit(0)
    if not os.path.exists(TIME_FOLDER) == 0:
        os._exit(0)
    if not os.path.isfile(TIME_FOLDER + '/time.txt'):
        os._exit(0)
    if os.path.isfile(TIME_FOLDER + '/time.txt'):
        with open(TIME_FOLDER + '/time.txt', 'r') as file:
            try:
                last_request_time = float(file.read())
            except Exception as e:
                print("error : ", str(e))
                os._exit(0)
            current_time = time.time()
            print('substraction : ', current_time - last_request_time)
            if current_time - last_request_time > 60 * 10:
                os._exit(0)
    if os.path.isfile(LOCK_FOLDER + '/ping.txt'):
        os.remove(LOCK_FOLDER + '/ping.txt')

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t
    