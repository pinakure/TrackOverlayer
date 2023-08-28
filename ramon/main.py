"""
        CHANGES:
        - Added auto refresh feature on rendered output HTML files
        - Added global hotkey to force data refresh (CTRL+F5)
        - Added custom css files for every HTML generated file ( info will be embedded in the HTML output )

        ------
        - Code refactor
        - Added preferences module
        - Bugfix: Fixed unlocked achievements position calculation, now displays correctly
        ------

        - Program now remembers last cheevo active after restart
        - Settings dialog

        ------
        Log window 
        ------
        Ability to remember viewport last size and position
        Ability to fine tune viewport position and size from config.txt and preferences dialog
        Ability to preview size and position when tweaking values @ preferences menu
        Added preferences -> output -> style personalization tab placeholders
        Ability to open each stylesheet related to each output html file @ preferences
        ------------
        Perspective Personalization for widgets
        Progressbar personalization
        ---------------------
        28-8-23
        - Added ORM (pewee) to keep better tracking of which cheevos have been notified (planning doing a splash to display as OBS overlay)
        - Turned Cheevo class into Model Class to interface the DB, added Game class
        - Auto game data scraping ( name, picture and game_id )
        - Now each cheevo has its own unique id, taken directly from RA id data
        - Made a field in Game table to store which achievement is selected, so that attribute is 
          saved for next sessions, and if game changes it changes automatically :)
        TODO: 
            - Ramon.collectNotifications() 
            - Ramon.dumpNotifications() -> Dumps Js + HTML + CSS to a auto updating, show only once notification queue
                - We may have to subdivide this into subclass
                - But hell it will be cool to be able to show em in overlay instead of 
                  being forced to use the embedded blocky Retroarch notifications, at expense of 
                  having to manually update or waiting for autoupdate, delaying the realtime notification 
                  when one achievement gets unlocked.

"""
try: 
    import os, sys
    from classes.ramon       import Ramon
except ImportError:
    os.system('pip install requests beautifulsoup4 dearpygui pynput peewee')
    os.system(f'pause')
    exit()

Ramon.start()
if Ramon.restart:
    import sys
    cmdline = " ".join(sys.argv)
    os.system(f'start {cmdline}')
