try: 
    from classes.ramon      import Ramon
    from classes.nogui.app  import App
except ImportError as E:
    # Auto install dependencies if any is missing when trying to run this on python
    import os
    os.system('pip install requests requests_toolbelt beautifulsoup4 dearpygui pynput peewee pyinstaller')
    os.system('pip install --upgrade websockets')
    os.system(f'pause')
    os._exit(0)    

Ramon.start()    