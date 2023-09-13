from classes.preferences    import Preferences
from classes.tools          import sane
import json


class Endpoints:

    debug = False
    
    def notifications():
        from classes.ramon import Ramon
        return sane(json.dumps(Ramon.data.notifications))
    
    
    def current_cheevo():
        from classes.ramon import Ramon
        from classes.plugin import Plugin        
        return sane(json.dumps( Ramon.data.cheevo if not Plugin.debug else "Test cheevo\nTest description"))
    
    def username():
        return Preferences.settings['username'] 
    
    
    def twitch_username():
        return Preferences.settings['twitch-username']
    
    
    def recent():
        from classes.ramon import Ramon
        return sane(json.dumps([ [ r.name, r.description, r.picture] for r in Ramon.data.recent] ))
    
    
    def progress():
        from classes.ramon import Ramon
        from classes.plugin import Plugin
        if Plugin.debug: 
            import random
            Ramon.data.progress = f'{str(int(random.random()*100))}%'
        return Ramon.data.progress 
    
    def last_progress():
        from classes.ramon import Ramon
        lp = Ramon.data.last_progress if Ramon.data.last_progress != '' else Ramon.data.progress
        Ramon.data.last_progress = Ramon.data.progress
        return lp
    
    
    def nop():
        return ''

    def getAll():
        return {
            'notifications'     : Endpoints.notifications(),
            'username'          : Endpoints.username(),
            'twitch-username'   : Endpoints.twitch_username(),
            'current-cheevo'    : Endpoints.current_cheevo().replace("'", "`"),
            'progress'          : Endpoints.progress(),
            #'last-progress'     : Endpoints.last_progress(),
            'recent'            : Endpoints.recent(),
            'superchat'         : Endpoints.nop(),
        }

    byName = {
        'notifications'     : notifications,
        'username'          : username,
        'twitch-username'   : twitch_username,
        'current-cheevo'    : current_cheevo,
        'progress'          : progress,
        #'last-progress'     : last_progress,
        'recent'            : recent,
        'superchat'         : nop,
    }

