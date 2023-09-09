from classes.plugin import Plugin, px

class plugin(Plugin):

    platforms = { 
        'neogeo'    : 'Neo-Geo'                             , 
        'nes'       : 'Nintendo Entertainment System'       ,
        'snes'      : 'Super Nintendo Entertainment System' ,
        'smd'       : 'Sega Mega Drive'                     ,
        'sms'       : 'Sega Master System'                  ,
        'gb'        : 'Gameboy'                             ,
        'gba'       : 'Gameboy advance'                     ,
        'gbc'       : 'Gameboy color'                       ,
        'dos'       : 'MS-DOS'                              ,
        'amiga'     : 'Commodore Amiga'                     ,
        'psx'       : 'Playstation'                         ,
        'pce'       : 'PC Engine / Turbografx 16'           ,
        'cps'       : 'Capcom Play System'                  ,
        'cps2'      : 'Capcom Play System II'               ,
        'cps3'      : 'Capcom Play System III'              ,
    }

    cartridge_sizes = {
        'neogeo'    : (200,200,200),
        'nes'       : (200,200,200),
        'snes'      : (200,200,200),
        'smd'       : (200,200,200),
        'sms'       : (200,200,200),
        'gb'        : (200,200,200),
        'gba'       : (200,200,200),
        'gbc'       : (200,200,200),
        'dos'       : (200,200,200),
        'amiga'     : (200,200,200),
        'psx'       : (200,200,200),
        'pce'       : (200,200,200),
        'cps'       : (200,200,200),
        'cps2'      : (200,200,200),
        'cps3'      : (200,200,200),
    }

    def __init__(self):
        Plugin.__init__(self)
        #@ Plugin Settings
        self.name        = 'cartridge'
        self.description = 'Rotating 3D Cartridge'
        self.endpoint    = None
        
        #@ Composer Settings
        self.z_index     = 0
        self.width       = Plugin.width
        self.height      = 1080
        self.scale       = 1
        self.zoom        = 8
        
        #@ Settings
        self.settings.update(
            {
                'auto-hide'                 : False,
                'pos-x'                     : 110,
                'pos-y'                     : 570,
                'size-x'                    : 300,
                'size-y'                    : 240,
                'rotation-speed'            : 1,
                #'rotation-speed'            : 1.5,
                'cartridge-type'            : 'platforms:neogeo',
                'cartridge-game'            : 'mslugx',
                'zoom'                      : self.zoom,
            }
        )

    def composerVars(self):
        return {
            'top'     : px(self.settings['pos-y']),
            'left'    : px(self.settings['pos-x']),
            'width'   : px(self.settings['size-x']),
            'height'  : px(self.settings['size-y']),
            'scale'   : self.scale,
            'z-index' : self.z_index,
        }
