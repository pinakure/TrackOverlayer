from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'rpgchat'
        self.description = 'RPGlike SuperChat Window'
        self.endpoint    = 'superchat'
        self.color       = '#cc0'

        self.settings.update({
            "username"          : "",
            "perspective"       : 0,
            "angle"             : 0,
            "text-color"        : [240,240,240,255],
            "text-font"         : "arcade", 
            "text-pos-x"        : 10,
            "text-pos-y"        : 10,
            "text-font-size"    : 16, 
            "text-font-italic"  : False, 
            "text-font-bold"    : False, 
            "text-shadow"       : [16,0,64,255], 
            "text-shadow-pos-x" : 1,
            "text-shadow-pos-y" : 1,
            "text-shadow-blur"  : 0, 
            "text-line-height"  : 18,             
        })

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 320 #Plugin.width
        self.height      = 160
        self.scale       = 2

        #@ Vars
        self.x           = 200
        self.y           = 200


        #@ Install settings
        self.files      = [
            'rpgchat.png',
        ]      



    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.width ),
            'left'    : "calc( 50% - 160px)",
            'top'     : "calc( 100% - 252px)",
            'height'  : px( self.height ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {
            'left' : px(0),
            'top'  : px(0),
        }