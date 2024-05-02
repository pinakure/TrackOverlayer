import os
from time                   import sleep
from dearpygui              import dearpygui as dpg
from datetime               import datetime
from classes.data           import Data
from classes.cheevo         import Cheevo
from classes.preferences    import Preferences
from classes.log            import Log
from classes.plugin         import Plugin
from classes.ui             import UI , row as ROW, column as COLUMN
from classes.tools          import mkdir, copy, elegant
from classes.hotkeys        import HotKeys
from classes.tdu            import Tdu
from classes.config         import Config
from classes.tags           import Tags
from threading              import Timer
                    
class Ramon:
    CLS                 = 'cls' # set this to 'clear' on UNIX!!!
    width               = 1440
    height              = 900
    inner_width         = 0
    inner_height        = 0
    x                   = 0
    y                   = 0
    text_only           = False
    menu_height         = 20
    titlebar_height     = 18
    log_line_count      = 15
    show_log            = True
    log_height          = (log_line_count * 16)
    statusbar_height    = 20
    padding             = 8    
    restart             = False    
    css                 = {}
    version             = Config.version
    timer               = None    
    plugins             = []
    data                = None
    run                 = True
    requesting          = False
    queue               = []
    tdu                 = None
        
    def updateCheevoManually(sender=None, args=None, user_data=None):
        with open(f'{Ramon.data.root}/data/current_cheevo.txt', "w") as file:
            file.write(dpg.get_value('cheevo'))
        os.truncate(f'{Ramon.data.root}/data/current_cheevo.png',0)
    
    def updateCheevo(sender=None, args=None, user_data=None):
        Cheevo.active_index = user_data
        Ramon.data.game.current = Cheevo.active_index
        Preferences.settings['current_cheevo'] = Cheevo.active_index
        Ramon.data.game.save()
        if not Preferences.settings['simple_ui']:
            for i in range(0,Cheevo.max):
                dpg.set_value(f'cheevo[{i+1}]', False)
            dpg.set_value(f'cheevo[{Cheevo.active_index}]', True)
        Ramon.data.writeCheevo()
        Plugin.runLoaded()
        Ramon.redraw()
    
    def trigger_exit(sender=None, user_data=None):
        Ramon.run = False         

    def openWeb(sender, args, type):
        if   type == 'overlay'      : web = f"{Preferences.settings['root']}/data/overlay.html"
        elif type == 'twitch-chat'  : web = f"https://www.twitch.tv/popout/{Preferences.settings['twitch-username']}/chat?popout="
        elif type == 'ra-user'      : web = f"https://retroachievements.org/user/{Preferences.settings['username']}"
        elif type == 'ra-game'      : web = f"https://retroachievements.org/game/{Ramon.data.game.id}"
        elif type == 'ra-cheevo'    : web = f"https://retroachievements.org/achievement/{Ramon.data.the_cheevo.id}"
        else:web = f"{Preferences.settings['root']}/data/{ type }.html"
        os.system(f'start {web}')
    
    def createMenu():
        data = {
            'actions'   : { 
                'force-overlay-rebuild' : [Plugin.compose   ,None],
                'update-profile-data'   : [Ramon.refresh    ,None],
                'refresh-locked-cheevos': [Cheevo.checkAll  ,None],
                'compile'               : [Ramon.compile    ,None],
                'exit'                  : [Ramon.exit       ,None],
            },
            'options'   : { 
                'preferences'           : [Preferences.show ,None],
            },
            'links'   : { 
                'to-overlay'            : [Ramon.openWeb    ,'overlay'],
                'twitch'                : {
                    'chat'                  : [Ramon.openWeb    ,'twitch-chat'  ],
                },
                'retroachievements'     : {
                    'user-profile'          : [Ramon.openWeb    ,'ra-user'      ],
                    'game-profile'          : [Ramon.openWeb    ,'ra-game'      ],
                    'cheevo-page'           : [Ramon.openWeb    ,'ra-cheevo'    ],
                },
            },
        }
        with dpg.menu_bar( tag='menu-root' ):
            menu( data, 'menu-root' )

    def resizeViewport(a,pos):
        Ramon.height        = dpg.get_viewport_height() 
        Ramon.width         = dpg.get_viewport_width()
        Ramon.inner_width   = Ramon.width - (Ramon.padding*2)
        Ramon.inner_height  = Ramon.height- (Ramon.titlebar_height + Ramon.menu_height)
        Ramon.x, Ramon.y    = dpg.get_viewport_pos()
        log_height = Ramon.log_height if Ramon.show_log else 0
        dpg.configure_item('main'        , width = Ramon.inner_width                     , height = Ramon.inner_height  )
        dpg.configure_item('main-content', width = Ramon.inner_width - (Ramon.padding*2) , height = Ramon.inner_height - (Ramon.statusbar_height + (log_height) +96) )
        dpg.configure_item('log-window'  , height= log_height, width = Ramon.inner_width - (Ramon.padding  ) , pos    = (0 , Ramon.inner_height - (Log.height + Ramon.statusbar_height  ) ) ,show  = Ramon.show_log)
        dpg.configure_item('log'         , height= log_height, width = Ramon.inner_width - (Ramon.padding*2) , pos    = (8 , Ramon.inner_height - (Log.height + Ramon.statusbar_height  )-8 ) ,show  = Ramon.show_log)
        dpg.configure_item('statusbar'   , width = Ramon.inner_width                     , pos    = (0 , Ramon.inner_height - Ramon.statusbar_height                              ) )
        Preferences.settings.update({
            'width'  : Ramon.width,
            'height' : Ramon.height,         
            'x-pos'  : Ramon.x,
            'y-pos'  : Ramon.y,
        })
        #UI.resize()
        Preferences.writecfg()

    __stage = 0
    def stage():
        print(f'{"-"*60}[ STAGE {Ramon.__stage} ]{"-"*4}')
        Ramon.__stage+=1
        
    def start():
        Ramon.stage()
        from classes.database   import DDBB
        from classes.server     import Server # private import needed here to avoid import loop
        Log.open(Ramon)
        Preferences.loadcfg(Ramon)
        DDBB.init()
        
        Ramon.data  = Data(Ramon)

        Ramon.data.retrieveSession()

        HotKeys.install()
        
        # Make required folders
        for folder in Config.folders:
            mkdir(folder)

        # Reset cheevo picture file to default TO file
        Cheevo.default(Ramon)
        
        # Configure Tags target
        Tags.setParent(Ramon)

        # Load plugin list
        Ramon.stage()
        Ramon.plugins = Plugin.discover()
        
        Ramon.stage()
        Ramon.createViewport()
        Ramon.createInterface()        
        
        Ramon.stage()
        Ramon.setPosition( Preferences.settings['x-pos'], Preferences.settings['y-pos'] )
        Ramon.loadPictures()
        
        Ramon.stage()
        Server.start(Ramon)
        print("Started Ramon server")
    
        # load plugins
        Ramon.stage()
        Plugin.loadThese( Ramon.plugins )

        # debug mode (GUI only)
        Ramon.debugMode()

        # enter main loop
        Ramon.render()
        return True
    
    def createViewport():
        Ramon.inner_width  = Ramon.width - (Ramon.padding*2)
        Ramon.inner_height = Ramon.height- Ramon.titlebar_height - Ramon.menu_height
        dpg.create_context()
        dpg.create_viewport(
            title   = "tRAckOverlayer", 
            width   = Ramon.width , 
            height  = Ramon.height,
        )
        dpg.set_viewport_resize_callback(Ramon.resizeViewport)
        dpg.set_viewport_small_icon     (f"{Preferences.settings['root']}/icon.ico")
        dpg.set_viewport_large_icon     (f"{Preferences.settings['root']}/icon.ico")
        dpg.setup_dearpygui()
        print("Viewport created")
        
    def loadPictures():
        #TODO: load only set for current game, this is actually loading in vram all the cache folder, which is nonsense.
        #      also, remember to release and reload the images when the game is changed...
        dirname = Preferences.settings['root']+'/data/cache'
       
        pictures = {}
        with dpg.texture_registry(show=False):
            files = [ x  for x in os.listdir( dirname ) if os.path.isfile(f'{dirname}/{x}') and x[0] != '.']
            count = 1
            for file in files:
                try:   
                    width, height, depth, data = dpg.load_image(f'{dirname}/{file}')                
                    pictures.update({
                        file : data,
                    })
                    dpg.add_static_texture(
                        width           = width, 
                        height          = height, 
                        default_value   = data, 
                        tag             = f"texture[{file}]",
                    )
                    print(f"Processing {count}/{len(files)} images", end="         \r")
                    count+=1
                except Exception as E:
                    print("")
                    Log.error(f"Cannot load '{file}'", E)
            print("")


    def createInterface():
        with dpg.window(
            tag                         = 'main',
            label                       = f"tRAckOverlayer v.{Ramon.version}", 
            width                       = 0,#Ramon.inner_width,
            height                      = 0,#Ramon.inner_height, 
            no_close                    = True, 
            no_collapse                 = True, 
            no_resize                   = True, 
            no_title_bar                = True,
            no_scrollbar                = True,
            no_bring_to_front_on_focus  = True, 
            no_move                     = True,            
        ):
            print("Setting up interface")
            Ramon.createMenu()
            row = 23
            row_height = 23
            UI.setCursor(0,1)
            UI.setColumns(3, Ramon.width/4 ) 
            UI.textfield("RA Username"              , 'username'            , on_enter=True)
            UI.textfield("Score"                    , 'score'               , readonly=True)
            UI.textfield("Rank"                     , 'rank'                , readonly=True)
            UI.textfield("Now Playing"              , 'game'                , readonly=True)
            UI.textfield("Last connection"          , 'date'                , readonly=True)
            UI.textfield("Cheevo"                   , 'cheevo'              , readonly=True)
            UI.jump()
            dpg.add_button(
                tag="refresh-profile-button", 
                label="Update Profile", 
                width=128, 
                pos=(
                    Ramon.inner_width-136, 
                    Ramon.titlebar_height+(Ramon.padding)+6
                ),
                callback=Ramon.refresh,
            )
            dpg.add_button(
                tag="refresh-cheevos-button", 
                label="Update Cheevos", 
                width=128,                 
                pos=(
                    Ramon.inner_width-136, 
                    Ramon.titlebar_height+(Ramon.padding)+6+24
                ),
                callback=Cheevo.checkAll,
            )
            row = ROW.input * UI.row_height
            with dpg.child_window(
                tag             = 'main-content',
                width           = int(Ramon.inner_width/2), 
                height          = (Ramon.height - 256),
                pos             = (8,row),
            ):
                dpg.add_text(
                    tag     = 'stdout',
                    pos     = (31,0),
                    color   = Preferences.settings['pending_cheevos'],
                )            
                for i in range(0,Cheevo.max):
                    dpg.add_checkbox(
                        default_value   = True if (i+1) == Cheevo.active_index else False, 
                        tag             = f'cheevo[{i+1}]', 
                        pos             = (8, (i*26)), 
                        show            = False, 
                        user_data       = i+1, 
                        callback        = Ramon.updateCheevo,
                        label           = f'Cheevo Title',
                    )
                dpg.add_text(
                    tag     = 'unlocked',
                    color   = Preferences.settings['unlocked_cheevos'],
                    pos     = (31,row_height*Cheevo.global_index)
                )
            Ramon.data.updatePictures()
            with dpg.window(
                modal           = True, 
                label           = "Processing data, please wait...",
                tag             = "process-window", 
                width           = 200, 
                height          = 45, 
                min_size        = [200, 45], 
                no_scrollbar    = True, 
                max_size        = [200, 45], 
                no_collapse     = True, 
                no_resize       = True, 
                show            = False,
                pos             = [
                    (Ramon.width  / 2) - 100, 
                    (Ramon.height / 2) -  32,
                ]):
                dpg.add_progress_bar(tag="progress", width=200, pos=[0, 22])
            dpg.add_input_text(
                tag             = 'statusbar',
                pos             = (0, Ramon.inner_height-Ramon.statusbar_height),
                width           = Ramon.inner_width-Ramon.padding,
                default_value   = "Ready",
                readonly        = True,
            )
            # Create log window
            Ramon.stage()
            Log.create( Ramon )            
            # Create preferences window
            Ramon.stage()
            Preferences.create( Ramon )
            print("Plugin preferences window created")
        
    def setPosition(x,y):
        Ramon.x = x
        Ramon.y = y
        dpg.set_viewport_pos( (x, y) )
    
    def setProgress(value):
        if value >= 1.0:
            dpg.hide_item('process-window')
        else:
            dpg.set_value('progress', value)
            dpg.show_item('process-window')

    def compile():
        # Create plugins.zip
        import shutil
        mkdir('xplugins')
        os.system('xcopy plugins xplugins\\plugins\\ /i /s /q /y ')
        os.system('erase xplugins\\plugins\\*.py  /S /Q')
        os.system('erase xplugins\\plugins\\*.pyc /S /Q')
        shutil.make_archive('plugins', 'zip', 'xplugins')
        os.system('@rmdir /q /s xplugins')
        
        with open("./compile.bat", "w") as file:
            plugins = " ".join([ f'--hidden-import plugins.{x}.plugin' for x in Plugin.discover()])
            plugins += ' --hidden-import pywintypes '
            plugins += ' --hidden-import win32gui '
            plugins += ' --hidden-import pywin32 '
            file.write(f'''@title Compiling tRAckOverlayer v.{Ramon.version}...'''+'\n')                       
            file.write(f'''@python3 -m PyInstaller --onefile -i icon.ico --noconsole {plugins} main.py '''+'\n'+'''@move dist\main.exe tRAckOverlayer.exe'''+"\n")
            #file.write(f'''@python3 -m PyInstaller --onefile -i icon.ico {plugins} main.py '''+'\n'+'''@move dist\main.exe tRAckOverlayer_debug.exe'''+"\n")
            file.write(f'''@python3 -m PyInstaller --onefile -i icon.ico {plugins} main_nogui.py '''+'\n'+'''@move dist\main_nogui.exe tRAckOverlayer-noGUI.exe'''+"\n")
            file.write(f'''@rmdir /q /s build'''+"\n")
            file.write(f'''@rmdir /q /s dist''' +"\n")
            file.write(f'''@erase main.spec'''+"\n")
            file.write(f'''@erase compile.bat && exit'''+"\n")
        os.system('start compile.bat')
        dpg.set_viewport_title('tRAckOverlayer - Launched "compile.bat" script succesfully')
    
    def msg(text):
        dpg.set_value('stdout', text)
        dpg.render_dearpygui_frame()        

    def render():
        if Preferences.settings['fullscreen'] : 
            dpg.toggle_viewport_fullscreen()
        dpg.show_viewport()
        Ramon.msg("Fetching Cheevo data...")
        Ramon.refresh()        
        # ---------------------------------------- LOOP START ---------------------------------------
        while dpg.is_dearpygui_running() and Ramon.run:
            dpg.render_dearpygui_frame()
            if Preferences.settings['auto_update'] and not Ramon.timer:
                Ramon.timer = Timer( Preferences.settings['auto_update_rate']*60, Cheevo.checkAll )
                Ramon.timer.start()           
            Ramon.data.dispatchQueue()
            Cheevo.dispatchQueue()
            if Ramon.restart: break
        # ----------------------------------------- LOOP END ----------------------------------------
        # ---------------------------------------- DEINIT START -------------------------------------
        # First of all Remove any timer left so it wont try to run on missing ui elements
        return Ramon.exit()
    
    def title(text):
        dpg.set_viewport_title(text)
        
    def exit():
        from classes.server   import Server
        from classes.database import DDBB
        import asyncio
        try:
            Ramon.data.storeSession()
            
            
            DDBB.db.close()
            
            if Ramon.timer:
                Ramon.timer.cancel()
                Ramon.timer = None
            # Begin deinitialization, begin dumping the log 
            Log.close()
            # Unbind messages from log to see them while ui is deinitializedlog             
            Log.stdout = True
            # Store window position and shape at exit
            pos  = dpg.get_viewport_pos()
            size = (dpg.get_viewport_width(), dpg.get_viewport_height() )
            Preferences.settings['x-pos'] = pos[0]
            Preferences.settings['y-pos'] = pos[1]
            Preferences.settings['width'] = size[0]-16
            Preferences.settings['height'] = size[1]
            Preferences.writecfg()
            Log.info("Settings stored")
            # Unitialize UI library
            dpg.remove_alias("main") 
            dpg.delete_item('main')
            dpg.destroy_context()        
            Log.info("Closed succesfully")
            print("Program end reached.")
            Ramon.run = False
            asyncio.run(Server.exit())
            return True
        except Exception as E:
            Log.error("Error during deinitialization", E)
            return False

    def txtRedraw():
        Ramon.clear()        
        payload, unlocked = Ramon.data.getRecent()
        return

    def redraw():
        if not Preferences.settings['simple_ui']: return Ramon.olredraw()
        try:
            Ramon.clear()
            for i in range(0,Cheevo.max):
                dpg.delete_item(f'cheevo[{i+1}]')
        except Exception as E: 
            pass

        dpg.set_value('game'  , Ramon.data.game.name      )
        dpg.set_value('rank'  , Ramon.data.site_rank      )
        dpg.set_value('score' , Ramon.data.score          )
        #dpg.set_value('date'  , Ramon.data.last_activity.strftime("%d %b %Y, %H:%M")  )
        dpg.set_value('cheevo', Ramon.data.cheevo.split('\n')[0])

        left = 0
        items = int(Ramon.inner_width / (64+(Ramon.padding*2)))
        group_index = 0        
        
        Ramon.data.getRecent()

        for d in Ramon.data.cheevos:
            if left==0:
                group_index+=1
                try:dpg.delete_item(f'simple-group[{group_index}]')
                except: pass
                dpg.add_group(tag=f"simple-group[{group_index}]", horizontal=True, parent='main-content')
                left = items
            if d.locked: 
                tag = f"cheebox[{d.picture}]"
                try:dpg.delete_item(tag)
                except: pass
                try:
                    dpg.add_image_button(
                        tag=tag,
                        width=64,
                        height=64,
                        texture_tag=f'texture[{d.picture}]',
                        parent=f'simple-group[{group_index}]',
                        user_data=d.index,
                        callback=Ramon.updateCheevo,
                    )
                    with dpg.tooltip( tag ):
                        dpg.add_text(d.name+"\n"+d.description)  
                except Exception as E:
                    Log.warning(str(E))
                left -= 1
        
    def olredraw():
        Ramon.clear()
        dpg.set_value('game'  , Ramon.data.last_seen      )
        dpg.set_value('rank'  , Ramon.data.site_rank      )
        dpg.set_value('score' , Ramon.data.score          )
        #dpg.set_value('date'  , Ramon.data.last_activity.strftime("%d %b %Y, %H:%M")  )
        dpg.set_value('cheevo', Ramon.data.cheevo.split('\n')[0])
        payload, unlocked = Ramon.data.getRecent()
        for d in Ramon.data.cheevos:
            if d.locked: 
                dpg.show_item(f'cheevo[{d.index}]')
                dpg.set_item_label(f'cheevo[{d.index}]', d.name)
        dpg.set_value('stdout'  , payload)
        # Turn unlocked cheevo display optional
        if Preferences.settings['show-unlocks']:
            dpg.set_value('unlocked', unlocked)
            dpg.set_item_pos('unlocked', (31,(26*Cheevo.global_index)))
    
    def clear():
        dpg.set_value('stdout', '')
        if Preferences.settings['simple_ui']: return
        for i in range(0,Cheevo.max):
            dpg.hide_item(f'cheevo[{i+1}]')
        dpg.set_value('unlocked', '')

    def refresh(sender=None, user_data=None, args=None):
        Ramon.requesting = True
        Ramon.timer = None
        Cheevo.global_index = 0
        
        if Preferences.settings['offline']:
            Ramon.data.last_activity = datetime.strptime(Preferences.settings['last_date'], "%d %b %Y, %H:%M")
            Ramon.data.last_seen     = Preferences.settings['last_game']
            Ramon.data.site_rank     = Preferences.settings['rank']
            Ramon.data.score         = Preferences.settings['score']
        Log.info("Scraping data...")
        metadata = Ramon.data.query()
        if metadata is not False:
            Log.info("Scraping done.")
            Ramon.redraw()
            Ramon.data.writeCheevo()
            Plugin.runLoaded()
            Ramon.title('tRAckOverlayer - '+("Offline Mode" if Preferences.settings["offline"] else "Ready"))
        else:
            Log.warning("Scraping failed.")
            Ramon.msg('Wrong Username Specified / RetroAchievements is Down')        
            Ramon.requesting = False
            return False
        Ramon.requesting = False
        return True

    def debugMode():
        if not Preferences.settings['debug']:return
        from dearpygui import dearpygui as D
        Preferences.show()
        D.set_value('preferences-tabs', 'tab_database')
        Plugin.debug = Preferences.settings['debug']    

    
def menu(node, parent):
    for name,value in node.items():
        if isinstance(value, dict):
            newmenu = dpg.add_menu(label=elegant(name), parent=parent)
            menu(value, newmenu )
        else:
            dpg.add_menu_item(
                label       = elegant(name), 
                callback    = value[0],
                user_data   = value[1],
                tag         = f"menu-{name.lower()}",
                parent      = parent,
            )