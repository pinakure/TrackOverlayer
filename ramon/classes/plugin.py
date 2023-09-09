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

    debug = False
    
    def notifications():
        from classes.ramon import Ramon
        return sane(json.dumps(Ramon.data.notifications))
    
    
    def current_cheevo():
        from classes.ramon import Ramon
        from classes.plugin import Plugin        
        return sane(json.dumps( Ramon.data.cheevo if not Plugin.debug else "Test cheevo\nTest description"))
    
    def username():
        return Preferences.settings['username'] 
    
    
    def twitch_username():
        return Preferences.settings['twitch-username']
    
    
    def recent():
        from classes.ramon import Ramon
        return sane(json.dumps([ [ r.name, r.description, r.picture] for r in Ramon.data.recent] ))
    
    
    def progress():
        from classes.ramon import Ramon
        from classes.plugin import Plugin
        if Plugin.debug: 
            import random
            Ramon.data.progress = f'{str(int(random.random()*100))}%'
        return Ramon.data.progress 
    
    def last_progress():
        from classes.ramon import Ramon
        lp = Ramon.data.last_progress if Ramon.data.last_progress != '' else Ramon.data.progress
        Ramon.data.last_progress = Ramon.data.progress
        return lp
    
    
    def nop():
        return ''

    def getAll():
        return {
            'notifications'     : Endpoints.notifications(),
            'username'          : Endpoints.username(),
            'twitch-username'   : Endpoints.twitch_username(),
            'current-cheevo'    : Endpoints.current_cheevo().replace("'", "`"),
            'progress'          : Endpoints.progress(),
            #'last-progress'     : Endpoints.last_progress(),
            'recent'            : Endpoints.recent(),
            'superchat'         : Endpoints.nop(),
        }

    byName = {
        'notifications'     : notifications,
        'username'          : username,
        'twitch-username'   : twitch_username,
        'current-cheevo'    : current_cheevo,
        'progress'          : progress,
        #'last-progress'     : last_progress,
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
    
    def updateComboSettings( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        setname     = user_data.split(':')[0]
        varname     = user_data.split(':')[1]
        plugin_name = sender.replace('plugin-setting-','').split('-')[0]
        plugin = Plugin.loaded[ plugin_name ]
        plugin.settings[ varname ] = f'{setname}:{value}'
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
        with open( f"{Preferences.settings['root']}/data/css/{self.name}.css", 'w') as file:
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
            link.href = `./css/{% name %}.css?${ rid }`;
            par.append(link);
            setTimeout(function(){ old.remove();}, 500);
            setTimeout(updatecss, 1000);
        }
        updatecss();
        """
    
    def getAutoHideSnippet():
        return r"""
        if({% Name %}.settings.auto.hide){
            current_cheevo = localStorage.getItem('current-cheevo').replaceAll('"', '');
            if (current_cheevo!=''){
                {% Name %}.dom.{% name %}.style.display = "inline-block";                        
            } else {
                {% Name %}.dom.{% name %}.style.display = "none";                        
            }
        }
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
    
    def getFrameworkMethods(self):
        return self.getLoadSettingsMethod() + r"""
                
                standalone : true,

                send  : function(msg, data=[]){
                    window.parent.postMessage(`{% name %}|${msg}|${JSON.stringify(data)}`, '*');
                },

                log   : {
                    print : function(text){
                        window.parent.postMessage(`{% name %}|print|${text}`, '*');
                    },
                    clear : function(text){
                        window.parent.postMessage("|log-clear|", '*');
                    }
                },

                messageHandler : function(){
                    // 'Event coming from parent' handler 
                    window.addEventListener('message', function(e) {
                        try{ message = e.data.split('|')[0]; } catch(e){ {% name %}.log.print(`Malformed message: ${e.data}`); return; }
                        try{ data = JSON.parse(e.data.split('|')[1]); } catch(e){data = null;}
                        switch( message ){
                            
                            case 'update-css':
                                var rid = parseInt(Math.random()*655356);
                                var par  = document.getElementsByTagName('head')[0];
                                var old  = document.getElementsByTagName('link')[0];
                                var link = document.createElement('link');
                                link.rel = "stylesheet";
                                link.type = "text/css";
                                link.href = `./css/{% name %}.css?${ rid }`;
                                par.append(link);
                                {% Name %}.log.print("style updated");
                                return;

                            case 'update-settings':
                                {% Name %}.settings = data;
                                {% Name %}.log.print("settings updated");
                                {% Name %}.send('request-data');
                                return;
                                
                            case 'update-data':
                                {% Name %}.standalone = false;
                                {% Name %}.update();
                                {% Name %}.log.print("data updated");
                                return;
                            
                            default:
                                try { 
                                    {% Name %}.handleMessage( message, data );
                                } catch(e){
                                    {% Name %}.log.print(`Error ${e}`);
                                }
                        }
                    });
                },
                """

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
             
    def getPluginList():
        return 'plugins: {'+",".join([f"{x}:undefined" for x in Plugin.loaded.keys() if Plugin.loaded[x].settings['enabled']])+"},"

    def injectScripts(self):
        from classes.dynamic_css import fonts
        from dearpygui import dearpygui as dpg
                
        for i in range(0,2):
            for key,value in {
                'Name'              : self.name.capitalize(),
                'name'              : self.name,
                'fullsized'         : "html { width : 100%; height : 100%; } body { width : 100%; height : 100%; top: 0px; left: 0px; } html { position: absolute; } body { position: absolute; }",
                'framework'         : self.getFrameworkMethods(),
                'plugin'            : "const False = false; const True = true; alternate='alternate'; forwards='forwards'; backwards='backwards';",
                'debug'             : 'true' if Plugin.debug else 'false',
                'password'          : dpg.get_value('twitch-password'),
                # deprecated
                'fonts'             : "\n\t\t".join([value for value in fonts.values()]),
                'update-css'        : Plugin.getCssAutoupdateSnippet() if Plugin.debug else '',
                'load-config'       : self.getLoadSettingsMethod(),
                'require-cheevo'    : Plugin.getAutoHideSnippet(),
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
        Endpoints.debug = Plugin.debug
        Log.verbose = Plugin.debug
        Preferences.settings['debug'] = Plugin.debug
        Plugin.runLoaded()
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
        data = data.replace( '/*VARS*/'     , cvars )
        data = data.replace( '/*CSS*/'      , css   )
        data = data.replace( '<!--HTML-->'  , html  )
        data = data.replace( '/*JS*/'       , js    )
        data = data.replace( '{% plugins %}', Plugin.getPluginList())
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
            elif isFloat(value) : value = parseFloat(value)
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
        from classes.ramon   import Ramon
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
            window.parent.postMessage('auto-update|auto-update|', '*');
            {reload}
        </script>
    </body>
</html>'''
        try:
            with open(f'{Preferences.settings["root"]}/data/autoupdate.html', "w") as file:
                file.write( payload )
            Ramon.data.notifications = []
        except Exception as E:
            Log.error("PLUGIN : Cannot write Autoupdate data script file", E)
        return payload

    #HACK: repeated code (first reference at Ramon.mkdir )
    def mkdir(dirname):
        if not os.path.exists(f'{Preferences.root}/{dirname}'):
            #Log.info(f"PLUGIN : Created directory '{dirname}'")
            os.mkdir(f'{Preferences.root}/{dirname}')
        else:
            #Log.info(f"PLUGIN : Using directory '{dirname}'")
            pass
    
    def copyDir(self, dirname):
        # Recursively copy a given directory
        if not os.path.exists( dirname ):return False        
        dirfiles    = os.listdir( dirname )
        # select all child dirs but leave out those beginning with '.' 
        
        dirs = [ x  for x in dirfiles if os.path.isdir(f'{dirname}/{x}') and x[0] != '.']
        # before copying any file of this dir, copy child dirs if any
        for dir in dirs:
            self.copyDir(f'{dirname}/{dir}')
        # select all files but leave out those beginning with '.'
        files = [ x for x in dirfiles if os.path.isfile(f'{dirname}/{x}') and x[0] != '.' ]
        # finally copy the files
        if len(files):
            for file in files:
                if not self.copy(f'{dirname}/{file}'):
                    return False
        return True

    def install( self ):
        # Add files under 'files' directory in each plugin to be automatically detected
        file_path   = f'{Preferences.root}/plugins/{self.name}/files'
        if os.path.exists(file_path):
            if not self.copyDir( file_path ):
                return False
            
        # Copy files declared in plugin.py definition
        if len(self.files):
            for file in self.files:
                if not self.copy( f'{Preferences.root}/plugins/{self.name}/{file}' ):
                    return False
        return True
    
    def copy( self, filename):
        # If initial filename is in a directory structure
        part = filename.split(f'plugins/{self.name}/')[1].split('/')
        file = part[-1]
        dirs = part[0:-1]
        dir_accumulated = f'{Preferences.root}/data' 
        if len(dirs):
            # Make sure it exist before trying to copy any file into.
            # Always create the files in data as fsroot
            for dir in dirs:
                dir_accumulated += f'/{dir}'
                Plugin.mkdir( dir_accumulated )
        outfile = f'{ dir_accumulated }/{ file }' 
        if os.path.exists(outfile): return True
        try:
            Log.info(f"Copying {self.name} plugin required file '{filename}'...")
            with open( filename , 'rb') as fpin:
                with open( outfile, "wb") as fpout:
                    fpout.write(fpin.read())
            return True
        except Exception as E:
            Log.error(f"{ self.name } : Failed to copy required file", E)
            return False

    
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
                if not Plugin.loaded[ name ].install():
                    Log.error(f"Cannot install required files for plugin { Plugin.loaded[ name ] }")
                    Plugin.loaded[ name ].enabled = False
                
            Log.time(True)  
        except Exception as E:
            Log.error(f'Cannot load Plugin {name}', E)
