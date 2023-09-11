import os, random, json
from dearpygui              import dearpygui as dpg
from datetime               import datetime, timedelta
from classes.cheevo         import Cheevo,Game, db
from classes.preferences    import Preferences
from classes.log            import Log
from classes.plugin         import Plugin
from classes.scraper        import Scraper
from classes.tools          import ascii, readfile

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
            cookies   = [ 'XSRF-TOKEN', 'retroachievements_session'   ],
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
        self.mine           = True
        self.notifications  = []
        self.recent         = []
        self.reload_rate    = 60
        self.game           = None
        self.game_id        = 0
        
        
        
    # below is un-refactored methods...
    # pretty much still

    def parseCheevos(self, game):
        cheevos = []
        with db.atomic():            
            Log.info(f'Parsing {len(self.cheevos_raw)} raw cheevos')
            for t, c in enumerate(self.cheevos_raw):
                if t%5 == 0: dpg.render_dearpygui_frame()
                cheevos.append( Cheevo.parse( game, c ) )
            Log.info(f'Got {len(cheevos)} sane cheevo instances')
        return cheevos       
        
    
    def getRank( self, usersummary ):
        try:
            Log.info("Parsing User Rank...")
            self.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
        except Exception as E:
            Log.error("Cannot parse User Rank", E)
            
    
    def getDate( self, usersummary ):
        try:
            Log.info("Parsing User Last Activity Date...")
            self.last_activityr = usersummary.split('Last Activity: ')[1].split('Account')[0]
            self.last_activity  = (datetime.strptime(self.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Preferences.settings['gmt']))
        except Exception as E:
            Log.error("Cannot parse User Last Activity Date", E)
        
    
    def getScore( self, usersummary ):
        try:
            Log.info("Parsing User Score...")
            self.score = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
        except Exception as E:
            Log.error("Cannot parse User Score", E)

    
    def getGame( self, usersummary_raw ):
        try:
            Log.info("Getting Game data...")
            gamepart = str(usersummary_raw).split('retroachievements.org/game/')[1]
            # Log.info(gamepart)           
            self.game_id = int(gamepart.split('"')[0])
            self.game    = Game.loadOrCreate(self.game_id)   
            self.last_seen_full = usersummary_raw.text.split('Last seen  in  ')[1].split('[')[0]
            self.last_seen      = self.last_seen_full.split('(')[0]              
        except Exception as E:
            Log.error("Cannot parse Game Data", E)

    
    def getUserSummary(self):
        try:
            Log.info("Getting User Summary HTML...")
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
        for i in range(0,Cheevo.max):
            dpg.set_value(f'cheevo[{i+1}]', False)
            dpg.set_value(f'cheevo[{Cheevo.active_index}]', True)
            
     
    def getCheevos(self):
        import random
        try:
            rid = random.random()
            Log.info("Updating cheevo info...")
            stats = str(self.parsed.body.find('div', attrs={'class':'userpage recentlyplayed'}))
            #self.last_progress = self.progress
            try:
                Log.info("Getting progress HTML")
                progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
                Log.info("Getting progress")
                self.progress  = progress_html.split('width:')[1].split('"')[0] if not Plugin.debug else f'{int(random.random()*100)}%'
            except:
                self.progress  = '0%'
                dpg.set_value('stdout', 'Asuming no achievements, since no progressbar was found.')
                return True
            Log.info("Getting metadata")
            self.stats = stats.split('<div class="mb-5">')[1].split('</div>')[0]
            Log.info("Getting cheevos raw data")
            self.cheevos_raw    = self.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
            Log.info("Parsing cheevos")
            self.cheevos        = self.parseCheevos(self.game)
            for t, d in enumerate(self.cheevos):
                if t%5 == 0:dpg.render_dearpygui_frame()
                if d.index == Cheevo.active_index:
                    self.the_cheevo = d
                    self.cheevo = d.name + "\n" + d.description
        except Exception as E:
            Log.error("Cannot parse Updated Cheevo information", E)

    def getPayload(self):
        # Try to get RA user profile HTML
        self.request( self.url(f'user/{ self.login_username }'), filename="profile" )
        if not self.response_text:
            Log.error("Cannot get RA Payload")
            return False
        return True
    
    
    def parse(self):
        # Try to parse profile HTML and extract metadata
        try:
            Scraper.parse(self)
            self.getUserSummary()
            self.setActiveCheevo( self.game.current )
            self.getCheevos()
            dpg.set_viewport_title(f'tRAckOverlayer - { f"{self.progress}  -  {len([cheevo for cheevo in self.cheevos if not cheevo.locked])}/{len(self.cheevos)}" if self.game else "No game"}')
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
        return self.get()
    
    def updatePictures(self):
        try:   
            width, height, depth, data = dpg.load_image(f'{Preferences.root}/data/current_cheevo.png')                
        except Exception as E:
            Log.error("Cannot load 'current_cheevo.png'", E)
        
        with dpg.texture_registry(show=False):
            try:
                dpg.delete_item('current_cheevo_img')
                #Log.info("deleted static_texture 'current_cheevo_img'.")
                dpg.delete_item('current_cheevo_image')
                #Log.info("deleted image 'current_cheevo_image'.")
            except:
                pass
            try:
                dpg.add_static_texture(
                    width=width, 
                    height=height, 
                    default_value=data, 
                    tag="current_cheevo_img",
                )
                #Log.info("Added static texture 'current_cheevo_img'.")
                dpg.add_image(
                    parent='main',
                    tag='current_cheevo_image', 
                    texture_tag="current_cheevo_img",
                    pos=(self.parent.width-width,69),
                    width=40,
                    height=40,
                )
                #Log.info("Added image 'current_cheevo_image'.")
            except Exception as E:
                Log.error("Cannot create static texture 'current_cheevo_img'.", E)
                
    
    def getCurrentCheevo( self, picture ):
        # try first if image is in cache
        cheevo_id = picture.split('.png')[0].split('_lock')[0]
        if not os.path.exists(f'{Preferences.root}/data/cache/{picture}'):
            Cheevo.getPicture( cheevo_id )
        data = {}
        with open(f'{Preferences.root}/data/cache/{cheevo_id}.png', 'rb') as file:
            # Log.info(f'Using cached image {picture}')
            data[0] = file.read()
        with open(f'{Preferences.root}/data/cache/{cheevo_id}_lock.png', 'rb') as file:
            # Log.info(f'Using cached image {picture}')
            data[1] = file.read()
        return data
        
    
    def writeCheevo(self):
        if Preferences.settings['username'] == '': return
        for d in self.cheevos:
            if d.index == Cheevo.active_index:
                with open(f'{Preferences.root}/data/current_cheevo.txt' , 'w') as file:   
                    file.write(str(d.name))
                    file.write('\n')
                    file.write(str(d.description))
                    self.cheevo = d.name + "\n" + d.description
                    # get achievement picture
                    data = self.getCurrentCheevo( d.picture )
                    if len(data)>0:
                        with open(f"{Preferences.root}/data/current_cheevo.png", 'wb') as picture:
                            picture.write(data[0] )
                        with open(f"{Preferences.root}/data/current_cheevo_lock.png", 'wb') as picture:
                            picture.write(data[1] )
                        self.updatePictures()
                
    
    def getReloadSnippet(self):
        return """<script>function refresh(){ window.location.reload(); } setInterval(refresh, """+str(self.reload_rate*500)+""")</script>"""

    
    def writeCheevos(self):
        script = self.getReloadSnippet()
        rid = random.random()
        with open(f'{Preferences.root}/data/cheevos.html'         , 'w') as file:   
            with open(f'{Preferences.root}/data/cheevos_locked.html'  , 'w') as locked:   
                with open(f'{Preferences.root}/data/cheevos_unlocked.html'  , 'w') as unlocked:   
                    file.write     ( f'<link rel="stylesheet" type="text/css" href="../css/cheevos.css?{rid}">{script}')
                    locked.write   ( f'<link rel="stylesheet" type="text/css" href="../css/locked.css?{rid}">{script}')
                    unlocked.write ( f'<link rel="stylesheet" type="text/css" href="../css/unlocked.css?{rid}">{script}')
                    file.write     ( '<div class="table">')
                    locked.write   ( '<div class="table">')
                    unlocked.write ( '<div class="table">')
                    count = 0
                    for d in self.cheevos:
                        self.parent.setProgress( count / len(self.cheevos) )
                        file.write( ascii(str(d)) + '\n' )
                        if d.locked:
                            locked.write( ascii(str(d)) + '\n' )
                        else:
                            unlocked.write( ascii(str(d)) + '\n' )
                        count+=1
                    file.write     ('</div>')
                    locked.write   ('</div>')
                    unlocked.write ('</div>')
                    self.parent.setProgress(1.0)
        
    
    def writeRecent(self):
        script = self.getReloadSnippet()
        rid = random.random()
        with open(f'{Preferences.root}/data/recent.html'        , 'w') as file:   
            file.write(f'''<link rel="stylesheet" type="text/css" href="../css/recent.css?{rid}">''')
            file.write(f'''{script}<table><tbody>''')
            for r in self.recent:
                file.write(f'''
                            <tr><td colspan="2"><hr/></td></tr>
                            <tr>
                                <td rowspan="2">
                                    <img style="border-radius: none !important" src="cache/{r.picture}">
                                </td>
                                <td><b>{ascii(r.name)}</b></td>
                            </tr>
                            <tr>
                                <td>{ascii(r.description)}</td>
                            </tr>
                ''')                
            file.write('''</tbody><table>''')

    
    def getNotifications(self):
        notifications = []
        cheevos = (Cheevo
                .select()
                .join(Game)
                .where(Cheevo.game==self.game, Cheevo.locked==False, Cheevo.notified==False)
                .order_by(Cheevo.index.asc())
            )
        for cheevo in cheevos:
            notifications.append( [ cheevo.name, cheevo.description, cheevo.picture.rstrip('.png').rstrip('_lock') ] )
            cheevo.notified = True
            cheevo.save()
        return notifications
        
    
    def writeNotifications(self):
        notifications = self.getNotifications()
        self.notifications = notifications
        data = json.dumps(notifications)
        
    
    def write(self):
        if Preferences.settings['username'] == '': return
        with open(f'{Preferences.root}/data/last_activity.txt'  , 'w') as file:   file.write(self.last_activity.strftime("%d %b %Y, %H:%M").upper() )
        with open(f'{Preferences.root}/data/last_seen.txt'      , 'w') as file:   file.write(ascii(self.last_seen     ))
        with open(f'{Preferences.root}/data/site_rank.txt'      , 'w') as file:   file.write(self.site_rank     )
        with open(f'{Preferences.root}/data/score.txt'          , 'w') as file:   file.write(self.score         )        
        self.writeNotifications()
        self.writeCheevo()
        self.writeCheevos()
        self.writeRecent()
