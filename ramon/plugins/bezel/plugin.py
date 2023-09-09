from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'bezel'
        self.description = 'Custom Bezel Overlay'
        self.endpoint    = None
        
        #@ Composer Settings
        self.z_index     = 9999
        self.width       = 1440
        self.height      = 810
        self.scale       = 1
        
        #@ Settings
        self.settings.update({
            'pos-x'                     : 0,
            'pos-y'                     : 0,
            'size-x'                    : self.width,
            'size-y'                    : self.height,
            'backdrop-file'             : "files/bezel/green.png",
            'backdrop-color'            : [192, 255, 192, 255],
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
