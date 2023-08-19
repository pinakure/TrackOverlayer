import requests, os
from dearpygui          import dearpygui as dpg
from datetime           import datetime, timedelta
from bs4                import BeautifulSoup    
from classes.cheevo     import Cheevo

class Data:
    parent          = None
    root            = '/'
    echo            = False
    score           = ''
    gmt             = 2
    site_rank       = ''
    last_seen       = ''
    last_activityr  = ''
    last_activity   = None
    progress_html   = ''
    progress        = ''
    stats           = ''
    cheevo          = ''
    cheevos_raw     = []
    cheevos         = []
    mine            = True
    username        = ''
    theme           = 'default'
    recent          = []
    reload_rate     = 60
    css             = {}

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
        Data.css = Data.parent.css
        if Data.username == '': return
        try:
            payload             = requests.get(f'https://www.retroachievements.org/user/{Data.username}').text
            parsed_html         = BeautifulSoup( payload, features='html.parser' )
            usersummary         = parsed_html.body.find('div', attrs={'class':'usersummary'}).text
        
            Data.score          = usersummary.split('Hardcore Points: ')[1].split(' (')[0]
            Data.site_rank      = usersummary.split('Site Rank: #')[1].split(' ranked')[0]
            Data.last_seen      = usersummary.split('Last seen  in  ')[1].split('(')[0]
            Data.last_activityr= usersummary.split('Last Activity: ')[1].split('Account')[0]
            Data.last_activity  = (datetime.strptime(Data.last_activityr, "%d %b %Y, %H:%M")+timedelta(hours=Data.gmt))
            stats               = str(parsed_html.body.find('div', attrs={'class':'userpage recentlyplayed'}))
            Data.progress_html  = stats.split('<div class="md:flex justify-between mb-3">')[1].split('</div></div></div>')[0].split('<div class="progressbar grow">')[1] 
            Data.progress       = Data.progress_html.split('width:')[1].split('"')[0]
            Data.progress_html  = f'<style>{Data.css["progress"].get()}</style><div class="progressbar grow">{Data.progress_html}</div>'
            Data.stats          = stats.split('<div class="mb-5">')[1].split('</div>')[0]
            Data.cheevos_raw    = Data.stats.split('<span @mouseleave="hideTooltip" @mousemove="trackMouseMovement($event)" @mouseover="showTooltip($event)" class="inline" x-data="tooltipComponent($el, { staticHtmlContent: useCard(')[1:]
            Data.cheevos        = Data.parseCheevos()
            for d in Data.cheevos:
                if d.index == Cheevo.active_index:
                    Data.cheevo = d.name + "\n" + d.description
            return True
        except Exception as E:
            print(str(E))
            return False
        
    @staticmethod
    def updatePictures():
        try:   
            width, height, depth, data = dpg.load_image(f'{Data.root}/data/current_cheevo.png')                
        except Exception as E:
            print("ERROR: Cannot load current_cheevo.png\n\n")
        
        with dpg.texture_registry(show=False):
            try:
                dpg.delete_item('current_cheevo_img')
                #print("INFO: deleted static_texture 'current_cheevo_img'.")
                dpg.delete_item('current_cheevo_image')
                #print("INFO: deleted image 'current_cheevo_image'.")

            except:
                #print("INFO: static_texture 'current_cheevo_img' does not exist. Nothing deleted.")
                pass
            try:
                dpg.add_static_texture(
                    width=width, 
                    height=height, 
                    default_value=data, 
                    tag="current_cheevo_img",
                )
                #print("INFO: Added static texture 'current_cheevo_img'.")
                dpg.add_image(
                    parent='main',
                    tag='current_cheevo_image', 
                    texture_tag="current_cheevo_img",
                    pos=(Data.parent.width-width,69),
                    width=40,
                    height=40,
                )
                #print("INFO: Added image 'current_cheevo_image'.")
            except Exception as E:
                #print("ERROR: Cannot create static texture 'current_cheevo_img'.")
                #print("       "+str(E))
                pass
        
    @staticmethod
    def getCurrentCheevo( picture ):
        # try first if image is in cache
        if os.path.exists(f'{Data.root}/data/cache/{picture}'):
            with open(f'{Data.root}/data/cache/{picture}', 'rb') as file:
                #print(f'INFO: Using cached image {picture}')
                return file.read()
        else:
            url = f'https://media.retroachievements.org/Badge/{picture}'
            try:
                #print(f'INFO: Requesting cheevo image "{picture}"')
                data = requests.get( url ).content
            except:
                print(f"ERROR: Failed to retrieve 'https://media.retroachievements.org/Badge/{picture}'!")
                return None                
            try:
                with open(f'{Data.root}/data/cache/{picture}', 'wb') as file:
                    #print(f'INFO: Storing cached image "{picture}"')
                    file.write(data)
            except:
                print(f"ERROR: Failed to store cache for 'https://media.retroachievements.org/Badge/{picture}'!")
                pass                
            return data

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
                    data = Data.getCurrentCheevo( d.picture )
                    if data:
                        with open(f"{Data.root}/data/current_cheevo.png", 'wb') as picture:
                            picture.write(data )
                        Data.updatePictures()
                
    @staticmethod
    def getReloadSnippet():
        return """<script>function refresh(){ window.location.reload(); } setInterval(refresh, """+str(Data.reload_rate*1000)+""")</script>"""

    @staticmethod
    def writeCheevos():
        script = Data.getReloadSnippet()
        with open(f'{Data.root}/data/cheevos.html'         , 'w') as file:   
            with open(f'{Data.root}/data/cheevos_locked.html'  , 'w') as locked:   
                with open(f'{Data.root}/data/cheevos_unlocked.html'  , 'w') as unlocked:   
                    file.write     ( f"<style>{Data.css['cheevos'  ].get()}</style>{script}")
                    locked.write   ( f"<style>{Data.css['locked'   ].get()}</style>{script}")
                    unlocked.write ( f"<style>{Data.css['unlocked' ].get()}</style>{script}")
                    count = 0
                    for d in Data.cheevos:
                        Data.parent.setProgress( count / len(Data.cheevos) )
                        file.write( str(d) + '\n' )
                        if d.locked:
                            locked.write( str(d) + '\n' )
                        else:
                            unlocked.write( str(d) + '\n' )
                        count+=1
                    Data.parent.setProgress(1.0)
        
    @staticmethod
    def writeRecent():
        script = Data.getReloadSnippet()
        with open(f'{Data.root}/data/recent.html'        , 'w') as file:   
            file.write(f'''<style>{Data.css['recent'].get()}</style>{script}<table><tbody>''')
            for r in Data.recent:
                file.write(f'''
                            <tr><td colspan="2"><hr/></td></tr>
                            <tr>
                                <td rowspan="2">
                                    <img style="border-radius: none !important" src="cache/{r.picture}">
                                </td>
                                <td><b>{r.name}</b></td>
                            </tr>
                            <tr>
                                <td>{r.description}</td>
                            </tr>
                ''')                
            file.write('''</tbody><table>''')

    @staticmethod
    def write():
        if Data.username == '': return
        with open(f'{Data.root}/data/progress.html'      , 'w') as file:   file.write(Data.progress_html )
        with open(f'{Data.root}/data/progress.txt'       , 'w') as file:   file.write(Data.progress      )
        with open(f'{Data.root}/data/last_activity.txt'  , 'w') as file:   file.write(Data.last_activity.strftime("%d %b %Y, %H:%M").upper() )
        with open(f'{Data.root}/data/last_seen.txt'      , 'w') as file:   file.write(Data.last_seen     )
        with open(f'{Data.root}/data/site_rank.txt'      , 'w') as file:   file.write(Data.site_rank     )
        with open(f'{Data.root}/data/score.txt'          , 'w') as file:   file.write(Data.score         )        
        Data.writeCheevo()
        Data.writeCheevos()
        Data.writeRecent()
