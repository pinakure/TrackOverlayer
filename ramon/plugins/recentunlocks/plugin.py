from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)

        #@ Plugin Settings
        self.name        = 'recentunlocks'
        self.description = 'Recent Cheevo unlocks list'
        self.endpoint    = 'recent'
        self.color       = '#88f'

        #@ Composer Settings
        self.z_index     = 30
        self.width       = 366
        self.height      = 420
        self.scale       = 1
        self.y           = 128
        self.x           = 4
        
        #@ Vars
        

        self.settings.update({
            "auto-hide"                 : False,
            "perspective"               : 0,
            "angle"                     : 0,
            
            "backdrop"                  : True,
            "backdrop-image"            : './recent-bg.png',

            "row-count"                 : 5,
           
            "table-color"               : [ 0, 255, 255, 128 ],
            "table-border-width"        : 2, 
            "table-border-color"        : [255,255,255,128], 
            "table-border-radius"       : 4,             
            "table-shadow-blur"         : 0, 
            "table-shadow-color"        : [0,0,0,0], 
            "table-shadow-pos-x"        : 0,
            "table-shadow-pos-y"        : 0,
            "table-pos-x"               : 0,
            "table-pos-y"               : 0,
            "table-size-x"              : self.width,
            "table-size-y"              : self.height,

            "row-color"                 : [ 0, 255, 255, 128 ],
            "row-border-width"          : 2, 
            "row-border-color"          : [255,255,255,128], 
            "row-border-radius"         : 4,             
            "row-shadow-blur"           : 0, 
            "row-shadow-color"          : [0,0,0,0], 
            "row-shadow-pos-x"          : 0,
            "row-shadow-pos-y"          : 0,
            "row-pos-x"                 : 0,
            "row-pos-y"                 : 0,
            "row-size-x"                : self.width,
            "row-size-y"                : 64,

           
            "name-color"                : [255,255,255,255],
            "name-font"                 : "arcade",
            "name-font-size"            : 16, 
            "name-font-italic"          : False, 
            "name-font-bold"            : True, 
            "name-pos-x"                : 0,
            "name-pos-y"                : 8,
            "name-shadow-blur"          : 0, 
            "name-shadow-color"         : [0,0,0,0], 
            "name-shadow-pos-x"         : 0,
            "name-shadow-pos-y"         : 0,
            "name-line-height"          : 18, 
            "name-border-width"         : 0, 
            "name-border-color"         : [0,0,0,0], 
            "name-border-radius"        : 0, 
            
            "description-color"         : [255,255,255,255],
            "description-font"          : "arcade",
            "description-font-size"     : 16, 
            "description-font-italic"   : False, 
            "description-font-bold"     : False, 
            "description-pos-x"         : 0,
            "description-pos-y"         : 32,
            "description-shadow-blur"   : 0, 
            "description-shadow-color"  : [0,0,0,0], 
            "description-shadow-pos-x"  : 0,
            "description-shadow-pos-y"  : 0,
            "description-line-height"   : 18, 
            "description-border-width"  : 0, 
            "description-border-color"  : [0,0,0,0], 
            "description-border-radius" : 0, 
        })


        #@ Install settings
        self.files      = [
            'recent-bg.png',
        ]



    def composerVars(self):
        return {
            'width'   : px(self.width   ),
            'height'  : px(self.height  ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
            'left'    : px(self.x),
            'top'     : px(self.y),
        }

    def templateVars(self):
        return {
        }