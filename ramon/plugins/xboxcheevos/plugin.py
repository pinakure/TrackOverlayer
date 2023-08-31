from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'xboxcheevos'
        self.description = 'XBox Achievement Notifications'
        self.endpoint    = 'notifications'
        self.color       = '#00f'

        #@ Composer Settings
        self.z_index     = 30
        self.width       = Plugin.width
        self.height      = 128
        self.scale       = 1
        
        #@ Vars
        




        #@ Install settings
        self.files      = [
            'xbox.wav',
        ]



    def composerVars(self):
        return {
            'width'   : px(self.width   ),
            'height'  : px(self.height  ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {
            'left' : px(self.x),
            'top'  : px(self.y),
        }