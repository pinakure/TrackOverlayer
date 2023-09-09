from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'rpgchat'
        self.description = 'RPGlike SuperChat Window'
        self.endpoint    = 'superchat'
        
        #@ Composer Settings
        self.z_index     = 10
        self.width       = 320 #Plugin.width
        self.height      = 160
        self.scale       = 2
        self.x           = 558
        self.y           = 557

        #@ Settings
        self.settings.update({
            "perspective"           : 0,
            "angle"                 : 0,
            "chars-per-line"        : 25,
            "pos-x"                 : self.x,
            "pos-y"                 : self.y,
            "text-color"            : [240,240,240,255],
            "text-font"             : "arcade", 
            "text-font-size"        : 10, 
            "text-font-italic"      : False, 
            "text-font-bold"        : False, 
            "text-shadow-blur"      : 0, 
            "text-shadow-color"     : [16,0,64,255], 
            "text-shadow-pos-x"     : 2,
            "text-shadow-pos-y"     : 2,
            "text-line-height"      : 18,             
            "text-border-color"     : [0,0,0,0],  
            "text-border-width"     : 0,
        })

        #@ Install settings
        self.files      = [
            'rpgchat.png',
        ]      



    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.width ),
            'height'  : px( self.height ),
            'left'    : px( self.settings['pos-x']),
            'top'     : px( self.settings['pos-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {
            'left' : px(0),
            'top'  : px(0),
        }