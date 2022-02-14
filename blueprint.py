import flask
import flask_cors
import os
import base64
import GeodeObjects
import werkzeug

routes = flask.Blueprint('routes', __name__)
flask_cors.CORS(routes)

@routes.route('/', methods=['GET'])
def root():
    try: 
        return "root"
    except Exception as e:
        print(e)
        print(e.args)
        print(type(e))
        return {
            "error": str(e)
        }

@routes.route('/ping', methods=['POST'])
def ping():
    try:
        response = flask.jsonify(message="Simple server is running")
        if not os.path.isfile('./ping.txt'):
            f = open('./ping.txt', 'a')
            f.close()
        return response
    except Exception as e:
        print(e)
        print(e.args)
        print(type(e))
        return {
            "error": str(e)
        }

@routes.route('/allowedfiles', methods=['POST'])
def allowedfiles():
    try:
        ObjectsList = GeodeObjects.ObjectsList()
        response = flask.jsonify({"extensions": ListExtensions(ObjectsList)})
        return response
    except Exception as e:
        print(e)
        print(e.args)
        print(type(e))
        return {
            "error": str(e)
        }

@routes.route('/allowedobjects', methods=['POST'])
def allowedobjects():
    try:
        FileName = flask.request.form['fileName']
        (_, file_extension) = os.path.splitext(FileName)
        ObjectsList = GeodeObjects.ObjectsList()

        return {"status": 200, "objects": ListObjects(ObjectsList, file_extension[1:])}
    except Exception as e:
        print(e)
        print(e.args)
        print(type(e))
        return {
            "error": str(e)
        }

@routes.route('/outputfileextensions', methods=['POST'])
def outputfileextensions():
    try:
        object = flask.request.values['object']
        print(object)
        return flask.jsonify({"status": 200, "outputfileextensions": GeodeObjects.ObjectsList()[object]['output'].list_creators()})
    except Exception as e:
        print(e)
        return {
            "error": str(e)
        }

@routes.route('/convertfile', methods=['POST'])
async def convertfile():
    try:
        UPLOAD_FOLDER = flask.current_app.config['UPLOAD_FOLDER']
        object = flask.request.values['object']
        file = flask.request.values['file']
        filename = flask.request.values['filename']
        extension = flask.request.values['extension']

        print(object)
        print(filename)
        print(extension)

        fileDecoded = base64.b64decode(file.split(',')[1])
        filename = werkzeug.utils.secure_filename(filename)
        filePath = os.path.join(UPLOAD_FOLDER, filename)
        f = open(filePath, "wb") # wb = WriteBinary
        f.write(fileDecoded)
        f.close()
        model = GeodeObjects.ObjectsList()[object]['load'](filePath)

        strictFileName = os.path.splitext(filename)[0]
        newFileName = strictFileName + '.' + extension
        print(newFileName)
        GeodeObjects.ObjectsList()[object]['save'](model, os.path.join(UPLOAD_FOLDER, newFileName))
        try:
            return flask.send_from_directory(directory=UPLOAD_FOLDER, path=newFileName, as_attachment=True, mimetype = "application/octet-binary")
        except FileNotFoundError:
            flask.abort(404)
    except Exception as e:
        print(e)
        print(e.args)
        print(type(e))
        return {
            "error": str(e)
        }

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
