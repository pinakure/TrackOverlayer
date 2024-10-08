from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'logos')
        #@ Plugin Settings        
        self.description = 'Current Game logo Display'
        self.endpoint    =  'game'
        
        #@ Composer Settings
        self.z_index     = 10
        self.width       = 320 #Plugin.width
        self.height      = 160
        self.scale       = 2
        self.x           = 558
        self.y           = 557

        #@ Settings
        self.setup({
            "pos-x"                 : self.x,
            "size-x"                : self.width,
            "pos-y"                 : self.y,
            "size-y"                : self.height,
            "angle"                 : 0,
            "perspective"           : 0,
        })
        
    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.settings['size-x']),
            'height'  : px( self.settings['size-y']),
            'left'    : px( self.settings['pos-x']),
            'top'     : px( self.settings['pos-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }