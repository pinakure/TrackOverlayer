import requests, os
from peewee                 import *
from classes.log            import Log
from classes.database       import DDBB
from classes.tools          import download
from classes.scraper        import Scraper
from classes.preferences    import Preferences


class GameScraper(Scraper):
    def __init__(self, game):
        Scraper.__init__(self, 
            protocol        = "https", 
            host            = "retroachievements.org", 
            port            = None, 
            needs_login     = False, 
            form_boundary   = False,
            login_form_url  = None, 
            login_post_url  = None, 
            login_username  = None,
            login_password  = None,
            login_fields    = {},
            login_tokens    = [],
            cookies         = [],
        )
        self.targets        = {
            'game'              : ["<img class='max-w-full rounded-sm' src='", "'"],
        }

    def query(self):
        Log.info("Requesting BoxArt...")
        return self.get()

class Game(Model):
    id      = IntegerField(unique=True, primary_key=True)
    name    = CharField()
    picture = CharField()
    current = IntegerField(default=1)
    romname = IntegerField(null=True, default='')
    platform= CharField()
    cached  = BooleanField(default=False)
    subset  = CharField()
    cheevos = IntegerField(default=1)
    _cheevos= []
    
    class Meta:
        database = DDBB.db

    
    def loadOrCreate(game_id, name=None, picture=None, subset='', cheevos=1, platform=platform):
        #query db loking for requested game
        #game_scraper = GameScraper(game_id)
        Log.info("Saving BoxArt...")
        download(f'https://media.retroachievements.org{picture}.png',f'{Preferences.settings["root"]}/data/files/logos/{game_id}.png')
        try:
            return Game.get(Game.id==game_id)
        except Exception as E:
            Log.info(f"Creating Game #{ game_id } ({ name })", force_redraw=True)
            return Game.downloadAndCreate(game_id, name, picture, subset, cheevos, platform)
    
    
    def downloadAndCreate( game_id, game_name, game_picture, subset='', cheevos=1, platform=platform):
        from classes.preferences import Preferences
        name        = game_name
        picture     = game_picture
        filename    = f'{Preferences.settings["root"]}/data/cache/{picture}.png'
        download(f'https://media.retroachievements.org/Images/{picture}.png', filename)
        return Game.create(
            id          = game_id, 
            name        = name, 
            picture     = picture, 
            romname     = '',
            platform    = platform,
            cached      = os.path.exists(filename),
            subset      = subset,
            cheevos     = cheevos,
        )
