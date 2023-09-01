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

class Endpoints:

    @staticmethod
    def autoupdate():
        from classes.data import Data
        payload = """<body style="width: 100%; height:100%; overflow: hidden; """+(f"""transition: background-color 500ms ease-in-out; " >""" if Plugin.debug else '">')+f"""
        <script>
            document.getElementsByTagName('body')[0].style.backgroundColor = '#0f0';
            localStorage.setItem('current-cheevo'   ,  {Endpoints.current_cheevo().replace("'", "`")  }   );
            localStorage.setItem('cheevo-progress'  , '{Endpoints.progress()        }'  );
            localStorage.setItem('username'         , '{Endpoints.username()        }'  );
            localStorage.setItem('twitch-username'  , '{Endpoints.twitch_username() }'  );
            localStorage.setItem('notifications'    , '{Endpoints.notifications()   }'  );
            """+"""
            setTimeout(function(){ location.reload(); }, 5000);
            """+("""setTimeout(function(){ document.getElementsByTagName('body')[0].style.backgroundColor = '#0000';},500);""" if Plugin.debug else "")+"""
            console.clear();
            console.log(JSON.parse(localStorage.getItem('notifications')));
            </script></body>"""
        try:
            with open(f'{Preferences.settings["root"]}/data/autoupdate.html', "w") as file:
                file.write( payload )
            Data.notifications = []
        except Exception as E:
            Log.error("Cannot write Autoupdate data script file", E)
        return payload

    @staticmethod
    def notifications():
        from classes.data import Data
        return sane(json.dumps(Data.notifications))
    
    @staticmethod
    def current_cheevo():
        from classes.data import Data
        return sane(json.dumps( Data.cheevo ))
    
    @staticmethod
    def username():
        return Preferences.settings['username']
    
    @staticmethod
    def twitch_username():
        return Preferences.settings['twitch-username']
    
    @staticmethod
    def progress():
        from classes.data import Data
        return Data.progress
    
    byName = {
        'notifications'     : notifications,
        'username'          : username,
        'twitch-username'   : twitch_username,
        'current-cheevo'    : current_cheevo,
        'progress'          : progress,
    }

class Plugin:

    loaded = {}
    width  = 1440
    debug  = False

    def __init__(self):
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
        self.endpoint       = None #defines which kind of data payload will be fed from @rendering
        self.template       = 'template.html'
    
    def open(self):
        with open( f"{Preferences.settings['root']}/plugins/{self.name}/{self.template}", 'r') as file:
            self.template_data = file.read()

    def write(self):
        with open( f"{Preferences.settings['root']}/data/{self.name}.html", 'w') as file:
            file.write( self.rendered )

    def render( self, payload='' ):
        Log.time()
        Log.info(f"Rendering plugin {self.name}...")
        self.open()
        payload = '' if payload is None else payload
        self.rendered = self.template_data
        self.rendered = self.rendered.replace( '/*VARS*/'   , self.getVars()    )
        self.rendered = self.rendered.replace( '/*CSS*/'    , self.getCSS()     )
        self.rendered = self.rendered.replace( '<!--HTML-->', self.getHTML()    )
        self.rendered = self.rendered.replace( '/*JS*/'     , payload           )
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

    def getCSS(self):
        return ''

    @staticmethod
    def runLoaded():
        # Feed plugin with the data corresponding to its data endpoint (that data is refreshed each time Ramon.refresh is summoned)
        for name,plugin in Plugin.loaded.items():
            try:
                payload = None if not plugin.endpoint else Endpoints.byName[ plugin.endpoint ]()
                plugin.render(payload)
            except Exception as E:
                Log.error(f"Cannot run plugin {name}", E)    
        Endpoints.autoupdate()        
    
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
        return f'<iframe id="{self.name}" autoplay="true" src="./{self.name}.html"></iframe>'+"\n\t\t"

    @staticmethod
    def toggleDebug():
        Plugin.debug = not Plugin.debug
        Log.verbose = Plugin.debug
        Plugin.compose()

    @staticmethod
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
        css   = "body { border: 1px dotted #f80; }" if Plugin.debug else ''
        html  = ""
        js    = ""
        data  = ""
        #
        # Get composer css vars, html nodes and css styles
        for name, plugin in Plugin.loaded.items():
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
        Endpoints.autoupdate()
        Log.time(True)  

    @staticmethod
    def discover():
        path = f'{Preferences.root}/plugins'        
        return [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f)) and not f[0]=='_']

    @staticmethod
    def load( name ):
        Log.info(f"Loading Plugin '{name}'")
        try:
            Log.time()
            module_name = f'plugins.{name}.plugin'
            module = importlib.import_module( module_name, '' )
            Plugin.loaded[ name ] = module.plugin()
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
