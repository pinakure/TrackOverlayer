from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'score')
        #@ Plugin Settings
        self.description = 'Score / Rank Tracker'
        self.endpoint    = 'score'
        
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

            'hiscore-color'             : [ 155, 255, 0 , 255],
            'hiscore-font-type'         : 'pinakure',
            'hiscore-font-size'         : 24,
            'hiscore-font-bold'         : True,
            'hiscore-font-italic'       : False,
            'hiscore-pos-x'             : 0,
            'hiscore-pos-y'             : 24,
            'hiscore-border-color'      : [0,0,0,0],
            'hiscore-border-width'      : 1,
            'hiscore-shadow-color'      : [0,0,0,255],
            'hiscore-shadow-pos-x'      : 1,
            'hiscore-shadow-pos-y'      : 1,
            'hiscore-shadow-blur'       : 1,

            'rank-color'                : [ 155, 255, 0 , 255],
            'rank-font-type'            : 'pinakure',
            'rank-font-size'            : 24,
            'rank-font-bold'            : True,
            'rank-font-italic'          : False,
            'rank-pos-x'                : 0,
            'rank-pos-y'                : 48,
            'rank-border-color'         : [0,0,0,0],
            'rank-border-width'         : 1,
            'rank-shadow-color'         : [0,0,0,255],
            'rank-shadow-pos-x'         : 1,
            'rank-shadow-pos-y'         : 1,
            'rank-shadow-blur'          : 1,
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
