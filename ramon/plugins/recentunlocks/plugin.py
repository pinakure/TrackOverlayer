from classes.plugin import Plugin, px
from classes.config import ranges, combos

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'recentunlocks')

        #@ Plugin Settings
        self.description = 'Recent Cheevo unlocks list'
        self.endpoint    = 'recent'
        
        #@ Composer Settings
        self.z_index     = 30
        self.width       = 360
        self.height      = 434
        self.scale       = 1
        self.x           = 12
        self.y           = 96
        
        # Define which integer values are being to be converted into ranged comboboxes        
        self.setRangedCombo('row-count' , 1, 10)
        self.setHelp('row-count'     , "Number of rows of recent cheevos to be displayed")
        
        #@ Settings
        self.settings.update({
            "pos-x"                     : self.x,
            "size-x"                    : self.width,
            "pos-y"                     : self.y,
            "size-y"                    : self.height,
            "angle"                     : 0,
            "perspective"               : 0,
            "backdrop-file"             : './files/recentunlocks/recent-bg.png',
            "overlay-file"              : './files/recentunlocks/recent-overlay.png',
            "row-count"                 : 5,
            "auto-hide"                 : False,
                       
            "division-color"            : [ 0, 255, 255, 128 ],
            "division-border-width"     : 1,            
            
            "table-color"               : [ 0, 255, 255, 128 ],
            "table-border-width"        : 2, 
            "table-border-color"        : [255,255,255,128], 
            "table-border-radius"       : 4,             
            "table-shadow-blur"         : 0, 
            "table-shadow-color"        : [0,0,0,0], 
            "table-shadow-pos-x"        : 1,
            "table-shadow-pos-y"        : 1,
            
            "row-color"                 : [ 0, 255, 255, 128 ],
            "row-border-width"          : 2, 
            "row-border-color"          : [255,255,255,128], 
            "row-border-radius"         : 4,             
            "row-shadow-blur"           : 0, 
            "row-shadow-color"          : [0,0,0,0], 
            "row-shadow-pos-x"          : 0,
            "row-shadow-pos-y"          : 0,
            "row-border-width"          : 2,
            "row-border-color"          : [255,255,255,255],
           
            "picture-color"             : [255,255,255,255],
            "picture-pos-x"             : 0,
            "picture-pos-y"             : 0,
            "picture-size-x"            : 0,
            "picture-size-y"            : 0,
            "picture-shadow-blur"       : 0, 
            "picture-shadow-color"      : [0,0,64,255], 
            "picture-shadow-pos-x"      : 0,
            "picture-shadow-pos-y"      : 0,
            "picture-border-width"      : 2, 
            "picture-border-color"      : [255,255,255,255], 
            "picture-border-radius"     : 4, 
           
            "name-color"                : [255,255,255,255],
            "name-font"                 : "arcade",
            "name-font-size"            : 16, 
            "name-font-italic"          : False, 
            "name-font-bold"            : True, 
            "name-pos-x"                : 74,
            "name-pos-y"                : 8,
            "name-shadow-blur"          : 0, 
            "name-shadow-color"         : [0,0,64,255], 
            "name-shadow-pos-x"         : 1,
            "name-shadow-pos-y"         : 1,
            "name-line-height"          : 18, 
            "name-border-width"         : 0, 
            "name-border-color"         : [240,240,240,255], 
            "name-border-radius"        : 1, 
            
            "description-color"         : [255,255,255,255],
            "description-font"          : "square",
            "description-font-size"     : 16, 
            "description-font-italic"   : False, 
            "description-font-bold"     : True, 
            "description-pos-x"         : 74,
            "description-pos-y"         : 32,
            "description-shadow-blur"   : 6, 
            "description-shadow-color"  : [0,0,64,255], 
            "description-shadow-pos-x"  : 0,
            "description-shadow-pos-y"  : 0,
            "description-line-height"   : 18, 
            "description-border-width"  : 0, 
            "description-border-color"  : [0,0,0,0], 
            "description-border-radius" : 0, 

            "up-color"                  : [  40, 192,  40, 255],
            "mid-color"                 : [  20,  96,  20, 255],
            "low-color"                 : [  10,  40,  10, 255],
        })

    def composerVars(self):
        return {
            'width'   : px(self.settings['size-x']),
            'height'  : px(self.settings['size-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
            'left'    : px(self.settings['pos-x']),
            'top'     : px(self.settings['pos-y']),
        }