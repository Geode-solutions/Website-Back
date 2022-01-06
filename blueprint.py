import flask
import flask_cors
import os
import opengeode  # Importe le package OpenGeode
import base64
import GeodeObjects
import threading

routes = flask.Blueprint('routes', __name__)
flask_cors.CORS(routes)
isAlive = False


def update_or_kill(update):
    global isAlive
    print("T", threading.get_ident())
    if update:
        isAlive = True
    else:
        if not isAlive:
            os._exit(0)
        else:
            print("isAlive", isAlive, flush=True)
            isAlive = False
            print("isAlive", isAlive, flush=True)


def set_interval(func, args, sec):
    def func_wrapper():
        set_interval(func, args, sec)
        func(args)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


@routes.route('/', methods=['GET'])
def root():
    return "root"


@routes.route('/start', methods=['POST'])
def start():
    print(isAlive)
    set_interval(update_or_kill, False, 40)
    print(isAlive)
    return {"status": 200}


@routes.route('/ping', methods=['GET'])
def ping():
    response = flask.jsonify(message="Simple server is running")
    update_or_kill(True)
    return response


@routes.route('/allowedfiles', methods=['GET'])
def allowedfiles():
    ObjectsList = GeodeObjects.ObjectsList()
    response = flask.jsonify({"extensions": ListExtensions(ObjectsList)})
    return response


@routes.route('/allowedobjects', methods=['GET', 'OPTIONS'])
def allowedobjects():
    FileName = flask.request.form['fileName']
    (_, file_extension) = os.path.splitext(FileName)
    ObjectsList = GeodeObjects.ObjectsList()
    return {"objects": ListObjects(ObjectsList, file_extension[1:])}


@routes.route('/readfile', methods=['GET'])
def readfile():
    UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
    File = flask.request.form['file']
    if File:
        FileDecoded = base64.b64decode(File.split(',')[1])
        filename = os.path.join(UPLOAD_FOLDER, flask.request.form['filename'])
        f = open(filename, "wb")
        f.write(FileDecoded)  # Writes in the file
        f.close()  # Closes

        model = opengeode.load_brep(filename)
        # model = getattr(O_G, "load_brep")(filename)
        return {"status": 200, "nb surfaces": model.nb_surfaces(), "name": model.name()}
    else:
        return {"status": 500}


def ListObjects(ObjectsList, Extension):
    """
    Purpose:
        Function that returns a list of objects that can handle the file, given his extension
    Args:
        Extension -- The exention of the file
        ObjectsList -- A list of objects with their InputFactory/OutputFactory/Name
    Returns:
        An ordered list of object's names
    """
    List = []  # Initializes an empty list
    for type, values in ObjectsList.items():  # Loops through objects
        # If object can handle this extension
        if values['input'].has_creator(Extension):
            if type not in List:  # If object's name isn't already in the list
                List.append(type)  # Adds the object's name to the list
    return List  # Returns the final list


def ListExtensions(ObjectsList):
    """
    Purpose:
        Function that returns a list of extensions that can handled by the objects given in parameter
    Args:
        ObjectsList -- A list of objects with their InputFactory/OutputFactory/Name
    Returns:
        An ordered list of file extensions
    """
    List = []  # Initializes an empty list
    for values in ObjectsList.values():  # Loops through objects
        # List of extensions this object can handle
        Creators = values['input'].list_creators()
        for Creator in Creators:  # Loop through
            if Creator not in List:  # If object's name isn't already in the list
                List.append(Creator)  # Adds the object's name to the list
    return List  # Returns the final list
