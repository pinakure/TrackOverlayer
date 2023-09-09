from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'flysim'
        self.description = 'Fly Simulator : Programable RetroPixel Overlay Demo'
        self.endpoint    = None
        
        #@ Composer Settings
        self.z_index     = 999 # on top of other plugins but bezel
        self.width       = 1024
        self.height      = 700
        self.scale       = 1
        self.x           = 400
        self.y           = 96
        
        
        #@ Settings
        self.settings.update({
            'pos-x'                     : self.x,
            'pos-y'                     : self.y,
            'size-x'                    : self.width,
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
