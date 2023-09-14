from classes.preferences    import Preferences
from classes.tools          import sane
import json


def response( raw ):
    return sane(json.dumps(raw))


class Endpoints:

    debug = False
    
    def notifications():
        from classes.ramon import Ramon
        return response(Ramon.data.getNotifications())
    
    def username():
        return Preferences.settings['username'] 
    
    def twitch_username():
        return Preferences.settings['twitch-username']
        
    def current_cheevo():
        from classes.ramon import Ramon
        from classes.plugin import Plugin        
        return response( Ramon.data.cheevo if not Plugin.debug else "Test cheevo\nTest description")
    
    def progress():
        from classes.ramon import Ramon
        from classes.plugin import Plugin
        if Plugin.debug: 
            import random
            Ramon.data.progress = f'{str(int(random.random()*100))}%'
        return Ramon.data.progress 
    
    def game():
        from classes.ramon import Ramon
        return response({ 
            'name'      : Ramon.data.game.name,
            'id'        : Ramon.data.game.id,
            'picture'   : Ramon.data.game.picture,
        })
    
    def score():
        from classes.ramon import Ramon
        return response({ 
            'site_rank' : Ramon.data.site_rank,
            'score'     : Ramon.data.score,            
        })
    
    def recent():
        from classes.ramon import Ramon
        return response([ 
            [ r.name, r.description, r.picture] for r in Ramon.data.recent
        ])
    
    def plugins():
        from classes.plugin import Plugin
        import inspect
        payload = {}
        for name,plugin in Plugin.loaded.items():
            settings = {}
            for key, value in inspect.getmembers(plugin):
                if key.startswith('_'): continue
                if isinstance(value, str) or isinstance(value, float) or isinstance(value, int) or isinstance(value, list):
                    settings.update({
                        key : value,
                    })
            payload.update({
                name        : { 
                    'name'      : name, 
                    'settings'  : json.dumps(settings),
                }
            })
        return json.dumps( payload )

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
            'plugins'           : Endpoints.plugins(),
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
        'plugins'           : plugins,
        'superchat'         : nop,
    }

