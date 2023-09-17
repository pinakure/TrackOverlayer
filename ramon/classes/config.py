class Config:
    
    width   = 1024#640
    height  = 600#480

    defaults = {
        'last_game'                 : 'TestGame',
        'last_date'                 : '01 Jan 2000, 00:00',
        'rank'                      : '1 / 50,000',
        'debug'                     : False,
        'score'                     : '999999',
        'width'                     : 1440,
        'height'                    :  900,
        'x-pos'                     :    0,
        'y-pos'                     :    0,
        'auto_update'               : True,
        'auto_update_rate'          : 1,
        'fullscreen'                : False,
        'vertical'                  : False,
        'username'                  : '',
        'password'                  : '',
        'twitch-username'           : '',
        'twitch-password'           : '',
        'root'                      : '.',
        'gmt'                       : 2,
        'twitch-app-key'            : '',
        'twitch-use-api'            : False,
        'ra-use-api'                : False,
        'ra-app-key'                : '',
        'offline'                   : False,
        'no-welcome'                : False,
        'simple_ui'                 : False,
        'pending_cheevos'           : [0,255,255],
        'unlocked_cheevos'          : [64, 128,0],
        'current_cheevo'            : 1,
        'plugin-rate'               : 5,
    }
    
    class range:
        pos_x   = [-1440, 1440]
        pos_y   = [-1080, 1080]
        size_x  = [-1440, 1440]
        size_y  = [-1080, 1440]
        zoom    = [ 1   ,  100]

    class main:
        height  = 282
    class detail:
        height  = 220
        extra   = 68


ranges = {
    'auto_update_rate'              : [     1,  301],
    'width'                         : [   320, 1440],
    'height'                        : [   240, 1080],
    'x-pos'                         : [ -5000, 5000], # Window position
    'y-pos'                         : [ -5000, 5000], # Window position
    'pos-y'                         : [ -1080, 1080], # Plugin position
    'pos-x'                         : [ -1444, 1444], # Plugin position
    'perspective'                   : [     1, 1600],
    'angle'                         : [ -180 , 180 ],
    'plugin-rate'                   : [     1, 1800],
}

combos = [
    'auto_update_rate',    
    'plugin-rate',
]

help = {    
    'username'                  : "RA Username.\nPlease press ENTER and restart program if value is changed.",
    'no-welcome'                : "Hide initial authorization screen in overlay.html",
    'plugin-rate'               : "How often the plugins will try to update their data",
    'auto_update'               : "Request cheevo information to RetroAchievements periodically",
    'auto_update_rate'          : "Time to wait between requests in minutes",
    'offline'                   : "Use this while setting up the look and feel, please",
    'twitch-password'           : "Not used at the moment, will give write permissions later",
    'ra-use-api'                : "Useless, while RA does not get up their Cheevo API ",
    'ra-app-key'                : "Useless, while RA does not get up their Cheevo API ",
    'password'                  : "Needed since 1/9/2023 to be able to deeper inspect user profile",
    'twitch-use-api'            : "Not uset at the moment, will give deeper twitch interaction",
    'twitch-app-key'            : "Not uset at the moment.",
    'twitch-username'           : "Use this to read your channel chat in the correspondent plugins",
}