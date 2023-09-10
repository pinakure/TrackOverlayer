from classes.plugin import Plugin, px

# TODO:
# - Countdown mode ( useful to 20 minute challenge )
# - Stopwatch mode ( with steps, like the app on any phone )
# - Alarm mode ( when alarm comes in, a variable is setup and/or a sound is playerd)
#   #

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'clock')
        #@ Plugin Settings
        self.description = 'Personalizable Clock Display'
        self.endpoint    = None #@deprecated : replaced by overlay autoupdate using localStorage
        
        #@ Composer Settings
        self.z_index     = 10
        self.width       = 70
        self.height      = 20
        self.scale       = 2
        self.x           = 50
        self.y           = 600

        #@ Settings
        self.settings.update({
            "pos-x"                 : self.x,
            "size-x"                : self.width,
            "pos-y"                 : self.y,
            "size-y"                : self.height,

            "analogic"              : False,

            "digits-color"          : [0,255,0,255],
            "digits-pos-x"          : 0,
            "digits-pos-y"          : 0,
            "digits-font"           : "digital-mono",
            "digits-font-size"      : 16,
            "digits-line-height"    : 18,
            "digits-font-bold"      : True,
            "digits-font-italic"    : False,
            "digits-shadow-blur"    : 2,
            "digits-shadow-color"   : [20,200,20,255],
            "digits-shadow-pos-x"   : 0,
            "digits-shadow-pos-y"   : 0,
            "digits-border-color"   : [0,0,0,0],
            "digits-border-width"   : 0,
        })

    def composerVars(self):
        #@deprecated : replaced by settings
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.settings['size-x']),
            'left'    : px( self.settings['pos-x']),
            'top'     : px( self.settings['pos-y']),
            'height'  : px( self.settings['size-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }
