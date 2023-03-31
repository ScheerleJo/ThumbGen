import json
import os
path = os.getcwd() + '\\cache\\filelocations.json'

def writeUpdatedPath(newPath:str, updatedParameter:str):

    with open(path, 'r') as file:
        data = json.load(file)
    i:int = 0

    for item in data:
        if item[0] == updatedParameter:
            data[i][1] = newPath
            break
        i += 1

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

# "calendarLocation"    [0][0-1]
# "docxLocation"        [1][0-1]
# "exportFolder"        [2][0-1]


def getPath(parameter:str):
    with open(path, 'r') as file:
        data = json.load(file)

    for item in data:
        if item[0] == parameter:
            location = item[1] 
            break
    return location