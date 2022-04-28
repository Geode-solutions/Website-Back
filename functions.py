import GeodeObjects

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
