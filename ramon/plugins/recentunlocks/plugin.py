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