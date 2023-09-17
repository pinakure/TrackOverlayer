from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'capture')
        #@ Plugin Settings
        self.description = 'Camera Capture'
        self.endpoint    = None
        
        #@ Composer Settings
        self.z_index     = 50
        self.width       = 1440
        self.height      = 810
        self.scale       = 1
        
        #@ Settings
        self.setup({
            'pos-x'                     : 0,
            'size-x'                    : self.width,
            'pos-y'                     : 0,
            'size-y'                    : self.height,            
        })

        self.interactive = True

    def composerVars(self):
        return {
            'left'      : px(self.settings['pos-x']),
            'top'       : px(self.settings['pos-y']),
            'width'     : px(self.settings['size-x']),
            'height'    : px(self.settings['size-y']),
            'scale'     : self.scale,
            'z-index'   : self.z_index,
        }
