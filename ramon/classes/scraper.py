import requests, os
from bs4 import BeautifulSoup    
from classes.preferences import Preferences
from classes.log import Log

class Scraper:
    picture_root = "https://thegamesdb.net/search.php?name="

    
    def getGamePicture( name ):
        try:
            response = requests.get(f'{Scraper.picture_root}{name.strip()}')
            parts    = response.content.decode('utf-8').replace('\t', '').replace('\n', '').split('<img class="card-img-top"')
            url      = parts[1].split('src="')[1].split('"')[0]
            response = requests.get(url).content
            with open(f'{Preferences.root}/data/last_seen.png', 'wb') as file:
                file.write(response)
        except Exception as E:
            try:
                os.unlink(f'{Preferences.root}/data/last_seen.png')
            except Exception as I:
                Log.warning(f"Cannot retrieve game picture from {Scraper.picture_root}", E)                
            Log.error(f"Cannot retrieve game picture from {Scraper.picture_root}", E)