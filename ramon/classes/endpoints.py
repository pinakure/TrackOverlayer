from classes.preferences    import Preferences
from classes.tools          import sane
from classes.superchat      import Superchat
import json
from datetime import datetime

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
        Ramon.data.progress = '0%' if Ramon.data.progress == '' else Ramon.data.progress
        return response({
            'progress'      : int(Ramon.data.progress.replace('%', '')),
        })
    
    def game():
        from classes.ramon import Ramon
        return response({ 
            'name'          : Ramon.data.game.name      if Ramon.data.game else 'no game',
            'id'            : Ramon.data.game.id        if Ramon.data.game else 0,
            'platform'      : Ramon.data.game.platform  if Ramon.data.game else 'unknown',
            'picture'       : Ramon.data.game.picture   if Ramon.data.game else '',
        })
    
    def current_cheevo():
        from classes.ramon import Ramon
        return response({ 
            'name'          : Ramon.data.the_cheevo.name                        if Ramon.data.the_cheevo else 'No Cheevo Active',
            'description'   : Ramon.data.the_cheevo.description                 if Ramon.data.the_cheevo else '---',
            'picture'       : Ramon.data.the_cheevo.picture.split('_lock')[0]   if Ramon.data.the_cheevo else 'default',
        })
    
    def score():
        from classes.ramon import Ramon
        return response({ 
            'site_rank'     : Ramon.data.site_rank,
            'site_rank'     : Ramon.data.site_rank,
            'score'         : Ramon.data.score,            
        })
    
    def recent():
        from classes.ramon import Ramon
        return response([ 
            [ r.name, r.description, r.picture] for r in Ramon.data.recent
        ])
    
    def resize(args):
        from classes.ramon  import Ramon
        from classes.plugin import Plugin
        target = args.split('|')[1]
        anchor = args.split('|')[2]
        offset = int(args.split('|')[3])
        plugin = Plugin.loaded[target]
        print("Resize "+anchor+" of "+target+f" {offset} pixels")
        if anchor == 'right'    : plugin.settings['size-x']+=offset
        if anchor == 'bottom'   : plugin.settings['size-y']+=offset
        if anchor=='left': 
            plugin.settings['size-x']-=offset
            plugin.settings['pos-x']+=offset
        if anchor=='top' : 
            plugin.settings['size-y']-=offset
            plugin.settings['pos-y']+=offset
        Plugin.writeConfig()
        plugin.run()
        Plugin.compose()
        return response({
            "target" : target,
            "size"   : {
                "x"     : plugin.settings['size-x'],
                "y"     : plugin.settings['size-y'],
            },
            "position"   : {
                "x"     : plugin.settings['pos-x'],
                "y"     : plugin.settings['pos-y'],
            },
        })

    def move(args):
        from classes.ramon  import Ramon
        from classes.plugin import Plugin
        print("Move", args)
        target = args.split('|')[1]
        offset = [
            int(args.split('|')[2]),
            int(args.split('|')[3]),
        ]
        plugin = Plugin.loaded[target]
        print("Move plugin "+target+f" {offset[0]}, {offset[1]} pixels")
        plugin.settings['pos-x']+=offset[0]
        plugin.settings['pos-y']+=offset[1]
        Plugin.writeConfig()
        plugin.run()
        Plugin.compose()
        return response({
            "target" : target,
            "position"   : {
                "x"     : plugin.settings['pos-x'],
                "y"     : plugin.settings['pos-y'],
            },
        })

    def clock():
        from classes.plugin import Plugin
        now = datetime.now()
        return response({
            'time'      : now.strftime('%H:%M:%S'),
            'alarm'     : Plugin.loaded['clock'].settings['clock-alarm'],
            'countdown' : Plugin.loaded['clock'].settings['clock-countdown'],
            'mode'      : Plugin.loaded['clock'].settings['clock-type'],
        })
    
    def superchat():
        return response( Superchat.getUnmarked() )
    
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

    def vpu():
        return response({
            'app'  : '',            
        })
    
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
            'superchat'         : Endpoints.superchat(),
            'clock'             : Endpoints.clock(),
            'vpu'               : Endpoints.vpu(),
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
        'superchat'         : superchat,
        'clock'             : clock,
        'vpu'               : vpu,
    }

    
    
