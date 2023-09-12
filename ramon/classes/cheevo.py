import requests, os, json
from classes.log        import Log
from classes.database   import db
from classes.game       import Game
from peewee             import *


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
    
    
    def getPicture( picture_id ):
        data = requests.get( f'https://media.retroachievements.org/Badge/{picture_id}.png' ).content
        with open(f'{Cheevo.root}/data/cache/{picture_id}.png', 'wb') as file:
            file.write(data)
        data = requests.get( f'https://media.retroachievements.org/Badge/{picture_id}_lock.png' ).content
        with open(f'{Cheevo.root}/data/cache/{picture_id}_lock.png', 'wb') as file:
            file.write(data)
        return data

    def _build_cache(picture):
        Cheevo.getPicture( picture.split('.png')[0].split('_lock')[0] )
            
    def build_cache(self):
        try:
            print(f"Caching cheevo picture {self.picture}...")
            Cheevo._build_cache(self.picture)
            self.cached = True
            self.save()

        except Exception as E:
            Log.error(f"Cannot create cache for cheevo {self.id}", E)
    
    def __str__(self):
        return f'<img class="{"active" if self.index == Cheevo.active_index else ""} round" width="48" height="48" src="cache/{self.picture}" title="{self.description}" name="{self.name}">'

    
    def parse( game, payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'")
        picture     = payload.split('img src=')[1].split('.png')[0].replace('\\\'', '') + ".png"
        cheevo_id   = int(payload.split('achievement/')[1].split('"')[0])
        locked      = picture.find('lock')>-1
        description = payload.split('mb-1')[1].split('gt')[1].split('&lt;/div')[0].replace(';', '')
        pic         = picture.strip('https://media.retroachievements.org/Badge/')+'.png'
        cached      = os.path.exists(f'{Cheevo.root}/data/cache/{pic}') 
        if not cached:
            Log.info(f"CHEEVO : Picture '{pic.split('.png')[0]}' not found, caching...", True)
            Cheevo._build_cache(pic)
            cached = os.path.exists(f'{Cheevo.root}/data/cache/{pic}')         
        
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
            cheevo.cached = cached
        
            cheevo.save()
            return cheevo
        except Exception as E:            
            # cheevo does not exist in DB, create new
            Log.info(f"DATABASE : New Cheevo '{cheevo_id}' found! Creating database entry...", True)
            
            return Cheevo.create(
                id          = cheevo_id,
                name        = name.replace('"', "´"), 
                description = description.replace('"', "´"), 
                picture     = picture.strip('https://media.retroachievements.org/Badge/')+'.png', 
                locked      = locked,
                index       = index,
                cached      = cached,
                game        = game,
            )


try:
    db.connect()
    db.create_tables([Game, Cheevo])
except Exception as E:
    Log.warning(str(E))
