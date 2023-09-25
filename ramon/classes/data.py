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
            target_url      = f"user/{ username }",
            login_fields    = {
                'User'      : username,
                'password'  : password,
            },
            login_tokens    = [ '_token'    , '_method'                     ],
            cookies         = [ 'XSRF-TOKEN', 'retroachievements_session'   ],
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

    def parseCheevos(self, game):
        self.parent.queue = []
        Log.info(f'SCRAPER : Loading {len(self.cheevos_raw)} cheevo payloads into parsing queue...')
        for t, c in enumerate(self.cheevos_raw):
            #if (t%5) == 0: dpg.render_dearpygui_frame()
            self.enqueueCheevoPayload( c )        
        Log.info(f'SCRAPER : Enqueued {len(self.parent.queue)} cheevos.')
        return []
    
    def getRank( self, usersummary ):
        try:
            Log.info("SCRAPER : Extracting User Rank...")
            self.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
        except Exception as E:
            Log.error("Cannot extract User Rank", E)
    
    def getDate( self, usersummary ):
        try:
            Log.info("SCRAPER : Extracting User Timestamp...")
            self.last_activityr = usersummary.split('Last Activity: ')[1].split('Account')[0]
            self.last_activity  = (datetime.strptime(self.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Preferences.settings['gmt']))
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
    
    def getScore( self, usersummary ):
        try:
            Log.info("SCRAPER : Extracting User Score...")
            self.score = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
        except Exception as E:
            Log.error("Cannot extract User Score", E)
    
    def getGame( self, usersummary_raw ):
        try:
            Log.info("SCRAPER : Extracting Game Data...")
            self.subset       = ''
            userdata            = usersummary_raw.contents[-1].contents[1].contents[0].contents
            self.game_id        = int(usersummary_raw.contents[-1].contents[1].contents[0].attrs['href'].split('/')[-1])
            self.game_picture   = userdata[0].attrs['src'].split('/')[-1].split('.png')[0]
            self.last_seen_full = userdata[1].lstrip(' ').rstrip(' ')
            self.last_seen      = self.last_seen_full.split('(')[0].split('[')[0].lstrip(' ').rstrip(' ')
            self.platform       = userdata[1].split('(')[1].split(')')[0].lstrip(' ').rstrip(' ')
            self.game_name      = self.last_seen.split('|')[0].lstrip(' ').rstrip(' ')
            if 'Subset' in  usersummary_raw.text.split('Last seen  in  ')[1]:
                self.subset         = userdata[2].contents[2].text
            # Create game instances
            self.game = Game.loadOrCreate(
                game_id     = self.game_id, 
                name        = self.game_name, 
                picture     = self.game_picture, 
                subset      = self.subset, 
                platform    = self.platform,
            )
            if Preferences.table_game is not None:
                Preferences.table_game.update()
        except Exception as E:
            Log.error("Cannot parse Game Data", E)
    
    def getUserSummary(self):
        try:
            Log.info("SCRAPER : Parse ok, extracing User Summary")
            usersummary_raw     = self.parsed.body.find('div', attrs={'class':'usersummary'})
            usersummary         = usersummary_raw.text
            self.getScore(usersummary)
            self.getRank(usersummary)
            self.getDate(usersummary)
            self.getGame(usersummary_raw)
        except Exception as E:
            Log.error("Cannot parse payload getting User Summary", E)

    
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
     
    def getCheevos(self):
        import random
        try:
            rid = random.random()
            Log.info("SCRAPER : Extracting Cheevo payload...")
            stats = str(self.parsed.body.find('div', attrs={'class':'userpage recentlyplayed'}))
            #self.last_progress = self.progress
            try:
                Log.info("SCRAPER : Getting progress payload...")
                progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
                Log.info("SCRAPER : Extracting progress")
                self.progress  = progress_html.split('width:')[1].split('"')[0] if not Plugin.debug else f'{int(random.random()*100)}%'
            except:
                self.progress  = '0%'
                dpg.set_value('stdout', 'Asuming no achievements, since no progressbar was found.')
                return True
            Log.info("SCRAPER : Parsing payload...")
            self.stats          = stats.split('<div class="mb-5">')[1].split('</div>')[0]
            self.cheevos_raw    = self.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
            self.locked         = []
            self.cheevos        = self.parseCheevos(self.game)
            
        except Exception as E:
            Log.error("Cannot parse Updated Cheevo information", E)

    def getPayload(self):
        # Try to get RA user profile HTML
        Log.info("SCRAPER : Requesting user profile payload")
        self.request( self.url(f'user/{ self.login_username }'), filename="profile" )
        if not self.response_text:
            Log.error("Cannot get RA Payload")
            return False
        return True
    
    def parse(self):
        # Try to parse profile HTML and extract metadata
        try:
            Log.info("SCRAPER : Got user profile payload, parsing data...")
            Scraper.parse(self)
            self.getUserSummary()
            self.setActiveCheevo( self.game.current )
            self.getCheevos()
            Log.info(f'{ f"{self.progress}  -  {len([cheevo for cheevo in self.cheevos if not cheevo.locked])}/{len(self.cheevos)}" if self.game else "No game"}')
            return True
        except Exception as E:
            Log.error("Cannot parse profile HTML, the structure may have be changed.", E)
            return False
    
    def query(self):
        self.login_username = Preferences.settings['username']
        self.target_url     = self.url(f"user/{ self.login_username }" )
        if Preferences.settings['offline']:
            Log.info("DATA : Faking request to retroachievements")
            self.response_text = readfile(f'{Preferences.settings["root"]}/data/profile.html')
            return self.parse()
        Log.info("Performing real request")
        return self.get()
    
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
                .where(Cheevo.game==self.game, Cheevo.locked==False, Cheevo.notified==False)
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
        