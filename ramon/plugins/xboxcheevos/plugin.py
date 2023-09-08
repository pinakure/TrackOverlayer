from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'xboxcheevos'
        self.description = 'XBox Achievement Notifications'
        self.endpoint    = 'notifications'

        #@ Composer Settings
        self.z_index     = 30
        self.width       = Plugin.width
        self.height      = 128
        self.scale       = 1
        self.picture_size= 80
        
        #@ Settings
        self.settings.update({
            "perspective"               : 0,
            "angle"                     : 0,
            'sound'                     : True,
            'sound-file'                : 'xbox.wav',
            'style'                     : 'xbox',
            'display-time'              : 3,
            'pos-x'                     : 0,
            'pos-y'                     : 0,
            'border-radius'             : int(self.height/2),
            'picture-color'             : [ 128,128,  0, 255],
            'picture-shadow-color'      : [   0,  0,  0, 255],
            'picture-shadow-blur'       : 8,
            'picture-shadow-pos-x'      : 0,
            'picture-shadow-pos-y'      : 0,
            'picture-border-color'      : [   0,  0,  0, 255],
            'picture-border-width'      : 2,
            'picture-pos-x'             : 4,
            'picture-pos-y'             : int((self.height/2)-(self.picture_size/2)),
            'picture-border-radius'     : int(self.picture_size/2),
            "text-color"                : [240,240,255,255],
            "text-font"                 : "ff6", 
            "text-pos-x"                : 10,
            "text-pos-y"                : 10,
            "text-font-size"            : 16, 
            "text-font-italic"          : False, 
            "text-font-bold"            : True, 
            "text-shadow-color"         : [0,0,0,0], 
            "text-shadow-pos-x"         : 0,
            "text-shadow-pos-y"         : 0,
            "text-shadow-blur"          : 0, 
            "text-line-height"          : 18, 
            "text-border-width"         : 18, 
            "text-border-color"         : [0,0,0,0], 
            "text-border-radius"        : 32, 
            'up-color'                  : [192, 192, 192, 255],
            'low-color'                 : [122, 122, 122, 255],
        })

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