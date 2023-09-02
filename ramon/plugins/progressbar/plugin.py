from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'progressbar'
        self.description = 'RetroAchievements Current Game progress bar widget'
        self.endpoint    = 'progress'
        self.color       = '#ff0'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = 360
        self.height      = 32
        self.scale       = 1   
        self.y           = 550
        self.x           = 10
        #@ Vars

        self.settings.update({
            "auto-hide"                 : True,
            "perspective"               : 0,
            "angle"                     : 0,
            "hard-gradient"             : False,
            "overlay"                   : True,
            "overlay-image"             : './progress-overlay.png',
            "sound"                     : True,
            "sound-file"                : './experience.png',
            "backdrop"                  : False,
            "backdrop-image"            : './progress-bg.png',
            "pos-x"                     : 0,
            "pos-y"                     : 0,
            
            "percent-color"             : [ 255, 255, 255, 255],
            "percent-font"              : "arcade",
            "percent-font-size"         : 16,
            "percent-line-height"       : 18,
            "percent-font-bold"         : False,
            "percent-font-italic"       : False,
            "percent-shadow"            : [   0,   0,   0, 255],
            "percent-pos-x"             : int((self.width / 2) - 12),
            "percent-pos-y"             : int((self.height/ 2) - 8),
            "percent-shadow-pos-x"      : 1,
            "percent-shadow-pos-y"      : 1,
            "percent-shadow-blur"       : 0,

            "up-color"                  : [ 255, 255,  0, 255 ],
            "mid-color"                 : [ 255, 255,255, 255 ],
            "low-color"                 : [ 255,   0,  0, 255 ],            
            "glow-color"                : [ 255, 255,255, 255 ],            
        })


        #@ Install settings
        self.files      = [
            'progress-overlay.png',
            'progress-bg.png',
            'experience.wav',
        ]    

    def composerVars(self):
        return {
            'width'   : px(self.width   ),
            'height'  : px(self.height  ),
            'left'    : px(self.x       ),
            'top'     : px(self.y       ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {            
        }

