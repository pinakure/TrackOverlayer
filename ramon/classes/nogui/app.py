import os
from datetime                   import datetime
from classes.tdu                import Tdu
from colorama                   import init as Colorama
from threading                  import Timer
from classes.database           import DDBB
from classes.log                import Log
from classes.preferences        import Preferences
from classes.config             import Config
from classes.cheevo             import Cheevo
from classes.data               import Data
from classes.tags               import Tags
from classes.tools              import mkdir
from classes.plugin             import Plugin
from classes.nogui.keylogger    import SafeInput as Keyboard
from classes.nogui.widgets      import CheevoBox,PluginBox,LogBox,MenuBar

class App(Keyboard):

    text_only   = True
    version     = Config.version
    
    def __init__(self) -> None:
        Colorama()
        os.system("title tRAckOverlayer")
        self.width          = 160
        os.system(f"mode {self.width},{50}")
        self.height         = 3
        self.run            = True
        self.activity       = False
        self.focus          = None
        self.data           = None
        self.queue          = []
        self.timer          = None
        self.requesting     = False
        self.back           = Tdu(self.width, self.height,x=0, y=0)
        self.tdu            = Tdu(self.width-2, self.height-2, x=1, y=1)
        self.menubar        = MenuBar( parent=self )
        self.cheevo_list    = CheevoBox( parent=self)
        self.plugin_list    = PluginBox( parent=self)
        self.log            = LogBox( parent=self)
        self.focuses        = [self.menubar, self.cheevo_list, self.plugin_list]
        self.focus_index    = 0
        self.focus          = self.focuses[ self.focus_index ]
        Keyboard.__init__(self, self.handle_keyboard)
        self.start()
    
    def preRender(self):
        self.back.border()
        self.back.render()

    def frame(self):
        self.activity=False            
        self.cheevo_list.render()
        self.plugin_list.render()
        self.menubar.render()
        self.log.render()
        self.tdu.render()

    def render(self):
        self.preRender()
        self.frame()
        self.refresh()
        while self.run:
            # Draw elements 
            self.frame()
            # Wait for activity on keyboard to re-loop
            while not self.activity:
                if Preferences.settings['auto_update'] and not self.timer:
                    self.timer = Timer( Preferences.settings['auto_update_rate']*60, Cheevo.checkAll )
                    self.timer.start()           
                self.data.dispatchQueue()
                Cheevo.dispatchQueue()
                #if len(self.queue)==0: 
                #    sleep(0.1)
        os._exit(0)

    def exit(self):
        try:
            Log.close()            
        except Exception as E:
            print(str(E))
        self.close()
        self.run = False

    def redraw(self):
        self.data.getRecent()

        self.cheevo_list.items = {}
        for d in self.data.cheevos:
            if d.locked: 
                self.cheevo_list.items.update({
                    d.name : d.description,
                })
        self.cheevo_list.redraw = True
        

    def refresh(self):
        self.requesting = True
        self.timer = None
        Cheevo.global_index = 0
        
        if Preferences.settings['offline']:
            self.data.last_activity = datetime.strptime(Preferences.settings['last_date'], "%d %b %Y, %H:%M")
            self.data.last_seen     = Preferences.settings['last_game']
            self.data.site_rank     = Preferences.settings['rank']
            self.data.score         = Preferences.settings['score']
        Log.info("Scraping data...")
        if self.data.query():
            Log.info("Scraping done.")
            self.redraw()
            self.data.writeCheevo()
            Plugin.runLoaded()
            self.log.print('tRAckOverlayer - '+("Offline Mode" if Preferences.settings["offline"] else " is ready"))
        else:
            #Log.warning("Scraping failed.")
            self.requesting = False
            return False
        self.requesting = False
        return True

    def handle_keyboard(self, key):
        from getkey import keys
        if key in [ keys.UP, keys.LEFT]:
            self.activity = True
            return self.focus.previous()        
        if key in [ keys.DOWN, keys.RIGHT]:
            self.activity = True
            return self.focus.next()        
        if key in [ keys.ENTER]:
            #self.activity = True
            return self.focus.activate()
        if key in [ keys.F5]:
            if self.timer:
                self.timer.cancel()
                self.timer = None
                self.refresh()
            return
        if key in [ keys.ESC]:
            return self.exit()
        if key in [ keys.TAB]:
            self.activity = True
            last_focus = self.focus
            self.focus_index+=1
            self.focus_index%=len(self.focuses)
            self.focus = self.focuses[ self.focus_index ]
            self.focus.redraw = True
            last_focus.redraw = True            
        
    def start(self):
        # Make required folders
        for folder in Config.folders:
            mkdir(folder)

        from classes.server import Server # private import needed here to avoid import loop
        Log.open(self)
        Preferences.loadcfg(self)
        DDBB.init()
        self.data  = Data(self)
        self.data.retrieveSession()
        
        
        
        # Reset cheevo picture file to default TO file
        Cheevo.default(self)

        # Configure Tags target
        Tags.setParent(self)
        
        # Start websocket server
        Server.start(self)

        # load plugins
        Plugin.loadThese( Plugin.discover() )
        self.plugin_list.updateSelection()

        # Enable keyboard listener
        Keyboard.start(self)
        
        # enter main loop
        self.render()

        return True