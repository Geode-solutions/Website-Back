import GeodeObjects

def MakeList(object: str = "",
            type: str = "",
            entension: str =""):
    ObjectsList = GeodeObjects.ObjectsList()
    List = []

    if object == "":
        if entension == "":
            for values in ObjectsList.values():  # Loops through objects
                # List of extensions this object can handle
                Creators = values[type].list_creators()
                for Creator in Creators:  # Loop through
                    if Creator not in List:  # If object's name isn't already in the list
                        List.append(Creator)  # Adds the object's name to the list
    elif entension == "":
        if type == "input":
            for type, values in ObjectsList.items():  # Loops through objects
                # If object can handle this extension
                if values['input'].has_creator(entension):
                    if type not in List:  # If object's name isn't already in the list
                        List.append(type)  # Adds the object's name to the list
        elif type == "output":

    List.sort()
    return List

print(MakeList(object = "", type = "input"))