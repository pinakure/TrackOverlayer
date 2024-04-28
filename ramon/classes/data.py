import os, random, json
from dearpygui              import dearpygui as dpg
from datetime               import datetime, timedelta
from classes.cheevo         import Cheevo
from classes.game           import Game
from classes.preferences    import Preferences
from classes.log            import Log
from classes.plugin         import Plugin
from classes.scraper        import Scraper
from classes.tools          import readfile,sane

class Data(Scraper):

    def __init__(self, parent):
        username = Preferences.settings[ 'username' ]
        password = Preferences.settings[ 'password' ]
        api_key  = Preferences.settings[ 'ra-app-key' ]

        Scraper.__init__(self, 
            protocol        = "https", 
            host            = "retroachievements.org", 
            port            = None, 
            needs_login     = True, 
            form_boundary   = True,
            login_form_url  = 'login', 
            login_post_url  = 'login', 
            login_username  = username,
            login_password  = password,
            login_fields    = {
                'User'      : username,
                'password'  : password,
            },
            login_tokens    = [ '_token'    , '_method'                     ],
            cookies         = [ 'XSRF-TOKEN', 'retroachievements_session'   ],
            api_key         = api_key,
        )
        self.parent         = parent        
        self.echo           = False
        self.score          = ''
        self.site_rank      = ''
        self.last_seen_full = ''
        self.last_seen      = ''
        self.last_activityr = ''
        self.last_activity  = None
        self.progress       = ''
        self.last_progress  = ''
        self.stats          = ''
        self.the_cheevo     = None
        self.cheevo         = ''
        self.cheevos_raw    = []
        self.cheevos        = []
        self.locked         = []
        self.unlocked       = []
        self.mine           = True
        self.notifications  = []
        self.recent         = []
        self.reload_rate    = 60
        self.game           = None
        self.game_id        = 0
        
        
    # below is un-refactored methods...
    # pretty much still

    def enqueueCheevoPayload(self, cheevo):
        self.parent.queue.append(cheevo)

    def dispatchQueue(self):
        last   = False
        redraw = False
        if not len(self.parent.queue): return
        head = self.parent.queue[0]
        if len(self.parent.queue)==1: 
            last   = True
        self.parent.queue = self.parent.queue[1:] if len( self.parent.queue)>1 else []
        cheevo = Cheevo.parse(self.game, head)
        if self.parent.text_only:
            self.parent.log.print(f"Parsed {'un' if not cheevo.locked else ''}locked cheevo {cheevo.name}")
        if cheevo.locked:
            self.locked.append(cheevo)
        self.cheevos.append( cheevo )
        if cheevo.index == Cheevo.active_index:
            redraw = True
            self.setActiveCheevo(cheevo.index)
            self.cheevo = cheevo.name + "\n" + cheevo.description
            self.writeCheevo()
        if redraw or last:
            if last: 
                Cheevo.checkAll()
                Plugin.compose()
                Log.info("Ready")
                # Set flag stating its safe to scan cheevos now
            self.parent.redraw()
        if self.parent.text_only:
            self.parent.cheevo_list.redraw=True
            self.parent.cheevo_list.selection=Cheevo.active_index-1
            self.parent.cheevo_list.render()
            self.parent.redraw()
            self.parent.activity = True

    def parseCheevos(self, game, payload):
        self.parent.queue = []
        Log.info(f'SCRAPER : Loading {len(self.cheevos_raw)} cheevo payloads into parsing queue...')
        for t, c in payload['cheevos'].items():
            #if (t%5) == 0: dpg.render_dearpygui_frame()
            self.enqueueCheevoPayload( c )        
        Log.info(f'SCRAPER : Enqueued {len(self.parent.queue)} cheevos.')
        return []
    
    
    def getDate( self, usersummary ):
        try:
            Log.info("SCRAPER : Extracting User Timestamp...")
        except Exception as E:
            Log.error("Cannot extract User Timestamp", E)
    
    def getRecent(self):
        self.recent = []
        unlocked = ''
        payload  = ''
        for d in self.cheevos:
            if d.locked: 
                payload += d.menu() + "\n"                
            else:
                if len(self.recent) < int(Plugin.loaded['recentunlocks'].settings['row-count']): 
                    self.recent.append(d)
                unlocked += '* '+ d.menu() + "\n"
        return payload, unlocked
    
    def setActiveCheevo(self, index):
        Cheevo.active_index = index
        Preferences.settings['current_cheevo'] = Cheevo.active_index
        if self.parent.text_only: 
            # do text only stuff
            return
        if not Preferences.settings['simple_ui']:
            for i in range(0,Cheevo.max):
                dpg.set_value(f'cheevo[{i+1}]', False)
            dpg.set_value(f'cheevo[{Cheevo.active_index}]', True)
     
    def parse(self, payload):
        # Try to parse profile HTML and extract metadata
        try:
            Log.info("SCRAPER : Extracing User Summary Data")
            self.locked         = []
            self.site_rank      = 1     #TODO: use user summary endpoint to get this data 
            self.last_activity  = ''    #TODO: use user summary endpoint to get this data 
            self.score          = payload['meta']['score']
            self.game_id        = payload['id']
            self.game_picture   = payload['boxart'].split('.png')[0]
            self.last_seen_full = payload['name']
            self.platform       = payload['platform']
            self.game_name      = payload['name']
            self.progress       = payload['progress']
            self.subset         = ''
            if 'Subset' in  self.game_name:
                #TODO: get current subset
                pass            
            # Create game instances
            self.game = Game.loadOrCreate(
                game_id     = self.game_id, 
                name        = self.game_name, 
                picture     = self.game_picture, 
                subset      = self.subset, 
                platform    = self.platform,
            )
            self.setActiveCheevo( self.game.current )
            self.cheevos        = self.parseCheevos(self.game, payload)
            if Preferences.table_game is not None:
                Preferences.table_game.update()  

            
            Log.info(f'{ f"{self.progress}  -  {len([cheevo for cheevo in self.cheevos if not cheevo.locked])}/{len(self.cheevos)}" if self.game else "No game"}')
            return True
        except Exception as E:
            Log.error("Cannot parse response data; Structure may have be changed.", E)
            return False
    
    def query(self):
        Log.info("Performing real request")
        payload = self.get()
        return self.parse(payload)
    
    def updatePictures(self):        
        try:   
            width, height, depth, data = dpg.load_image(f'{Preferences.root}/data/current_cheevo.png')                
        except Exception as E:
            Log.error("Cannot load 'current_cheevo.png'", E)
        
        with dpg.texture_registry(show=False):
            try:
                dpg.delete_item('current_cheevo_img')
                dpg.delete_item('current_cheevo_image')               
            except:
                pass
            try:
                dpg.add_static_texture(
                    width           = width, 
                    height          = height, 
                    default_value   = data, 
                    tag             = "current_cheevo_img",
                )
                dpg.add_image(
                    parent          = 'main',
                    tag             = 'current_cheevo_image', 
                    texture_tag     = "current_cheevo_img",
                    pos             = (self.parent.padding,self.parent.menu_height+4),
                    width           = 64,
                    height          = 64,
                )
            except Exception as E:
                Log.error("Cannot create static texture 'current_cheevo_img'.", E)
    
    def getCurrentCheevo( self, picture ):
        # try first if image is in cache
        cheevo_id = picture.split('.png')[0].split('_lock')[0]
        if not os.path.exists(f'{Preferences.root}/data/cache/{picture}'):
            Cheevo.getPicture( cheevo_id )
        data = {}
        with open(f'{Preferences.root}/data/cache/{cheevo_id}.png', 'rb') as file:
            data[0] = file.read()
        with open(f'{Preferences.root}/data/cache/{cheevo_id}_lock.png', 'rb') as file:
            data[1] = file.read()
        return data
    
    #TODO: Move to endpoints
    def markNotification(self, notification_name):
        from classes.cheevo import Cheevo
        Log.info(f"Marking cheevo '{notification_name}' as notified.")
        try:
            cheevo = Cheevo.get(Cheevo.name==notification_name.replace('`', "'"))
            cheevo.notified = True
            cheevo.save()
        except Exception as E:
            Log.error(f"Cannot mark notification '{notification_name}'", E)
    
    #TODO: Move to endpoints
    def getNotifications(self):
        notifications = []
        cheevos = (Cheevo
                .select()
                .join(Game)
                .where(Cheevo.game==self.game, Cheevo.locked==False, Cheevo.notified==0)
                .order_by(Cheevo.index.asc())
            )
        for cheevo in cheevos:
            notifications.append( [ 
                sane(cheevo.name),
                sane(cheevo.description).split('.')[0].split('[')[0], 
                cheevo.picture.rstrip('.png').rstrip('_lock') 
            ] )
            try:
                cheevo.save()
            except:
                pass
        return notifications
    
    def writeCheevo(self):
        for d in self.cheevos:
            if d.index == Cheevo.active_index:
                self.the_cheevo = d
                self.cheevo = d.name + "\n" + d.description
                # get achievement picture
                data = self.getCurrentCheevo( d.picture )
                if len(data)>0:
                    with open(f"{Preferences.root}/data/current_cheevo.png", 'wb') as picture:
                        picture.write(data[0] )
                    with open(f"{Preferences.root}/data/current_cheevo_lock.png", 'wb') as picture:
                        picture.write(data[1] )
                    if not self.parent.text_only:
                        self.updatePictures()
    
    def write(self):
        if Preferences.settings['username'] == '': return
        self.writeCheevo()
        