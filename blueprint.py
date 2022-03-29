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
    return flask.make_response({"message": "root"}, 200)

@routes.route('/ping', methods=['POST'])
def ping():
    if not os.path.isfile('./ping.txt'):
        f = open('./ping.txt', 'a')
        f.close()
    return flask.make_response({"message": "Flask server is running"}, 200)

@routes.route('/allowedfiles', methods=['POST'])
def allowedfiles():
    extensions = MakeList(type = 'input')
    return {"status": 200, "extensions": extensions}

@routes.route('/allowedobjects', methods=['POST'])
def allowedobjects():
    filename = flask.request.form.get('filename')
    if filename is None:
        return flask.make_response({"error_message": "No file sent"}, 400)
    file_extension = os.path.splitext(filename)[1:]
    print(file_extension)

    # # ObjectsList = GeodeObjects.ObjectsList()
    objects = MakeList(extension=file_extension)
    # # ListObjects(ObjectsList, file_extension[1:])
    return flask.make_response({"objects": objects}, 200)
    # return flask.make_response({}, 200)

@routes.route('/outputfileextensions', methods=['POST'])
def outputfileextensions():
    object = flask.request.form.get('object')
    if object is None:
        return flask.make_response({"error_message": "No object sent"}, 400)
    list = GeodeObjects.ObjectsList()[object]['output'].list_creators()
    # list = Make
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
        try:
            return flask.send_from_directory(directory=UPLOAD_FOLDER, path=newFileName, as_attachment=True, mimetype = "application/octet-binary")
        except FileNotFoundError:
            flask.make_response({"error_message": "File not found"}, 404)
    except Exception as e:
        print("error : ", str(e))
        return {"status": 500, "error_message": str(e)}

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
    List.sort()
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
    List.sort()
    return List  # Returns the final list

def MakeList(type: str = "",
            extension: str = ""):
    List = []  # Initiaslizes an empty list
    ObjectsList = GeodeObjects.ObjectsList() # Dict to loop through

    if type:
        for Object in ObjectsList.values():
            values = Object[type]
            for value in values:
                creators = value.list_creators()
                for creator in creators:  # Loop through
                    if creator not in List:  # If object's name isn't already in the list
                        List.append(creator)  # Adds the object's name to the list
    elif extension:
        for Object in ObjectsList.values():  # Loops through objects
            # If object can handle this extension
            inputs = Object['input']
            if inputs.has_creator(extension):
                if type not in List:  # If object's name isn't already in the list
                    List.append(type)  # Adds the object's name to the list
    List.sort()
    return List