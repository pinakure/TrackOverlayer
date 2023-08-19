import requests, os 
from classes.log    import Log

class Cheevo:
    root            = '.'
    max             = 128    
    min_width       = 0
    global_index    = 0
    active_index    = 1
    
    def __init__(self, name, description, picture):
         self.name = name.replace('"', "´")
         self.picture = picture.strip('https://media.retroachievements.org/Badge/')+'.png'
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
        if not os.path.exists(f'{Cheevo.root}/data/cache/{self.picture}'):
            Log.info(f"Caching cheevo picture {self.picture}...")
            data = requests.get( f'https://media.retroachievements.org/Badge/{self.picture}' ).content
            with open(f'{Cheevo.root}/data/cache/{self.picture}', 'wb') as file:
                file.write(data)
        return f'<img class="{"active" if self.index == Cheevo.active_index else ""} round" width="48" height="48" src="cache/{self.picture}" title="{self.description}" name="{self.name}">'

    @staticmethod
    def parse( payload ):
        name        = payload.split('/&gt;&lt;div&gt;&lt;div&gt;&lt;b&gt;')[1].split('&lt;/b&gt;&lt;/div&gt;&lt;div')[0].replace("\\'", "'")
        picture     = payload.split('img src=')[1].split('.png')[0].replace('\\\'', '') + ".png"
        description = payload.split('mb-1')[1].split('gt')[1].split('&lt;/div')[0].replace(';', '')
        #picture     = f'{picture}.png'
        return Cheevo(name, description, picture)

