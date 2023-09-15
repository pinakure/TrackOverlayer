from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'flysim')
        #@ Plugin Settings
        self.description = 'Fly Simulator : Programable RetroPixel Overlay Demo'
        self.endpoint    = 'vpu'
        
        #@ Composer Settings
        self.z_index     = 999 # on top of other plugins but bezel
        self.width       = 1024
        self.height      = 700
        self.scale       = 1
        self.x           = 400
        self.y           = 96
        
        
        #@ Settings
        self.setup({
            'pos-x'                     : self.x,
            'size-x'                    : self.width,
            'pos-y'                     : self.y,
            'size-y'                    : self.height,            
        })


    def composerVars(self):
        return {
            'left'      : px(self.settings['pos-x']),
            'top'       : px(self.settings['pos-y']),
            'width'     : px(self.settings['size-x']),
            'height'    : px(self.settings['size-y']),
            'scale'     : self.scale,
            'z-index'   : self.z_index,
        }
