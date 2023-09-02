from classes.plugin import Plugin, px

class plugin(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'cheevocube'
        self.description = 'Current Achievement Rotating 3D Cube'
        self.endpoint    = 'current-cheevo'
        self.color       = '#0f0'

        #@ Composer Settings
        self.z_index     = 10
        self.width       = Plugin.width
        self.height      = 256
        self.scale       = 0.35

        #@ Vars
        self.size        = 200
        self.x           = 48
        self.y           = 20 









    def composerVars(self):
        factor = (self.scale / 2)+1
        return {
            'width'   : px( Plugin.width ),            
            'left'    : "calc( calc( var(--width) * var(--cheevocube-scale) ) * -0.925 )",
            'top'     : "calc( -1 * calc( 240px * var(--cheevocube-scale) ) )",
            'height'  : px( self.height  ),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }

    def templateVars(self):
        return {
            'size' : px(self.size),
            'left' : px(self.x),
            'top'  : px(self.y),
        }