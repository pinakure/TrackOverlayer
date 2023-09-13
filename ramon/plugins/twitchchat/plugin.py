from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        from classes.preferences import Preferences
        Plugin.__init__(self, 'twitchchat')
        #@ Plugin Settings
        self.description = 'Twitch Live Chat Typewriter'
        self.endpoint    = 'twitch-username'
        self.color       = '#f00'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 1024
        self.height      = 128
        self.scale       = 1   
        self.y           = 88
        #@ Vars

        self.setRangedCombo('message-count', 1, 25)
        self.setRangedCombo('message-time' , 1, 25)

        self.setup({
            "pos-x"                     : self.x,
            "size-x"                    : self.width,
            "pos-y"                     : self.y,
            "size-y"                    : self.height,
            "angle"                     : 0,
            "perspective"               : 0,
            "user"                      : Preferences.settings['twitch-username'],
            'message-count'             : 5,
            "sound-file"                : "./files/twitchchat/tick01.wav",#client will automatically try to find tick0[1-3].wav upon filename
            'message-time'              : 5,

            'username-color'            : [ 255,255,0,255 ],
            'username-font'             : 'arcade',
            'username-font-size'        : 16,
            'username-line-height'      : 18,
            'username-font-bold'        : False,
            'username-font-italic'      : False,
            'username-shadow-color'     : [ 0, 0, 0, 255 ],
            'username-shadow-pos-x'     : 1,
            'username-shadow-pos-y'     : 1,
            'message-color'             : [ 250,250,250,255 ],
            'message-font'              : 'arcade',
            'message-font-size'         : 16,
            'message-line-height'       : 18,
            'message-font-bold'         : False,
            'message-font-italic'       : False,
            'message-shadow-color'      : [ 0, 0, 0, 255 ],
            'message-shadow-pos-x'      : 1,
            'message-shadow-pos-y'      : 1,
        })

    def composerVars(self):
        return {
            'width'   : px(self.width   ),
            'height'  : px(self.height  ),
            'left'    : 'calc( calc( var(--width) - var(--twitchchat-width) ) - 16px );',
            'top'     : px(self.y),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {            
        }

