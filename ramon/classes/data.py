import requests, os, random, json
from dearpygui              import dearpygui as dpg
from datetime               import datetime, timedelta
from bs4                    import BeautifulSoup    
from classes.cheevo         import Cheevo,Game
from classes.preferences    import Preferences
from classes.log            import Log
from classes.plugin         import Plugin
from classes.scraper        import Scraper

def ascii(string):
    table = {
        'ū' : 'u',
        'à' : 'a',
        'è' : 'e',
        'ì' : 'i',
        'ò' : 'o',
        'ù' : 'u',
    }
    for key, value in table.items():
        string = string.replace(key, value)
    return str(string)

class Data:
    parent          = None
    echo            = False
    score           = ''
    site_rank       = ''
    last_seen_full  = ''
    last_seen       = ''
    last_activityr  = ''
    last_activity   = None
    progress        = ''
    stats           = ''
    cheevo          = ''
    cheevos_raw     = []
    cheevos         = []
    mine            = True
    username        = ''
    recent          = []
    reload_rate     = 60
    css             = {}
    game            = None
    game_id         = 0
    parsed          = None

    @staticmethod
    def parseCheevos(game):
        cheevos = []
        for i, c in enumerate(Data.cheevos_raw):
            cheevos.append( Cheevo.parse( game, c ) )
        return cheevos       
        
    @staticmethod
    def getRank( usersummary ):
        try:
            Log.info("Parsing User Rank...")
            Data.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
        except Exception as E:
            Log.error("Cannot parse User Rank", E)
            
    @staticmethod
    def getDate( usersummary ):
        try:
            Log.info("Parsing User Last Activity Date...")
            Data.last_activityr = usersummary.split('Last Activity: ')[1].split('Account')[0]
            Data.last_activity  = (datetime.strptime(Data.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Preferences.settings['gmt']))
        except Exception as E:
            Log.error("Cannot parse User Last Activity Date", E)
        
    @staticmethod
    def getScore( usersummary ):
        try:
            Log.info("Parsing User Score...")
            Data.score = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
        except Exception as E:
            Log.error("Cannot parse User Score", E)

    @staticmethod
    def getGame( usersummary_raw ):
        try:
            Log.info("Getting Game data...")
            Data.game_id = int(str(usersummary_raw).split('retroachievements.org/game/')[1].split('"')[0])
            Data.game    = Game.loadOrCreate(Data.game_id)   
            Data.last_seen_full = usersummary_raw.text.split('Last seen  in  ')[1]
            Data.last_seen      = Data.last_seen_full.split('(')[0]              
        except Exception as E:
            Log.error("Cannot parse Game Data", E)

    @staticmethod
    def getUserSummary():
        try:
            Log.info("Getting User Summary HTML...")
            usersummary_raw     = Data.parsed.body.find('div', attrs={'class':'usersummary'})
            usersummary         = usersummary_raw.text
            Data.getScore(usersummary)
            Data.getRank(usersummary)
            Data.getDate(usersummary)
            Data.getGame(usersummary_raw)
        except Exception as E:
            Log.error("Cannot parse payload getting User Summary", E)
    
    @staticmethod
    def setActiveCheevo(index):
        Cheevo.active_index = index
        Preferences.settings['current_cheevo'] = Cheevo.active_index
        for i in range(0,Cheevo.max):
            dpg.set_value(f'cheevo[{i+1}]', False)
            dpg.set_value(f'cheevo[{Cheevo.active_index}]', True)
            
    @staticmethod 
    def getCheevos():
        import random
        try:
            rid = random.random()
            Log.info("Updating cheevo info...")
            stats = str(Data.parsed.body.find('div', attrs={'class':'userpage recentlyplayed'}))
            try:
                Log.info("Getting progress HTML")
                progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
                Log.info("Getting progress")
                Data.progress  = progress_html.split('width:')[1].split('"')[0] if not Plugin.debug else f'{int(random.random()*100)}%'
            except:
                Data.progress  = '0%'
                dpg.set_value('stdout', 'Asuming no achievements, since no progressbar was found.')
                return True
            Log.info("Getting metadata")
            Data.stats = stats.split('<div class="mb-5">')[1].split('</div>')[0]
            Log.info("Getting cheevos raw data")
            Data.cheevos_raw    = Data.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
            Log.info("Parsing cheevos")
            Data.cheevos        = Data.parseCheevos(Data.game)
            for d in Data.cheevos:
                if d.index == Cheevo.active_index:
                    Data.cheevo = d.name + "\n" + d.description
        except Exception as E:
            Log.error("Cannot parse Updated Cheevo information", E)

    @staticmethod
    def query():
        Log.info('Refreshing data...')
        Data.css = Data.parent.css
        Preferences.data = Data
        if Preferences.settings['username'] == '': return
        try:
            payload             = requests.get(f'https://www.retroachievements.org/user/{Preferences.settings["username"]}').text
            Data.parsed         = BeautifulSoup( payload, features='html.parser' )
            Data.getUserSummary()
            Data.setActiveCheevo( Data.game.current )
            Data.getCheevos()
            dpg.set_viewport_title(f'RAMon - { f"{Data.progress}  -  {len([cheevo for cheevo in Data.cheevos if not cheevo.locked])}/{len(Data.cheevos)}" if Data.game else "No game"}')
            return True
        except Exception as E:
            Log.error("Cannot query RetroAchievements", E)
            return False
        
    @staticmethod
    def updatePictures():
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
                    pos=(Data.parent.width-width,69),
                    width=40,
                    height=40,
                )
                #Log.info("Added image 'current_cheevo_image'.")
            except Exception as E:
                Log.error("Cannot create static texture 'current_cheevo_img'.", E)
                
    @staticmethod
    def getCurrentCheevo( picture ):
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
        
    @staticmethod
    def writeCheevo():
        if Preferences.settings['username'] == '': return
        for d in Data.cheevos:
            if d.index == Cheevo.active_index:
                with open(f'{Preferences.root}/data/current_cheevo.txt' , 'w') as file:   
                    file.write(str(d.name))
                    file.write('\n')
                    file.write(str(d.description))
                    Data.cheevo = d.name + "\n" + d.description
                    # get achievement picture
                    data = Data.getCurrentCheevo( d.picture )
                    if len(data)>0:
                        with open(f"{Preferences.root}/data/current_cheevo.png", 'wb') as picture:
                            picture.write(data[0] )
                        with open(f"{Preferences.root}/data/current_cheevo_lock.png", 'wb') as picture:
                            picture.write(data[1] )
                        Data.updatePictures()
                
    @staticmethod
    def getReloadSnippet():
        return """<script>function refresh(){ window.location.reload(); } setInterval(refresh, """+str(Data.reload_rate*500)+""")</script>"""

    @staticmethod
    def writeCheevos():
        script = Data.getReloadSnippet()
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
                    for d in Data.cheevos:
                        Data.parent.setProgress( count / len(Data.cheevos) )
                        file.write( ascii(str(d)) + '\n' )
                        if d.locked:
                            locked.write( ascii(str(d)) + '\n' )
                        else:
                            unlocked.write( ascii(str(d)) + '\n' )
                        count+=1
                    file.write     ('</div>')
                    locked.write   ('</div>')
                    unlocked.write ('</div>')
                    Data.parent.setProgress(1.0)
        
    @staticmethod
    def writeRecent():
        script = Data.getReloadSnippet()
        rid = random.random()
        with open(f'{Preferences.root}/data/recent.html'        , 'w') as file:   
            file.write(f'''<link rel="stylesheet" type="text/css" href="../css/recent.css?{rid}">''')
            file.write(f'''{script}<table><tbody>''')
            for r in Data.recent:
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

    @staticmethod
    def getNotifications():
        notifications = []
        cheevos = (Cheevo
                .select()
                .join(Game)
                .where(Cheevo.game==Data.game, Cheevo.locked==False, Cheevo.notified==False)
                .order_by(Cheevo.index.asc())
            )
        for cheevo in cheevos:
            notifications.append( [ cheevo.name, cheevo.description, cheevo.picture.rstrip('.png').rstrip('_lock') ] )
            cheevo.notified = True
            cheevo.save()
        return notifications
        
    @staticmethod
    def writeNotifications():
        notifications = Data.getNotifications()
        Data.notifications = notifications
        data = json.dumps(notifications)
        
    @staticmethod
    def write():
        if Preferences.settings['username'] == '': return
        with open(f'{Preferences.root}/data/last_activity.txt'  , 'w') as file:   file.write(Data.last_activity.strftime("%d %b %Y, %H:%M").upper() )
        with open(f'{Preferences.root}/data/last_seen.txt'      , 'w') as file:   file.write(ascii(Data.last_seen     ))
        with open(f'{Preferences.root}/data/site_rank.txt'      , 'w') as file:   file.write(Data.site_rank     )
        with open(f'{Preferences.root}/data/score.txt'          , 'w') as file:   file.write(Data.score         )        
        Data.writeNotifications()
        Data.writeCheevo()
        Data.writeCheevos()
        Data.writeRecent()
