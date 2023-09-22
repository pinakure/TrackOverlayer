from classes.preferences    import Preferences
from classes.tools          import parseBool, parseColor, parseFloat, parseInt
from classes.tools          import isBool   , isColor   , isFloat   , isInt
from classes.tools          import jsvalue, mkdir
from classes.endpoints      import Endpoints
from classes.tools          import tag, templatetag
from classes.log            import Log
from classes.icons          import Icons
from classes.tags           import Tags
import importlib, json, os

class Plugin:

    loaded  = {}
    width   = 1440
    debug   = False
    rate    = 5
    
    def __init__(self, name):
        import random
        self.template_data  = None
        self.rendered       = ''
        self.name           = name
        self.description    = 'New plugin human description'
        self.width          = 1280
        self.height         = 1024
        self.z_index        = 0
        self.x              = 0
        self.y              = 0
        self.scale          = 1
        self.interactive    = False
        self.files          = []
        self.color          = f'rgb( { int(127 + (random.random()*128))}, { int(127 + (random.random()*128))}, { int(127 + (random.random()*128))})' # Debugging purposes
        self.defaults       = {}
        self.dicts          = ''
        self.strings        = []
        self.edit           = False
        self.settings       = {
            'enabled'   : False,
            'pos-x'     : 0,
            'size-x'    : 128,
            'pos-y'     : 0,
            'size-y'    : 128,
        }
        self.endpoint       = None #defines which kind of data payload will be fed from @rendering
        self.template       = 'template.html'
        self.setRangedCombo ('angle'        , -180,  180)
        self.setRangedCombo ('zoom'         ,     1, 100)
        self.setRanged      ('pos-x'        , -1444,1444)
        self.setRanged      ('pos-y'        , -1080,1080)
        self.setRanged      ('size-x'       ,     1,1444)
        self.setRanged      ('size-y'       ,     1,1080)
        self.setRanged      ('border-radius',     0, 128)
        self.setRanged      ('perspective'  ,     1,1600)
        
        self.setHelp        ('auto-hide' , "Automatically hide plugin when no game or cheevo is selected")

    
    def setup(self, settings):
        self.settings.update(settings)
        self.introspect()

    def introspect(self):
        # Search for special values in settings and take note of them:
        
        # combo dictionaries
        self.dicts = []
        for k,v in self.settings.items():
            if not isinstance(v, str): continue
            if v.find('|') > 0:
                self.dicts.append(v.split('|')[0])

    def dumpDicts(self):
        dicts = []
        for dictname in self.dicts:
            obj = eval(f'self.{dictname}')
            jsvars = [ f"{ k } : { jsvalue(v,k) }" for k,v in obj.items()]
            dicts.append( dictname + ' : {\n' + ",\n\t".join( jsvars ) + "}," )
        return '\n'.join(dicts)

    def templateVars(self):
        return {

        }

    def saveDefaults(self):
        self.defaults.update(self.settings)

    def toggleEdit(sender, value, plugin):
        from classes.server import Server
        import asyncio
        Plugin.loaded[plugin].edit ^= 1
        Plugin.compose()
        #6asyncio.run(Server.send('reload', { 'plugin' : plugin } ))
        

    def setDefaults(sender, value, plugin):
        from dearpygui import dearpygui as dpg
        self = Plugin.loaded[plugin]
        for key,value in self.defaults.items():
            if key=='enabled': continue
            target = f'plugin-setting-{plugin}-{key}'
            dpg.set_value(target, value)
            self.settings[key] = value
        Plugin.writeConfig()

    def updateColor( sender=None, value=None, user_data=None ):
        varname =user_data
        plugin_name = sender.replace('plugin-setting-', '').split('-')[0]
        plugin = Plugin.loaded[ plugin_name ]
        value[0] = int( value[0] * 255)
        value[1] = int( value[1] * 255)
        value[2] = int( value[2] * 255)
        value[3] = int( value[3] * 255)
        plugin.settings[ varname ] = value
        Plugin.writeConfig()        
        plugin.run()
    
    def selectFilename( sender=None, value=None, user_data=None ):
        from dearpygui import dearpygui as dpg
        dpg.configure_item('file_dialog_id', user_data=user_data)
        dpg.show_item('file_dialog_id')

    def updateFilenameSetting( sender=None, value=None, user_data=None ):
        from dearpygui      import dearpygui as dpg
        from classes.ramon  import Ramon
        dpg.hide_item('file_dialog_id')
        sender      = user_data
        varname     = user_data
        try:
            filename    = list(value['selections'].keys())[0]
            print(value)
        except Exception as E:
            Log.error("Cannot update file field", E)
            return 
        dpg.configure_item(sender, label=filename)
        if filename == '': return
        plugin_name = sender.replace('plugin-setting-','').split('-')[0]
        varname = sender.replace(f'plugin-setting-{plugin_name}-','')
        plugin = Plugin.loaded[ plugin_name ]
        plugin.settings[ varname ] = filename
        Plugin.writeConfig()
        plugin.run()
        Ramon.redraw()
        
    def updateSettings( sender=None, value=None, user_data=None ):
        from classes.ramon  import Ramon
        from dearpygui import dearpygui as dpg
        varname     = user_data
        plugin_name = sender.replace('plugin-setting-','').split('-')[0]
        plugin = Plugin.loaded[ plugin_name ]
        plugin.settings[ varname ] = value.replace('|', '') if isinstance(value, str) else value
        Plugin.writeConfig()
        plugin.run()
        Ramon.redraw()
    
    def updateComboSettings( sender=None, value=None, user_data=None ):
        from classes.ramon  import Ramon
        from dearpygui import dearpygui as dpg
        setname     = user_data.split('|')[0]
        varname     = user_data.split('|')[1]
        
        plugin_name = sender.replace('plugin-setting-','').split('-')[0]
        plugin = Plugin.loaded[ plugin_name ]
        plugin.settings[ varname ] = f'{setname}|{value}'
        Plugin.writeConfig()
        plugin.run()
        Ramon.redraw()

    def setRangedCombo(self, varname, min, max):
        from classes.config import ranges,combos
        self.setRanged(varname, min, max)
        combos.append(f'plugin-setting-{self.name}-{varname}')

    def setRanged(self, varname, min, max):
        from classes.config import ranges,combos
        ranges.update({
            f'plugin-setting-{self.name}-{varname}' : [ min, max],
        })
    
    def setHelp(self, varname, text):
        from classes.config import help
        help.update({
            f'plugin-setting-{self.name}-{varname}' : text,
        })

    def enable( sender=None, value=None, user_data=None ):
        from classes.ramon  import Ramon
        from dearpygui      import dearpygui as dpg
        enabled = dpg.get_item_configuration('enabled-plugins')['items']
        if not value in enabled:
            Plugin.loaded[value].settings['enabled'] = True
            Plugin.writeConfig()
            enabled.append( value )
            dpg.configure_item('enabled-plugins', items = enabled)
            # Run Plugin
            Plugin.loaded[value].run()
            # Re-generate overlay with enabled plugin
            Plugin.compose()
            # Redraw interface. ¿¿¿why???
            Ramon.redraw()
    
    def disable( sender=None, value=None, user_data=None ):
        from classes.ramon  import Ramon
        from dearpygui      import dearpygui as dpg
        enabled = dpg.get_item_configuration('enabled-plugins')['items']
        if value in enabled:
            Plugin.loaded[value].settings['enabled'] = False
            Plugin.writeConfig()
            enabled.remove( value )
            dpg.configure_item('enabled-plugins', items = enabled)
            # Run Plugin
            Plugin.loaded[value].run()
            # Re-generate overlay with disabled plugin
            Plugin.compose()
            # Redraw interface. ¿¿¿why???
            Ramon.redraw()

    def open(self):
        with open( f"{Preferences.settings['root']}/plugins/{self.name}/{self.template}", 'r') as file:
            self.template_data = file.read()

    def write(self):        
        with open( f"{Preferences.settings['root']}/data/css/{self.name}.css", 'w') as file:
            file.write( self.getCSS() )
        with open( f"{Preferences.settings['root']}/data/{self.name}.html", 'w') as file:
            file.write( self.rendered )
            
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
            elif key.endswith('-type'   ) : value = f'`{value}`'
            elif key in self.strings      : value = f'`{value}`'
            if isinstance(value, str):
                # Combo value, definition should exist in target client class with same name (autogenerated)
                if value.find('|')>0:
                    value = f"{self.name.capitalize()}.{(value.replace('|', '.').replace('`', ''))}"
            self.rendered = self.rendered.replace(tag(key), str(value))

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
        self.rendered = Tags.replace(self.rendered, self)
        self.rendered = Icons.replaceTags(self.rendered)
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
        if   '-color'       in key: return f'[{value[0]},{value[1]},{value[2]},{value[3]}]'
        elif '-file'        in key: return f"`{value}`"
        elif '-font'        in key: return f'`{value}`'
        elif '-type'        in key: return f'`{value}`'
        return value

    def translateCSSVar(key, value):
        from classes.tools  import px
        from classes.config import pxfields,urlfields,strfields,degreefields
        
        for field in pxfields:
            if field in key: 
                return px(value)
        
        for field in urlfields:
            if field in key: 
                return f"url('{value}')"
        
        for field in strfields:
            if field in key: 
                return f'"{value}"'
        
        for field in degreefields:
            if field in key: 
                return f'{value}deg'
        
        # Special cases
        if   '-color'   in key: value = f'rgba({value[0]},{value[1]},{value[2]},{value[3]})';return value
        elif '-bold'    in key: value = "800" if value else "400"
        elif '-italic'  in key: value = "italic" if value else "normal"
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
        return
        
    def cssRule(self):
        return f'#{self.name}, #{self.name}-border'+'{'+f"""
            left        : var(--{self.name}-left);
            top         : var(--{self.name}-top);
            width       : var(--{self.name}-width);
            height      : var(--{self.name}-height);
            z-index     : var(--{self.name}-z-index);
            transform   : scale(var(--{self.name}-scale));
            { ('border: 2px dashed '+self.color+';') if Plugin.debug else ''} 
        """+'}\n\t\t\t'

    def __iframe__(self):
        return f'<iframe style="{"pointer-events: none;" if not self.interactive else ""} overflow: hidden;" id="{self.name}" autoplay="true" src="./{self.name}.html"></iframe>'+"\n\t\t"
    
    def updateOverlaySetting(sender, value, user_data):
        from classes.ramon import Ramon
        Preferences.settings[sender] = value
        Log.verbose = Endpoints.debug = Plugin.debug = Preferences.settings['debug']
        Plugin.runLoaded()
        Plugin.compose()
        Ramon.redraw()
        Preferences.writecfg()

    def getOverlayTemplate():
        data = None
        try:
            with open(f'{Preferences.settings["root"]}/plugins/overlay.html', "r") as file:
                data = file.read()
        except Exception as E:
            Log.error("Cannot read Plugin Overlay template file", E)
        return data
    
    def writeOverlayTemplate( data ):
        try:
            with open(f'{Preferences.settings["root"]}/data/overlay.html', "w") as file:
                file.write( data )
        except Exception as E:
            Log.error("Cannot write Plugin Overlay template file", E)
        
    def compose(sender=None, user_data=None):
        # Generates overlay.html file:
        # This file holds an iframe per each one of the plugins, shaping their geometry from info inside each plugin.py
        # so it will be the only file to be included in OBS, which contains all the plugins running at once in a single
        # document, lowering down CPU usage at OBS hopefully.
        # This action needs to be done once per execution, as all plugins load their configuration in loadtime, and that 
        # settings are hardcoded in each plugin.py file, so we will have to stick with static configuration for a while
        Log.time()
        if sender=='menu-compose':Plugin.runLoaded()
        #
        Log.info("Merging plugins into single overlay...")
        cvars = Plugin.getOverlayCVars()
        css   = Plugin.getOverlayCSS()
        html  = ""
        data  = ""
        #
        # Get composer css vars, html nodes and css styles
        for name, plugin in Plugin.loaded.items():
            if plugin.settings['enabled']:
                cvars += plugin.getCVars()
                html  += plugin.__iframe__()
                css   += plugin.cssRule()
        # Get template
        data = Plugin.getOverlayTemplate()
        if not data: return
        #
        # Inject payloads 
        data = data.replace( '/*VARS*/'         , cvars )
        data = data.replace( '/*CSS*/'          , css   )
        data = data.replace( '<!--HTML-->'      , html  )
        plug = Plugin('overlay')
        data = Tags.replace(data, plug)
        data = Icons.replaceTags(data)
        #
        # Dump data into rendered template
        if not Plugin.writeOverlayTemplate( data ): return
        #
        # Create plugin data feeder js script 
        Log.time(True)  
    
    def getOverlayCSS():
        return ".debug { display: inline-block; }" if Plugin.debug else ' .debug { display: none; }'
    
    def getOverlayCVars():
        return f'--width : {Plugin.width}px;'+'\n\t\t\t\t'
    
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
                mkdir( dir_accumulated )
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
            plugin = module.plugin()
            plugin.saveDefaults()
            Plugin.loaded[ name ] = plugin
            Plugin.readConfig()
            if Plugin.loaded[ name ].settings['enabled']:
                # Install required files at data folder, if any specified in plugin.py
                if not Plugin.loaded[ name ].install():
                    Log.error(f"Cannot install required files for plugin { Plugin.loaded[ name ] }")
                    Plugin.loaded[ name ].enabled = False
                
            Log.time(True)  
        except Exception as E:
            Log.error(f'Cannot load Plugin {name}', E)
