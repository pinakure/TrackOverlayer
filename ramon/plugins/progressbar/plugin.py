from classes.plugin import Plugin
from classes.tools  import px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self, 'progressbar')
        #@ Plugin Settings        
        self.description = 'Game Mastery ProgressBar'
        self.endpoint    = 'progress'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 360
        self.height      = 32
        self.scale       = 1   
        self.x           = 10
        self.y           = 545

        #@ Settings
        self.setup({
            "pos-x"                     : self.x,
            "size-x"                    : self.width,
            "pos-y"                     : self.y,
            "size-y"                    : self.height,
            
            "angle"                     : 0,#TODO
            "perspective"               : 0,#TODO
            "overlay-file"              : './files/progressbar/progress-overlay.png',
            "backdrop-file"             : './files/progressbar/progress-bg.png',
            "sound-file"                : './files/progressbar/experience.wav',
            "hard-gradient"             : False,
            "bar-opacity"               : 0.65,
            "auto-hide"                 : True,
            
            
            
            "percent-color"             : [ 245, 255,   0, 255],
            "percent-font"              : "vhs",
            "percent-font-size"         : 25,
            "percent-line-height"       : 29,
            "percent-font-bold"         : False,
            "percent-font-italic"       : False,
            "percent-shadow-blur"       : 4,
            "percent-shadow-color"      : [   0,   0, 255, 255],
            "percent-shadow-pos-x"      : 1,
            "percent-shadow-pos-y"      : 1,
            "percent-border-color"      : [ 230, 255,   0, 255],
            "percent-border-width"      : 1,

            "up-color"                  : [  55, 255,  0, 128 ],
            "mid-color"                 : [ 128, 255,  0, 128 ],
            "low-color"                 : [  64, 128,  0, 128 ],            
            "glow-color"                : [ 255, 255,  0, 255 ],            
        })

    def composerVars(self):
        return {
            'width'   : px(self.settings['size-x']  ),
            'height'  : px(self.settings['size-y']  ),
            'left'    : px(self.settings['pos-x']   ),
            'top'     : px(self.settings['pos-y']   ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }