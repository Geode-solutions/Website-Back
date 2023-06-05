import os
import threading
import time
import base64
import werkzeug
import uuid

import flask
import pkg_resources

import geode_objects
import opengeode_geosciences as og_gs

def list_all_input_extensions():
    """
    Purpose:
        Function that returns a list of all input extensions
    Returns:
        An ordered list of input file extensions
    """
    List = []
    objects_list = geode_objects.objects_list()

    for Object in objects_list.values():
        values = Object['input']
        for value in values:
            list_creators = value.list_creators()
            for creator in list_creators:
                if creator not in List:
                    List.append(creator)
    List.sort()
    return List

def list_objects(extension: str):
    """
    Purpose:
        Function that returns a list of objects that can handle a file, given his extension
    Args:
        extension -- The extension of the file
    Returns:
        An ordered list of object's names
    """
    List = []
    objects_list = geode_objects.objects_list()

    for geode_object, values in objects_list.items():
        list_values = values['input']
        for value in list_values:
            if value.has_creator(extension):
                if geode_object not in List:
                    List.append(geode_object)
    List.sort()
    return List

def list_output_file_extensions(geode_object: str):
    """
    Purpose:
        Function that returns a list of output file extensions that can be handled by an object
    Args:
        geode_object -- The name of the geode_object
    Returns:
        An ordered list of file extensions
    """
    List = []
    objects_list = geode_objects.objects_list()

    values = objects_list[geode_object]['output']
    for value in values:
        list_creators = value.list_creators()
        for creator in list_creators:
            if creator not in List:
                List.append(creator)
    List.sort()
    return List


def get_versions(list_packages: list):
    list_with_versions = []
    for package in list_packages:
        list_with_versions.append({"package": package, "version": pkg_resources.get_distribution(package).version})
    return list_with_versions

def upload_file(file: str, filename: str, uploadFolder: str, filesize: int):
    if not os.path.exists(uploadFolder):
        os.mkdir(uploadFolder)
    file_decoded = base64.b64decode(file.split(',')[-1])
    secure_filename = werkzeug.utils.secure_filename(filename)
    file_path = os.path.join(uploadFolder, secure_filename)
    f = open(file_path, "wb")
    f.write(file_decoded)
    f.close()

    final_size =  os.path.getsize(file_path)
    return int(filesize) == int(final_size)

def create_lock_file():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    flask.g.UUID = uuid.uuid4()
    file_path = f'{LOCK_FOLDER}/{str(flask.g.UUID)}.txt'
    f = open(file_path, 'a')
    f.close()

def create_time_file():
    TIME_FOLDER = flask.current_app.config['TIME_FOLDER']
    if not os.path.exists(TIME_FOLDER):
        os.mkdir(TIME_FOLDER)
    file_path = f'{TIME_FOLDER}/time.txt'
    if not os.path.isfile(file_path):
        f = open(file_path, 'w')
        f.close()

    f = open(TIME_FOLDER + '/time.txt', 'w')
    f.write(str(time.time()))
    f.close()

def remove_lock_file():
    LOCK_FOLDER = flask.current_app.config['LOCK_FOLDER']
    os.remove(f'{LOCK_FOLDER}/{str(flask.g.UUID)}.txt')

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t


def is_model(geode_object):
    return geode_objects.objects_list()[geode_object]['is_model']

def is_3D(geode_object):
    return geode_objects.objects_list()[geode_object]['is_3D']

def get_builder(geode_object, data):
    return geode_objects.objects_list()[geode_object]['builder'](data)

def get_geographic_coordinate_systems(geode_object):
    if is_3D(geode_object):
        return og_gs.GeographicCoordinateSystem3D.geographic_coordinate_systems()
    else:
        return og_gs.GeographicCoordinateSystem2D.geographic_coordinate_systems()

def get_geographic_coordinate_systems_info(geode_object, crs):
    if is_3D(geode_object):
        return og_gs.GeographicCoordinateSystemInfo3D(crs['authority'], crs['code'], crs['name'])
    else:
        return og_gs.GeographicCoordinateSystemInfo2D(crs['authority'], crs['code'], crs['name'])

def asign_geographic_coordinate_system_info(geode_object, data, input_crs):
    builder = get_builder(geode_object, data)
    info = get_geographic_coordinate_systems_info(geode_object, input_crs)
    geode_objects.objects_list()[geode_object]['crs']['assign'](data, builder, input_crs['name'], info)

def convert_geographic_coordinate_system_info(geode_object, data, output_crs):
    builder = get_builder(geode_object, data)
    info = get_geographic_coordinate_systems_info(geode_object, output_crs)
    geode_objects.objects_list()[geode_object]['crs']['convert'](data, builder, output_crs['name'], info)
    