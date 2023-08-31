from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'progressbar'
        self.description = 'RetroAchievements Current Game progress bar widget',
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




        #@ Install settings
        self.files      = [
            'progress-overlay.png',
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

