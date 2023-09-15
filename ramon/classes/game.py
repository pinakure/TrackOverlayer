import requests, os
from classes.log        import Log
from classes.database   import DDBB
from peewee import *
from classes.scraper    import Scraper


class GameScraper(Scraper):
    pass

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
        try:
            return Game.get(Game.id==game_id)
        except Exception as E:
            Log.info(f"Creating Game #{ game_id } ({ name })", force_redraw=True)
            return Game.downloadAndCreate(game_id, name, picture, subset, cheevos, platform)
    
    
    def downloadAndCreate( game_id, game_name, game_picture, subset='', cheevos=1, platform=platform):
        from classes.preferences import Preferences
        name    = game_name
        picture = game_picture
        filename= f'{Preferences.settings["root"]}/data/cache/{picture}.png'
        data    = requests.get(f'https://media.retroachievements.org/Images/{picture}.png')
        if data.status_code==200:
            with open(filename, 'wb') as file:
                file.write( data.content )
        return Game.create(
            id      = game_id, 
            name    = name, 
            picture = picture, 
            romname = '',
            platform= platform,
            cached  = os.path.exists(filename),
            subset  = subset,
            cheevos = cheevos,
        )
