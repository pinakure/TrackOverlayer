from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'roulette')
        #@ Plugin Settings
        self.description = 'Roulette'
        self.endpoint    = 'games'
        
        #@ Composer Settings
        self.z_index     = 30
        self.width       = 1024
        self.height      = 1024
        self.scale       = 1
        self.interactive = True
        
        #@ Settings
        self.setup({
            'pos-x'                     : 0,
            'size-x'                    : self.width,
            'pos-y'                     : 0,
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
