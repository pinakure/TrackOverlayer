import requests, os, json
from classes.log         import Log
from classes.game        import Game
from classes.database    import DDBB
from peewee              import *
from classes.scraper     import Scraper
from classes.preferences import Preferences
from classes.tools       import extract

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
        database = DDBB.db

    def menu(self):
        return f'{self.name.ljust(Cheevo.min_width, " ")}'+"\n"+(" "*9)+f'{self.description}'
    
    def setupScraper(self):
        from classes.ramon import Ramon
        self.scraper = Scraper()
        self.scraper.protocol         = Ramon.data.protocol
        self.scraper.host             = Ramon.data.host
        self.scraper.port             = Ramon.data.port
        self.scraper.session          = Ramon.data.session
        self.scraper.cookies          = Ramon.data.cookies
        self.scraper.login_tokens     = Ramon.data.login_tokens
        self.scraper.needs_login      = False
        self.scraper.logged_in        = True
        self.scraper.parsed           = None
        self.scraper.target_url       = self.scraper.url( f'achievement/{self.id}' )
        self.scraper.user_agent       = f'tRAckOverlayer/{ Preferences.settings["username"] }'
        self.scraper.response         = None
        self.scraper.response_text    = None
        self.scraper.response_code    = None
        self.scraper.response_content = None
        
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
            Log.info(f"Caching cheevo picture {self.picture}...")
            Cheevo._build_cache(self.picture)
            self.cached = True
            self.save()

        except Exception as E:
            Log.error(f"Cannot create cache for cheevo {self.id}", E)
    
    def __str__(self):
        return f'<img class="{"active" if self.index == Cheevo.active_index else ""} round" width="48" height="48" src="cache/{self.picture}" title="{self.description}" name="{self.name}">'

    checking = False
    queue    = []

    def checkAll():
        from classes.ramon import Ramon
        Cheevo.queue = []
        for cheevo in Ramon.data.locked:
            Cheevo.queue.append( cheevo )
            #cheevo.check()

    def check(self):
        from classes.ramon import Ramon
        if Preferences.settings['offline']: 
            Log.info(f"Skipping cheevo '{ self.name }' checking due to offline mode")
            return
    
        if self.locked: 
            Log.info(f"Checking cheevo '{ self.name }'...")
            self.scraper.get()
            data = extract(
                self.scraper.response_text,
                f'<a href="/achievement/{self.id}">',
                '</a>'
            )
            if not '_lock' in data:
                Log.info(f"    Cheevo { self.id } has just been unlocked!")
                self.notified = False
                self.locked = False
                Ramon.data.locked.remove(self)
                self.save()
                return
            Log.info(f"    Cheevo is still locked.")

    def dispatchQueue():
        from classes.ramon import Ramon
        last   = False
        if not len(Cheevo.queue): return
        head = Cheevo.queue[0]
        if len(Cheevo.queue)==1: 
            last   = True
        Cheevo.queue = Cheevo.queue[1:] if len( Cheevo.queue)>1 else []
        head.check()
        if last:
            Cheevo.checking = False
            Log.info("Finished checking cheevos")                
            Ramon.redraw()

    def parse( game, payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'").split('&lt')[0].rstrip()
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
            cheevo.setupScraper()
            cheevo.locked  = locked
            cheevo.picture = picture.strip('https://media.retroachievements.org/Badge/')+'.png'
            cheevo.index   = index
            cheevo.cached  = cached        
            cheevo.save()
            return cheevo
        except Exception as E:            
            # cheevo does not exist in DB, create new
            Log.info(f"DATABASE : New Cheevo '{cheevo_id}' found! Creating database entry...", True)
            
            cheevo = Cheevo.create(
                id          = cheevo_id,
                name        = name.replace('"', "´"), 
                description = description.replace('"', "´"), 
                picture     = picture.strip('https://media.retroachievements.org/Badge/')+'.png', 
                locked      = locked,
                index       = index,
                cached      = cached,
                game        = game,
            )
            cheevo.setupScraper()
            return cheevo


