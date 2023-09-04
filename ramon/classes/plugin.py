from classes.preferences    import Preferences
from classes.log            import Log
import importlib, json, os
        
def px(value):
    return f'{value}px'

def pc(value):
    return f'{value}%'

def cvar(name, value):
    return f'--{name}:{value},'+"\n"

def sane( insane ):
    return insane.replace("'", "`").replace(r'\`', '`')

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


class Endpoints:

    
    def notifications():
        from classes.data import Data
        return sane(json.dumps(Data.notifications))
    
    
    def current_cheevo():
        from classes.data import Data
        return sane(json.dumps( Data.cheevo ))
    
    
    def username():
        return Preferences.settings['username']
    
    
    def twitch_username():
        return Preferences.settings['twitch-username']
    
    
    def recent():
        from classes.data import Data
        return sane(json.dumps([ [ r.name, r.description, r.picture] for r in Data.recent] ))
    
    
    def progress():
        from classes.data import Data
        return Data.progress
    
    
    def nop():
        return ''

    def getAll():
        return {
            'notifications'     : Endpoints.notifications(),
            'username'          : Endpoints.username(),
            'twitch-username'   : Endpoints.twitch_username(),
            'current-cheevo'    : Endpoints.current_cheevo().replace("'", "`"),
            'progress'          : Endpoints.progress(),
            'recent'            : Endpoints.recent(),
            'superchat'         : Endpoints.nop(),
        }

    byName = {
        'notifications'     : notifications,
        'username'          : username,
        'twitch-username'   : twitch_username,
        'current-cheevo'    : current_cheevo,
        'progress'          : progress,
        'recent'            : recent,
        'superchat'         : nop,
    }

class Plugin:

    loaded = {}
    width  = 1440
    debug  = False
    rate   = 5

    def __init__(self):
        import random
        self.template_data  = None
        self.rendered       = ''
        self.name           = 'new-plugin'
        self.description    = 'New plugin human description'
        self.width          = 1280
        self.height         = 1024
        self.z_index        = 0
        self.x              = 0
        self.y              = 0
        self.scale          = 1
        self.files          = []
        self.color          = f'rgb( { int(127 + (random.random()*128))}, { int(127 + (random.random()*128))}, { int(127 + (random.random()*128))})' # Debugging purposes
        self.settings       = {
            'enabled' : False,
        }
        self.endpoint       = None #defines which kind of data payload will be fed from @rendering
        self.template       = 'template.html'
    
    def templateVars(self):
        return {

        }


    
    def updateColor( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        varname =user_data
        plugin_name = sender.replace('plugin-setting-', '').split('-')[0]
        # print("SENDER: "+sender)
        # print("USRDAT: "+user_data)
        plugin = Plugin.loaded[ plugin_name ]
        value[0] = int( value[0] * 255)
        value[1] = int( value[1] * 255)
        value[2] = int( value[2] * 255)
        value[3] = int( value[3] * 255)
        plugin.settings[ varname ] = value
        Plugin.writeConfig()        
        plugin.run()

    
    def updateSettings( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        varname     = user_data
        plugin_name = sender.replace('plugin-setting-','').split('-')[0]
        plugin = Plugin.loaded[ plugin_name ]
        plugin.settings[ varname ] = value
        Plugin.writeConfig()
        plugin.run()
        Plugin.compose()

    
    def enable( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        enabled = dpg.get_item_configuration('enabled-plugins')['items']
        if not value in enabled:
            Plugin.loaded[value].settings['enabled'] = True
            Plugin.writeConfig()
            enabled.append( value )
            dpg.configure_item('enabled-plugins', items = enabled)
            # Re-generate overlay with enabled plugin
            Plugin.compose()
            # Run Plugin
            Plugin.loaded[value].run()
    
    
    def disable( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        enabled = dpg.get_item_configuration('enabled-plugins')['items']
        if value in enabled:
            Plugin.loaded[value].settings['enabled'] = False
            Plugin.writeConfig()
            enabled.remove( value )
            dpg.configure_item('enabled-plugins', items = enabled)
            # Re-generate overlay with enabled plugin
            Plugin.compose()
            # Run Plugin
            Plugin.loaded[value].run()

    def open(self):
        with open( f"{Preferences.settings['root']}/plugins/{self.name}/{self.template}", 'r') as file:
            self.template_data = file.read()

    def write(self):        
        with open( f"{Preferences.settings['root']}/data/{self.name}.css", 'w') as file:
            file.write( self.getCSS() )
        with open( f"{Preferences.settings['root']}/data/{self.name}.html", 'w') as file:
            file.write( self.rendered )
            
    def getCssAutoupdateSnippet():
        return r"""
        function updatecss(){
            console.log("Erasing css...");
            var rid = parseInt(Math.random()*655356);
            var par  = document.getElementsByTagName('head')[0];
            var old  = document.getElementsByTagName('link')[0];
            var link = document.createElement('link');
            link.rel = "stylesheet";
            link.type = "text/css";
            link.href = `./{% name %}.css?${ rid }`;
            par.append(link);
            setTimeout(function(){ old.remove();}, 500);
            setTimeout(updatecss, 1000);
        }
        updatecss();
        """
    
    def aux(payload):
        from io import StringIO        
        file = StringIO(payload)
        ini = {}
        for line in file:
            try :
                node = ini
                key, value = line.rstrip().split(' = ')
                *parents, key = key.split('-')
                for parent in parents:
                    node[parent] = node = node.get(parent, {})
                node[key] = value
            except Exception as E: 
                Log.error("Cannot translate plugin settings", E)            
        return ini

    def getLoadSettingsMethod(self):
        #sort variables longer first
        sorted = []
        longest = 1
        for key in self.settings.keys():
            if len(key)>longest: longest = len(key)
        for length in range(longest+1, 0, -1):
            for key in self.settings.keys():
                if len(key)==length: sorted.append(key)

        payload = ""
        for key in sorted:
            parts = key.split('-')
            o = len(parts)
            tkey = ''
            for i, pkey in enumerate(parts):
                tkey += pkey
                if i==o-1: 
                    # dirty workaround for quotes
                    if pkey in ["file", "font", "color"]:
                        continue
                    else:
                        payload+=f'{tkey} = '+'{%_'+tkey+'_%}\n'                        
                else:
                    tkey+='-'
        payload = json.dumps( Plugin.aux(payload) ).replace('"', '').replace('_', ' ')
        return "loadSettings    : function(){\n\t\t\t\t\ttry {\n\t\t\t\t\t\t{% Name %}.settings = JSON.parse(localStorage.getItem('{% name %}-settings'));\n\t\t\t\t\t\tsettings.update.rate = 1;\n\t\t\t\t\t} catch (e){\n\t\t\t\t\t\t{% Name %}.settings = "+payload+";\n\t\t\t\t\t}\n\t\t\t\t},"
             
    def injectScripts(self):
        from classes.dynamic_css import fonts
        for i in range(0,2):
            for key,value in {
                'Name'       : self.name.capitalize(),
                'name'       : self.name,
                'update-css' : Plugin.getCssAutoupdateSnippet(),
                'fonts'      : "\n\t\t".join([value for value in fonts.values()]),
                'plugin'     : "const False = false; const True = true;",
                'load-config': self.getLoadSettingsMethod(),
            }.items():         
                self.rendered = self.rendered.replace('{% '+key+' %}', str(value))        

    def injectSettings(self):
        #sort variables longer fists
        sorted = []
        longest = 1
        for key in self.settings.keys():
            if len(key)>longest: longest = len(key)
        for length in range(longest+1, 0, -1):
            for key in self.settings.keys():
                if len(key)==length: sorted.append(key)

        for key in sorted:
            value = self.settings[key]
            if   key.endswith('-color'  ) : value = f'rgba({value[0]},{value[1]},{value[2]},{value[3]})'
            self.rendered = self.rendered.replace('{% '+key+' %}', str(value))

    def render( self, payload='' ):
        Log.time()
        Log.info(f"Rendering plugin {self.name}...")
        self.open()
        payload = '' if payload is None else payload
        self.rendered = self.template_data
        # These 4 replaces are deprecated, remove en as soon as you replace all vars with django style scapes
        self.rendered = self.rendered.replace( '/*VARS*/'   , self.getVars()    )
        self.rendered = self.rendered.replace( '/*CSS*/'    , self.getCSS()     )
        self.rendered = self.rendered.replace( '<!--HTML-->', self.getHTML()    )
        self.rendered = self.rendered.replace( '/*JS*/'     , payload           )
        # Inject plugin settings in the template, Django style
        self.injectScripts()  # Note: These scripts can also inject variables before translation !
        self.injectSettings()
        self.write()
        Log.time(True)

    def getCVars(self):
        # Variables for the composer iframe which will hold the plugin widget inside
        payload = ''
        for key, value in self.composerVars().items():
            payload += f'--{self.name}-{key} : { value };'+'\n\t\t\t\t'
        return payload

    def getVars(self):
        # Variables for the plugin widget
        payload = ''
        for key, value in self.templateVars().items():
            payload += f'--{self.name}-{key} : { value };'+'\n'
        return payload

    def getHTML(self):
        return ''

    def translateJSVar(key, value):
        if   '-color'       in key: value = f'[{value[0]},{value[1]},{value[2]},{value[3]}]'
        elif '-file'        in key: value = f"`{value}`"
        elif '-font'        in key: value = f'`{value}`'
        return value

    def translateCSSVar(key, value):
        if   '-color'       in key: value = f'rgba({value[0]},{value[1]},{value[2]},{value[3]})'
        elif '-font-size'   in key: value = f'{value}px'
        elif '-width'       in key: value = f'{value}px'
        elif '-height'      in key: value = f'{value}px'
        elif 'pos-'         in key: value = f'{value}px'
        elif 'size-'        in key: value = f'{value}px'
        elif '-blur'        in key: value = f'{value}px'
        elif '-bold'        in key: value = "800" if value else "400"
        elif '-italic'      in key: value = "italic" if value else "normal"
        elif '-file'        in key: value = f"url('{value}')"
        elif '-font'        in key: value = f'"{value}"'
        return value

    def getCSS(self):
        payload = ':root {\n\t'
        for key,value in self.settings.items():            
            value = Plugin.translateCSSVar(key, value)
            if not value: continue
            payload += f'--{key.ljust(30, " ")} : {value};'+"\n\t"
        payload+='\n}\n'
        return payload
    
    def run(self):
        payload = None if not self.endpoint else Endpoints.byName[ self.endpoint ]()
        self.render(payload)
    
    def runLoaded():
        # Feed plugin with the data corresponding to its data endpoint (that data is refreshed each time Ramon.refresh is summoned)
        for name,plugin in Plugin.loaded.items():
            if not plugin.settings['enabled']: continue
            try:                
                plugin.run()
            except Exception as E:
                Log.error(f"Cannot run plugin {name}", E)    
        Plugin.autoupdate()        
    
    def cssRule(self):
        return f'#{self.name}'+'{'+f"""
            left        : var(--{self.name}-left);
            top         : var(--{self.name}-top);
            width       : var(--{self.name}-width);
            height      : var(--{self.name}-height);
            z-index     : var(--{self.name}-z-index);
            transform   : scale(var(--{self.name}-scale));
            { ('border: 2px dashed '+self.color+';') if Plugin.debug else ''} 
        """+'}\n\t\t\t'

    def iframe(self):
        return f'<iframe style="overflow: hidden;" id="{self.name}" autoplay="true" src="./{self.name}.html"></iframe>'+"\n\t\t"

    
    def toggleDebug():
        Plugin.debug = not Plugin.debug
        Log.verbose = Plugin.debug
        Plugin.compose()

    
    def compose():
        # Generates overlay.html file:
        # This file holds an iframe per each one of the plugins, shaping their geometry from info inside each plugin.py
        # so it will be the only file to be included in OBS, which contains all the plugins running at once in a single
        # document, lowering down CPU usage at OBS hopefully.
        # This action needs to be done once per execution, as all plugins load their configuration in loadtime, and that 
        # settings are hardcoded in each plugin.py file, so we will have to stick with static configuration for a while
        Log.time()
        #
        Log.info("Merging plugins into single overlay...")
        cvars = f'--width : {Plugin.width}px;'+'\n\t\t\t\t'
        css   = ".debug { display: inline-block; }" if Plugin.debug else ' .debug { display: none; }'
        html  = ""
        js    = ""
        data  = ""
        #
        # Get composer css vars, html nodes and css styles
        for name, plugin in Plugin.loaded.items():
            if plugin.settings['enabled']:
                cvars += plugin.getCVars()
                html  += plugin.iframe()
                css   += plugin.cssRule()
        # Get template
        try:
            with open(f'{Preferences.settings["root"]}/plugins/overlay.html', "r") as file:
                data = file.read()
        except Exception as E:
            Log.error("Cannot read Plugin Overlay template file", E)
        #
        # Inject payloads 
        data = data.replace( '/*VARS*/'   , cvars )
        data = data.replace( '/*CSS*/'    , css   )
        data = data.replace( '<!--HTML-->', html  )
        data = data.replace( '/*JS*/'     , js    )
        #
        # Dump data into rendered template
        try:
            with open(f'{Preferences.settings["root"]}/data/overlay.html', "w") as file:
                file.write( data )
        except Exception as E:
            Log.error("Cannot write Plugin Overlay template file", E)
        #
        # Create plugin data feeder js script 
        Plugin.autoupdate()
        Log.time(True)  

    
    def discover():
        path = f'{Preferences.root}/plugins'        
        return [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f)) and not f[0]=='_']

    
    def readConfig( ):
        with open(f'{Preferences.settings["root"]}/plugins.cfg', "r") as file: 
            config = file.read()
        lines    = config.split('\n')
        settings = {}
        current  = None
        for line in lines:
            if len(line)==0:continue
            if line[0] == '[':
                if current and current in Plugin.loaded.keys():
                    Plugin.loaded[current].settings = settings
                current  = line.strip('[').strip(']')
                settings = {} if not current in Plugin.loaded.keys() else Plugin.loaded[current].settings
                continue
            [ key, value ] = line.split('=')
            if isColor(value)   : value = parseColor(value)
            elif isInt(value)   : value = parseInt(value)
            elif isBool(value)  : value = parseBool(value)
            settings[ key ] = value
        if current and current in Plugin.loaded.keys():
            Plugin.loaded[current].settings = settings
            
    
    def writeConfig( ):
        config = ''
        for name, plugin in Plugin.loaded.items():
            config += f'[{ name }]'+"\n"
            settings = plugin.settings
            for key,value in settings.items():
                config += f'{ key }={ value }'+"\n"
        with open(f'{Preferences.settings["root"]}/plugins.cfg', "w") as file: 
            file.write(config)

    def autoupdate():
        from classes.data   import Data
        beat    = "setTimeout(function(){ document.getElementsByTagName('body')[0].style.backgroundColor = '#0000';},500);"
        reload  = "setTimeout(function(){ location.reload(); }, 5000);"
        body    = 'transition: background-color 500ms ease-in-out;' if Plugin.debug else ''
        ls      = { (f"""localStorage.setItem('{ plugin.name }-settings', '{ json.dumps(plugin.settings) }');"""+'\n') for name,plugin in Plugin.loaded.items()}
        ls.update({ (f"""localStorage.setItem('{ name        }'         , '{ value                       }');"""+'\n') for name,value in Endpoints.getAll().items()})
        payload = f'''<!DOCTYPE html>
</head>
    <body style="width: 100%; height:100%; overflow: hidden; {body}">
        <script>
            document.getElementsByTagName('body')[0].style.backgroundColor = '#0f0';
            localStorage.setItem('debug', '{1 if Plugin.debug else 0 }'  );
            {"".join(ls)}
            { beat if Plugin.debug else '' }
            {reload}
        </script>
    </body>
</html>'''
        try:
            with open(f'{Preferences.settings["root"]}/data/autoupdate.html', "w") as file:
                file.write( payload )
            Data.notifications = []
        except Exception as E:
            Log.error("Cannot write Autoupdate data script file", E)
        return payload


    
    def load( name ):
        Log.info(f"Loading Plugin '{name}'")
        try:
            Log.time()
            module_name = f'plugins.{name}.plugin'
            module = importlib.import_module( module_name, '' )
            Plugin.loaded[ name ] = module.plugin()            
            Plugin.readConfig()
            if Plugin.loaded[ name ].settings['enabled']:
                # Install required files at data folder, if any specified in plugin.py
                files = Plugin.loaded[ name ].files            
                if len(files):
                    for file in files:
                        if not os.path.exists(f'{Preferences.settings["root"]}/data/{file}'):
                            try:
                                Log.info(f"Copying {name} plugin required file '{file}'...")
                                with open(f'{Preferences.root}/plugins/{name}/{file}', 'rb') as fpin:
                                    with open(f'{Preferences.root}/data/{file}', "wb") as fpout:
                                        fpout.write(fpin.read())
                            except Exception as E:
                                Log.error("Cannot read/write required file", E)
            Log.time(True)  
        except Exception as E:
            Log.error(f'Cannot load Plugin {name}', E)
