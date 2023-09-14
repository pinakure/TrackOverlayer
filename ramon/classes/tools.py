import json, os

def elegant( filthy ):
    return filthy.replace('_', ' ').replace('-', ' ').capitalize()

class Color:
    lime    = (128,255,0)
    banana  = (205,255,0)
    lichi   = (205,255,255)
    grape   = (180,  0,255)


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

def px(value):
    return f'{value}px'

def pc(value):
    return f'{value}%'

def cvar(name, value):
    return f'--{name}:{value},'+"\n"

def sane( insane ):
    return insane.replace("'", "`").replace(r'\`', '`')

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

def jsvalue(value, name=''):
    if isinstance( value, bool ): return 'true' if value else 'false'
    if isinstance( value, float): return value
    if isinstance( value, int  ): return value
    if isinstance( value, list ): return f'rgba({value[0],value[1],value[2],value[3]})' if 'color' in name else json.dumps(value)
    if isinstance( value, str  ): return f'"{value}"'
    return 'non-interpretable-property'
        
def tag( name ):
    return '{% '+name+' %}'

def templatetag( name ):
    return '{%_'+name+'_%}'

def mkdir(dirname):
    from classes.preferences import Preferences
    if not os.path.exists(f'{Preferences.root}/{dirname}'):
        #Log.info(f"PLUGIN : Created directory '{dirname}'")
        os.mkdir(f'{Preferences.root}/{dirname}')
    else:
        #Log.info(f"PLUGIN : Using directory '{dirname}'")
        pass
