from classes.preferences    import Preferences
from classes.tools          import sane
import json


class Endpoints:

    debug = False
    
    def notifications():
        from classes.ramon import Ramon
        return sane(json.dumps(Ramon.data.getNotifications()))
    
    def username():
        return Preferences.settings['username'] 
    
    def twitch_username():
        return Preferences.settings['twitch-username']
        
    def current_cheevo():
        from classes.ramon import Ramon
        from classes.plugin import Plugin        
        return sane(json.dumps( Ramon.data.cheevo if not Plugin.debug else "Test cheevo\nTest description"))
    
    def progress():
        from classes.ramon import Ramon
        from classes.plugin import Plugin
        if Plugin.debug: 
            import random
            Ramon.data.progress = f'{str(int(random.random()*100))}%'
        return Ramon.data.progress 
    
    def game():
        from classes.ramon import Ramon
        return sane(json.dumps({ 
            'name'      : Ramon.data.game.name,
            'id'        : Ramon.data.game.id,
            'picture'   : Ramon.data.game.picture,
        }))
    
    def score():
        from classes.ramon import Ramon
        return sane(json.dumps({ 
            'site_rank' : Ramon.data.site_rank,
            'score'     : Ramon.data.score,            
        }))
    
    def recent():
        from classes.ramon import Ramon
        return sane(json.dumps([ [ r.name, r.description, r.picture] for r in Ramon.data.recent] ))
    
    def nop():
        return ''

    def getAll():
        return {
            'notifications'     : Endpoints.notifications(),
            'username'          : Endpoints.username(),
            'twitch-username'   : Endpoints.twitch_username(),
            'current-cheevo'    : Endpoints.current_cheevo().replace("'", "`"),
            'progress'          : Endpoints.progress(),
            'game'              : Endpoints.game(),
            'score'             : Endpoints.score(),
            'recent'            : Endpoints.recent(),
            'superchat'         : Endpoints.nop(),
        }

    byName = {
        'notifications'     : notifications,
        'username'          : username,
        'twitch-username'   : twitch_username,
        'current-cheevo'    : current_cheevo,
        'progress'          : progress,
        'game'              : game,
        'score'             : score,
        'recent'            : recent,
        'superchat'         : nop,
    }

