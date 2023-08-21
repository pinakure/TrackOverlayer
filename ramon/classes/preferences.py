import json, os 
from datetime               import datetime, timedelta
from dearpygui              import dearpygui as dpg
from classes.cheevo         import Cheevo
from classes.dynamic_css    import DynamicCSS, fonts
from classes.log            import Log

class Preferences:
    root            = '.'
    width           = 640
    height          = 480
    parent          = None
    data            = None
    
    @staticmethod
    def writecfg( restart=False ):
        Preferences.root = Preferences.settings['root']        
        with open(f'{Preferences.root}/config.txt', 'w') as file:
            for key,value in Preferences.settings.items():
                file.write(f'{key}={value}'+"\n")
        Preferences.parent.restart = restart

    @staticmethod
    def loadcfg():
        defaults = {
            'version'                   : Preferences.parent.version,
            'last_game'                 : '',
            'width'                     : 1440,
            'height'                    :  900,
            'x-pos'                     :    0,
            'y-pos'                     :    0,
            'auto_update'               : True,
            'auto_update_rate'          : 1,
            'fullscreen'                : False,
            'vertical'                  : False,
            'username'                  : '',
            'root'                      : '.',
            'gmt'                       : 2,
            'api_key'                   : '',
            'twitch-app-key'            : '',
            'use_api'                   : False,
            'simple_ui'                 : False,
            'pending_cheevos'           : [0,255,255],
            'unlocked_cheevos'          : [64, 128,0],
            'current_cheevo'            : 1,

            'progress-upper-color'      : [255,255,0],
            'progress-lower-color'      : [0,255,255],
            'progress-hard-gradient'    : True,
            'progress-overlay-text'     : False,
            
            'cheevos-border-radius'     : 16,
            'cheevos-border-width'      : 3,
            'cheevos-border-color'      : [255,255,255],
            'cheevos-active-color'      : [255,255,  0],
            'cheevos-shadow'            : True,
            'cheevos-3d'                : False,
            'cheevos-perspective'       : 800,
            'cheevos-rotation'          : 45,
            'cheevos-x'                 : 10, 
            'cheevos-y'                 : 170,
            
            'locked-border-radius'      : 16,
            'locked-border-width'       : 3,
            'locked-border-color'       : [255,255,255],
            'locked-shadow'             : True,
            'locked-3d'                 : False,
            'locked-perspective'        : 800,
            'locked-rotation'           : 45,
            'locked-x'                  : 10, 
            'locked-y'                  : 170,
            
            'unlocked-border-radius'    : 16,
            'unlocked-border-width'     : 3,
            'unlocked-border-color'     : [255,255,255],
            'unlocked-shadow'           : True,
            'unlocked-3d'               : False,
            'unlocked-perspective'      : 800,
            'unlocked-rotation'         : 45,
            'unlocked-x'                : 10, 
            'unlocked-y'                : 170,

            'recent-border-radius'      : 4,
            'recent-border-width'       : 0,
            'recent-font-glow'          : True,
            'recent-border-color'       : [255,255,255],
            'recent-font-color'         : [0,255,255],
            'recent-font-size'          : 16,
            'recent-font'               : 'ff6',
            'recent-3d'                 : True,
            'recent-perspective'        : 800,
            'recent-rotation'           : 45,
            'recent-x'                  : 10, 
            'recent-y'                  : 170,
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
                #----------------------------
                'gmt'                       ,
                'auto_update_rate'          ,
                'pending_cheevos'           ,
                'unlocked_cheevos'          ,
                'current_cheevo'            ,
                #----------------------------
                'cheevos-border-radius'     ,
                'cheevos-border-width'      ,
                'cheevos-border-color'      ,
                'cheevos-active-color'      ,
                #----------------------------
                'locked-border-radius'      ,
                'locked-border-width'       ,
                'locked-border-color'       ,
                #----------------------------                
                'unlocked-border-radius'    ,
                'unlocked-border-width'     ,
                'unlocked-border-color'     ,
                #----------------------------
                'recent-border-radius'      ,
                'recent-border-width'       ,
                'recent-border-color'       ,
                'recent-font-color'         ,  
                #----------------------------
                'progress-upper-color'      ,
                'progress-lower-color'      ,
                #----------------------------
                'recent-perspective'        ,
                'recent-rotation'           ,
                'recent-x'                  ,
                'recent-y'                  ,
                #----------------------------
                'locked-perspective'        ,
                'locked-rotation'           ,
                'locked-x'                  ,
                'locked-y'                  ,
                #----------------------------
                'unlocked-perspective'      ,
                'unlocked-rotation'         ,
                'unlocked-x'                ,
                'unlocked-y'                ,
                #----------------------------
                'cheevos-perspective'       ,
                'cheevos-rotation'          ,
                'cheevos-x'                 ,
                'cheevos-y'                 ,
                #----------------------------
            ]
            for field in json_fields:                
                Preferences.settings[field] = json.loads( str(Preferences.settings[field]) )
            Cheevo.active_index = Preferences.settings['current_cheevo']
        except Exception as E:
            Log.error(str(E))
            return 

    @staticmethod
    def updateSettingsGMT(sender=None, user_data=None, args=None):
        Preferences.settings['gmt'] = int(dpg.get_value('gmt'))
        Preferences.data.last_activity  = (datetime.strptime(Preferences.data.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Preferences.settings['gmt']))
        with open(f'{Preferences.root}/data/last_activity.txt'  , 'w') as file:   file.write(Preferences.data.last_activity.strftime("%d %b %Y, %H:%M").upper() )
        dpg.set_value('date'  , Preferences.data.last_activity.strftime("%d %b %Y, %H:%M")  )
        Preferences.writecfg( restart = False )

    @staticmethod
    def updateUsername(sender=None, user_data=None, args=None):
        Preferences.settings['username'] = dpg.get_value('username')
        Preferences.writecfg( restart=False)
        Preferences.parent.refresh()

    @staticmethod
    def updateSetting(sender=None, user_data=None, args=None):
        Preferences.settings[sender]         = dpg.get_value(sender)
        Preferences.writecfg( restart=False )
    
    @staticmethod
    def updateSettingBoolean(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = dpg.get_value(sender)
        Preferences.writecfg( restart=False )
    
    @staticmethod
    def updateSettingInteger(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        Preferences.writecfg( restart=False )
   
    @staticmethod
    def updateSettingVideo(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = int(dpg.get_value(sender))
        dpg.set_viewport_pos( (Preferences.settings['x-pos'], Preferences.settings['y-pos']) )
        dpg.set_viewport_width( Preferences.settings['width'] +16 )
        dpg.set_viewport_height( Preferences.settings['height'] )
        dpg.configure_item( 'main', width=Preferences.settings['width'], height=Preferences.settings['height'] )
        Preferences.writecfg( restart=False )
   
    @staticmethod
    def updateSettingColor(sender=None, user_data=None, args=None):
        Preferences.settings[sender] = dpg.get_value(sender)        
        Preferences.writecfg( restart=False )
   
    @staticmethod
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
                
    @staticmethod
    def loadCustomization( category ):
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
            Log.info(f"No 'active-color' set for {category}. Skipping variable setup.")
        try:
            DynamicCSS.settings['recent']['font'            ] = Preferences.settings['recent-font'          ]
            DynamicCSS.settings['recent']['font-size'       ] = Preferences.settings['recent-font-size'     ]
            DynamicCSS.settings['recent']['font-color'      ] = Preferences.settings['recent-font-color'    ]
            DynamicCSS.settings['recent']['font-glow'       ] = Preferences.settings['recent-font-glow'     ]
        except: 
            Log.info(f"No 'font' set for {category}. Skipping variable setup.")
        try:
            DynamicCSS.settings['progress']['overlay'       ] = Preferences.settings['progress-overlay-text']
            DynamicCSS.settings['progress']['hard'          ] = Preferences.settings['progress-hard-gradient']
            DynamicCSS.settings['progress']['upper-color'   ] = Preferences.settings['progress-upper-color' ]
            DynamicCSS.settings['progress']['lower-color'   ] = Preferences.settings['progress-lower-color' ]
        except: 
            Log.info(f"No 'gradient' set for {category}. Skipping variable setup.")
        
    @staticmethod
    def loadCustomizations():
        Preferences.loadCustomization('cheevos' )
        Preferences.loadCustomization('locked'  )
        Preferences.loadCustomization('unlocked')
        Preferences.loadCustomization('recent'  )
        # Manual fixes for locked and unlocked 
        DynamicCSS.settings['locked'    ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        DynamicCSS.settings['unlocked'  ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        DynamicCSS.settings['recent'    ]['active-color' ] = DynamicCSS.settings['cheevos']['active-color'  ]
        
    @staticmethod
    def updateCustomizations(sender=None, args=None, user_data=None):
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

    @staticmethod
    def addCustomizationPanel(tag):
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

    @staticmethod
    def addProgressPanel():
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

    @staticmethod
    def createOutputTab():
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
                                        
                                    
    @staticmethod
    def createInputTab():
        with dpg.tab(label="Input", tag="tab_input"):
            with dpg.child_window():
                dpg.add_text( "Twitch Integration" , color=(255,255,0))
                createStringField ('App Key'            , 'twitch-app-key'  )
                dpg.add_text( "API" , color=(255,255,0))
                createBooleanField('Enabled'            , 'use_api'          )
                createStringField ('API Key'            , 'api_key'          )
                #TODO: Use api, until then, these should be kept disabled and readonly
                dpg.configure_item('api_key'            , pos=(96, 32), readonly=True)
                dpg.configure_item('use_api'            , enabled=False)

                dpg.add_text( "Auto Update data"        , color=(255,255,0))
                createBooleanField('Enabled'            , 'auto_update'      )
                createIntegerField('Minutes'            , 'auto_update_rate' , min_value=1,max_value=60)
                dpg.configure_item('auto_update_rate'   , pos=(96, 78))

    @staticmethod
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
            with dpg.tab_bar():
                Preferences.createInterfaceTab()
                Preferences.createInputTab()
                Preferences.createOutputTab()
        Preferences.loadCustomizations()

    @staticmethod
    def show():
        dpg.show_item('preferences_main')

    @staticmethod
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
    dpg.add_color_picker(height=128, width=128,label = name, tag = setting_name, callback=callback,default_value=Preferences.settings[setting_name], user_data=False) 
