import json, os 
from datetime               import datetime, timedelta
from dearpygui              import dearpygui as dpg
from classes.cheevo         import Cheevo
from classes.dynamic_css    import DynamicCSS, fonts
from classes.log            import Log


class cfg:
    class range:
        pos_x   = [-1440, 1440]
        pos_y   = [-1080, 1080]
        size_x  = [-1440, 1440]
        size_y  = [-1080, 1440]
        zoom    = [ 1   ,  100]

    class main:
        height  = 282
    class detail:
        height  = 220
        extra   = 68

        
def elegant( filthy ):
    # TODO: move to tools
    return filthy.replace('_', ' ').replace('-', ' ').capitalize()

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
    

class Preferences:
    root            = '.'
    width           = 1024#640
    height          = 600#480
    parent          = None
    data            = None
    
    
    def writecfg( restart=False ):
        Preferences.root = Preferences.settings['root']        
        with open(f'{Preferences.root}/config.txt', 'w') as file:
            for key,value in Preferences.settings.items():
                file.write(f'{key}={value}'+"\n")
        Preferences.parent.restart = restart

    
    def loadcfg():
        defaults = {
            'version'                   : Preferences.parent.version,
            'last_game'                 : 'TestGame',
            'last_date'                 : '01 Jan 2000, 00:00',
            'rank'                      : '1 / 50,000',
            'debug'                     : False,
            'score'                     : '999999',
            'width'                     : 1440,
            'height'                    :  900,
            'x-pos'                     :    0,
            'y-pos'                     :    0,
            'auto_update'               : True,
            'auto_update_rate'          : 1,
            'fullscreen'                : False,
            'vertical'                  : False,
            'username'                  : '',
            'password'                  : '',
            'twitch-username'           : '',
            'twitch-password'           : '',
            'root'                      : '.',
            'gmt'                       : 2,
            'twitch-app-key'            : '',
            'twitch-use-api'            : False,
            'ra-use-api'                : False,
            'ra-app-key'                : '',
            'offline'                   : False,
            'simple_ui'                 : False,
            'pending_cheevos'           : [0,255,255],
            'unlocked_cheevos'          : [64, 128,0],
            'current_cheevo'            : 1,
        }
        Preferences.settings = defaults
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
                    Log.info(f"Found version {Preferences.settings['version']} config file")
            except:
                Log.warning("Configuration file was invalid. Generating new one.")
                root = Preferences.settings['root']
                username = Preferences.settings['username']
                Preferences.settings = defaults
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
        except Exception as E:
            Log.error("Cannot parse/load config.txt", E)
            return 

    
    def updateSettingsGMT(sender=None, user_data=None, args=None):
        Preferences.settings['gmt'] = int(dpg.get_value('gmt'))
        Preferences.data.last_activity  = (datetime.strptime(Preferences.data.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Preferences.settings['gmt']))
        with open(f'{Preferences.root}/data/last_activity.txt'  , 'w') as file:   file.write(Preferences.data.last_activity.strftime("%d %b %Y, %H:%M").upper() )
        dpg.set_value('date'  , Preferences.data.last_activity.strftime("%d %b %Y, %H:%M")  )
        Preferences.writecfg( restart = False )

    
    def updateUsername(sender=None, user_data=None, args=None):
        Preferences.settings['username'] = dpg.get_value('username')
        Preferences.writecfg( restart=False)
        Preferences.parent.refresh()

    
    def updateSetting(sender=None, user_data=None, args=None):
        Preferences.settings[sender]         = dpg.get_value(sender)
        Preferences.writecfg( restart=False )
    
    
    def updateSettingBoolean(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = dpg.get_value(sender)
        Preferences.writecfg( restart=False )
    
    
    def updateSettingInteger(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        Preferences.writecfg( restart=False )
   
    
    def updateSettingVideo(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        dpg.set_viewport_pos( (Preferences.settings['x-pos'], Preferences.settings['y-pos']) )
        dpg.set_viewport_width( Preferences.settings['width'] +16 )
        dpg.set_viewport_height( Preferences.settings['height'] )
        dpg.configure_item( 'main', width=Preferences.settings['width'], height=Preferences.settings['height'] )
        Preferences.writecfg( restart=False )
   
    
    def updateSettingColor(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = dpg.get_value(sender)        
        Preferences.writecfg( restart=False )
   
    
    def createInterfaceTab():
        with dpg.tab(label="Interface", tag="tab_general"):
            with dpg.child_window():
                dpg.add_text("General", color=(255,255,0))
                createBooleanField('Simple UI       '   , 'simple_ui'       , restart=True)
                dpg.configure_item('simple_ui', enabled=False)
                createBooleanField('Fullscreen      '   , 'fullscreen'      , restart=True)
                # Window dimensions
                dpg.add_text("Window Geometry", color=(255,255,0))
                createBooleanField('Vertical Layout ( swaps width & height )', 'vertical'        , restart=True)
                createIntegerField('Width'              , 'width'           , min_value=320,max_value=1440, callback=Preferences.updateSettingVideo)
                createIntegerField('Height'             , 'height'          , min_value=320,max_value=1440, callback=Preferences.updateSettingVideo)
                createIntegerField('X Position'         , 'x-pos'           , min_value=0,  max_value=3000, callback=Preferences.updateSettingVideo)
                createIntegerField('Y Position'         , 'y-pos'           , min_value=0,  max_value=3000, callback=Preferences.updateSettingVideo)
                # Window colors
                dpg.add_text("Achievement Colors", tag='ach-colors', color=(255,255,0))
                createColorField  ('Pending '   , 'pending_cheevos' )
                createColorField  ('Unlocked'   , 'unlocked_cheevos' )
                pos = dpg.get_item_pos('ach-colors')
                dpg.configure_item('pending_cheevos' , pos=(0, 240))
                pos = dpg.get_item_pos('pending_cheevos')
                dpg.configure_item('unlocked_cheevos', pos=(pos[0]+192, pos[1]))
                dpg.set_value('unlocked_cheevos', Preferences.settings['unlocked_cheevos'   ])
                dpg.set_value('pending_cheevos' , Preferences.settings['pending_cheevos'    ])
                
    
    def loadCustomization( category ):
        return
        DynamicCSS.settings[category]['border-width'    ] = Preferences.settings[f'{category}-border-width' ]
        DynamicCSS.settings[category]['border-radius'   ] = Preferences.settings[f'{category}-border-radius']
        DynamicCSS.settings[category]['border-color'    ] = Preferences.settings[f'{category}-border-color' ]
        DynamicCSS.settings[category]['3d'              ] = Preferences.settings[f'{category}-3d'           ]
        DynamicCSS.settings[category]['perspective'     ] = Preferences.settings[f'{category}-perspective'  ]
        DynamicCSS.settings[category]['rotation'        ] = Preferences.settings[f'{category}-rotation'     ]
        DynamicCSS.settings[category]['position'        ] = [ Preferences.settings[f'{category}-x'], Preferences.settings[f'{category}-y']]
        try:
            DynamicCSS.settings[category]['active-color'  ] = Preferences.settings[f'{category}-active-color' ]
        except: 
            Log.warning(f"No 'active-color' set for {category}. Skipping variable setup.")
        try:
            DynamicCSS.settings['recent']['font'            ] = Preferences.settings['recent-font'          ]
            DynamicCSS.settings['recent']['font-size'       ] = Preferences.settings['recent-font-size'     ]
            DynamicCSS.settings['recent']['font-color'      ] = Preferences.settings['recent-font-color'    ]
            DynamicCSS.settings['recent']['font-glow'       ] = Preferences.settings['recent-font-glow'     ]
        except: 
            Log.warning(f"No 'font' set for {category}. Skipping variable setup.")
        try:
            DynamicCSS.settings['progress']['overlay'       ] = Preferences.settings['progress-overlay-text']
            DynamicCSS.settings['progress']['hard'          ] = Preferences.settings['progress-hard-gradient']
            DynamicCSS.settings['progress']['upper-color'   ] = Preferences.settings['progress-upper-color' ]
            DynamicCSS.settings['progress']['lower-color'   ] = Preferences.settings['progress-lower-color' ]
        except: 
            Log.warning(f"No 'gradient' set for {category}. Skipping variable setup.")
        
    
    def loadCustomizations():
        return
        Preferences.loadCustomization('cheevos' )
        Preferences.loadCustomization('locked'  )
        Preferences.loadCustomization('unlocked')
        Preferences.loadCustomization('recent'  )
        # Manual fixes for locked and unlocked 
        DynamicCSS.settings['locked'    ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        DynamicCSS.settings['unlocked'  ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        DynamicCSS.settings['recent'    ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        
    
    def updateCustomizations(sender=None, args=None, user_data=None):
        return
        Preferences.settings['progress-hard-gradient'   ] = dpg.get_value('progress-hard-gradient'      )
        Preferences.settings['progress-upper-color'     ] = dpg.get_value('progress-upper-color'        )
        Preferences.settings['progress-lower-color'     ] = dpg.get_value('progress-lower-color'        )
        Preferences.settings['progress-overlay-text'    ] = dpg.get_value('progress-overlay-text'       )
        Preferences.settings['cheevos-border-radius'    ] = int(dpg.get_value('cheevos-border-radius'   ))
        Preferences.settings['locked-border-radius'     ] = int(dpg.get_value('locked-border-radius'    ))
        Preferences.settings['unlocked-border-radius'   ] = int(dpg.get_value('unlocked-border-radius'  ))
        Preferences.settings['cheevos-border-width'     ] = int(dpg.get_value('cheevos-border-width'    ))
        Preferences.settings['recent-border-radius'     ] = int(dpg.get_value('recent-border-radius'    ))
        Preferences.settings['locked-border-width'      ] = int(dpg.get_value('locked-border-width'     ))
        Preferences.settings['unlocked-border-width'    ] = int(dpg.get_value('unlocked-border-width'   ))
        Preferences.settings['recent-border-width'      ] = int(dpg.get_value('recent-border-width'     ))        
        Preferences.settings['cheevos-border-color'     ] = dpg.get_value    ('cheevos-border-color'    )
        Preferences.settings['cheevos-active-color'     ] = dpg.get_value    ('cheevos-active-color'    )
        Preferences.settings['locked-border-color'      ] = dpg.get_value    ('locked-border-color'     )
        Preferences.settings['unlocked-border-color'    ] = dpg.get_value    ('unlocked-border-color'   )
        Preferences.settings['recent-border-color'      ] = dpg.get_value    ('recent-border-color'     )
        Preferences.settings['recent-font'              ] = dpg.get_value    ('recent-font'             )
        Preferences.settings['recent-font-size'         ] = int(dpg.get_value('recent-font-size'        ))
        Preferences.settings['recent-font-color'        ] = dpg.get_value    ('recent-font-color'       )
        Preferences.settings['recent-font-glow'         ] = dpg.get_value    ('recent-font-glow'        )
        Preferences.settings['recent-3d'                ] = dpg.get_value    ('recent-3d'               )
        Preferences.settings['recent-perspective'       ] = int(dpg.get_value('recent-perspective'      ))
        Preferences.settings['recent-rotation'          ] = int(dpg.get_value('recent-rotation'         ))
        Preferences.settings['recent-x'                 ] = int(dpg.get_value('recent-x'                ))
        Preferences.settings['recent-y'                 ] = int(dpg.get_value('recent-y'                ))
        Preferences.settings['unlocked-3d'              ] = dpg.get_value    ('unlocked-3d'             )
        Preferences.settings['unlocked-perspective'     ] = int(dpg.get_value('unlocked-perspective'    ))
        Preferences.settings['unlocked-rotation'        ] = int(dpg.get_value('unlocked-rotation'       ))
        Preferences.settings['unlocked-x'               ] = int(dpg.get_value('unlocked-x'              ))
        Preferences.settings['unlocked-y'               ] = int(dpg.get_value('unlocked-y'              ))        
        Preferences.settings['locked-3d'                ] = dpg.get_value    ('locked-3d'               )
        Preferences.settings['locked-perspective'       ] = int(dpg.get_value('locked-perspective'      ))
        Preferences.settings['locked-rotation'          ] = int(dpg.get_value('locked-rotation'         ))
        Preferences.settings['locked-x'                 ] = int(dpg.get_value('locked-x'                ))
        Preferences.settings['locked-y'                 ] = int(dpg.get_value('locked-y'                ))        
        Preferences.settings['cheevos-3d'               ] = dpg.get_value    ('cheevos-3d'              )
        Preferences.settings['cheevos-perspective'      ] = int(dpg.get_value('cheevos-perspective'     ))
        Preferences.settings['cheevos-rotation'         ] = int(dpg.get_value('cheevos-rotation'        ))
        Preferences.settings['cheevos-x'                ] = int(dpg.get_value('cheevos-x'               ))
        Preferences.settings['cheevos-y'                ] = int(dpg.get_value('cheevos-y'               ))
        Preferences.loadCustomizations()
        Preferences.writecfg( restart=False )

    
    def addCustomizationPanel(tag):
        return
        file = {
            'cheevos'           : 'cheevos',
            'locked'            : 'cheevos_locked',
            'unlocked'          : 'cheevos_unlocked',
            'progress'          : 'progress',
            'recent'            : 'recent',
        }[tag]
        with dpg.child_window():
            dpg.add_text("Shape & Behavior", color=(255,255,0))
            createIntegerField('Border Radius'      , f'{tag}-border-radius'   , max_value=128, callback=Preferences.updateCustomizations)
            createIntegerField('Border Width'       , f'{tag}-border-width'    , max_value=16 , callback=Preferences.updateCustomizations)
            dpg.add_text("Widget colors"            , color=(255,255,0), pos=(8,84))
            if tag=='cheevos':
                createColorField('Active'               , f'{tag}-active-color'    , callback=Preferences.updateCustomizations)
            createColorField('Border'                   , f'{tag}-border-color'    , callback=Preferences.updateCustomizations)
            if tag=='cheevos':
                dpg.configure_item(f'{tag}-active-color', pos=(14,108))
                pos = dpg.get_item_pos(f'{tag}-active-color')
                dpg.configure_item(f'{tag}-border-color', pos=(pos[0]+192, pos[1]))
            else:
                dpg.configure_item(f'{tag}-border-color', pos=(14,108))
            dpg.add_button(label="Edit CSS File", pos=(Preferences.width - 132,3) , tag=f"css-{tag}"    , callback=lambda: os.system('notepad '+Preferences.root.replace('/', '\\')+"\\css\\"+tag+".css"))
            dpg.add_button(label="Apply Changes", pos=(Preferences.width - 132,24), tag=f"gen-{tag}"    , callback=DynamicCSS.customize, user_data=Preferences.parent.css[tag])
            dpg.add_button(label="Open  Preview", pos=(Preferences.width - 132,45), tag=f"preview-{tag}", callback=lambda: os.system('start '+Preferences.root.replace('/', '\\')+"\\data\\"+file+".html"))
            with dpg.child_window(
                tag=f'{tag}-effect-settings',
                pos=(Preferences.width - 240, 80),
            ):                                     
                with dpg.tab_bar():
                    with dpg.tab( label="3D Effects" ):                                
                        createBooleanField("Enable"     , f'{tag}-3d'           , callback=Preferences.updateCustomizations)
                        dpg.add_text("3D Perspective"   , color=(255,255,0))
                        createIntegerField(None         , f'{tag}-perspective'  , callback=Preferences.updateCustomizations, min_value=   1, max_value=1600)
                        dpg.add_text("Angle"            , color=(255,255,0))
                        createIntegerField(None         , f'{tag}-rotation'     , callback=Preferences.updateCustomizations, min_value=-180, max_value= 180)
                        dpg.add_text("Position"         , color=(255,255,0))
                        createIntegerField("X"          , f'{tag}-x'            , callback=Preferences.updateCustomizations, min_value=-800, max_value= 800)
                        createIntegerField("Y"          , f'{tag}-y'            , callback=Preferences.updateCustomizations, min_value=-800, max_value= 800)

    
    def addProgressPanel():
        return
        with dpg.child_window():
            dpg.add_text("Progressbar colors"           , color=(255,255,0))
            createBooleanField('Overlay Percentage'     , 'progress-overlay-text'    , callback=Preferences.updateCustomizations)
            createBooleanField('Hard Gradient'          , 'progress-hard-gradient'   , callback=Preferences.updateCustomizations)
            createColorField('Upper'                    , 'progress-upper-color'     , callback=Preferences.updateCustomizations)
            dpg.configure_item('progress-upper-color'   , pos=(14,80))
            pos = dpg.get_item_pos('progress-upper-color')
            createColorField('Lower'                    , 'progress-lower-color'     , callback=Preferences.updateCustomizations)
            dpg.configure_item('progress-lower-color'   , pos=(pos[0]+192, pos[1]))
            dpg.add_button(label="Edit CSS File"        , pos=(Preferences.width - 132, 3), tag="css-progress"      , callback=lambda: os.system('notepad '+Preferences.root.replace('/', '\\')+"\\css\\progress.css"))
            dpg.add_button(label="Apply Changes"        , pos=(Preferences.width - 132,24), tag="gen-progress"      , callback=DynamicCSS.customize, user_data=Preferences.parent.css['progress'])
            dpg.add_button(label="Open  Preview"        , pos=(Preferences.width - 132,45), tag="preview-progress"  , callback=lambda: os.system('start '+Preferences.root.replace('/', '\\')+"\\data\\progress.html"))

    
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
                                dpg.add_text("  Debug Mode" , color=(255,255,0)), 
                                dpg.add_text(" Reload Time" , color=(255,255,0)), 
                            ]
                            dpg.configure_item(labels[0], pos=(   8,   8 ) )
                            dpg.configure_item(labels[1], pos=( 500,   8 ) )
                            dpg.configure_item(labels[2], pos=(   8, 400 ) )
                            dpg.configure_item(labels[3], pos=(   8, 424 ) )
                            dpg.add_listbox(tag='available-plugins' , items=available_plugins   , width=484, num_items=20, pos=(   8,  32 ), callback=Plugin.enable , default_value=None)
                            with dpg.tooltip('available-plugins'):
                                dpg.add_text("Click a plugin to enable it")
                            dpg.add_listbox(tag='enabled-plugins'   , items=[]                  , width=484, num_items=20, pos=( 500,  32 ), callback=Plugin.disable, default_value=None)
                            with dpg.tooltip('enabled-plugins'):
                                dpg.add_text("Click a plugin to disable it")
                            dpg.add_checkbox(tag="debugplugins"     , callback=Plugin.toggleDebug,default_value=Preferences.settings['debug'], pos=(108, 400))
                            dpg.add_combo(tag="plugin_rate"         , items=list(range(1, 1800)), callback=Plugin.compose, default_value=Plugin.rate, pos=(108, 424), width=64)

    

    def capturePluginItemSetting(name, value):
        from classes.plugin     import parseBool
        # Skip corrupt or malformed settings
        if name in ['enabled', '']: return True
        # Process settings which always come grouped, such as                         
        # - Item color, font, line height
        # These will be placed in individual tabs grouped, to do so use 
        # the same prefix for line-height, font-size and color, then they will
        # spawn in the same tab. 
        if   '-border-color'    in name: bcolors[name] = value; return True     
        elif '-border-width'    in name: bwidths[name] = value; return True     
        elif '-border-radius'   in name: bradius[name] = value; return True     
        elif '-shadow-color'    in name: shadows[name] = value; return True
        elif '-shadow-pos-x'    in name: sposxs [name] = value; return True
        elif '-shadow-pos-y'    in name: sposys [name] = value; return True
        elif '-color'           in name: colors [name] = value; return True     
        elif '-font-size'       in name: sizes  [name] = value; return True
        elif '-line-height'     in name: heights[name] = value; return True
        elif '-font-italic'     in name: italics[name] = parseBool(value); return True
        elif '-font-bold'       in name: bolds  [name] = parseBool(value); return True
        elif '-pos-x'           in name: posxs  [name] = value; return True
        elif '-pos-y'           in name: posys  [name] = value; return True
        elif '-size-x'          in name: sizexs [name] = value; return True
        elif '-size-y'          in name: sizeys [name] = value; return True
        elif '-shadow-blur'     in name: blurs  [name] = value; return True
        elif '-font'            in name: types  [name] = value; return True                        
        return False


    def populatePluginsTab():
        from classes.plugin     import Plugin        
        from classes.attribute  import Attribute
        # Make a tab for every plugin' settings
        for name, plugin in Plugin.loaded.items():            
            with dpg.tab(label=name, tag=f"tab_plugins-{name}", parent='plugin-tabs'):
                Attribute.parent = f'tab-window-{name}'
                with dpg.child_window(border=False, tag=Attribute.parent, height=cfg.main.height) as window:
                    perspective = 0
                    project = False                    
                    row     = [ 32,  32, 32]
                    columns = [  0, 105]
                    Attribute.label(8, 8, plugin.description, color=(55,155,255))
                    for name,value in plugin.settings.items():
                        if Preferences.capturePluginItemSetting( name, value ): continue
                        # If setting is not a part specific attribute, then try to parse it as a
                        # general setting (placed in the upper area )
                        Attribute.plugin = plugin.name
                        # Temporal patch for projection settings
                        if name in ['perspective', 'angle', 'pos-x', 'pos-y', 'size-x', 'size-y']: 
                            max_value = {
                                'perspective'   : 1600,
                                'angle'         : 360,
                                'pos-x'         : 2048,
                                'pos-y'         : 2048,
                                'size-x'        : 2048,
                                'size-y'        : 2048,
                            }
                            negative = {
                                'perspective'   : False,
                                'angle'         : True,
                                'pos-x'         : True,
                                'pos-y'         : True,
                                'size-x'        : True,
                                'size-y'        : True,
                            }
                            Attribute.label     ( 300, row[1], elegant(name).rjust(12, ' ') , parent=Attribute.parent+'-projection')
                            Attribute.integer   ( 395, row[1], name, value                  , parent=Attribute.parent+'-projection', max_value=max_value[name], negative=negative[name])
                            row[1]+=24
                        else:
                            Attribute.label(columns[0], row[0], elegant(name).rjust(14, ' '))
                            if   isinstance( value, bool )  : Attribute.boolean (columns[1], row[0], name, value )
                            elif isinstance( value, int  )  : Attribute.integer (columns[1], row[0], name, value )
                            elif isinstance( value, float)  : Attribute.decimal (columns[1], row[0], name, value )
                            elif ':' in value               : Attribute.combo   (columns[1], row[0], name, value )
                            else                            : Attribute.text    (columns[1], row[0], name, value )
                            row[0]+=24
                            
                    
                    if not len(colors):
                        dpg.configure_item(window, height=381)
                        continue
                    
                #
                # If this point is reached means colors were detected, so we will generate a tab with specific 
                # font related settings for each detected color type variable with a font associated
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
                                    Attribute.color         (   3,  13 , color)
                                    if name.replace('color', 'font') in types.keys():
                                        Attribute.label         ( 220,   8 , "Font Settings", parent=window)
                                    Attribute.font          ( 220,  32 )
                                    Attribute.font_size     ( 318,  32 )
                                    Attribute.line_height   ( 360,  32 )
                                    Attribute.italic        ( 318,   8 )
                                    Attribute.bold          ( 339,   8 )
                                    if name.replace('color', 'shadow') in shadows.keys():
                                        Attribute.label         ( 220,  54 , "Shadow Color", parent=window)
                                    Attribute.shadow        ( 220,  75 )
                                    Attribute.shadow_pos_x  ( 370,  70 )
                                    Attribute.shadow_pos_y  ( 370,  90 )
                                    Attribute.pos_x         ( 410,  12 )
                                    Attribute.pos_y         ( 410,  32 )
                                    Attribute.size_x        ( 219,  12 )
                                    Attribute.size_y        ( 219,  32 )
                                    Attribute.shadow_blur   ( 370, 110 )
                                    Attribute.border_width  ( 370, 130 )
                                    Attribute.border_radius ( 370, 150 )
                                    if name.replace('color', 'border-color') in bcolors.keys():
                                        Attribute.label         ( 442,  54 , "Border Color", parent=window)
                                    Attribute.border_color  ( 442,  75 )
                
    
    def updatePluginLists():
        from classes.plugin import Plugin
        items = [ plugin.name for name,plugin in Plugin.loaded.items() if plugin.settings['enabled']]
        dpg.configure_item( 'enabled-plugins', items=items )        

    
    def createOutputTab():
        return
        #TODO: remove this block if nothing goes weird
        with dpg.tab(label="Output", tag="tab_output"):
            with dpg.child_window():
                dpg.add_text("Date & Time Adjust", color=(255,255,0))
                createIntegerField('GMT Zone'  , 'gmt'        , min_value=-12,max_value=12,callback=Preferences.updateSettingsGMT)
                dpg.add_text("Style Personalization", color=(255,255,0))
                with dpg.tab_bar():
                    with dpg.tab(label="cheevos.html", tag="css_cheevos"):
                        Preferences.addCustomizationPanel('cheevos')                        
                    with dpg.tab(label="cheevos_locked.html", tag="css_cheevos_locked"):
                        Preferences.addCustomizationPanel('locked')                        
                    with dpg.tab(label="cheevos_unlocked.html", tag="css_cheevos_unlocked"):
                        Preferences.addCustomizationPanel('unlocked')                        
                    with dpg.tab(label="progress.html", tag="css_progress"):
                        Preferences.addProgressPanel()
                    with dpg.tab(label="recent.html", tag="css_recent"):
                        with dpg.child_window():
                            dpg.add_text("Shape & Behavior", color=(255,255,0))
                            createIntegerField('Border Radius'      , 'recent-border-radius'    , callback=Preferences.updateCustomizations, max_value=64)
                            createIntegerField('Border Width'       , 'recent-border-width'     , callback=Preferences.updateCustomizations,max_value=16)
                            dpg.add_text("Widget colors"            , color=(255,255,0), pos=(8, 84))
                            createColorField('Border'               , 'recent-border-color'     , callback=Preferences.updateCustomizations)
                            dpg.configure_item('recent-border-color', pos=(14,108))
                            pos = dpg.get_item_pos('recent-border-color')
                            createColorField('Font'                 , 'recent-font-color'       , callback=Preferences.updateCustomizations)
                            dpg.configure_item('recent-font-color'  , pos=(pos[0]+192, pos[1]))
                            dpg.add_button(label="Edit CSS File"    , pos=(Preferences.width - 132, 3), tag="css-recent"        , callback=lambda: os.system('notepad '+Preferences.root.replace('/', '\\')+"\\css\\recent.css"))
                            dpg.add_button(label="Apply Changes"    , pos=(Preferences.width - 132,24), tag="gen-recent"        , callback=DynamicCSS.customize, user_data=Preferences.parent.css['recent'])
                            dpg.add_button(label="Open  Preview"    , pos=(Preferences.width - 132,45), tag=f"preview-recent"   , callback=lambda: os.system('start '+Preferences.root.replace('/', '\\')+"\\data\\recent.html"))
                            with dpg.child_window(
                                tag='recent-effect-settings',
                                pos=(Preferences.width - 240, 80),
                            ):                                     
                                with dpg.tab_bar():
                                    with dpg.tab(label="Font"):
                                        dpg.add_text("Font Type", color=(255,255,0))
                                        dpg.add_combo(tag='recent-font'     , items=list(fonts.keys())  , callback=Preferences.updateCustomizations, default_value=Preferences.settings['recent-font'])
                                        dpg.add_text("Font Glow"            , color=(255,255,0))
                                        createBooleanField('Enabled'        , 'recent-font-glow'        , callback=Preferences.updateCustomizations)
                                        dpg.add_text("Font Size"            , color=(255,255,0))
                                        createIntegerField(None             , 'recent-font-size'        , callback=Preferences.updateCustomizations, min_value=1, max_value=64)
                                        dpg.configure_item('recent-font-size')
                                    with dpg.tab( label="3D Effects" ):                                
                                        createBooleanField("Enable"         , 'recent-3d'               , callback=Preferences.updateCustomizations)
                                        dpg.add_text("3D Perspective"       , color=(255,255,0))
                                        createIntegerField(None             , 'recent-perspective'      , callback=Preferences.updateCustomizations, min_value=   1, max_value=1600)
                                        dpg.add_text("Angle"                , color=(255,255,0))
                                        createIntegerField(None             , 'recent-rotation'         , callback=Preferences.updateCustomizations, min_value=-180, max_value= 180)
                                        dpg.add_text("Position"             , color=(255,255,0))
                                        createIntegerField("X"              , 'recent-x'                , callback=Preferences.updateCustomizations, min_value=-800, max_value= 800)
                                        createIntegerField("Y"              , 'recent-y'                , callback=Preferences.updateCustomizations, min_value=-800, max_value= 800)
                                        
                                    
    
    def createInputTab():
        with dpg.tab(label="Input", tag="tab_input"):
            with dpg.child_window():
                dpg.add_text( "Twitch"          , tag="twitch-label"        , color=(205,255,0) )
                dpg.add_text( "API Key"         , tag="twitch-app-key-label", color=(255,255,0) )
                dpg.add_text( "Use API"         , tag="twitch-use-api-label", color=(255,255,0) )
                dpg.add_text( "IRC Channel"     , tag="twitch-username-label",color=(255,255,0) )
                dpg.add_text( "IRC Password"    , tag="twitch-password-label",color=(255,255,0) )
                createStringField (''           , 'twitch-app-key'                              )
                createStringField (''           , 'twitch-username'                             )
                createStringField (''           , 'twitch-password'                             )
                createBooleanField(''           , 'twitch-use-api'                              )
                dpg.add_text( "RetroAchievements",tag="ra-label"            , color=(205,255,0) )
                dpg.add_text( "API Key"         , tag="ra-app-key-label"    , color=(255,255,0) )
                dpg.add_text( "Use API"         , tag="ra-use-api-label"    , color=(255,255,0) )
                createStringField (''           , 'ra-app-key'                                  )
                createBooleanField(''           , 'ra-use-api'                                  )
                dpg.add_text( "RA Password"     , tag="ra-password-label"   , color=(255,255,0) )
                dpg.add_text( "Offline Mode"    , tag="ra-offline-label"    , color=(255,255,0) )
                createStringField (''           , 'password'                                    )
                createBooleanField(''           , 'offline'                                     )
                dpg.add_text( "AutoRefresh Rate", tag="auto-update-rate-label",color=(255,255,0))
                dpg.add_text( "Use AutoRefresh" , tag="auto-update-enable-lbl",color=(255,255,0))
                createBooleanField(''           , 'auto_update'     )
                createIntegerField('Minutes'    , 'auto_update_rate' , min_value=1,max_value=60)
                columns = [ 150, 16 ]
                y = 8
                dpg.configure_item('twitch-label'           , pos=(          8,   y ));y+=24
                dpg.configure_item('twitch-app-key-label'   , pos=( columns[0],   y ))
                dpg.configure_item('twitch-use-api-label'   , pos=( columns[1],   y ));y+=24
                dpg.configure_item('twitch-app-key'         , pos=( columns[0],   y ))
                dpg.configure_item('twitch-use-api'         , pos=( columns[1],   y ));y+=24
                dpg.configure_item('twitch-username-label'  , pos=( columns[0],   y ));y+=24
                dpg.configure_item('twitch-username'        , pos=( columns[0],   y ));y+=24
                dpg.configure_item('twitch-password-label'  , pos=( columns[0],   y ));y+=24
                dpg.configure_item('twitch-password'        , pos=( columns[0],   y ));y+=24
                y+=24
                dpg.configure_item('ra-label'               , pos=(          8,   y ));y+=24
                dpg.configure_item('ra-app-key-label'       , pos=( columns[0],   y ))
                dpg.configure_item('ra-use-api-label'       , pos=( columns[1],   y ));y+=24
                dpg.configure_item('ra-app-key'             , pos=( columns[0],   y ))
                dpg.configure_item('ra-use-api'             , pos=( columns[1],   y ));y+=24
                dpg.configure_item('ra-password-label'      , pos=( columns[0],   y ))
                dpg.configure_item('ra-offline-label'       , pos=( columns[1],   y ));y+=24
                dpg.configure_item('password'               , pos=( columns[0],   y ))
                dpg.configure_item('offline'                , pos=( columns[1],   y ));y+=24
                dpg.configure_item('auto-update-rate-label' , pos=( columns[0],   y ))
                dpg.configure_item('auto-update-enable-lbl' , pos=( columns[1],   y ));y+=24
                dpg.configure_item('auto_update_rate'       , pos=( columns[0],   y ))
                dpg.configure_item('auto_update'            , pos=( columns[1],   y ));y+=24                
                dpg.configure_item('password'               , password=True)
                dpg.configure_item('ra-app-key'             , password=True)
                dpg.configure_item('twitch-app-key'         , password=True)
                dpg.configure_item('twitch-password'        , password=True)

    
    def create( parent ):
        Preferences.parent = parent
        with dpg.window(
            tag='preferences_main',
            label="Preferences", 
            width=Preferences.width, 
            height=Preferences.height, 
            no_collapse=True, 
            no_resize=True,
            modal = True,
            show = False,
            on_close=lambda:dpg.hide_item('preferences_main'),
            pos=((Preferences.parent.width / 2) - (Preferences.width / 2),(Preferences.parent.height / 2) - (Preferences.height / 2))
        ):
            with dpg.tab_bar(tag="preferences-tabs"):
                Preferences.createInterfaceTab()
                Preferences.createInputTab()
                Preferences.createPluginsTab()
        

    
    def show():
        dpg.show_item('preferences_main')

    
    def hide():
        dpg.hide_item('preferences_main')

def createBooleanField(name, setting_name, callback=Preferences.updateSettingBoolean, restart=False):
    dpg.add_checkbox(
        label = name, 
        tag = setting_name, 
        callback=callback, 
        
        default_value=Preferences.settings[setting_name], 
        user_data=restart
    ) 

def createIntegerField(name, setting_name, callback=Preferences.updateSettingInteger, restart=False, min_value=0, max_value=9999):
    dpg.add_slider_int(label = name, tag = setting_name, callback=callback,default_value=int(Preferences.settings[setting_name]), min_value=min_value, max_value=max_value, user_data=restart) 

def createStringField(name, setting_name, callback=Preferences.updateSetting, restart=False):
    dpg.add_input_text(label = name, tag = setting_name, callback=callback,default_value=Preferences.settings[setting_name], user_data=False) 

def createColorField(name, setting_name, callback=Preferences.updateSettingColor):
    dpg.add_color_picker(
        height=128, 
        width=128,
        label = name, 
        tag = setting_name, 
        callback=callback,
        default_value=Preferences.settings[setting_name], 
        user_data=False
    ) 
