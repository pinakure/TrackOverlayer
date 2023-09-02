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
        

        self.settings = {
            "enabled"                   : False,
            "perspective"               : 0,
            "angle"                     : 0,
            
            "border-radius"             : 32,
            "border-width"              : 8,
            "name-color"                : [255,255,255,255],
            "name-font"                 : "ff6", 
            "name-font-size"            : 16, 
            "name-font-italic"          : False, 
            "name-font-bold"            : False, 
            "name-shadow"               : [0,0,0,0], 
            "name-shadow-pos-x"         : 0,
            "name-shadow-pos-y"         : 0,
            "name-shadow-blur"          : 0, 
            "name-line-height"          : 18, 
            "description-color"         : [255,255,255,255],
            "description-font"          : "ff6", 
            "description-font-size"     : 16, 
            "description-font-italic"   : False, 
            "description-font-bold"     : False, 
            "description-shadow"        : [0,0,0,0], 
            "description-shadow-pos-x"  : 0,
            "description-shadow-pos-y"  : 0,
            "description-shadow-blur"   : 0, 
            "description-line-height"   : 18, 
        } 


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