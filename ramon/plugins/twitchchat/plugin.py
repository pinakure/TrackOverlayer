from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'twitchchat'
        self.description = 'Twitch Live Chat Typewriter',
        self.endpoint    = 'twitch-username'
        self.color       = '#f00'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 1024
        self.height      = 128
        self.scale       = 1   
        self.y           = 88
        #@ Vars





        #@ Install settings
        self.files      = [
            'tick01.wav',
            'tick02.wav',
            'tick03.wav',
        ]    

    def composerVars(self):
        return {
            'width'   : px(self.width   ),
            'height'  : px(self.height  ),
            'left'    : px(self.x),
            'top'     : px(self.y),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {            
        }

