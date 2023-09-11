from classes.plugin import Plugin, px

class plugin(Plugin):

    glowtypes = {
        'alternate' : 'alternate', 
        'forwards'  : 'forwards', 
        'backwards' : 'backwards', 
        'none'      : 'none', 
    }

    def __init__(self):
        Plugin.__init__(self, 'cheevocube')
        #@ Plugin Settings
        self.description = 'Current Achievement Rotating 3D Cube'
        self.endpoint    = 'current-cheevo'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = Plugin.width
        self.height      = 256
        self.scale       = 1
        self.x           = 0
        self.y           = 0

        #@ Settings
        self.settings.update({
            "pos-x"                     : self.x,
            "size-x"                    : self.width,
            "pos-y"                     : self.y,
            "size-y"                    : self.height,
            "texture-file"              : "./current_cheevo.png",
            "glow-file"                 : "./current_cheevo_lock.png",
            "zoom"                      : 35,
            "glow-type"                 : 'glowtypes|alternate',
            "auto-hide"                 : True,
            
            "cube-color"                : [0,0,0,0],
            "cube-pos-x"                : 50,
            "cube-pos-y"                : 20,
            "cube-size-x"               : 200,
            "cube-shadow-blur"          : 0,
            "cube-shadow-color"         : [255, 0, 0, 255],            
            "cube-shadow-pos-x"         : 0,
            "cube-shadow-pos-y"         : 0,
            "cube-border-color"         : [82, 53, 0, 255],
            "cube-border-width"         : 2,
            "cube-border-radius"        : 0,
            
            
            "name-color"                : [0,255,0,255],
            "name-pos-x"                : 104,
            "name-pos-y"                : 2,
            "name-border-color"         : [0,205,0,255],
            "name-border-width"         : 1,
            "name-shadow-color"         : [0,0,0,128],
            "name-shadow-pos-x"         : 2,
            "name-shadow-pos-y"         : 2,
            "name-shadow-blur"          : 0,
            "name-font"                 : 'arcade',
            "name-font-bold"            : False,
            "name-font-italic"          : False,
            "name-font-size"            : 16,
            "name-line-height"          : 68,
            
            "description-color"         : [231, 230, 227, 255],
            "description-pos-x"         : 105,
            "description-pos-y"         : 25,
            "description-border-color"  : [205, 0, 0, 0],
            "description-border-width"  : 0,
            "description-shadow-color"  : [0,0,0,255],
            "description-shadow-pos-x"  : 2,
            "description-shadow-pos-y"  : 2,
            "description-shadow-blur"   : 0,
            "description-font"          : 'square',
            "description-font-bold"     : True,
            "description-font-italic"   : False,
            "description-font-size"     : 27,
            "description-line-height"   : 27,            
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
