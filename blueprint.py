import flask
import flask_cors
import os
import base64
import GeodeObjects
import werkzeug
import pkg_resources

routes = flask.Blueprint('routes', __name__)
flask_cors.CORS(routes)

@routes.route('/', methods=['GET'])
def root():
    return flask.make_response({"message": "root"}, 200)

@routes.route('/versions', methods=['GET'])
def versions():
    list_packages = ['OpenGeode-core', 'OpenGeode-IO', 'OpenGeode-Geosciences', 'OpenGeode-GeosciencesIO']
    list_with_versions = {}
    for package in list_packages:
        list_with_versions[package] = pkg_resources.get_distribution(package).version
    return flask.make_response({"versions": list_with_versions}, 200)

@routes.route('/ping', methods=['POST'])
def ping():
    if not os.path.isfile('./ping.txt'):
        f = open('./ping.txt', 'a')
        f.close()
    return flask.make_response({"message": "Flask server is running"}, 200)

@routes.route('/allowedfiles', methods=['POST'])
def allowedfiles():
    extensions = ListAllInputExtensions()
    return {"status": 200, "extensions": extensions}

@routes.route('/allowedobjects', methods=['POST'])
def allowedobjects():
    filename = flask.request.form.get('filename')
    if filename is None:
        return flask.make_response({"error_message": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1][1:]
    objects = ListObjects(file_extension)
    return flask.make_response({"objects": objects}, 200)

@routes.route('/outputfileextensions', methods=['POST'])
def outputfileextensions():
    object = flask.request.form.get('object')
    if object is None:
        return flask.make_response({"error_message": "No object sent"}, 400)
    list = ListOutputFileExtensions(object)
    return flask.make_response({"outputfileextensions": list}, 200)

@routes.route('/convertfile', methods=['POST'])
async def convertfile():
    try:
        UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
        object = flask.request.form.get('object')
        file = flask.request.form.get('file')
        filename = flask.request.form.get('filename')
        extension = flask.request.form.get('extension')
        
        if object is None:
            return flask.make_response({"error_message": "No object sent"}, 400)
        elif file is None:
            return flask.make_response({"error_message": "No file sent"}, 400)
        elif filename is None:
            return flask.make_response({"error_message": "No filename sent"}, 400)
        elif extension is None:
            return flask.make_response({"error_message": "No extension sent"}, 400)

        fileDecoded = base64.b64decode(file.split(',')[-1])
        filename = werkzeug.utils.secure_filename(filename)
        filePath = os.path.join(UPLOAD_FOLDER, filename)
        f = open(filePath, "wb") # wb = WriteBinary
        f.write(fileDecoded)
        f.close()
        model = GeodeObjects.ObjectsList()[object]['load'](filePath)
        strictFileName = os.path.splitext(filename)[0]
        newFileName = strictFileName + '.' + extension

        GeodeObjects.ObjectsList()[object]['save'](model, os.path.join(UPLOAD_FOLDER, newFileName))
        return flask.send_from_directory(directory=UPLOAD_FOLDER, path=newFileName, as_attachment=True, mimetype = "application/octet-binary")
    except FileNotFoundError:
        return flask.make_response({"error_message": "File not found"}, 404)
    except RuntimeError as e:
        return flask.make_response({"error_message": str(e)}, 500)
    except Exception as e:
        print("error : ", str(e))
        return flask.make_response({"error_message": str(e)}, 500)

def ListAllInputExtensions():
    """
    Purpose:
        Function that returns a list of all input extensions
    Returns:
        An ordered list of input file extensions
    """
    List = []  # Initiaslizes an empty list
    ObjectsList = GeodeObjects.ObjectsList() # Dict to loop through

    for Object in ObjectsList.values():
        values = Object['input']
        for value in values:
            list_creators = value.list_creators()
            for creator in list_creators:  # Loop through
                if creator not in List:  # If object's name isn't already in the list
                    List.append(creator)  # Adds the object's name to the listlist
    List.sort()
    return List  # Returns the final list

def ListObjects(extension: str):
    """
    Purpose:
        Function that returns a list of objects that can handle a file, given his extension
    Args:
        extension -- The extension of the file
    Returns:
        An ordered list of object's names
    """
    List = []  # Initializes an empty list
    ObjectsList = GeodeObjects.ObjectsList() # Dict to loop through

    for Object, values in ObjectsList.items():  # Loops through objects
        list_values = values['input']
        for value in list_values:
            if value.has_creator(extension):
                if Object not in List:  # If object's name isn't already in the list
                    List.append(Object)  # Adds the object's name to the list
    List.sort()
    return List  # Returns the final list

def ListOutputFileExtensions(object: str):
    """
    Purpose:
        Function that returns a list of output file extensions that can be handled by an object
    Args:
        object -- The name of the object
    Returns:
        An ordered list of file extensions
    """
    List = []  # Initializes an empty list
    ObjectsList = GeodeObjects.ObjectsList() # Dict to loop through

    values = ObjectsList[object]['output']
    for value in values:
        list_creators = value.list_creators()
        for creator in list_creators:  # Loop through
            if creator not in List:  # If object's name isn't already in the list
                List.append(creator)  # Adds the object's name to the listlist
    List.sort()
    return List  # Returns the final list
