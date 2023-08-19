from datetime import datetime, timedelta
from dearpygui import dearpygui as dpg

    
class Preferences:

    root            = '.'
    width           = 800
    height          = 600
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
        Preferences.settings = {
            'width'             : 1440,
            'height'            :  900,
            'auto_update'       : True,
            'auto_update_rate'  : 1,
            'fullscreen'        : True,
            'vertical'          : False,
            'username'          : '',
            'root'              : '.',
            'gmt'               : 2,
            'simple_ui'         : False,
        }
        Preferences.root     = Preferences.settings['root']
        
        try:
            with open(f'{Preferences.root}/config.txt', 'r') as file:
                data = file.read().split('\n')
                for setting in data:
                    if len(setting)==0:continue
                    parts = setting.split('=')
                    Preferences.settings[parts[0]] = True if parts[1].lower() == 'true' else False if parts[1].lower() == 'false' else parts[1]
            Preferences.root                        = Preferences.settings['root']
            Preferences.parent.width                = int(Preferences.settings['width' ]) - (4 if Preferences.settings['fullscreen'] else 0)
            Preferences.parent.height               = int(Preferences.settings['height'])
            Preferences.settings['gmt']             = int(Preferences.settings['gmt'])
            Preferences.settings['auto_update_rate']= int(Preferences.settings['auto_update_rate'])
            Preferences.settings['width']           = Preferences.parent.width
            Preferences.settings['height']          = Preferences.parent.height
        except Exception as E:
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
        Preferences.writecfg()
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
    def createInterfaceTab():
        with dpg.tab(label="Interface", tag="tab_general"):
            with dpg.child_window():
                createBooleanField('Simple UI       ' , 'simple_ui'     , restart=True)
                createBooleanField('Fullscreen      ' , 'fullscreen'    , restart=True)
                createBooleanField('Vertical Layout ' , 'vertical'      , restart=True)
                
    @staticmethod
    def createOutputTab():
        with dpg.tab(label="Output", tag="tab_output"):
            with dpg.child_window():
                createIntegerField('GMT Correction'  , 'gmt'        , min_value=-12,max_value=12,callback=Preferences.updateSettingsGMT)

    @staticmethod
    def createInputTab():
        with dpg.tab(label="Input", tag="tab_input"):
            with dpg.child_window():
                createBooleanField('Auto Update'        , 'auto_update'      )
                createIntegerField('Auto Update Rate'   , 'auto_update_rate' , min_value=1,max_value=60)

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
            on_close=lambda:dpg.hide_item('preferences_main'),
            pos=((Preferences.parent.width / 2) - (Preferences.width / 2),(Preferences.parent.height / 2) - (Preferences.height / 2))
        ):
            with dpg.tab_bar():
                Preferences.createInterfaceTab()
                Preferences.createInputTab()
                Preferences.createOutputTab()

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
