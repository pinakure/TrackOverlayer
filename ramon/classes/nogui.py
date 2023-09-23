import os, time
import pywintypes
from datetime               import datetime
from classes.tdu            import Tdu
from colorama               import Fore, Back, Style, init
from pynput                 import keyboard
from threading              import Thread, Timer
#from win32gui               import GetWindowText, GetForegroundWindow
from classes.database       import DDBB
from classes.log            import Log
from classes.preferences    import Preferences
from classes.config         import Config
from classes.cheevo         import Cheevo
from classes.data           import Data
from classes.tags           import Tags
from classes.tools          import mkdir
from classes.plugin         import Plugin
        
init()


class KeyLogger:
    def __init__(self) -> None:
        self.is_paused=False  # pause keylog listener
        self.is_closed=False  # stop and close keylog
        self.l=None  # listener
        #self.listened_window=GetWindowText(GetForegroundWindow())  # set listened window name
        self.focused_checker=Thread(target=self.check_focused)  # check if out of focused window in a thread
        self.focused_checker.start()
    
    def start(self):
        # initialize and start listener
        self.l=keyboard.Listener( on_press=self.on_press, on_release=self.on_release)
        self.l.start()

    def close(self):
        # stop and close keylog
        self.is_closed=True
        self.stop()

    def stop(self):
        # stop listener
        self.l.stop()
        self.l.join()
        
    def check_focused(self):
        return True
        while not self.is_closed:
            if GetWindowText(GetForegroundWindow())!=self.listened_window:  # compare now focused window with listened window
                if not self.is_paused:  # if different and not paused, stop listening
                    self.stop()
                    self.is_paused=True
            elif self.is_paused:  # if same but paused, restart listening
                    self.start()
                    self.is_paused=False
            time.sleep(0.1)

class ListBox:
    def __init__(self, parent, x=0, y=0, width=1, height=1, multiple=False, items=[],selection=0) -> None:
        self.parent     = parent
        self.width      = width
        self.height     = height
        self.back       = Tdu(self.width, self.height, x=x, y=y)
        self.tdu        = Tdu(self.width-2, self.height-2, x=x+1, y=y+1, parent=self.parent.tdu)
        self.multiple   = multiple
        self.items      = items
        self.selection  = selection
        self.cursor     = 0
        self.redraw     = True
        self.preRender()
        self.render()
    
    def preRender(self):
        self.back.border()
        self.back.render()

    def activate(self):
        self.redraw = True
        
    def next(self):
        self.redraw = True
        max = (len(self.items) if isinstance(self.items, list) else len(self.items.keys()))-1 
        self.cursor += 1
        self.cursor = 0 if self.cursor > max else self.cursor
    
    def previous(self):
        self.redraw = True
        max = (len(self.items) if isinstance(self.items, list) else len(self.items.keys()))-1 
        self.cursor -= 1
        self.cursor = max if self.cursor < 0 else self.cursor

        
class CheevoBox(ListBox):
    def __init__(self, parent):
        from classes.plugin import Plugin
        self.x      = 0
        self.y      = 3
        self.width  = 130
        self.height = 40
        cheevos     = {}
        ListBox.__init__(self, parent=parent, x=self.x, y=self.y, width=self.width, height=self.height, multiple=False, items=cheevos)

    def render(self):
        if not self.redraw: return
        self.redraw = False
        self.parent.activity = True
        BG = Back.YELLOW if self.parent.focus == self else Back.WHITE
        for row, key in enumerate(self.items.keys()):
            item = self.items[key]
            self.tdu.setCursor(0 , row*2)
            self.tdu.print(f'{Fore.BLACK}({BG if self.cursor==row else Back.WHITE}{" " if self.selection != row else "*"}{Back.WHITE}) {Fore.BLUE}{key[0:self.width-6]}')
            self.tdu.setCursor(4 , (row*2)+1)
            self.tdu.print(f'{Fore.BLACK}{item[0:self.width-6]}')
        
    def activate(self):
        ListBox.activate(self)
        if len(self.items.keys()) == 0:return
        self.selection = self.cursor
        Preferences.settings['current_cheevo'] = Cheevo.active_index = self.selection+1
        # Update current cheevo at Game database table correspondent item
        self.parent.data.game.current = Cheevo.active_index
        self.parent.data.game.save()
        # Update cheevo data files and picture
        self.parent.data.writeCheevo()
        # Update plugins 
        Plugin.runLoaded()
        self.redraw = True
        
class PluginBox(ListBox):
    def __init__(self, parent):
        from classes.plugin import Plugin
        self.x          = 130
        self.y          = 3
        self.width      = 30
        self.height     = 40
        ListBox.__init__(self, parent=parent, x=self.x, y=self.y, width=self.width, height=self.height, multiple=True, items=Plugin.discover(), selection=[])

    def updateSelection(self):
        self.selection  = ([ name for name, plugin in Plugin.loaded.items() if plugin.settings['enabled']])
        self.redraw     = True

    def render(self):
        if not self.redraw: return
        self.redraw = False
        self.parent.activity = True
        BG = Back.YELLOW if self.parent.focus == self else Back.WHITE
        for row, item in enumerate(self.items):
            self.tdu.setCursor(0 , row)
            self.tdu.print(f'{Fore.BLACK}[{BG if self.cursor==row else Back.WHITE}{"x" if item in self.selection else " "}{Back.WHITE}] {Fore.BLUE if item in self.selection else Fore.BLACK}{item}')
        
    def activate(self):
        ListBox.activate(self)
        value = self.items[self.cursor]
        Plugin.loaded[value].settings['enabled'] ^= 1
        self.parent.log.print(f'{"En" if Plugin.loaded[value].settings["enabled"] else "Dis"}abled plugin "{value}"')
        Plugin.writeConfig()
        if Plugin.loaded[value].settings['enabled']:
            Plugin.loaded[value].run()
        Plugin.compose()
        self.updateSelection()
        
class LogBox(ListBox):
    def __init__(self, parent):
        self.x          = 0
        self.y          = 43
        self.height     = 7
        self.width      = parent.width
        ListBox.__init__(self, parent=parent, x=self.x, y=self.y, width=self.width, height=self.height, multiple=True, items=[], selection=0)
        self.print("tRAckOverlayer : Interface loaded successfully")

    def render(self):
        if not self.redraw: return
        self.redraw = False
        self.parent.activity = True
        self.tdu.clear()
        for row, item in enumerate(self.items[-5:]):
            self.tdu.setCursor(0 , row)
            space   = self.width - 2
            payload = f'{Fore.BLUE}{item[0:space]}{Fore.WHITE}'
            remain  = space - (len(payload)-(len(Fore.BLUE)+len(Fore.WHITE)))
            self.tdu.print(payload + (" "*remain))

    def print(self, text):
        self.items.append(text.replace('\n', '').replace('\r', '').replace('\t', '    '))
        self.redraw = True

class MenuBar:
    def __init__(self, parent) -> None:
        self.parent     = parent
        self.width      = parent.width
        self.height     = 1
        self.tdu        = Tdu(self.width, self.height, x=0, y=0, parent=self.parent.tdu)
        self.tdu.x      = 1
        self.tdu.y      = 1
        self.selection  = 0

    def next(self):
        self.selection += 1
        self.selection = 0 if self.selection >= 3 else self.selection
    
    def previous(self):
        self.selection -= 1
        self.selection = 2 if self.selection < 0 else self.selection

    def activate(self):
        if   self.selection == 0: self.parent.refresh()
        elif self.selection == 1: Cheevo.checkAll()
        elif self.selection == 2: Plugin.compose()

    def render(self):
        self.tdu.restore()
        BG = Back.YELLOW if self.parent.focus == self else Back.WHITE
        self.tdu.print(f"{Style.DIM}{Fore.BLACK}ACTIONS: {Style.BRIGHT}[")
        self.tdu.print(f"{Fore.WHITE if self.selection==0 else Fore.BLACK}{BG if self.selection==0 else Back.WHITE} REFRESH GAME ")
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] [")
        self.tdu.print(f"{Fore.WHITE if self.selection==1 else Fore.BLACK}{BG if self.selection==1 else Back.WHITE} REFRESH CHEEVOS ")
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] [")
        self.tdu.print(f"{Fore.WHITE if self.selection==2 else Fore.BLACK}{BG if self.selection==2 else Back.WHITE} REFRESH OVERLAY ")        
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] ")

class App(KeyLogger):

    text_only   = True
    version     = Config.version
    up          = False
    down        = False
    left        = False
    right       = False
    tab         = False
    enter       = False
    esc         = False
    f5          = False
    ctrl        = False
    alt         = False
    shift       = False
    
    def __init__(self) -> None:
        os.system("title tRAckOverlayer")
        self.width          = 160
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
        KeyLogger.__init__(self)
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

    def on_press(self, key):
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r] :
            self.ctrl = True
            return 
        if key in [keyboard.Key.alt_l, keyboard.Key.alt_r] :
            self.alt = True
            return 
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r] :
            self.shift = True
            return 
        if key == keyboard.Key.left or key == keyboard.Key.up:
            self.activity = True
            return self.focus.previous()        
        if key == keyboard.Key.right or key == keyboard.Key.down:
            self.activity = True
            return self.focus.next()        
        if key == keyboard.Key.esc:
            return self.exit()
        if key == keyboard.Key.enter:
            self.activity = True
            return self.focus.activate()
        if key == keyboard.Key.tab:
            self.activity = True
            last_focus = self.focus
            if self.shift:                
                self.focus_index-=1
                self.focus_index=(len(self.focuses)-1)if self.focus_index<0 else self.focus_index
            else:
                self.focus_index+=1
                self.focus_index%=len(self.focuses)
            self.focus = self.focuses[ self.focus_index ]
            self.focus.redraw = True
            last_focus.redraw = True
            
            return
        if key == keyboard.Key.f4 and self.alt:
            return self.exit()
        if key == keyboard.Key.f5 and self.ctrl:
            if self.timer:
                self.timer.cancel()
                self.timer = None
                self.refresh()

    def on_release(self, key):
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r] :
            self.ctrl = False
            return 
        if key in [keyboard.Key.alt_l, keyboard.Key.alt_r] :
            self.alt = False
            return 
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r] :
            self.shift = False
            return 
        
    def start(self):
        from classes.server import Server # private import needed here to avoid import loop
        Log.open(self)
        Preferences.loadcfg(self)
        DDBB.init()
        self.data  = Data(self)
        self.data.retrieveSession()
        
        # Make required folders
        for folder in Config.folders:
            mkdir(folder)
        
        # Reset cheevo picture file to default TO file
        Cheevo.default(self)

        # Configure Tags target
        Tags.setParent(self)
        
        # Start websocket server
        Server.start(self)

        # load plugins
        Plugin.loadThese( Plugin.discover() )
        self.plugin_list.updateSelection()

        # Enable keyboard listener (dont panic about its name, its not logging any password, its just listening arrows, enter and tab keys)
        KeyLogger.start(self)
        
        # enter main loop
        self.render()

        return True