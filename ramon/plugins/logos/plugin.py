from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'logos'
        self.description = 'Current Game logo Display'
        self.endpoint    =  None
        
        #@ Composer Settings
        self.z_index     = 10
        self.width       = 320 #Plugin.width
        self.height      = 160
        self.scale       = 2
        self.x           = 558
        self.y           = 557

        #@ Settings
        self.settings.update({
            "perspective"           : 0,
            "angle"                 : 0,
            "pos-x"                 : self.x,
            "pos-y"                 : self.y,
            "size-x"                : self.width,
            "size-y"                : self.height,
        })
        
    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.width ),
            'height'  : px( self.height ),
            'left'    : px( self.settings['pos-x']),
            'top'     : px( self.settings['pos-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }