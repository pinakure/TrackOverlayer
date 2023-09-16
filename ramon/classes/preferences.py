import json
from dearpygui              import dearpygui as dpg
from classes.config         import Config as cfg 
from classes.log            import Log
from classes.ui             import UI
from classes.attribute      import Attribute
from classes.database       import DBTable
from classes.tools          import elegant, Color, parseInt, parseColor, parseFloat, parseBool

    
class Preferences:
    root            = '.'
    width           = cfg.width
    height          = cfg.height
    parent          = None
    data            = None
    
    defaults        = cfg.defaults
    table_game      = None
    
    def nop(sender, value, varname):
        print("Sender : ", sender )
        print("Value  : ", value  )
        print("Varname: ", varname)


    def create( parent ):
        Preferences.parent = parent
        with dpg.window(
            tag         = 'preferences_main',
            label       = "Preferences", 
            width       = Preferences.width, 
            height      = Preferences.height, 
            no_collapse = True, 
            no_resize   = True,
            modal       = True,
            show        = False,
            on_close    = lambda:dpg.hide_item('preferences_main'),
            pos         = (
                (Preferences.parent.width / 2) - (Preferences.width / 2),
                (Preferences.parent.height / 2) - (Preferences.height / 2)
            )
        ):
            with dpg.tab_bar(tag="preferences-tabs"):
                Preferences.createGeneralTab()
                Preferences.createPluginsTab()
                Preferences.createDatabaseTab()

        from classes.plugin import Plugin
        with dpg.file_dialog(
            # directory_selector  = True, 
            show                = False, 
            modal               = True,
            callback            = Plugin.updateFilenameSetting, 
            tag                 = "file_dialog_id",
            cancel_callback     = Preferences.nop, 
            file_count          = 1,
            width               = 700,
            height              = 400,            
            user_data           = '--plugin-variable-name--',
        ):
            dpg.add_file_extension(".*")
            dpg.add_file_extension("", color=(150,255,150,255))
            dpg.add_file_extension("Picture files (*.png *.jpg *.gif){.png,.jpg,.gif}", color=(0, 255, 255, 255))
            dpg.add_file_extension("Audio files (*.wav *.mp3 ){.wav,.mp3}", color=(0, 255, 255, 255))
            

    def createGeneralTab():
        from classes.plugin import Plugin
        with dpg.tab(label="General", tag="tab_general"):
            with dpg.child_window():
                UI.setCursor(0,0)
                last_width,last_count = UI.setColumns(4, (Preferences.width/4)-8)
                UI.label        ("Interface"        , Color.grape        , left_align=True   ); UI.jump()
                UI.checkbox     ("Simple UI"        , 'simple_ui'                           , enabled = False)
                UI.checkbox     ("Fullscreen"       , 'fullscreen'                          )
                UI.checkbox     ("Vertical Layout"  , 'vertical'                            )
                UI.jump()
                UI.jump()
                
                UI.label        ("Window Geometry"  , Color.grape       , left_align=True   )
                UI.jump()
                UI.numeric      ("Width"            , 'width'                               , callback=Preferences.updateSettingVideo )
                UI.numeric      ("Height"           , 'height'                              , callback=Preferences.updateSettingVideo )
                UI.numeric      ("X Position"       , 'x-pos'                               , callback=Preferences.updateSettingVideo )
                UI.numeric      ("Y Position"       , 'y-pos'                               , callback=Preferences.updateSettingVideo )
                UI.jump()
                
                UI.setColumns   (last_count, last_width)
                last_width,last_count = UI.setColumns(4, Preferences.width/4)
                
                UI.label        ("Twitch"           , Color.grape       , left_align=True   )
                UI.jump()
                UI.textfield    ("IRC Password"     , 'twitch-password' , password=True     )
                UI.checkbox     ("Use API"          , 'twitch-use-api'                      )
                UI.textfield    ("API Key"          , 'twitch-app-key'  , password=True     ) 
                UI.textfield    ("IRC Channel"      , 'twitch-username'                     )
                UI.jump()
                UI.label        ("RetroAchievements", Color.grape       , left_align=True   )
                UI.jump()
                UI.textfield    ("RA Password"      , 'password'        , password=True     )
                UI.checkbox     ("Use API"          , 'ra-use-api'                          )
                UI.textfield    ("API Key"          , 'ra-app-key'      , password=True     )
                UI.jump()
                UI.jump()
                UI.label        ("RA Scraper Setup" , Color.grape        , left_align=True   ); UI.jump()
                UI.checkbox     ("Offline Mode"     , 'offline'                             )
                UI.checkbox     ("Auto Refresh"     , 'auto_update'                         )
                UI.numeric      ("Refresh Rate"     , 'auto_update_rate'                    )
                #UI.textfield    ("Username"         , 'username'                          ); UI.jump()
                UI.jump()
                UI.label        ("Plugin Overlay Setup", Color.grape        , left_align=True   )
                UI.jump()
                UI.checkbox     ("No Welcome"       , 'no-welcome'                              , callback=Plugin.updateOverlaySetting)
                UI.checkbox     ("Debug Mode"       , 'debug'                                   , callback=Plugin.updateOverlaySetting)
                UI.numeric      ("Plugin Rate"      , "plugin-rate"                             , callback=Plugin.updateOverlaySetting)
                

    
    def createDatabaseTab():
        from classes.plugin import Plugin
        with dpg.tab(label="Database", tag="tab_database"):
            with dpg.child_window():
                with dpg.tab_bar(tag="database-tabs"):
                    # Create as many tabs as tables on the database
                    Preferences.table_game = DBTable.create(
                        'game', 
                        fields=[
                            'id',
                            'romname',
                            'name',
                            'subset',
                            'picture',
                            'cached',
                            'current',
                            'platform',
                        ], 
                        editable=['romname', 'name']
                    )
                    Preferences.table_cheevo = DBTable.create(
                        'cheevo', 
                        fields=[
                            'id',
                            'name',
                            'description',
                            'locked',
                            'notified',
                            'picture',
                            'index',
                            'cached',
                            'game',                            
                        ], 
                        editable=['description', 'name', 'notified']
                    )
                    Preferences.table_superchat = DBTable.create(
                        'superchat', 
                        fields=[
                            'id',
                            'avatar',
                            'user',
                            'quantity',
                            'currency',
                            'text',
                            'acknowledged',                    
                        ], 
                        editable=['acknowledged']
                    )
                    
        Preferences.table_game.update()        

    def createPluginsTab():
        from classes.plugin import Plugin
        with dpg.tab(label="Plugins", tag="tab_plugins"):
            with dpg.child_window():
                with dpg.tab_bar(tag="plugin-tabs"):
                    with dpg.tab(label="General", tag="tab_plugins-general"):
                        with dpg.child_window():
                            plugins = Plugin.discover()
                            available_plugins = list(plugins)
                            labels = [ 
                                dpg.add_text("Found"        , color=(255,255,0)), 
                                dpg.add_text("Enabled"      , color=(255,255,0)), 
                            ]
                            dpg.configure_item(labels[0], pos=(   8,   8 ) )
                            dpg.configure_item(labels[1], pos=( 500,   8 ) )
                            dpg.add_listbox(tag='available-plugins' , items=available_plugins   , width=484, num_items=25, pos=(   8,  32 ), callback=Plugin.enable , default_value=None)
                            with dpg.tooltip('available-plugins'):
                                dpg.add_text("Click a plugin to enable it")
                            dpg.add_listbox(tag='enabled-plugins'   , items=[]                  , width=484, num_items=25, pos=( 500,  32 ), callback=Plugin.disable, default_value=None)
                            with dpg.tooltip('enabled-plugins'):
                                dpg.add_text("Click a plugin to disable it")

    def populatePluginsTab():
        global _item_details
        UI.columns = [ 8, 450 ]
        UI.setColumnWidth(445)
        from classes.plugin     import Plugin        
        # Make a tab for every plugin' settings
        for name, plugin in Plugin.loaded.items():
            clearVariableBuffer()
            with dpg.tab(label=name, tag=f"tab_plugins-{name}", parent='plugin-tabs'):
                Attribute.parent = f'tab-window-{name}'
                #
                # Create main plugin controls, collect all details on the way to dump them altogether in
                # the window we are about to create right after this one. 
                # Note only fields matching certain suffixes will be collected and therefore 
                # those will not show on the main window
                #                
                with dpg.child_window(border=False, tag=Attribute.parent, height=cfg.main.height) as window:
                    Attribute.label(8, 8, plugin.description, color=(55,155,255))
                    UI.setCursor(0,1)
                    _item_details = False
                    for name,value in plugin.settings.items():
                        if capturePluginItemSetting( name, value ): continue
                        # general setting (placed in the upper area )
                        Attribute.plugin = plugin.name
                        if   isinstance( value, bool )  : Attribute.boolean (0,0, name, value , callback=Plugin.updateSettings)
                        elif isinstance( value, int  )  : Attribute.integer (0,0, name, value , callback=Plugin.updateSettings)
                        elif isinstance( value, float)  : Attribute.integer (0,0, name, value , callback=Plugin.updateSettings)
                        #elif name.endswith('-file')     : Attribute.filename(0,0, name, value , callback=Plugin.selectFilename)
                        elif '|' in value               : Attribute.combo   (0,0, name, value , callback=Plugin.updateComboSettings)
                        else                            : Attribute.text    (0,0, name, value , callback=Plugin.updateSettings)
                
                    if not len(colors):
                        dpg.configure_item(window, height=381)
                    #
                    # Add buttons on main window
                    #
                    dpg.add_button(label="Preview", pos=( cfg.width - 96, 8), callback=Preferences.parent.openWeb,  user_data=plugin.name)
                    dpg.add_button(label="Default", pos=( cfg.width - 96,48), callback=Plugin.setDefaults, user_data=plugin.name)
                if not _item_details: continue
                #
                # Create plugin details window and all expected details controls
                #
                detail_height   = cfg.detail.height
                extra           = cfg.detail.extra
                with dpg.child_window( no_scrollbar=True, pos=(8,Preferences.height - extra - detail_height), height=detail_height):
                    with dpg.tab_bar(tag=f"plugin-tabs-{plugin.name}"):
                        for name, color in colors.items():
                            gname = name.rstrip("-color")
                            group = f'plugin-setting-{plugin.name}-{gname}'
                            tname = f"tab-plugins-{plugin.name}-{gname}"
                            Attribute.setup( gname, group, types, name, sizes, heights, italics, bolds, shadows, posxs, posys, blurs, bcolors, bwidths, sposxs, sposys, bradius, sizexs, sizeys )
                            with dpg.tab( label = elegant(gname), tag = tname ):
                                with dpg.child_window(no_scrollbar=True, height=180) as window:
                                    Attribute.color         (   3,  13 , color, callback=Plugin.updateColor)
                                    # if name.replace('color', 'font') in types.keys():
                                    #     Attribute.label         ( 220,   8 , "Font Settings", parent=window)
                                    Attribute.font          ( 220,  32 , callback=Plugin.updateSettings)
                                    Attribute.font_size     ( 318,  32 , callback=Plugin.updateSettings)
                                    Attribute.line_height   ( 360,  32 , callback=Plugin.updateSettings)
                                    Attribute.italic        ( 318,   8 , callback=Plugin.updateSettings)
                                    Attribute.bold          ( 339,   8 , callback=Plugin.updateSettings)
                                    # if name.replace('color', 'shadow') in shadows.keys():
                                    #     Attribute.label         ( 220,  54 , "Shadow Color", parent=window)
                                    Attribute.shadow        ( 220,  75 , callback=Plugin.updateColor)
                                    Attribute.shadow_pos_x  ( 370,  70 , callback=Plugin.updateSettings)
                                    Attribute.shadow_pos_y  ( 370,  90 , callback=Plugin.updateSettings)
                                    Attribute.pos_x         ( 410,  12 , callback=Plugin.updateSettings)
                                    Attribute.pos_y         ( 410,  32 , callback=Plugin.updateSettings)
                                    Attribute.size_x        ( 219,  12 , callback=Plugin.updateSettings)
                                    Attribute.size_y        ( 219,  32 , callback=Plugin.updateSettings)
                                    Attribute.shadow_blur   ( 370, 110 , callback=Plugin.updateSettings)
                                    Attribute.border_width  ( 370, 130 , callback=Plugin.updateSettings)
                                    Attribute.border_radius ( 370, 150 , callback=Plugin.updateSettings)
                                    # if name.replace('color', 'border-color') in bcolors.keys():
                                    #     Attribute.label         ( 442,  54 , "Border Color", parent=window)
                                    Attribute.border_color  ( 442,  75 , callback=Plugin.updateColor)
    def show():
        dpg.hide_item('preferences_main')
        dpg.show_item('preferences_main')

    def hide():
        dpg.hide_item('preferences_main')

    def writecfg( restart=False ):
        Preferences.root = Preferences.settings['root']        
        with open(f'{Preferences.root}/config.txt', 'w') as file:
            for key,value in Preferences.settings.items():
                file.write(f'{key}={value}'+"\n")
        Preferences.parent.restart = restart
    
    def loadcfg():
        from classes.cheevo import Cheevo
        Preferences.settings = Preferences.defaults
        Preferences.settings.update({'version' : Preferences.parent.version})
        Preferences.root     = Preferences.settings['root']
        
        try:
            with open(f'{Preferences.root}/config.txt', 'r') as file:
                data = file.read().split('\n')
                for setting in data:
                    if len(setting)==0:continue
                    parts = setting.split('=')
                    Preferences.settings[parts[0]] = True if parts[1].lower() == 'true' else False if parts[1].lower() == 'false' else parts[1]
            try:
                if Preferences.settings['version'] == Preferences.parent.version:
                    Log.info(f"PREFERENCES : Found version {Preferences.settings['version']} config file")
            except:
                Log.warning("PREFERENCES : Configuration file was invalid. Generating new one.")
                root = Preferences.settings['root']
                username = Preferences.settings['username']
                Preferences.settings = Preferences.defaults
                Preferences.settings['root'     ] = root
                Preferences.settings['username' ] = username
            Preferences.root                            = Preferences.settings['root']
            Preferences.parent.width                    = int(Preferences.settings['width' ]) - (4 if Preferences.settings['fullscreen'] else 0)
            Preferences.parent.height                   = int(Preferences.settings['height'])
            Preferences.settings['width']               = Preferences.parent.width
            Preferences.settings['height']              = Preferences.parent.height
            json_fields = [
                'x-pos'                     ,
                'y-pos'                     ,
                'gmt'                       ,
                'auto_update_rate'          ,
                'pending_cheevos'           ,
                'unlocked_cheevos'          ,
                'current_cheevo'            ,                
            ]
            for field in json_fields:                
                Preferences.settings[field] = json.loads( str(Preferences.settings[field]) )
            Cheevo.active_index = Preferences.settings['current_cheevo']

            # Restore last session if any
            if 'session' in Preferences.settings.keys():
                Log.info("Found session data in config file")
                sessiondata = json.loads(Preferences.settings['session'])
                if len(sessiondata):
                    Log.info("Attempting session restore...")
                    session = sessiondata
            else: 
                session = None
            

        except Exception as E:
            Log.error("PREFERENCES : Cannot parse/load config.txt", E)
            return 

    def updatePluginLists():
        from classes.plugin import Plugin
        items = [ plugin.name for name,plugin in Plugin.loaded.items() if plugin.settings['enabled']]
        dpg.configure_item( 'enabled-plugins', items=items )        
    
    def updateSetting(sender=None, value=None, refresh=False):
        Preferences.settings[sender]         = dpg.get_value(sender)
        Preferences.writecfg( restart=False )
        if refresh: Preferences.parent.refresh()
    
    def updateSettingInteger(sender=None, value=None, user_data=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        Preferences.writecfg( restart=False )
   
    def updateSettingVideo(sender=None, value=None, user_data=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        dpg.set_viewport_pos( (Preferences.settings['x-pos'], Preferences.settings['y-pos']) )
        dpg.set_viewport_width( Preferences.settings['width'] +16 )
        dpg.set_viewport_height( Preferences.settings['height'] )
        dpg.configure_item( 'main', width=Preferences.settings['width'], height=Preferences.settings['height'] )
        Preferences.writecfg( restart=False )












#
# END - OF - FILE 
#






















































































































#HACK Dont blame me, this makes the construction of the UI and gathering properties without
# caring of which order they come into, it works too fast it worths the hassle of having 
# this piece of shit down here. Sorry about your eyes, who told you to see further the end of
# the class definition ? =)
# 
# 
# 
# field collectors
#
# 
# 
sizexs      = {}
sizeys      = {}
bradius     = {}
bwidths     = {}
bcolors     = {}
colors      = {}
types       = {}
heights     = {}
italics     = {}
bolds       = {}
posxs       = {}
posys       = {}
sposys      = {}
sposxs      = {}
blurs       = {}
shadows     = {}
sizes       = {}

def clearVariableBuffer():
    global sizexs
    global sizeys
    global bradius
    global bwidths
    global bcolors
    global colors
    global types 
    global heights
    global italics
    global bolds
    global posxs
    global posys
    global sposys
    global sposxs
    global blurs
    global shadows
    global sizes
    [ 
        sizexs, 
        sizeys, 
        bradius,
        bwidths, 
        bcolors, 
        colors, 
        types , 
        heights, 
        italics, 
        bolds, 
        posxs, 
        posys, 
        sposys, 
        sposxs, 
        blurs, 
        shadows, 
        sizes ,
    ] = [ 
        {} , 
        {} , 
        {} , 
        {} , 
        {} , 
        {} , 
        {} , 
        {} , 
        {}, 
        {}, 
        {}, 
        {}, 
        {}, 
        {}, 
        {}, 
        {}, 
        {},
    ]    

# plugin preferences config globals
_item_details = 0

def capturePluginItemSetting(name : str, value : str):
        global _item_details
        # Skip corrupt or malformed settings
        if name in ['enabled', '']: return True
        if name.startswith('.'): return True
        # Process settings which always come grouped, such as                         
        # - Item color, font, line height
        # These will be placed in individual tabs grouped, to do so use 
        # the same prefix for line-height, font-size and color, then they will
        # spawn in the same tab. 
        if   '-border-color'    in name: _item_details = True; bcolors[name] = value; return True     
        elif '-border-width'    in name: _item_details = True; bwidths[name] = value; return True     
        elif '-border-radius'   in name: _item_details = True; bradius[name] = value; return True     
        elif '-shadow-color'    in name: _item_details = True; shadows[name] = value; return True
        elif '-shadow-pos-x'    in name: _item_details = True; sposxs [name] = value; return True
        elif '-shadow-pos-y'    in name: _item_details = True; sposys [name] = value; return True
        elif '-color'           in name: _item_details = True; colors [name] = value; return True     
        elif '-font-size'       in name: _item_details = True; sizes  [name] = value; return True
        elif '-line-height'     in name: _item_details = True; heights[name] = value; return True
        elif '-font-italic'     in name: _item_details = True; italics[name] = parseBool(value); return True
        elif '-font-bold'       in name: _item_details = True; bolds  [name] = parseBool(value); return True
        elif '-pos-x'           in name: _item_details = True; posxs  [name] = value; return True
        elif '-pos-y'           in name: _item_details = True; posys  [name] = value; return True
        elif '-size-x'          in name: _item_details = True; sizexs [name] = value; return True
        elif '-size-y'          in name: _item_details = True; sizeys [name] = value; return True
        elif '-shadow-blur'     in name: _item_details = True; blurs  [name] = value; return True
        elif '-font'            in name: _item_details = True; types  [name] = value; return True                        
        return False

# Anyway, if you're MrCheevos or LeslieMishigan, thanks for coming so far to check my code. I'm very glad. 