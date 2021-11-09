import flask
import flask_cors
import os
import opengeode  # Importe le package OpenGeode
import base64
import GeodeObjects
import threading

import sched
import time
s = sched.scheduler(time.time, time.sleep)

time_to_sleep = 20


def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    killIfNotAlive()
    s.enter(time_to_sleep, 1, do_something, (sc,))


app = flask.Flask(__name__)
flask_cors.CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

toto = True
text = "Empty"


def update_toto(value):
    listOfGlobals = globals()
    listOfGlobals['toto'] = value
    # global toto
    # toto = value


def update_text(value):
    listOfGlobals = globals()
    listOfGlobals['text'] = value
    # global text
    # text = value


@app.route('/')
def testRoute():
    return "Coucou !!"


def set_interval(func, sec):
    # print("interval")

    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def killIfNotAlive():
    # global toto
    # global text
    print("toto", toto, flush=True)
    print("text", text, flush=True)
    if not toto:
        os._exit(0)
    else:
        update_toto(False)


@app.route('/ping', methods=['POST'])
def Revive():
    print("toto 2", toto, flush=True)
    print("text 2", text, flush=True)
    update_text("Set")
    update_toto(True)
    print("toto 3", toto, flush=True)
    print("text 3", text, flush=True)
    return {"status": 200}


@app.route('/allowedfiles', methods=['POST'])
@flask_cors.cross_origin()
def AllowedFiles():
    ObjectsList = GeodeObjects.ObjectsList()
    return {"extensions": ListExtensions(ObjectsList)}


@app.route('/allowedObjects', methods=['POST'])
def AllowedObjects():
    FileName = flask.request.form['fileName']
    (_, file_extension) = os.path.splitext(FileName)
    ObjectsList = GeodeObjects.ObjectsList()
    return {"objects": ListObjects(ObjectsList, file_extension[1:])}


@app.route('/readfile', methods=['POST'])
def UploadFile():
    if flask.request.method == 'POST':
        File = flask.request.form['file']
        if File == '':  # Si pas de fichier
            return {"status": 500}
        if File:  # Si fichier présent
            FileDecoded = base64.b64decode(File.split(',')[1])
            filename = os.path.join(
                app.config['UPLOAD_FOLDER'], flask.request.form['filename'])
            f = open(filename, "wb")
            f.write(FileDecoded)  # Writes in the file
            f.close()  # Closes

            # model = opengeode.load_brep(filename)
            model = getattr(opengeode, "load_brep")(filename)
            return {"status": 200, "nb surfaces": model.nb_surfaces(), "name": model.name()}


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


if __name__ == '__main__':

    if not os.path.exists("./uploads"):
        os.mkdir("./uploads")

    # set_interval(killIfNotAlive, 20)

    s.enter(time_to_sleep, 1, do_something, (s,))
    s.run()

    app.run(debug=True, host='0.0.0.0', port=5000)  # If main run in debug mode
    # flask_cors.CORS(app)
