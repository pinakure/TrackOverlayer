from classes.tdu                import Tdu
from colorama                   import Fore, Back, Style
from classes.preferences        import Preferences
from classes.cheevo             import Cheevo
from classes.plugin             import Plugin

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
        self.scroll     = 0
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
            if row >= (self.height>>1)-2: continue
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
        for row, item in enumerate(self.items[self.scroll:(self.scroll+self.height-2)]):
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
        self.tdu.print(f"{Style.DIM}{Fore.BLACK}REFRESH: {Style.BRIGHT}[")
        self.tdu.print(f"{Fore.WHITE if self.selection==2 else Fore.BLACK}{BG if self.selection==2 else Back.WHITE} OVERLAY ")        
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] [")
        self.tdu.print(f"{Fore.WHITE if self.selection==0 else Fore.BLACK}{BG if self.selection==0 else Back.WHITE} GAME DATA ")
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] [")
        self.tdu.print(f"{Fore.WHITE if self.selection==1 else Fore.BLACK}{BG if self.selection==1 else Back.WHITE} LOCKED CHEEVOS ")
        self.tdu.print(f"{Back.WHITE}{Fore.BLACK}] ")

