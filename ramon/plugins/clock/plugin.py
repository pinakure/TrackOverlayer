from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'clock'
        self.description = 'Personalizable Clock Display'
        self.endpoint    = None #@deprecated : replaced by overlay autoupdate using localStorage
        
        #@ Composer Settings
        self.z_index     = 10
        self.width       = 70
        self.height      = 20
        self.scale       = 2
        self.x           = 130
        self.y           = 616

        #@ Settings
        self.settings.update({
            "pos-x"                 : self.x,
            "pos-y"                 : self.y,
            "size-x"                : self.width,
            "size-y"                : self.height,
            "analogic"              : False,
            "digits-color"          : [255,255,200,255],
            "digits-pos-x"          : 0,
            "digits-pos-y"          : 0,
            "digits-font"           : "pinakure",
            "digits-font-size"      : 16,
            "digits-line-height"    : 18,
            "digits-font-bold"      : True,
            "digits-font-italic"    : False,
            "digits-shadow-blur"    : 0,
            "digits-shadow-color"   : [0,0,0,255],            
            "digits-shadow-pos-x"   : 1,
            "digits-shadow-pos-y"   : 1,
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
