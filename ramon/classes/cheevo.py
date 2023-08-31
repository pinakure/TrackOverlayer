import requests, os, json
from classes.log        import Log
from peewee import *

db = SqliteDatabase('ramon.db')

class Game(Model):
    id      = IntegerField(unique=True, primary_key=True)
    name    = CharField()
    picture = CharField()
    current = IntegerField(default=1)

    class Meta:
        database = db

    @staticmethod
    def loadOrCreate(game_id):
        #query db loking for requested game
        try:
            return Game.get(Game.id==game_id)
        except:
            #if game does not exist download metadata
            return Game.download(game_id)
    
    @staticmethod
    def download( game_id ):
        data    = str(requests.get(f'https://retroachievements.org/game/{game_id}').content)
        name    = data.split('block mb-1">')[1].split('</span>')[0]
        picture = data.split('h-[96px]" \\n        src="https://media.retroachievements.org/Images/')[1].split('.png')[0].split('_lock')[0]
        Log.info("Downloaded game metadata")
        return Game.create(id=game_id, name=name, picture=picture)

class Cheevo(Model):
    root            = '.'
    max             = 256    
    min_width       = 0
    global_index    = 0
    active_index    = 1

    id          = CharField(unique=True, primary_key=True)
    name        = CharField(default="")
    description = CharField(default="")
    locked      = BooleanField(default=True)
    notified    = BooleanField(default=False)
    picture     = CharField()
    index       = IntegerField()
    cached      = BooleanField(default=False)
    game        = ForeignKeyField(Game, backref='cheevos')

    class Meta:
        database = db

    def menu(self):
        return f'{self.name.ljust(Cheevo.min_width, " ")}'+"\n"+(" "*9)+f'{self.description}'
    
    @staticmethod
    def getPicture( cheevo_id ):
        data = requests.get( f'https://media.retroachievements.org/Badge/{cheevo_id}.png' ).content
        with open(f'{Cheevo.root}/data/cache/{cheevo_id}.png', 'wb') as file:
            file.write(data)
        data = requests.get( f'https://media.retroachievements.org/Badge/{cheevo_id}_lock.png' ).content
        with open(f'{Cheevo.root}/data/cache/{cheevo_id}_lock.png', 'wb') as file:
            file.write(data)
        return data

    def build_cache(self):
        try:
            Log.info(f"Caching cheevo picture {self.picture}...")
            Cheevo.getPicture( self.picture.split('.png')[0].split('_lock')[0] )
            self.cached = True
            self.save()
        except Exception as E:
            Log.error(f"Cannot create cache for cheevo {self.id}", E)
    
    def __str__(self):
        if not self.cached:
            #if not os.path.exists(f'{Cheevo.root}/data/cache/{self.picture}'):
            self.build_cache()            
        return f'<img class="{"active" if self.index == Cheevo.active_index else ""} round" width="48" height="48" src="cache/{self.picture}" title="{self.description}" name="{self.name}">'

    @staticmethod
    def parse( game, payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'")
        picture     = payload.split('img src=')[1].split('.png')[0].replace('\\\'', '') + ".png"
        cheevo_id   = picture.split('/')[-1].split('.png')[0].split('_lock')[0]
        locked      = picture.find('lock')>-1
        description = payload.split('mb-1')[1].split('gt')[1].split('&lt;/div')[0].replace(';', '')
        index       = 0
        if locked:
            Cheevo.global_index+=1
            index = Cheevo.global_index
            if len(name)>Cheevo.min_width:
                Cheevo.min_width = len(name)+1
        try:
            # cheevo already exists in DB
            cheevo = Cheevo.get(id=cheevo_id)            
            cheevo.locked = locked
            cheevo.picture = picture.strip('https://media.retroachievements.org/Badge/')+'.png'              
            cheevo.index  = index
            cheevo.save()
            return cheevo
        except:            
            # cheevo does not exist in DB, create new
            return Cheevo.create(
                id          = cheevo_id,
                name        = name.replace('"', "´"), 
                description = description.replace('"', "´"), 
                picture     = picture.strip('https://media.retroachievements.org/Badge/')+'.png', 
                locked      = locked,
                index       = index,
                game        = game,
            )


try:
    db.connect()
    db.create_tables([Game, Cheevo])
except Exception as E:
    Log.warning(str(E))
