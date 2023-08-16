import os, time
try: 
    import requests
    from bs4 import BeautifulSoup    
    from dearpygui import dearpygui as dpg
except ImportError:
    os.system('pip install requests beautifulsoup4 dearpygui')
    exit()


class Cheevo:
    
    min_width       = 0
    global_index    = 0
    active_index    = 1
    
    def __init__(self, name, description, picture):
         self.name = name.replace('"', "´")
         self.picture = picture
         self.locked  = picture.find('lock')>-1
         self.description = description.replace('"', "´")
         self.index = 0
         if self.locked:
            Cheevo.global_index+=1
            self.index = Cheevo.global_index
            if len(name)>Cheevo.min_width:
              Cheevo.min_width = len(name)+1

    def menu(self):
        return f'{self.name.ljust(Cheevo.min_width, " ")}'+"\n"+(" "*9)+f'{self.description}'
        #return f'{"->" if Cheevo.active_index == self.index else "  " }[{str(self.index).rjust(3)} ] {self.name.ljust(Cheevo.min_width, " ")}'+"\n"+(" "*9)+f'{self.description}'

    def __str__(self):
        return f'<img class="{"active" if self.index == Cheevo.active_index else ""}" width="48" height="48" src="{self.picture}" title="{self.description}" name="{self.name}">'

    @staticmethod
    def parse( payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'")
        picture     = payload.split('img src=')[1].split('.png')[0].replace('\\\'', '') + ".png"
        description = payload.split('mb-1')[1].split('gt')[1].split('&lt;/div')[0].replace(';', '')
        #picture     = f'{picture}.png'
        return Cheevo(name, description, picture)

class Data:
    root            = '/'
    echo            = False
    score           = ''
    site_rank       = ''
    last_seen       = ''
    last_activity   = ''
    progress_html   = ''
    progress        = ''
    stats           = ''
    cheevo          = ''
    cheevos_raw     = []
    cheevos         = []
    mine            = True
    username        = ''

    @staticmethod
    def setUsername():
        Data.username = dpg.get_value('username')

    @staticmethod
    def parseCheevos():
        cheevos = []
        for c in Data.cheevos_raw:
            cheevos.append( Cheevo.parse( c ) )
        return cheevos
        
    @staticmethod
    def query():
        if Data.username == '': return
        from datetime import datetime, timedelta
        payload             = requests.get(f'https://www.retroachievements.org/user/{Data.username}').text
        parsed_html         = BeautifulSoup( payload, features='html.parser' )
        usersummary         = parsed_html.body.find('div', attrs={'class':'usersummary'}).text
        Data.score          = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
        Data.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
        Data.last_seen      = usersummary.split('Last seen  in  ')[1].split('(')[0]
        Data.last_activity  = usersummary.split('Last Activity: ')[1].split('Account')[0]
        Data.last_activity  = (datetime.strptime(Data.last_activity, "%d %b %Y, %H:%M")+timedelta(hours=2)).strftime("%d %B %Y, %H:%M")
        stats               = str(parsed_html.body.find('div', attrs={'class':'userpage recentlyplayed'}))
        Data.progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
        Data.progress_html  = f'<div class="progressbar grow">{Data.progress_html}</div>'
        Data.progress       = Data.progress_html.split('width:')[1].split('"')[0]
        Data.stats          = stats.split('<div class="mb-5">')[1].split('</div>')[0]
        Data.cheevos_raw    = Data.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
        Data.cheevos        = Data.parseCheevos()
        for d in Data.cheevos:
            if d.index == Cheevo.active_index:
                Data.cheevo = d.name + "\n" + d.description
        
    @staticmethod
    def writeCheevo():
        if Data.username == '': return
        with open(f'{Data.root}/data/current_cheevo.txt' , 'w') as file:   
            for d in Data.cheevos:
                if d.index == Cheevo.active_index:
                    file.write(d.name)
                    file.write('\n')
                    file.write(d.description)
                    Data.cheevo = d.name + "\n" + d.description
                    # get achievement picture
                    data = requests.get(d.picture)
                    with open(f"{Data.root}/data/current_cheevo.png", 'wb') as picture:
                        picture.write(data.content)
                
    @staticmethod
    def write():
        if Data.username == '': return
        with open(f'{Data.root}/data/progress.html'      , 'w') as file:   file.write(Data.progress_html )
        with open(f'{Data.root}/data/progress.txt'       , 'w') as file:   file.write(Data.progress      )
        with open(f'{Data.root}/data/last_activity.txt'  , 'w') as file:   file.write(Data.last_activity.upper() )
        with open(f'{Data.root}/data/last_seen.txt'      , 'w') as file:   file.write(Data.last_seen     )
        with open(f'{Data.root}/data/site_rank.txt'      , 'w') as file:   file.write(Data.site_rank     )
        with open(f'{Data.root}/data/score.txt'          , 'w') as file:   file.write(Data.score         )
        Data.writeCheevo()
        with open(f'{Data.root}/data/cheevos.html'       , 'w') as file:   
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
                    border: 2px solid #0000;
                }
                img.active {
                   filter: brightness(1.5) hue-rotate(270deg);
                    animation: flash 2s linear 0s infinite alternate;
                }
                       
                @keyframes flash {
                    from {border: 2px solid #FF0;}
                    to   {border: 2px solid #F00;}
                }
            </style>""")
            for d in Data.cheevos:
                file.write( str(d) )            
                file.write( '\n' )            



class Ramon:
    width               = 900
    height              = 1440
    
    settings            = {}

    @staticmethod
    def writecfg():
        with open(f'{Data.root}/config.txt', 'w') as file:
            for key,value in Ramon.settings.items():
                file.write(f'{key}={value}'+"\n")

    @staticmethod
    def loadcfg():
        Ramon.settings            = {
            'auto_update'   : True,
            'fullscreen'    : True,
            'username'      : '',
            'root'          : '.',
        }
        Data.root     = Ramon.settings['root']
        Data.username = Ramon.settings['username']#workaround a design flaw

        try:
            with open(f'{Data.root}/config.txt', 'r') as file:
                data = file.read().split('\n')
                for setting in data:
                    if len(setting)==0:continue
                    parts = setting.split('=')
                    Ramon.settings[parts[0]] = True if parts[1].lower() == 'true' else False if parts[1].lower() == 'false' else parts[1]
            Data.username = Ramon.settings['username']#workaround a design flaw
            Data.root     = Ramon.settings['root']
        except Exception as E:
            return 
        
    @staticmethod
    def updateSettings(sender=None, user_data=None, args=None):
        Ramon.settings['auto_update'] = dpg.get_value('auto_update')
        Ramon.settings['fullscreen' ] = dpg.get_value('fullscreen')
        Ramon.settings['username'   ] = dpg.get_value('username')
        Ramon.settings['root'       ] = '.'
        Data.root = Ramon.settings['root']
        if Data.username != Ramon.settings['username']:
           Data.setUsername()
           Ramon.refresh()
        Ramon.writecfg()

    @staticmethod
    def updateCheevoManually(sender=None, args=None, user_data=None):
        with open(f'{Data.root}/data/current_cheevo.txt', "w") as file:
            file.write(dpg.get_value('cheevo'))
        os.truncate(f'{Data.root}/data/current_cheevo.png')

    @staticmethod
    def updateCheevo(sender=None, args=None, user_data=None):
        Cheevo.active_index = user_data
        for i in range(0,64):
            dpg.set_value(f'cheevo[{i+1}]', False)
        dpg.set_value(f'cheevo[{user_data}]', True)
        Data.writeCheevo()
        Ramon.redraw()

    @staticmethod
    def exit():
        Data.mine = False         

    @staticmethod
    def createMenu():
        with dpg.menu_bar():
            with dpg.menu(label="Actions"):
                dpg.add_menu_item(label="Redump  "   , callback=Data.write)
                dpg.add_menu_item(label="Refresh "   , callback=Ramon.refresh)
                dpg.add_menu_item(label="Exit    "   , callback=Ramon.exit  )
            with dpg.menu(label="Options"):
                dpg.add_checkbox(label="Auto Update", tag="auto_update" , default_value=Ramon.settings['auto_update']   , callback=Ramon.updateSettings)
                dpg.add_checkbox(label="Fullscreen" , tag="fullscreen"  , default_value=Ramon.settings['fullscreen']    , callback=Ramon.updateSettings)

    @staticmethod
    def start():
        Ramon.loadcfg()
        try:
            os.mkdir(f'{Data.root}/data')
        except:
            pass
        dpg.create_context()
        dpg.create_viewport(title="RAMon", width=Ramon.width, height=Ramon.height)
        dpg.setup_dearpygui()
        with dpg.window(
            label="RAMon", 
            width=Ramon.width, 
            height=Ramon.height, 
            no_close=True, 
            no_collapse=True, 
            no_resize=True, 
            no_title_bar=True, 
            no_bring_to_front_on_focus=True, 
            no_move=True
        ):
            Ramon.createMenu()
            row = 23
            row_height = 23
            dpg.add_text(
                color=(220,255,0),
                default_value="RA Username", 
                pos=(8, row),
            )
            dpg.add_input_text(
                tag='username', 
                default_value=Ramon.settings['username'],
                pos=(96, row),
                width=110,
                callback=Ramon.updateSettings,
                on_enter=True,
            )
            dpg.add_text(
                default_value="Last connection", 
                pos=(230,row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='date', 
                pos=(346, row),    
                width=200,            
                readonly=True,  
            )
            dpg.add_text(
                default_value="Score", 
                pos=(566, row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='score', 
                pos=(610, row),    
                width=80,          
                readonly=True,  
            )
            dpg.add_text(
                default_value="Rank", 
                pos=(708, row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='rank', 
                pos=(746, row),    
                width=132,          
                readonly=True,  
            )
            row+=row_height
            dpg.add_text(
                color=(220,255,0),
                default_value="Now playing", 
                pos=(8, row),
            )
            dpg.add_input_text(
                tag='game', 
                default_value="",
                pos=(96, row),
                width=(Ramon.width - 118),
            )            
            row+=row_height
            dpg.add_text(
                color=(220,255,0),
                default_value="     Cheevo", 
                pos=(8, row),
            )
            dpg.add_input_text(
                tag='cheevo', 
                default_value="",
                pos=(96, row),
                width=(Ramon.width - 118),
                height=42,
                multiline=True,
                on_enter=True,
                callback=Ramon.updateCheevoManually
            )            
            row+=row_height*2
            dpg.add_input_text(
                tag='stdout', 
                width=(Ramon.width-31), 
                height=(Ramon.height - row)-46,
                multiline=True,
                readonly=True,
                pos=(32,row),
            )            
            for i in range(0,64):
                dpg.add_checkbox(default_value=True if (i+1) == Cheevo.active_index else False, tag=f'cheevo[{i+1}]', pos=(8, row+(i*26)), show=False, user_data=i+1, callback=Ramon.updateCheevo )
        #keyboard.Listener( on_release=Ramon.on_release).start()
        return Ramon.render()
        
    @staticmethod
    def render():
        import time
        if Ramon.settings['fullscreen'] : 
            dpg.toggle_viewport_fullscreen()
        dpg.show_viewport()
        Ramon.refresh()
        last_update = time.time()
        while dpg.is_dearpygui_running() and Data.mine:
            dpg.render_dearpygui_frame()            
            delta = int(time.time() - last_update)
            if  delta >= 60:
                last_update = time.time()
                if Ramon.settings['auto_update']:
                    Ramon.refresh()
        dpg.destroy_context()
        Ramon.writecfg()

    @staticmethod
    def redraw():
        for i in range(0,64):
            dpg.hide_item(f'cheevo[{i+1}]')
        dpg.set_value('game'  , Data.last_seen      )
        dpg.set_value('rank'  , Data.site_rank      )
        dpg.set_value('score' , Data.score          )
        dpg.set_value('date'  , Data.last_activity  )
        dpg.set_value('cheevo', Data.cheevo         )
        payload = ''
        for d in Data.cheevos:
            if d.locked: 
                payload += d.menu() + "\n"
                dpg.show_item(f'cheevo[{d.index}]')
        dpg.set_value('stdout', payload)

    @staticmethod
    def refresh(sender=None, user_data=None, args=None):
        dpg.set_value('stdout','Reloading...')
        Cheevo.global_index = 0
        Data.query()
        Ramon.redraw()
        Data.write()

    @staticmethod
    def message(text):
        dpg.set_value('stdout', dpg.get_value('stdout')+'\n'+text)

Ramon.start()