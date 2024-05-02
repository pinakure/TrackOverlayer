from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'status')
        #@ Plugin Settings
        self.description = 'Rich Presence Widget'
        self.endpoint    = 'status'
        
        #@ Composer Settings
        self.z_index     = 40
        self.width       = 200
        self.height      = 96
        self.x           = 1240
        self.y           = 0
        self.scale       = 1
        
        #@ Settings
        self.setup({
            'pos-x'                     : self.x,
            'size-x'                    : self.width,
            'pos-y'                     : self.y,
            'size-y'                    : self.height,            
            'angle'                     : -35,
            'perspective'               : 800,
            
            'caption-color'             : [ 255, 205, 0 , 255],
            'caption-font-type'         : 'arcade',
            'caption-font-size'         : 24,
            'caption-font-bold'         : True,
            'caption-font-italic'       : False,
            'caption-pos-x'             : 0,
            'caption-pos-y'             : 0,
            'caption-border-color'      : [0,0,0,0],
            'caption-border-width'      : 1,
            'caption-shadow-color'      : [0,0,0,255],
            'caption-shadow-pos-x'      : 1,
            'caption-shadow-pos-y'      : 1,
            'caption-shadow-blur'       : 1,
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
