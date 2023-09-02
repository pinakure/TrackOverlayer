from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'clock'
        self.description = 'Personalizable Clock Display'
        self.endpoint    = None
        self.color       = '#222'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 400
        self.height      = 256
        self.scale       = 0.35

        #@ Vars
        self.size        = 200
        self.x           = 48
        self.y           = 20 


        self.settings.update({
            "analogic"               : False,
            "digits-color"           : [255,255,255,0],
            "digits-shadow"          : [0,0,0,255],            
            "digits-pos-x"           : 0,
            "digits-pos-y"           : 0,
            "digits-font"            : "arcade",
            "digits-font-size"       : 48,
            "digits-line-height"     : 64,
            "digits-font-bold"       : True,
            "digits-font-italic"     : False,
            "digits-shadow-pos-x"    : 0,
            "digits-shadow-pos-y"    : 0,
            "digits-shadow-blur"     : 0,
            "digits-border-color"    : [0,0,0,0],
            "digits-border-width"    : 0,
            "digits-border-radius"   : 0,
        })







    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( Plugin.width ),            
            'left'    : px(self.x),
            'top'     : px(self.y),
            'height'  : px( self.height  ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }
