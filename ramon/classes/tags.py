import json
from classes.preferences    import Preferences
from classes.log            import Log
from classes.tools          import tag, templatetag

class Tags:
    
    parent = None

    def setParent(parent):
        Tags.parent = parent

    def getTags():
        return {
            'debug'             : Tags.debug,
            'fonts'             : Tags.fonts,
            'game'              : Tags.game,
            'framework'         : Tags.framework,
            'fullsized'         : Tags.fullsized,
            'load-config'       : Tags.load_config,
            'monitor'           : Tags.monitor,
            'Name'              : Tags.Name,
            'name'              : Tags.name,
            'no-welcome'        : Tags.no_welcome,
            'non-interactive'   : Tags.non_interactive,
            'plugin'            : Tags.plugin,
            'plugins'           : Tags.plugins,
            'require-cheevo'    : Tags.require_cheevo,
            'reload'            : Tags.reload,
            'update-css'        : Tags.update_css,
            'twitch-password'   : Tags.twitch_password,
            'update-rate'       : Tags.update_rate,
            'websocket'         : Tags.websocket,
        }

    def replace( payload , self=None):
        for i in range(0,2):
            for k,v in Tags.getTags().items():
                payload = payload.replace(tag(k),str(v(self)))
        return payload
    
    # TAG Translation callbacks below

    def fullsized(self):
        return """
            html { 
                width   : 100%; 
                height  : 100%; 
            } 
            body { 
                width   : 100%; 
                height  : 100%; 
                top     : 0px; 
                left    : 0px; 
            } 
            html { 
                position: absolute; 
            } 
            body { 
                position: absolute; 
            }
        """
    
    def framework(self):
        if self is None:
            Log.warning("framework tag summoned outside plugin template!")
            return ''
        return Tags.load_config(self) + r"""
                
                standalone      : true,
                connected       : false,
                

                send            : function(msg, data=[]){
                    window.parent.postMessage(`{% name %}|${msg}|${JSON.stringify(data)}`, '*');
                },

                log             : {
                    print           : function(text){
                        window.parent.postMessage(`{% name %}|print|${text}`, '*');
                    },
                    clear           : function(text){
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
                                var rid     = parseInt(Math.random()*655356);
                                var par     = document.getElementsByTagName('head')[0];
                                var old     = document.getElementsByTagName('link')[0];
                                var link    = document.createElement('link');
                                link.rel    = "stylesheet";
                                link.type   = "text/css";
                                link.href   = `./css/{% name %}.css?${ rid }`;
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
                """+self.dumpDicts()

    def game(self):
        return Tags.parent.data.game.id

    def plugins(self):
        '@OBJECT'
        from classes.plugin import Plugin
        return 'plugins: {'+",".join([f"{x}:undefined" for x in Plugin.loaded.keys() if Plugin.loaded[x].settings['enabled']])+"},"
    
    def plugin(self):
        # Common Plugin Consts and globals
        return """
            const False     = false; 
            const True      = true; 
            const None      = null; 
            const alternate = 'alternate' /*DEPRECATED*/; 
            const forwards  = 'forwards'  /*DEPRECATED*/; 
            const backwards = 'backwards' /*DEPRECATED*/;
        """     

    def no_welcome(self):
        '@JSCRIPT'
        return '''
            TO.dom.overlay.remove();
            TO.start();
        ''' if Preferences.settings['no-welcome'] else ''
    
    def reload(self):
        '@JSCRIPT:DEPRECATED'
        return "function refresh(){ window.location.reload(); } setInterval(refresh,5000);"

    def non_interactive(self):
        '@CSSRULE'
        return '* { pointer-events: none; }'

    def monitor(self):
        from classes.preferences import Preferences
        style = """#monitor { display: none !important; }""" if not Preferences.settings['show-disconnect-icon'] else """
            #monitor {
                mix-blend-mode  : screen; 
                font-family     : 'square'; 
                font-weight     : 800; 
                overflow        : visible !important; 
                display         : inline-block; 
                position        : absolute; 
                color           : #ff0000; 
                right           : calc( 50% - 16px); 
                bottom          : calc( 50% - 16px); 
                width           : 32px; 
                height          : 32px;                    
            }
        """
        return f"""<style>{ style }</style>"""+"""
            <div id="monitor">
                <img title="{% Name %} has lost connection with tRAckOverlayer" src="{% icon|disconnected %}">
            </div>
        """
            
    
    def require_cheevo(self):
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
    
    def twitch_password(self):
        if Tags.parent.text_only: 
            from classes.preferences import Preferences
            return Preferences.settings['twitch-password']            
        from dearpygui import dearpygui as dpg        
        return dpg.get_value('twitch-password')

    def load_config(self):
        if self is None:
            Log.warning("load_config tag summoned outside plugin template!")
            return ''
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
                        payload+=f'{tkey} = {templatetag(tkey)}'+'\n'                        
                else:
                    tkey+='-'
        payload = json.dumps( aux(payload) ).replace('"', '').replace('_', ' ')
        return "loadSettings    : function(){\n\t\t\t\t\ttry {\n\t\t\t\t\t\t{% Name %}.settings = JSON.parse(localStorage.getItem('{% name %}-settings'));\n\t\t\t\t\t\tsettings.update.rate = 1;\n\t\t\t\t\t} catch (e){\n\t\t\t\t\t\t{% Name %}.settings = "+payload+";\n\t\t\t\t\t}\n\t\t\t\t},"
    
    def update_css(self):
        if self is None:
            Log.warning("update-css tag summoned outside plugin template!")
            return ''
        from classes.plugin import Plugin
        if not Plugin.debug: return ""
        return r"""
        function updatecss(){
            console.log("Erasing css...");
            var rid = parseInt(Math.random()*655356);
            var par  = document.getElementsByTagName('head')[0];
            var old  = document.getElementsByTagName('link')[0];
            var link = document.createElement('link');
            link.rel = "stylesheet";
            link.type = "text/css";
            link.href = `./css/"""+self.name+""".css?${ rid }`;
            par.append(link);
            setTimeout(function(){ old.remove();}, 500);
            setTimeout(updatecss, 1000);
        }
        updatecss();
        """
    
    def fonts(self):
        from classes.plugin import Plugin
        from classes.fonts import fonts        
        # If debug is enabled, css all fonts can be used while tweaking plugin, 
        # so we need all of them preloaded 
        if not Plugin.debug: return "\n\t\t".join([value for value in fonts.values()])
        #TODO: Return for injection only those fonts being used by the plugin (self)
        return "\n\t\t".join([value for value in fonts.values()])
            
    def Name(self):
        return Tags.name(self).capitalize()
    
    def name(self):
        if self is None:
            Log.warning("name tag summoned outside plugin template!")
            return ''
        return self.name
    
    def debug(self):
        from classes.plugin import Plugin
        return 'true' if Plugin.debug else 'false'
                
    def update_rate(self):
        return "5000"

    def websocket(self):
        return f"endpoint    : '{ self.endpoint }',"+"""
            socket      : null,
            connected   : false,
            reconnect   : function(){
                if( !{% Name %}.connected ){
                    console.log("{% Name %} : WSRECON");
                    const socket = new WebSocket("ws://localhost:8765");
                    {% Name %}.socket = socket;
                    socket.addEventListener("open"      , {% Name %}.socketOpen  );
                    socket.addEventListener("close"     , {% Name %}.socketClose );
                    socket.addEventListener("message"   , {% Name %}.socketHandle);
                }
            },                
            socketOpen  : function( event ) {
                console.log("{% Name %} : WSOPEN");                    
                {% Name %}.connected = true;
                {% Name %}.update();
                document.getElementById('monitor').style.display='none';
            },                
            socketClose : function( event ) {
                console.log("{% Name %} : WSCLOSE");
                document.getElementById('monitor').style.display='inline-block';
                {% Name %}.connected = false;
                {% Name %}.reconnect();
            },
            connect     : function(){
                const socket = new WebSocket("ws://localhost:8765");
                {% Name %}.socket = socket;
                socket.addEventListener("open"      , {% Name %}.socketOpen  );
                socket.addEventListener("close"     , {% Name %}.socketClose );
                socket.addEventListener("message"   , {% Name %}.socketHandle);
            },
        """