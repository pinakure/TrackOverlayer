from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'mascots'
        self.description = 'Mascots related to current game autodisplay'
        self.endpoint    = None
        
        #@ Composer Settings
        self.z_index     = 9999
        self.width       = Plugin.width
        self.height      = 1080
        self.scale       = 1
        
        #@ Settings
        self.settings.update({
            'pos-x'                     : 0,
            'pos-y'                     : 0,
            'size-x'                    : self.width,
            'size-y'                    : self.height,
            'mascots'                   : '[]',
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
