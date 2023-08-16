try: 
    import obspython as obs
except ImportError:
    pass
import os, time
try: 
    import requests
    from bs4 import BeautifulSoup    
except ImportError:
    os.system('pip install requests beatifulsoup4')
    exit()

def get_payload():
    return response

class Cheevo:
    def __init__(self, name, description, picture):
         self.name = name.replace('"', "´")
         self.description = description.replace('"', "´")
         self.picture = picture

    def __str__(self):
        return f'<img width="48" height="48" src="{self.picture}" title="{self.description}" name="{self.name}">'

    @staticmethod
    def parse( payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'")
        picture     = payload.split('img src=')[1].split('.png')[0].replace('\\\'', '') + ".png"
        description = payload.split('mb-1')[1].split('gt')[1].split('&lt;/div')[0].replace(';', '')
        #picture     = f'{picture}.png'
        return Cheevo(name, description, picture)

class Data:

    score           = 0
    site_rank       = 0
    last_seen       = 0
    last_activity   = 0
    progress_html   = ''
    progress        = ''
    stats           = ''
    cheevos_raw     = []
    cheevos         = []

    @staticmethod
    def parseCheevos():
        cheevos = []
        for c in Data.cheevos_raw:
            cheevos.append( Cheevo.parse( c ) )
        return cheevos
        
    @staticmethod
    def query():
        payload             = requests.get('https://www.retroachievements.org/user/smiker').text
        parsed_html         = BeautifulSoup( payload, features='html.parser' )
        usersummary         = parsed_html.body.find('div', attrs={'class':'usersummary'}).text
        Data.score          = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
        Data.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
        Data.last_seen      = usersummary.split('Last seen  in  ')[1].split('(')[0]
        Data.last_activity  = usersummary.split('Last Activity: ')[1].split('Account')[0]
        stats               = str(parsed_html.body.find('div', attrs={'class':'userpage recentlyplayed'}))
        Data.progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
        Data.progress_html  = f'<div class="progressbar grow">{Data.progress_html}</div>'
        Data.progress       = Data.progress_html.split('width:')[1].split('"')[0]
        Data.stats          = stats.split('<div class="mb-5">')[1].split('</div>')[0]
        Data.cheevos_raw    = Data.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
        Data.cheevos        = Data.parseCheevos()
        
    @staticmethod
    def dump():
        print(Data.score         )
        print(Data.site_rank     )
        print(Data.last_seen     )
        print(Data.last_activity )
        print( '-' * 80          )
        print( Data.progress_html)
        print( Data.progress     )
        for d in Data.cheevos:
           print(d)  

    @staticmethod
    def write():
        with open('/src/ramon/data/progress.html'      , 'w') as file:   file.write(Data.progress_html )
        with open('/src/ramon/data/progress.txt'       , 'w') as file:   file.write(Data.progress      )
        with open('/src/ramon/data/last_activity.txt'  , 'w') as file:   file.write(Data.last_activity.upper() )
        with open('/src/ramon/data/last_seen.txt'      , 'w') as file:   file.write(Data.last_seen     )
        with open('/src/ramon/data/site_rank.txt'      , 'w') as file:   file.write(Data.site_rank     )
        with open('/src/ramon/data/score.txt'          , 'w') as file:   file.write(Data.score         )
        with open('/src/ramon/data/cheevos.html'       , 'w') as file:   
            file.write( """<style>
                html, body {
                    height: 100%;
                    overflow-x: hidden;
                    overflow-y: hidden;
                }
                html, img, body {
                    background-color: rgba(0,0,0,0);
                    padding:           0px 0px 0px 0px;
                    line-height:        16px;
                }
                img {
                    border-radius: 24px 24px 24px 24px;
                    box-shadow: 2px 2px 0px #0008;
                }
            </style>""")
            for d in Data.cheevos:
                file.write( str(d) )            
def update_text():
    Data.query()
    Data.dump()
    Data.write()

def refresh_pressed(props, prop):
	update_text()

# ------------------------------------------------------------
def script_defaults(settings):
	pass
    #obs.obs_data_set_default_int(settings, "interval", 30)

def script_description():
	return "Updates retroachievement info for current game"

def script_properties():
	props = obs.obs_properties_create()

def script_update(settings):
	obs.timer_remove(update_text)
	obs.timer_add(update_text, 60 * 1000)

while 1:
    update_text()
    time.sleep(60)