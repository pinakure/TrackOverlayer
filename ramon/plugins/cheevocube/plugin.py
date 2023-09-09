from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'cheevocube'
        self.description = 'Current Achievement Rotating 3D Cube'
        self.endpoint    = 'current-cheevo'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = Plugin.width
        self.height      = 256
        self.scale       = 0.35
        self.x           = -466
        self.y           = -83 

        #@ Settings
        self.settings.update({
            "pos-x"                     : self.x,
            "pos-y"                     : self.y,
            "size-x"                    : self.width,
            "size-y"                    : self.height,
            
            "auto-hide"                 : True,
            
            "cube-color"                : [0,0,0,0],
            "cube-pos-x"                : 50,
            "cube-pos-y"                : 20,
            "cube-size-x"               : 200,
            "cube-shadow-blur"          : 0,
            "cube-shadow-color"         : [0,255,0,255],            
            "cube-shadow-pos-x"         : 0,
            "cube-shadow-pos-y"         : 0,
            "cube-border-color"         : [0,255,0,255],
            "cube-border-width"         : 2,
            "cube-border-radius"        : 0,#TODO
            
            "texture-file"              : "./current_cheevo.png",
            "glow-file"                 : "./current_cheevo_lock.png",
            "glow-type"                 : 'alternate',
            
            "name-color"                : [0,255,0,255],
            "name-pos-x"                : 295,
            "name-pos-y"                : 20,
            "name-border-color"         : [0,205,0,255],
            "name-border-width"         : 1,
            "name-shadow-color"         : [0,0,0,128],
            "name-shadow-pos-x"         : 4,
            "name-shadow-pos-y"         : 4,
            "name-shadow-blur"          : 0,
            "name-font"                 : 'arcade',
            "name-font-bold"            : False,
            "name-font-italic"          : False,
            "name-font-size"            : 40,
            "name-line-height"          : 68,
            
            "description-color"         : [0,255,0,255],
            "description-pos-x"         : 304,
            "description-pos-y"         : 68,
            "description-border-color"  : [0,205,0,255],
            "description-border-width"  : 1,
            "description-shadow-color"  : [0,0,0,255],
            "description-shadow-pos-x"  : 2,
            "description-shadow-pos-y"  : 2,
            "description-shadow-blur"   : 0,
            "description-font"          : 'square',
            "description-font-bold"     : True,
            "description-font-italic"   : False,
            "description-font-size"     : 54,
            "description-line-height"   : 52,
            
        })







    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( self.settings['size-x'] ),
            'left'    : px( self.settings['pos-x']),
            'top'     : px( self.settings['pos-y']),
            'height'  : px( self.settings['size-y'] ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }
