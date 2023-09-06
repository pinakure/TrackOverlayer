from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)

        #@ Plugin Settings
        self.name        = 'recentunlocks'
        self.description = 'Recent Cheevo unlocks list'
        self.endpoint    = 'recent'
        
        #@ Composer Settings
        self.z_index     = 30
        self.width       = 366
        self.height      = 420
        self.scale       = 1
        self.x           = 4
        self.y           = 128
        
        #@ Settings
        self.settings.update({
            "pos-x"                     : self.x,
            "pos-y"                     : self.y,
            "size-x"                    : self.width,
            "size-y"                    : self.height,
            
            "auto-hide"                 : False,
            
            "perspective"               : 0,
            "angle"                     : 0,
            
            "backdrop-file"             : './recent-bg.png',
            "overlay-file"              : './recent-overlay.png',
           
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
            
            "row-count"                 : 5,
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
            "description-font-bold"     : False, 
            "description-pos-x"         : 74,
            "description-pos-y"         : 32,
            "description-shadow-blur"   : 0, 
            "description-shadow-color"  : [0,0,64,255], 
            "description-shadow-pos-x"  : 1,
            "description-shadow-pos-y"  : 1,
            "description-line-height"   : 18, 
            "description-border-width"  : 0, 
            "description-border-color"  : [0,0,0,0], 
            "description-border-radius" : 0, 

            "up-color"                  : [  40, 192,  40, 255],
            "mid-color"                 : [  20,  96,  20, 255],
            "low-color"                 : [  10,  40,  10, 255],
        })


        #@ Install settings
        self.files      = [
            'recent-bg.png',
            #'recent-overlay.png',
        ]



    def composerVars(self):
        return {
            'width'   : px(self.settings['size-x']),
            'height'  : px(self.settings['size-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
            'left'    : px(self.settings['pos-x']),
            'top'     : px(self.settings['pos-y']),
        }