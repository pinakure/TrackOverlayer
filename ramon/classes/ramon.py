import os
from dearpygui              import dearpygui as dpg
from datetime               import datetime
from classes.data           import Data
from classes.cheevo         import Cheevo
from classes.preferences    import Preferences
from classes.log            import Log
from classes.plugin         import Plugin
from classes.ui             import UI , row as ROW, column as COLUMN
from classes.tools          import mkdir, copy
from classes.hotkeys        import HotKeys
from threading              import Timer

class Ramon:
    width               = 1440
    height              = 900
    inner_width         = 0
    inner_height        = 0
    x                   = 0
    y                   = 0
    menu_height         = 20
    titlebar_height     = 18
    log_line_count      = 15
    show_log            = True
    log_height          = (log_line_count * 16)
    statusbar_height    = 20
    padding             = 8    
    restart             = False    
    css                 = {}
    version             = 1.51
    timer               = None    
    plugins             = []
    data                = None
    run                 = True
    requesting          = False
    queue               = []
    
    def updateCheevoManually(sender=None, args=None, user_data=None):
        with open(f'{Ramon.data.root}/data/current_cheevo.txt', "w") as file:
            file.write(dpg.get_value('cheevo'))
        os.truncate(f'{Ramon.data.root}/data/current_cheevo.png',0)
    
    def updateCheevo(sender=None, args=None, user_data=None):
        Cheevo.active_index = user_data
        Ramon.data.game.current = Cheevo.active_index
        Preferences.settings['current_cheevo'] = Cheevo.active_index
        Ramon.data.game.save()
        for i in range(0,Cheevo.max):
            dpg.set_value(f'cheevo[{i+1}]', False)
        dpg.set_value(f'cheevo[{Cheevo.active_index}]', True)
        Ramon.data.writeCheevo()
        Plugin.runLoaded()
        Ramon.redraw()
    
    def exit():
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
        # menu = {
        #     'Actions'   : { 
        #         'Redump'                : Ramon.data.write,
        #         'Refresh'               : Ramon.refresh,
        #         'Compile'               : Ramon.compile,
        #         'Exit'                  : Ramon.exit,
        #     },
        #     'Options'   : { 
        #         'Preferences'           : Preferences.show,
        #         'Message Log'           : Log.show,
        #     },
        #     'Links'   : { 
        #         'Message Log'           : Log.show,
        #         'Twitch'   : { 
        #         },
        #         'RetroAchievements'   : { 
        #         },
        #     },
        # }
        with dpg.menu_bar():
            with dpg.menu(label="Actions"):
                dpg.add_menu_item(label="Redump                "   , callback=Ramon.data.write)
                dpg.add_menu_item(label="Refresh               "   , callback=Ramon.refresh)
                dpg.add_menu_item(label="Compile               "   , callback=Ramon.compile)
                dpg.add_menu_item(label="Exit                  "   , callback=Ramon.exit  )
            with dpg.menu(label="Options"):
                dpg.add_menu_item(label="Preferences"       , tag="preferences" , callback=Preferences.show     )
                dpg.add_menu_item(label="Log"               , tag="view_log"    , callback=Log.show             )
            with dpg.menu(label="Links"):
                dpg.add_menu_item(label="TO Overlay"           , tag="overlay-link" , callback=Ramon.openWeb, user_data="overlay"  )
                with dpg.menu(label="Twitch"):
                    dpg.add_menu_item(label="Chat"              , tag="twitch_chat" , callback=Ramon.openWeb, user_data="twitch-chat"  )
                with dpg.menu(label="RetroAchievements"):
                    dpg.add_menu_item(label="User Profile"      , tag="ra_user_profile" , callback=Ramon.openWeb, user_data="ra-user"     )
                    dpg.add_menu_item(label="Game Profile"      , tag="ra_game_profile" , callback=Ramon.openWeb, user_data="ra-game"     )
                    dpg.add_menu_item(label="Cheevo Page"       , tag="ra_cheevo_page"  , callback=Ramon.openWeb, user_data="ra-cheevo"   )

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
        Preferences.writecfg()

    def start():
        from classes.database   import DDBB
        from classes.server     import Server # private import needed here to avoid import loop
        Preferences.parent = Ramon
        Preferences.loadcfg()
        DDBB.init()
        os.truncate(f'{Preferences.root}/data/current_cheevo.png', 0)
        copy(
            f'{Preferences.settings["root"]}/plugins/default.png',
            f'{Preferences.settings["root"]}/data/current_cheevo.png',
        )
        copy(
            f'{Preferences.settings["root"]}/plugins/default.png',
            f'{Preferences.settings["root"]}/data/current_cheevo_lock.png',
        )

        Ramon.data  = Data(Ramon)
        HotKeys.install()
        mkdir('data')
        mkdir('data/cache')
        mkdir('data/css')
        if Preferences.settings['vertical']:
            w, h = Ramon.width,Ramon.height
            Ramon.height = w
            Ramon.width  = h
        Ramon.plugins = Plugin.discover()
        Ramon.createViewport()
        Ramon.createInterface()        
        Ramon.setPosition( Preferences.settings['x-pos'], Preferences.settings['y-pos'] )
        if not Preferences.settings['username'] or len(Ramon.data.cheevos) == 0:
            Ramon.setProgress(1.0)
        Server.start()
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
            Log.create( Ramon )
            # Create preferences window
            Preferences.create( Ramon )
        
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
            file.write(f'''@title Compiling tRAckOverlayer v.{Ramon.version}...'''+'\n'+'''@move dist\main.exe tRAckOverlayer_debug.exe'''+"\n")
            file.write(f'''@rmdir /q /s xplugins''' +"\n")
            file.write(f'''@python3 -m PyInstaller --onefile -i icon.ico {plugins} main.py '''+'\n'+'''@move dist\main.exe tRAckOverlayer_debug.exe'''+"\n")
            file.write(f'''@python3 -m PyInstaller --onefile --noconsole -i icon.ico {plugins} main.py '''+'\n'+'''@move dist\main.exe tRAckOverlayer.exe'''+"\n")
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
        while dpg.is_dearpygui_running() and Ramon.run and not Ramon.restart:
            dpg.render_dearpygui_frame()
            if Preferences.settings['auto_update'] and not Ramon.timer:
                Ramon.timer = Timer( Preferences.settings['auto_update_rate']*60, Cheevo.checkAll )
                Ramon.timer.start()           
            Ramon.data.dispatchQueue()
            Cheevo.dispatchQueue()
        # ----------------------------------------- LOOP END ----------------------------------------
        # ---------------------------------------- DEINIT START -------------------------------------
        # First of all Remove any timer left so it wont try to run on missing ui elements
        return Ramon.exit()
        
    def exit():
        from classes.server   import Server
        from classes.database import DDBB
        try:
            Server.exit.set()
            DDBB.db.close()
            #Server._thread.stop()
            if Ramon.timer:
                Ramon.timer.cancel()
                Ramon.timer = None
            # Begin deinitialization, begin dumping the log 
            with open('ramon.log', "w") as file:
                file.write(dpg.get_value('log'))
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
            return True
        except Exception as E:
            Log.error("Error during deinitialization", E)
            return False

    def redraw():
        Ramon.clear()
        dpg.set_value('game'  , Ramon.data.last_seen      )
        dpg.set_value('rank'  , Ramon.data.site_rank      )
        dpg.set_value('score' , Ramon.data.score          )
        dpg.set_value('date'  , Ramon.data.last_activity.strftime("%d %b %Y, %H:%M")  )
        dpg.set_value('cheevo', Ramon.data.cheevo         )
        payload  = ''
        unlocked = ''
        Ramon.data.recent = []
        for d in Ramon.data.cheevos:
            if d.locked: 
                payload += d.menu() + "\n"
                dpg.show_item(f'cheevo[{d.index}]')
                dpg.set_item_label(f'cheevo[{d.index}]', d.name)
            else:
                if len(Ramon.data.recent) < 5: 
                    Ramon.data.recent.append(d)
                unlocked += '* '+ d.menu() + "\n"
        #Plugin.compose()
        dpg.set_value('stdout'  , payload)
        dpg.set_value('unlocked', unlocked)
        dpg.set_item_pos('unlocked', (31,(26*Cheevo.global_index)))
    
    def clear():
        dpg.set_value('stdout', '')
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
        if Ramon.data.query():
            Log.info("Scraping done.")
            Ramon.clear()
            Ramon.redraw()
            Ramon.data.write()
            Plugin.runLoaded()
            dpg.set_viewport_title('tRAckOverlayer - '+("Offline Mode" if Preferences.settings["offline"] else "Ready"))
        else:
            Log.warning("Scraping failed.")
            dpg.set_value('stdout','Wrong Username Specified / RetroAchievements is Down')        
            Ramon.requesting = False
            return False
        Ramon.requesting = False
        return True
    
