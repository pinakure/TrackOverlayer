import json

def elegant( filthy ):
    # TODO: move to tools
    return filthy.replace('_', ' ').replace('-', ' ').capitalize()

class Color:
    lime    = (128,255,0)
    banana  = (205,255,0)
    lichi   = (205,255,255)


def parseBool(string):
    string = str(string)
    return string.lower() in [ 'true', '1', 'yes']

def isBool(string):
    return string.lower() in [ 'true', 'false', '1', '0', 'yes', 'no']

def isInt(string):
    try:
        number = int( string )
        return True
    except:
        return False
    
def parseInt(string):
    return int(string)

def isFloat(string):
    try:
        number = float( string )
        return True
    except:
        return False

def parseFloat(string):
    return float(string)

def isColor(string):
    return (
        ( len(string) > 0 ) and 
        ( string[0] == '[' ) and 
        ( string[-1]== ']' )
    )
    
def parseColor(string):
    return json.loads(string)

def readfile(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except:
        return ""

def ascii(string):
    table = {
        'ū' : 'u',
        'à' : 'a',
        'è' : 'e',
        'ì' : 'i',
        'ò' : 'o',
        'ù' : 'u',
    }
    for key, value in table.items():
        string = string.replace(key, value)
    return str(string)
